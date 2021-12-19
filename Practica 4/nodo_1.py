from Practica4.practica4 import publisher
import rospy 
from std_msgs.msg import String, Bool
from sensor_msgs.msg import JointState
import time
import threading


class nodo_1:

    joint=list
    posicion=float
    velocidad=float
    esfuerzo=float
    n_movs = 0
    mov = False

    def __init__(self) -> None:
        pass

    def file_log(self)->None:
        tiempo = 0
        while self.mov == True:
            tiempo = tiempo + time.time()
            
        with open('movimientos_robot', 'a+') as f:
            f.write(str(self.n_movs) + "->" + str(tiempo))


    def callback_function(self,data:JointState)->None: 
        # rospy.loginfo("He recibido: %f, %f y %f", data.position, data.velocity, data.effort)
        print("He recibido: %f, %f y %f", data.position, data.velocity, data.effort)

        self.velocidad=data.velocity
        self.posicion=data.position
        self.esfuerzo=data.effort

    

    def publisher(self)->None: 
        rospy.init_node('Nodo1', anonymous=True) #Inicializa nodo 
        pub = rospy.Publisher('/movimiento', Bool, queue_size=10) #Crea el publicador en el topic /movimiento y tipo de mensaje String
        rospy.init_node('publicador', anonymous=True) #inicia el nodo publicador
        rate = rospy.Rate(60) 
        mensaje = Bool() #declaro la variable mensaje como tipo Bool
        # rospy.loginfo("Publicando en el topic /movimiento") #Escribo en log
        #Se subscribe al topic /joint_states con mensajes tipo String llamando a la funcion callback_function cuando se reciba mensaje
        rospy.Subscriber("/joint_states", JointState, nodo_1.callback_function)
        # rospy.Subscriber("/movimiento", String, callback_function)
        rospy.spin()
        while not rospy.is_shutdown(): #mientras ROS siga funcionando
            if self.velocidad > 0:
                self.mov = True
                self.n_movs = self.n_movs + 1

            else:
                self.mov = False
            mensaje.data = self.mov
            pub.publish(mensaje) #publica el mensaje en el topic
            rospy.loginfo("%s", mensaje.data) #escribe en log el mensaje
            rate.sleep()




x=nodo_1()
if __name__ == '__main__':

    hilo1 = threading.Thread(target=publisher)
    hilo2 = threading.Thread(target=file_log)
    hilo1.start()
    hilo2.start()
    x.publisher()
    x.file_log()
