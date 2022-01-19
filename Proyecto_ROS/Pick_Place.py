import rospy
import sys
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from math import pi        
from geometry_msgs.msg import Pose
from RG2_ROS_Driver.srv import Grip,GripRequest
from std_msgs.msg import Float64,String
from moveit_commander import roscpp_initialize, MoveGroupCommander,RobotCommander, PlanningSceneInterface
from time import sleep

class PickPlace:
    """
        asdasd
    """

    def __init__(self) -> None:
        """
            asdasd
        """
        rospy.init_node('ProyectoRos_Grupo1',anonymous=True)
        roscpp_initialize(sys.argv)
        self.robot=RobotCommander() 
        self.escena=PlanningSceneInterface()
        self.robot1=MoveGroupCommander("robot_1")
        self.robot2=MoveGroupCommander("robot_2")
        self.publicador=rospy.Publisher("LCD",String,queue_size=10)
        self.distancia_x=None   
        self.inicio1=Pose()
        self.posicion_cubo_inicial = Pose()
        self.posicion_cubo_final = Pose()  
        self.posicion_cubo_intermedia_1=Pose()
        self.posicion_cubo_intermedia_2=Pose()
        self.servicio_pinza_1 = rospy.ServiceProxy('robot_1/rg2/grip', Grip)
        self.servicio_pinza_2 = rospy.ServiceProxy('robot_2/rg2/grip', Grip)
        self.var_cubo = 0.025
        self.cubo=1
        self.contador = 0

        while not rospy.is_shutdown():
            try:                
                self.talker()
            except rospy.ROSInterruptException:
                pass

    def OB100(self)->None:
        """
            asdas
        """
        self.inicio1.position.x=0.15802545255793177
        self.inicio1.position.y=0.15922947364131035
        self.inicio1.position.z=1.1936716765955642
        self.inicio1.orientation.w=0.9240322715144885
        self.inicio1.orientation.x=-0.00029335692243719964
        self.inicio1.orientation.y=.0024024709762824215
        self.inicio1.orientation.z=0.3823068182424936
        inicio2=Pose()
        inicio2.position.x=0.719707091452666
        inicio2.position.y=0.14075013043696466
        inicio2.position.z=1.1936732125644935
        inicio2.orientation.w=0.3049306553217612
        inicio2.orientation.x=-0.001977829849686988
        inicio2.orientation.y=0.0014433287412299375
        inicio2.orientation.z=0.9523714088717027
        try:
            self.robot1.go(self.inicio1,wait=True)
            self.robot2.go(inicio2,wait=True)
        except:
            pass
        self.grip_abrir_1()
        self.grip_abrir_2()
    
    def __inicializar(self)->None:
        """
            asdasd
        """
        self.posicion_cubo_inicial.position.x=0.11090371265053467
        self.posicion_cubo_inicial.position.y=0.46286956325479534
        self.posicion_cubo_inicial.position.z=0.8363695312953106
        angulos1=quaternion_from_euler(pi/2,pi/2,2*pi)
        self.posicion_cubo_inicial.orientation.x=angulos1[0]
        self.posicion_cubo_inicial.orientation.y=angulos1[1]
        self.posicion_cubo_inicial.orientation.z=angulos1[2]
        self.posicion_cubo_inicial.orientation.w=angulos1[3]

        self.posicion_cubo_final.position.x=0.7771019187832774
        self.posicion_cubo_final.position.y=0.43383607017033393
        self.posicion_cubo_final.position.z=0.8378529075664301
        angulos2=quaternion_from_euler(pi/2,pi/2,2*pi)
        self.posicion_cubo_final.orientation.x=angulos2[0]
        self.posicion_cubo_final.orientation.y=angulos2[1]
        self.posicion_cubo_final.orientation.z=angulos2[2]
        self.posicion_cubo_final.orientation.w=angulos2[3] 

        self.posicion_cubo_intermedia_1.position.x=0
        self.posicion_cubo_intermedia_1.position.y=0
        self.posicion_cubo_intermedia_1.position.z=0
        angulos2=quaternion_from_euler(pi/2,pi/2,2*pi)
        self.posicion_cubo_intermedia_1.orientation.x=angulos2[0]
        self.posicion_cubo_intermedia_1.orientation.y=angulos2[1]
        self.posicion_cubo_intermedia_1.orientation.z=angulos2[2]
        self.posicion_cubo_intermedia_1.orientation.w=angulos2[3]

        self.posicion_cubo_intermedia_2.position.x=0
        self.posicion_cubo_intermedia_2.position.y=0
        self.posicion_cubo_intermedia_2.position.z=0
        angulos2=quaternion_from_euler(pi/2,pi/2,2*pi)
        self.posicion_cubo_intermedia_2.orientation.x=angulos2[0]
        self.posicion_cubo_intermedia_2.orientation.y=angulos2[1]
        self.posicion_cubo_intermedia_2.orientation.z=angulos2[2]
        self.posicion_cubo_intermedia_2.orientation.w=angulos2[3]

    def grip_cerrar_1(self)->None:
        """
            asdasd
        """
        peticion = GripRequest()
        peticion.force.data = 40 # 0-40 N
        peticion.width.data = 60 # 0-100 mm
        peticion.depth_compensation.data = False
        self.servicio_pinza_1.call(peticion)

        peticion.force.data = 5 # 0-40 N
        peticion.width.data = 0 # 0-100 mm
        peticion.depth_compensation.data = False
        self.servicio_pinza_1.call(peticion)

    def grip_cerrar_2(self)->None:
        """
            asdasd
        """
        peticion = GripRequest()
        peticion.force.data = 40 # 0-40 N
        peticion.width.data = 60 # 0-100 mm
        peticion.depth_compensation.data = False
        self.servicio_pinza_2.call(peticion)

        peticion.force.data = 5 # 0-40 N
        peticion.width.data = 0 # 0-100 mm
        peticion.depth_compensation.data = False
        self.servicio_pinza_2.call(peticion)

    def grip_abrir_1(self)->None:
        """
            asdasd
        """
        peticion = GripRequest()
        peticion.force.data = 40 # 0-40 N
        peticion.width.data = 100 # 0-100 mm
        peticion.depth_compensation.data = False
        self.servicio_pinza_1.call(peticion)

    def grip_abrir_2(self)->None:
        """
            asdasd
        """
        peticion = GripRequest()
        peticion.force.data = 40 # 0-40 N
        peticion.width.data = 100 # 0-100 mm
        peticion.depth_compensation.data = False
        self.servicio_pinza_2.call(peticion)

    def pick_1(self)->None:
        """
            asdasd
        """
        try:
            self.robot1.go(self.posicion_cubo_inicial, wait = True)
        except:
            print("Error Pick_1 go 1")
        puntos=self.robot1.get_current_pose().pose
        puntos.position.z-=0.1
        (plan,porcentaje_ejecucion) = self.robot1.compute_cartesian_path(puntos,0.01,0.0)
        if porcentaje_ejecucion==1:
            try:
                self.robot1.execute(plan,wait=True)
            except:
                print("Error Pick_1 execute 1")
        self.grip_cerrar_1()
        puntos.position.z+=0.1
        (plan,porcentaje_ejecucion) = self.robot1.compute_cartesian_path(puntos,0.01,0.0)
        if porcentaje_ejecucion==1:
            try:
                self.robot1.execute(plan,wait=True)
            except:
                print("Error Pick_1 execute 2")


    def pick_2(self)->None:
        """
            asdasd
        """
        try:
            self.robot1.go(self.posicion_cubo_intermedia_2, wait = True)
        except:
            print("Error Pick_2 go 1")
        puntos=self.robot1.get_current_pose().pose
        puntos.position.z-=0.1
        (plan,porcentaje_ejecucion) = self.robot1.compute_cartesian_path(puntos,0.01,0.0)
        if porcentaje_ejecucion==1:
            try:
                self.robot1.execute(plan,wait=True)
            except:
                print("Error Pick_2 execute 1")
        self.grip_cerrar_1()
        puntos.position.z+=0.1
        (plan,porcentaje_ejecucion) = self.robot1.compute_cartesian_path(puntos,0.01,0.0)
        if porcentaje_ejecucion==1:
            try:
                self.robot1.execute(plan,wait=True)
            except:
                print("Error Pick_2 execute 2")

    def place_1(self)->None:
        """
            asdasd
        """
        try:
            self.robot1.go(self.posicion_cubo_intermedia_1, wait = True)
        except:
            print("Error Place_1 go 1")
        puntos=self.robot1.get_current_pose().pose
        puntos.position.z-=0.1
        (plan,porcentaje_ejecucion) = self.robot1.compute_cartesian_path(puntos,0.01,0.0)
        if porcentaje_ejecucion==1:
            try:
                self.robot1.execute(plan,wait=True)
            except:
                print("Error Place_1 execute 1")
        self.grip_cerrar_1()
        puntos.position.z+=0.1
        (plan,porcentaje_ejecucion) = self.robot1.compute_cartesian_path(puntos,0.01,0.0)
        if porcentaje_ejecucion==1:
            try:
                self.robot1.execute(plan,wait=True)
            except:
                print("Error Place_1 execute 2")


    def place_2(self)->None:
        """
            asdasd
        """
        try:
            self.robot1.go(self.posicion_cubo_final, wait = True)
        except:
            print("Error Place_2 go 1")
        puntos=self.robot1.get_current_pose().pose
        puntos.position.z-=0.1
        (plan,porcentaje_ejecucion) = self.robot1.compute_cartesian_path(puntos,0.01,0.0)
        if porcentaje_ejecucion==1:
            try:
                self.robot1.execute(plan,wait=True)
            except:
                print("Error Place_2 execute 1")
        self.grip_cerrar_1()
        puntos.position.z+=0.1
        (plan,porcentaje_ejecucion) = self.robot1.compute_cartesian_path(puntos,0.01,0.0)
        if porcentaje_ejecucion==1:
            try:
                self.robot1.execute(plan,wait=True)
            except:
                print("Error Place_2 execute 2")

    
    def mover(self)->None:
        """
            asdasd
        """
        self.__inicializar()
        self.OB100()
        for i in range(8):
            if self.cubo==6:
                self.posicion_cubo_final.position.y+=0.1
            if self.cubo==9:
                self.posicion_cubo_final.position.y+=0.075
            self.contador=0
            self.pick_1()
            self.contador+=1
            self.place_1()
            self.contador+=1
            self.pick_2()
            self.contador+=1
            self.place_2()
            self.contador+=1
            self.cubo += 1
            self.posicion_cubo_inicial.position.y-=self.var_cubo
            self.posicion_cubo_final.position.y-=self.var_cubo
    
    def talker(self)->None:
        """
            asdasd
        """
        mensaje=String()
        if self.contador==0:
            pass
        if self.contador==1:
            mensaje.data=f"Cubo {self.cubo} recogido por robot 1"
            self.publicador.publish(mensaje)
        if self.contador==2:
            mensaje.data=f"Cubo {self.cubo} dejado por robot 1"
            self.publicador.publish(mensaje)
        if self.contador==3:
            mensaje.data=f"Cubo {self.cubo} recogido por robot 2"
            self.publicador.publish(mensaje)
        if self.contador==4:
            mensaje.data=f"Cubo {self.cubo} dejado por robot 2"
            self.publicador.publish(mensaje)
        if self.contador==4:
            mensaje.data=f"Rutina cubo {self.cubo} ejecutado correctamente"
            self.publicador.publish(mensaje)
 
Prueba=PickPlace()
Prueba.mover()