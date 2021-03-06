
import random
import math
from enum import Enum

import Events
import simulator
from msg import Msg
from visualGraph import *
from sim_config import config



class State(Enum):
	VULNERABLE = 0
	INFECTED = 1
	RECOVERED = 2



# TODO: dist and in_range are the critical part of the program (most of the time spent inside them).
#       Should precompute, for the current value of RMIN, the which car is in range of which other car,
#       Maybe saving in each Car object the (plates of) other cars at distance <= RMIN

def dist(p,q):  #eucledian distance
	return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)
def in_range(p,q,radius):	#returns true whether the distance p,q is less than radius
	return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2) < radius


class Car:

	def __init__(self, plate, pos, neighbors):
		self.plate = plate          #identifier of the car
		self.pos = pos              #tuple (x,y)
		self.neighbors = neighbors  #list of plates of neighbor cars

		# Simulation attributes
		self.messages = []   #messages received during the waiting phase
		self.state = State.VULNERABLE    #state of the vehicle w.r.t. the disseminated message
		self.sim = None   # Each car keeps track of its own simulator object, which is set right before starting the simulation


	def on_receive(self, msg):
		"""
		Implements the receiving of a message
		"""
		#Simulate message loss while receiving
		if random.random() < config.drop:
			return

		self.sim.rcv_messages += 1   #for simulation statistics

		# If I already received this message (RECOVERED state) I don't do anything
		if self.state == State.RECOVERED:
			return

		if self.state == State.VULNERABLE:
			# If it's the first time that I receive the message, then transition to state infected and update simulation stats
			self.sim.t_last_infected = self.sim.t
			self.sim.t_infected[self.sim.t] += 1
			self.sim.infected_counter += 1
			self.state = State.INFECTED

			# Add waiting phase event
			waiting_time = self.getWaitingTime(msg.last_emit)
			event = Events.WaitingEvent(self, waiting_time)
			self.sim.schedule_event(event)

		# Store the received message
		self.messages.append(msg)


	def getWaitingTime(self, emit_pos):
		"""
		Returns the waiting time a vehicle has to wait when infected.
		Calculated using the distance between me and the emitter that sent 
		me the message, expressed as number of simulator ticks
		"""
		dAS = dist(self.pos, emit_pos) 
		waiting_time = config.Tmax*(1 - dAS/config.Rmax)  #waiting time, in seconds

		if waiting_time <= config.Tmin:
			waiting_time = config.Tmin
		if waiting_time >= config.Tmax:
			waiting_time = config.Tmax

		return waiting_time  #in seconds



	def broadcast_phase(self):
		"""
		After the waiting phase, a vehicle has to decide whether or not to relay the received message.
		Here we perform the decision process and, if positive, we send the message to all our radio neighbors (infect)
		"""

		# Decide whether to relay or not. If the CBF algorithm is being used, it just
		# counts how many messages it has received and broadcasts if they are lower than the threshold.
		if config.use_CBF:
			# Here -1 since len(self.messages) is always >=1, because it will always contain the
			# message that infected this vehicle. The message threshold refers to how many messages
			# are received during the waiting phase, so not considering this first message.
			bcast = len(self.messages) - 1 < config.CBF_msg_thresh
		else:
			bcast = self.evaluate_positions(self.messages, self.pos)
		
		if bcast:
			# Take the first message in the list of incoming messages (the first message generated the infection)
			# and modify it to be ready for broadcast
			msg_recv = self.messages[0]
			msg = self.modify_msg(msg_recv)

			# Don't broadcast if the message reached its hop limit
			if msg.hop == msg.ttl:
				return

			# Update simulator statistics
			self.sim.sent_messages += 1
			self.sim.network_traffic += msg.size()   #EPIC
			#self.sim.network_traffic += len(msg.text)  #probabilistic

			# Send the message by scheduling an event for the simulator (this implements some network delay)
			#self.send_msg_to_neighbors(msg)
			bcast_event = Events.BroadcastEvent(self, msg)
			self.sim.schedule_event(bcast_event)

		# Change state to recovered and update simulation statistics, either the vehicle has broadcasted or not
		self.messages.clear()
		self.sim.infected_counter -= 1
		self.state = State.RECOVERED


	def modify_msg(self, _msg):
		"""
		Before a vehicle retransmit a message, this last one must be modified by
		adding data of the vehicle which is about to broadcast it. It returns a new Msg object, no side effects
		"""

		msg = _msg.clone()
		
		# Update 'msg''s last emitter with this vehicle position
		msg.last_emit = self.pos

		# Update hop counter
		msg.hop += 1

		# Retrieve the set of all known emitters. It is the union of all emitters inside all messages
		# received during the sleep time.
		all_emitters = set([self.pos])
		for m in self.messages:
			all_emitters = all_emitters.union(m.emitters)
		
		# Sort the emitters list by the distance between them and this vehicle, in ascending order
		key = lambda x: dist(x, self.pos)
		all_emitters_srtd = sorted(list(all_emitters), key=key)
		# Keep only the closest to me, since there is Msg.EMITTERS_LIMIT limit on the max. number of emitters stored inside a message
		msg.emitters = all_emitters_srtd[:Msg.EMITTERS_LIMIT]

		return msg
		



	# Now a barrage of different 'evaluate_positions' functions, that decide whether
	# or not a vehicle has to relay a message. Each function follows its own policy


	# WE USED THIS
	def evaluate_positions(self, messages, my_pos):
		# Fetch all emitters that broadcasted the message (union of emitters of each received message)
		emitters = set()
		for m in messages:
			emitters = emitters.union(m.emitters)

		# Find the set of my neighbors already covered by an emitter
		covered_neighbors = set()
		for neighbor in self.neighbors:  #for each of my neighbors
			neighbor_pos = self.sim.getCar(neighbor).pos
			for emit in emitters:  #for each different emitter
				if in_range(neighbor_pos, emit, config.Rmin):  #check if my neighbor was covered by emit
					covered_neighbors.add(neighbor_pos)
		
		# return true (relay) only if there is a percentage ALPHA of uncoverd neighbors
		n_neighbors = len(self.neighbors)
		n_not_covered = n_neighbors - len(covered_neighbors)
		return n_not_covered > config.alpha * n_neighbors


	# WE USED THIS as algorithm comparison
	def evaluate_positions_no_geo(self, messages, my_pos):
		return not len(messages)>3

	# WE USED THIS as algorithm comparison
	def evaluate_positions_w_p_pers(self, messages, my_pos):
		P = []
		for m in messages:
			d = dist(m.last_emit, my_pos)
			Rmean = (config.Rmin/4) / 2
			P.append(d/Rmean)
		return random.random() > (1-min(P))



	# WE USED THIS as the probabilistic dissemination
	def evaluate_positions_probabilistic(self, messages, my_pos):
		#relay the message with probability P
		'''bcast_force = True
		for m in messages:
			if dist(my_pos, m.last_emit) <= Simulator.RMIN:
				bcast_force = False'''
		bcast_force = len(messages) > 1
		P = 0.6
		return bcast_force or random.random() > (1-P)

		#other prb relay (inv proportional to the distance from the closest relay)
		'''
		min_dist = Simulator.RMAX
		for m in messages:
			for emit in m.emitters:  #per ogni emitter diversa che ha mandato il messaggio
				d = dist(emit, self.pos)
				if d < min_dist:
					min_dist = d
		min_dist = min(min_dist, Simulator.RMAX)
		p = min_dist / Simulator.RMIN    #p is the relay probability
		return random.random() > (1-p)
		'''

		#other prb relay (inv prop with the number of neighbors)
		'''
		n_neighbors = 0   #number of neighbors cars
		for c, i in zip(self.adj, range(len(self.adj))):
			if c == 1:
				#Ho preso la macchina corrispondente
				obj = self.sim.getCar(i)
				if obj != None:
					n_neighbors += 1

		k = 45  #const
		if n_neighbors <= k:
			return True
		p = k/n_neighbors
		return random.random() > (1-p)
		'''


