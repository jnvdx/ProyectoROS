import rospy
from time import sleep
from std_msgs.msg import Bool
from threading import Thread

class DetectorMovimiento:
    def __init__(self) -> None:
        """
            Inicializa el nodo, el publicador y el subscriptor ademas de algunas variables de la clase
    
            El while al final es para llamar al talker mientras el programa no pierda conexion con ROS
        """
        rospy.init_node('Nodo_2', anonymous=True)
        rospy.Subscriber("movimiento_robot_1", Bool, self.__callback1)
        rospy.Subscriber("movimiento_robot_2", Bool, self.__callback2)
        self.publicador = rospy.Publisher('led', Bool, queue_size=1)
        self.movimiento1 = False 
        self.movimiento2 = False 
        
        while not rospy.is_shutdown():
            try:                
                self.talker()
            except rospy.ROSInterruptException:
                pass

    def __callback1(self,movimiento1:Bool)->None:
        """
            Recoge los datos de movimiento del robot

            @param Bool movimiento1 = Booleano de ROS entragdo por el sensor del robot 1
        """
        self.movimiento1=movimiento1.data
    
    def __callback2(self,movimiento2:Bool)->None:
        """
            Recoge los datos de movimiento del robot

            @param Bool movimiento2 = Booleano de ROS entragdo por el sensor del robot 2
        """
        self.movimiento2=movimiento2.data

    def talker(self)->None:
        """
            La funcion en la que vamos a enviar la informacion al led, en este caso sera un booleano
        """
        encender=Bool()
        apagar=Bool()
        encender.data=True; apagar.data=False; movimiento=True
        self.publicador.publish(apagar)

        while self.movimiento1==True or self.movimiento2==True:
            frecuencia=rospy.Rate(10)
            if self.movimiento1 and self.movimiento2:
                frecuencia=rospy.Rate(20)
            self.publicador.publish(encender)
            frecuencia.sleep
            self.publicador.publish(apagar)
            frecuencia.sleep()
 
        self.publicador.publish(apagar)
    
        
if __name__=="__main__":
    prueba=DetectorMovimiento()