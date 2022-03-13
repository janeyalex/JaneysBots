
import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c
import os
import random

class SOLUTION:
    def __init__(self):
        self.weights = np.empty([3,2])
        for i in range(3):
            for j in range(2):
                self.weights [i][j] = np.random.rand()
        self.weights = self.weights * 2 - 1
        
    def Evaluate(self, displaySetting):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        os.system('python3 simulate.py ' + displaySetting)

        f = open("fitness.txt", "r")
        self.fitness = float(f.read())
        f.close()


        
        

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[c.x,c.y,c.z] , size=[c.length,c.width,c.height])       
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        ###### Joe's Code
        pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[c.length, c.width, c.height])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[1, 0, 1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-.5, 0, -.5], size=[c.length, c.width, c.height])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2, 0, 1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[.5, 0, -.5], size=[c.length, c.width, c.height])
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

        row = [0,1,2]
        col = [0,1]
        for currentRow in row:
            for currentColumn in col:
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+3, weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        self.randRow = random.randint(0,2)
        self.randCol = random.randint(0,1)


        self.weights[self.randRow][self.randCol]= (np.random.rand()) *2 -1