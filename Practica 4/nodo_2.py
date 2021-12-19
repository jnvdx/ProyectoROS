from Practica4.practica4 import publisher
import rospy 
from std_msgs.msg import String, Bool
from sensor_msgs.msg import JointState
import time
import threading


class nodo_2:

    def __init__(self) -> None:
        pass

    def callback_function(self,data:Bool)->None: 
        pub = rospy.Publisher('/movimiento', Bool, queue_size=10) #Crea el publicador en el topic /movimiento y tipo de mensaje String
        rospy.init_node('publicador', anonymous=True) #inicia el nodo publicador
        mensaje = Bool()
        while data == True:
            mensaje.data = True
            pub.publish(mensaje)
            time.sleep(0.1)
            mensaje.data = False
            pub.publish(mensaje)
            time.sleep(0.1)

    def suscriber(self)->None: 
        rospy.init_node('Nodo2', anonymous=True) #Inicializa nodo 
        rate = rospy.Rate(60)
        rospy.Subscriber("/led", Bool, nodo_2.callback_function)
        rospy.spin()