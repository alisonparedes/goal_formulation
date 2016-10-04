'''
Created on Sep 3, 2015

@author: Alison
'''

from collections import deque
import problem
  
def dijkstra(self, initial_state): #TODO: Run to a horizon, i.e. number of nodes expanded
    #TODO: Open list
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

def is_duplicate(self, node):
    if self.closed_list.get(hash(node.state)) != None:
        return True
    return False
        
if __name__ == '__main__':
    pass
    



   
