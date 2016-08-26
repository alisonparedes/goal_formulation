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


    def __init__(self, parent, state, problem, action):
        '''
        Constructor
        '''
        self.parent = parent
        self.state = state
        self.problem = problem
        self.action = action
        if parent != None:
            self.g = parent.g + 1
        else:
            self.g = 0


class UniformCostSearchTree(object):
    '''
    classdocs
    '''
    frontier = None
    nodes_generated = 0
    nodes_expanded = 0
    closed_list = {}

    def __init__(self, problem):
        '''
        Constructor
        '''
        self.problem = problem
        self.root = Node(None, problem.initialstate, problem, None)
        self.frontier = []
        heapq.heappush(self.frontier,(0,self.root))
        self.nodes_generated = 0

        
    def search(self):
        
        while len(self.frontier) > 0:
            explored = heapq.heappop(self.frontier)[1]

            if self.problem.isgoal(explored.state):
                return self.get_plan(explored)
            self.closed_list.update({hash(explored.state.pos):True})
            
            self.nodes_expanded = self.nodes_expanded + 1
            
            for action in self.problem.actions:
                generated = Node(explored, self.problem.transition(explored.state, action), problem, action)
                self.nodes_generated = self.nodes_generated + 1 
                if not self.is_duplicate(generated):
                    heapq.heappush(self.frontier, (generated.g, generated))  
                    self.closed_list.update({hash(generated.state.pos):True})                   
                    
        return False
    

    def get_plan(self, node):
        plan = list([node.action])
        parent = node.parent
        while parent != self.root:
            plan.append(parent.action)
            parent = parent.parent
        plan.reverse()
        return plan
    
    def is_duplicate(self, node):
        if self.closed_list.get(hash(node.state.pos)) != None:
            return True
        return False
        
if __name__ == '__main__':
    pass
    



   
