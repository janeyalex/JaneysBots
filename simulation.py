from world import WORLD
from robot import ROBOT
import pybullet as p 
import pybullet_data
import pyrosim.pyrosim as pyrosim
from time import sleep

class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        self.world = WORLD()
        self.robot = ROBOT()
        

    def Run(self):
        for timeStep in range(1000):
             sleep(1/60)
             p.stepSimulation()
             self.robot.Sense(timeStep)
             exit()
             self.robot.Think()
             self.robot.Act()


        
    def __del__(self):
        p.disconnect()


    