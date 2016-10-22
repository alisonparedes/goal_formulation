'''
Created on Oct 22, 2016

@author: Alison
'''
import unittest
from world import * #Test modules in issolation

class Test(unittest.TestCase):
    
    def testSampleCell(self):
        random.seed(1)
        problem_distribution_arr = [(0.999,(0,0),'F'),(0.001,(0,0),'E')]
        cell = sample_cell(problem_distribution_arr)
        self.assertEquals(cell, (0.999,(0,0),'F'), cell)
        random.seed(None) #Tear down


    def testSample(self):
        random.seed(1) #TODO: If I ran this a bunch of times without the seed what should happen?
        problem_distribution_arr = [(0.999,(0,1),'F'),(0.001,(0,1),'E')]
        state_dict = {(0,0):'H',(3,3):'B'}
        n=1
        new_state_dict = sample(problem_distribution_arr, state_dict, n) 
        self.assertEquals(new_state_dict,{(0,1):'F',(0,0):'H',(3,3):'B'},new_state_dict)
        random.seed(None) #Tear down
        
    def testSampleNone(self):
        random.seed(2) 
        problem_distribution_arr = [(0.5,(0,1),'F'),(0.5,None)]
        state_dict = {(0,0):'H',(3,3):'B'}
        n=1
        new_state_dict = sample(problem_distribution_arr, state_dict, n) 
        self.assertEquals(new_state_dict,{(0,0):'H',(3,3):'B'},new_state_dict)
        random.seed(None) #Tear down
    
    def testSampleH(self):
        random.seed(1) 
        problem_distribution_arr = [(0.5,(0,0),'F'),(0.5,None)]
        state_dict = {(0,0):'H',(3,3):'B'}
        n=1
        new_state_dict = sample(problem_distribution_arr, state_dict, n) 
        self.assertEquals(new_state_dict,{(0,0):'f',(3,3):'B'},new_state_dict)
        random.seed(None) #Tear down

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()