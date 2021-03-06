import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from collections import Counter
from collections import namedtuple

class State():
    """ Agent state """
    def __init__(self,inputs,next_waypoint):
        self.inputs = inputs
        self.next_waypoint = next_waypoint

    def __hash__(self):
        return hash((self.inputs['light'],self.inputs['oncoming'],self.inputs['left'],self.inputs['right'],self.next_waypoint))

    def __eq__(self,other):
        return (self.inputs['light'],self.inputs['oncoming'],self.inputs['left'],self.inputs['right'],self.next_waypoint) == (other.inputs['light'],other.inputs['oncoming'],other.inputs['left'],other.inputs['right'],other.next_waypoint)

    def __ne__(self,other):
        return not(self == other)



class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        # Initialize a random seed:
        random.seed(0)
        # the set of valid actions:
        self.valid_actions = [None, 'forward', 'left', 'right']
        # the state of the agent
        self.state = None
        # store the previous state, action and reward.
        self.prev_state = None
        self.prev_action = None
        self.prev_reward = None
        # the Q-table as a dict:
        # Q-table initialization to 0:
        self.q_table = dict()
        for light in ['green','red']:
            for oncoming in [None, 'forward', 'left', 'right']:
                for left in [None, 'forward', 'left', 'right']:
                    for right in [None, 'forward', 'left', 'right']:
                        for waypoint in ['forward', 'left', 'right']:
                            self.q_table[State({'light':light,'oncoming':oncoming,'left':left,'right':right},waypoint)] = {None:0,'forward':0,'left':0,'right':0}

        # parameters:
        self.gamma = 0.1
        self.learning_rate = 0.5
        self.epsilon = 0.1


    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.state = None
        # gradually increase the value of epsilon as the training progress (assuming a total of 100 training trials)
        if self.epsilon < 1.0:
            self.epsilon += 0.01


    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        # review 2: codify the states as a dictionary
        # state is codified as string with the value of all inputs plus the next_waypoint value:
        state_dict = inputs
        state_dict ['next_waypoint'] = self.next_waypoint
        # compose the state as string (transforming None to string 'None')
        state_light = 'None' if state_dict['light']==None else state_dict['light']
        state_oncoming = 'None' if state_dict['oncoming']==None else state_dict['oncoming']
        state_left = 'None' if state_dict['left']==None else state_dict['left']
        state_right = 'None' if state_dict['right']==None else state_dict['right']

        #self.state = state_light+state_oncoming+state_left+state_right+state_dict['next_waypoint']
        self.state = State(inputs,self.next_waypoint)
        #print "current state: {}".format(self.state)

               
        # TODO: Select action according to your policy
        
        #instead of chosing a random action, select the best_action_a Q(s,a)
        counter = Counter(self.q_table[self.state])

        # get the best_action value and the q-max value.
        
        max_q_value = counter.most_common(1)[0][1]
        best_action = counter.most_common(1)[0][0]

        # use of epsilon to balance between exploration and exploitation

        action = best_action if random.random()<=self.epsilon else  self.valid_actions[random.randint(0,len(self.valid_actions)-1)]

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        if self.prev_action != None:
            #update q_table:
            # review 1:  To fix this, you should calculate the highest Q-value associated with the current state and use that instead.
            # The max value for self.q_table[self.state][action] is stored on the best_action variable:
            self.q_table[self.prev_state][self.prev_action] = (1-self.learning_rate)*self.q_table[self.prev_state][self.prev_action] + \
            self.learning_rate* (self.prev_reward + self.gamma*max_q_value)

        # now update the prev variables:
        self.prev_action = action
        self.prev_reward = reward
        self.prev_state = self.state

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.01, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
