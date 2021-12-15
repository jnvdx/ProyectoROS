import rospy 
from std_msgs.msg import String
from msg import joint 

def callback_function(data): 
    rospy.loginfo("He recibido: %f, %f y %f", data.position, data.velocity, data.effort)
    print("He recibido: %f, %f y %f", data.position, data.velocity, data.effort)

def publisher(): 
    rospy.init_node('JonelPutoamo', anonymous=True) #Inicializa nodo 

    pub = rospy.Publisher('/movimiento', String, queue_size=10) #Crea el publicador en el topic /movimiento y tipo de mensaje String
    rospy.init_node('publicador', anonymous=True) #inicia el nodo publicador
    rate = rospy.Rate(0.5) # 0.5 Hz
    mensaje = String() #declaro la variable mensaje como tipo String
    rospy.loginfo("Publicando en el topic /movimiento") #Escribo en log

    #Se subscribe al topic /joint_states con mensajes tipo String llamando a la funcion callback_function cuando se reciba mensaje
    rospy.Subscriber("/joint_states", joint, callback_function)
    rospy.Subscriber("/movimiento", String, callback_function)
    rospy.spin()

    while not rospy.is_shutdown(): #mientras ROS siga funcionando
        if joint.velocity > 0:
            mov = "True"
        else:
            mov = "False"
        mensaje.data = mov
        pub.publish(mensaje) #publica el mensaje en el topic
        rospy.loginfo("%s", mensaje.data) #escribe en log el mensaje 
        rate.sleep()


if __name__ == '__main__':
    publisher()
    