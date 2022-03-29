import pybullet as p 
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c

class ROBOT:
    def __init__(self, solutionID):
        self.solutionID= solutionID
        self.brainName = "brain" +str(self.solutionID)+".nndf"
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK(self.brainName)

        os.system('rm ' +self.brainName)
        

    def Prepare_To_Sense(self):
        self.sensors ={}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, timeStep):
        self.timeStep=timeStep
        for i in self.sensors:
            self.sensorI = self.sensors[i]
            self.sensorI.getValue(self.timeStep)


    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName]= MOTOR(jointName)

    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motorI = self.motors[jointName]
                self.motorI.Set_Value(self.robotId,desiredAngle)
                
    def Think(self):
        self.nn.Update()
        #self.nn.Print()
    
    def Get_Fitness(self):
        #self.stateOfLinkZero = p.getLinkState(self.robotId,0)
        self.basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        #self.positionOfLinkZero = self.stateOfLinkZero[0]
        self.basePosition = self.basePositionAndOrientation[0]
        #self.xCoordinateOfLinkZero = self.positionOfLinkZero[0]
        self.xPosition = self.basePosition[0]
        #print(self.xCoordinateOfLinkZero)
        
        self.fileName = 'tmp'+str(self.solutionID)+'.txt'
        f = open(self.fileName, "w")
        f.write(str(self.xPosition))
        f.close()

        self.newFileName = 'fitness'+str(self.solutionID)+'.txt'
        os.system('mv ' + self.fileName+ ' '+ self.newFileName)

    
        
