import pybullet as p 
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK

class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK("brain.nndf")
        
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
            print(neuronName)
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                print(neuronName)
                print(jointName)

        for motor in self.motors:
            self.motorI = self.motors[motor]
            self.motorI.Set_Value(self.robotId,self.timeStep)

    def Think(self):
        self.nn.Update()
        self.nn.Print()
        
