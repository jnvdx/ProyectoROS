import rospy 
from std_msgs.msg import String, Bool
from sensor_msgs.msg import JointState


class practica4:
    joint=list
    posicion=float
    velocidad=float
    esfuerzo=float

    def __init__(self) -> None:
        
        pass


    def callback_function(self,data:JointState)->None: 
        # rospy.loginfo("He recibido: %f, %f y %f", data.position, data.velocity, data.effort)
        print("He recibido: %f, %f y %f", data.position, data.velocity, data.effort)

        self.velocidad=data.velocity
        self.posicion=data.position
        self.esfuerzo=data.effort
        return
    

    def publisher(self)->None: 
        rospy.init_node('JonelPutoamo', anonymous=True) #Inicializa nodo 
        pub = rospy.Publisher('/movimiento', Bool, queue_size=10) #Crea el publicador en el topic /movimiento y tipo de mensaje String
        rospy.init_node('publicador', anonymous=True) #inicia el nodo publicador
        rate = rospy.Rate(0.5) # 0.5 Hz
        mensaje = Bool() #declaro la variable mensaje como tipo Bool
        # rospy.loginfo("Publicando en el topic /movimiento") #Escribo en log
        #Se subscribe al topic /joint_states con mensajes tipo String llamando a la funcion callback_function cuando se reciba mensaje
        rospy.Subscriber("/joint_states", JointState, practica4.callback_function)
        # rospy.Subscriber("/movimiento", String, callback_function)
        rospy.spin()
        while not rospy.is_shutdown(): #mientras ROS siga funcionando
            if self.velocidad > 0:
                mov = True
            else:
                mov = False
            mensaje.data = mov
            pub.publish(mensaje) #publica el mensaje en el topic
            rospy.loginfo("%s", mensaje.data) #escribe en log el mensaje
            rate.sleep()
        return

x=practica4()
if __name__ == '__main__':
    x.publisher()