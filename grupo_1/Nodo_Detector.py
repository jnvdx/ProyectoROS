import rospy
from time import sleep,time
from std_msgs.msg import Bool
from sensor_msgs.msg import JointState
from threading import Thread

class DetectorMovimiento:

    def __init__(self) -> None:
        """
            Inicializa el nodo, el publicador y el subscriptor ademas de algunas variables de la clase
    
            El while al final es para llamar al talker mientras el programa no pierda conexion con ROS
        """
        rospy.init_node('Nodo_1', anonymous=True)
        self.subscriptor=rospy.Subscriber("joint_states", JointState, self.__callback)
        self.publicador = rospy.Publisher('movimiento', Bool, queue_size=10)
        self.posicion=JointState()
        self.movimiento=False
        self.inicio=False
        self.memoria=[]
        self.num_movimiento=0
        
        while not rospy.is_shutdown():
            try:                
                self.talker()
            except rospy.ROSInterruptException:
                pass
        
    def __callback(self,jointstate:JointState):
        """
            Recoge los datos de posicion de los joints del robot

            @param Jointstate jointstate = Datos del robot
        """
        self.posicion=jointstate
    
    def talker(self):
        """
            Manda un booleano al topic subscrito diciendole si el robot se mueve o no
            Ademas recoge en una variable de la clase el tiempo que ha tardado y el numero de movimiento
            para luego meterlo en un fichero
        """
        self.__ComprobarMovimiento()

        if self.inicio==False  and self.movimiento==True:    
            self.tiempo = time()
            self.inicio = True

        if self.inicio==True and self.movimiento==False:
            self.inicio = False
            t = time() - self.tiempo 
            self.memoria.append([self.num_movimiento,t])

            with open("movimientos_robot","a+") as file: 
                file.write(str(self.memoria[self.num_movimiento-1])) 
                file.write("\n")

            self.num_movimiento+=1

        self.publicador.publish(self.movimiento)  

    def __ComprobarMovimiento(self):
        """
            Comprueba si el robot se mueve o no
        """
        if not self.posicion.position:
            return
        velocidad = list(self.posicion.velocity)
        robot = velocidad[:6]     
        for i in range(0,5):
            if ((robot[i]<0.001)and(robot[i]>-0.001)): 
                self.movimiento = False
            else:
                self.movimiento = True
    

if __name__=="__main__":
    prueba=DetectorMovimiento()