'''
Created on Sep 3, 2015

@author: Alison
'''

from collections import deque
import problem
import heapq
        
class Node(object):
    '''
    classdocs
    '''
    action = None
    g = None
    parent = None
    state = None
    problem = None


    def __init__(self, parent, state, action):
        '''
        Constructor
        '''
        self.parent = parent
        self.state = state
        self.action = action
        if parent != None:
            self.g = parent.g + 1 #TODO: Get f instead of g
        else:
            self.g = 0


class UniformCostSearchTree(object): #TODO: Rename to BestFirstSearch
    '''
    classdocs
    '''
    frontier = None
    nodes_generated = 0
    nodes_expanded = 0
    closed_list = {}

    def __init__(self):
        '''
        Constructor
        '''

        
    def search(self, initial_state): #TODO: Run to a horizon, i.e. number of nodes expanded
        #TODO: Making search a function
        self.root = Node(None, initial_state, None) 
        self.frontier = []
        heapq.heappush(self.frontier,(0,self.root))
        self.horizon = 1
        depth = 0
        while depth < self.horizon:  #TODO: Instead of goal state run to horizon, i.e. run n times
            explored = heapq.heappop(self.frontier)[1]
            self.closed_list.update({hash(explored.state):True}) #TODO: Encapsulate this into its own function           
            depth += 1 #TODO: How to encapsulate this to better describe the purpose it is serving, in support of running the search out to a limited horizon           
            '''
            for action in self.actions(explored.state): 
                generated = Node(explored, self.transition(explored.state, action), action)
                self.nodes_generated = self.nodes_generated + 1  #TODO: Write to log
                if not self.is_duplicate(generated):
                    heapq.heappush(self.frontier, (generated.g, generated))  #TODO: I assume heap push sorts. Consider encapsulating this into a more descriptive method.
                    self.closed_list.update({hash(generated.state):True})    
            '''                
        return self.get_plan(explored) #Always returns something, since there is no goal state, only a reward

    def actions(self, state):
        '''
        Actions applicable in given state
        '''
        return [1] #TODO:
    
    def transition(self, state, action):
        return state
    
    def get_plan(self, node): #TODO: I don't need to return a plan right now
        plan = list([node.action])
        parent = node.parent
        while parent != self.root:
            plan.append(parent.action)
            parent = parent.parent
        plan.reverse()
        return plan
    
    def is_duplicate(self, node):
        if self.closed_list.get(hash(node.state)) != None:
            return True
        return False
        
if __name__ == '__main__':
    pass
    



   
