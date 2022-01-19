
from multiprocessing.connection import wait
import rospy
import sys
from sensor_msgs.msg import JointState
from time import time, sleep
from copy import deepcopy
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from math import pi        
from geometry_msgs.msg import Pose
from RG2_ROS_Driver.srv import Grip, GripRequest, GripResponse
from std_msgs.msg import Float64
from moveit_commander.move_group import MoveGroupCommander
from moveit_commander.robot import RobotCommander
from moveit_commander.planning_scene_interface import PlanningSceneInterface
from moveit_commander.roscpp_initializer import roscpp_initialize

class PickPlace:

    def __init__(self) -> None:
        rospy.init_node('suscriptor_basico',anonymous=True)
        roscpp_initialize(sys.argv)
        self.escena=PlanningSceneInterface
        self.robot=RobotCommander
        self.robot1=MoveGroupCommander("/robot_1")
        self.robot2=MoveGroupCommander("/robot_2")
        self.ultrasonidos1=rospy.Subscriber("ultrasonidos_1/distancia_ultrasonidos",Float64,self.callback1)
        self.distancia_x:float   
        self.posicion_inicial_1:Pose()=[0.5792169525645172,0.13646120053232186,0.8870346085351367,0.5,0.5,0.5,-0.5]     
        self.posicion_inicial_:Pose()=[0.35778275648725827,0.11665991347163007,0.9170555365465255,-0.5,0.5,0.5,0.5] 
        self.servicio_pinza_1 = rospy.ServiceProxy('/robot_1/rg2/grip', Grip)
        self.servicio_pinza_2 = rospy.ServiceProxy('/robot_2/rg2/grip', Grip)
        self.posicion_pick = []
        self.posicion_place = []
        self.altura_funcionamiento = 0.20
        self.var_cubo = 0.025
        self.var_cubo_2 = 0.025
        self.contador = 0
        self.altura_place = 0
        

        while not rospy.is_shutdown():
            try:                
                self.talker()
            except rospy.ROSInterruptException:
                pass
    
    def callback1(self, dato:Float64):
        pass
    

    def grip_cerrar_1(self):
        peticion = GripRequest()
        peticion.force.data = 40 # 0-40 N
        peticion.width.data = 60 # 0-100 mm
        peticion.depth_compensation.data = False

        self.servicio_pinza_1.call(peticion)

        peticion.force.data = 5 # 0-40 N
        peticion.width.data = 0 # 0-100 mm
        peticion.depth_compensation.data = False

        self.servicio_pinza_1.call(peticion)

    def grip_cerrar_2(self):
        peticion = GripRequest()
        peticion.force.data = 40 # 0-40 N
        peticion.width.data = 60 # 0-100 mm
        peticion.depth_compensation.data = False

        self.servicio_pinza_2.call(peticion)

        peticion.force.data = 5 # 0-40 N
        peticion.width.data = 0 # 0-100 mm
        peticion.depth_compensation.data = False

        self.servicio_pinza_2.call(peticion)

    def grip_abrir_1(self):
        peticion = GripRequest()
        peticion.force.data = 0 # 0-40 N
        peticion.width.data = 100 # 0-100 mm
        peticion.depth_compensation.data = False

        self.servicio_pinza_1.call(peticion)

    def grip_abrir_2(self):
        peticion = GripRequest()
        peticion.force.data = 0 # 0-40 N
        peticion.width.data = 100 # 0-100 mm
        peticion.depth_compensation.data = False

        self.servicio_pinza_2.call(peticion)

    def pick_1(self):

        self.robot1.go(self.posicion_inicial_1, wait = True)

        self.var_cubo = self.var_cubo + 0.25 #Referenciar anchura cubo
        self.posicion_inicial_1.position.x = 0.4 + self.var_cubo
        self.posicion_inicial_1.position.y = 0.4
        self.posicion_inicial_1.position.z = 0.04
        time.sleep(200)
        
        self.robot1.go(self.posicion_inicial_1, wait = True)
        
        self.posicion_inicial_1.position.z = 0.04 - self.altura_funcionamiento

        self.robot1.go(self.posicion_inicial_1, wait = True)
        
        self.grip_cerrar_1()
        
        self.posicion_inicial_1.position.z = 0.04 - self.altura_funcionamiento

        self.robot1.go(self.posicion_inicial_1, wait = True)

        self.posicion_inicial_1.position.z = 0.04 - self.altura_funcionamiento

        self.robot1.go(self.posicion_inicial_1, wait = True)


    def pick_2(self):

        self.robot2.go(self.posicion_inicial_2, wait = True)

        self.posicion_inicial_2.position.z = 0.04 + self.altura_funcionamiento

        self.robot2.go(self.posicion_inicial_2, wait = True)

        self.posicion_inicial_2.position.z = 0.04 + self.altura_funcionamiento
        self.posicion_inicial_2.position.x = 0.3
        self.posicion_inicial_2.position.y = 0.6

        self.robot2.go(self.posicion_inicial_2, wait = True)
        
        self.grip_cerrar_2()

        self.posicion_inicial_2.position.z = 0.04 + self.altura_funcionamiento

        self.robot2.go(self.posicion_inicial_2, wait = True)

    def place_1(self):

        self.posicion_inicial_1.position.z = 0.04 - self.altura_funcionamiento
        self.posicion_inicial_1.position.x = 0.3
        self.posicion_inicial_1.position.y = 0.6 

        self.robot1.go(self.posicion_inicial_1, wait = True)

        self.grip_abrir_1()

        self.posicion_inicial_1.position.z = 0.04 + self.altura_funcionamiento

        self.robot1.go(self.posicion_inicial_1, wait = True)

        self.posicion_inicial_1=[0.5792169525645172,0.13646120053232186,0.8870346085351367,0.5,0.5,0.5,-0.5]

        self.robot1.go(self.posicion_inicial_1, wait = True)


    def place_2(self):


        if self.contador == 10:
            self.contador = 0
            self.altura_place = 0

        if self.contador <= 5:
            self.var_cubo_2 = 0.075
            self.altura_place = 0

        if self.contador > 5 and self.contador <=8:
            self.var_cubo_2 = 0.05
            self.altura_place = 0.025 #Referencia altura de cubo

        if self.contador == 9:
            self.altura_place = 0.05 #Referencia altura de cubo


    
        self.var_cubo_2 = self.var_cubo_2 + 0.025
        self.posicion_inicial_2.position.x = 0.6
        self.posicion_inicial_2.position.x = self.posicion_inicial.position.x + self.var_cubo_2

        self.robot2.go(self.posicion_inicial_2, wait = True)

        self.posicion_inicial.position.z = 0.04 + self.altura_place

        self.robot2.go(self.posicion_inicial_2, wait = True)

        self.grip_abrir_2()

        self.posicion_inicial_2.position.z = 0.04 + self.altura_funcionamiento

        self.robot2.go(self.posicion_inicial_2, wait = True)
        

    def mover(self):
        self.var_cubo = -0.025
        self.var_cubo_2 = -0.025
        self.contador = 0
        self.grip_abrir_2()
        self.grip_abrir_1()
        self.robot1.go(self.posicion_inicial_1,wait=True)
        self.robot2.go(self.posicion_inicial_2,wait=True)

        while self.contador < 10:
            self.pick_1()
            print("Pick 1 del cubo %i ejecutado correctamente", self.contador)
            self.place_1()
            print("Place 1 del cubo %i ejecutado correctamente", self.contador)
            self.pick_2()
            print("Pick 2 del cubo %i ejecutado correctamente", self.contador)
            self.place_2()
            print("Place 2 del cubo %i ejecutado correctamente", self.contador)
            self.contador += 1


    
