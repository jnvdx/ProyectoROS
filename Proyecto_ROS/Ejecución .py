# from Pick_Place import PickPlace
# 
# Prueba=PickPlace()
# Prueba.mover()
# from math import pi
# from tf.transformations import quaternion_from_euler, euler_from_quaternion
# from moveit_commander import MoveGroupCommander, roscpp_initialize, RobotCommander
# import rospy
# import sys
# rospy.init_node('suscriptor_basico',anonymous=True)
# roscpp_initialize(sys.argv)
# 
# robot=RobotCommander()
# robot1=MoveGroupCommander("robot_1")
# robot2=MoveGroupCommander("robot_2")
# 
# pos=robot1.get_current_pose().pose
# pos2=robot2.get_current_pose()
# angulos=quaternion_from_euler(pi/2,pi/2,2*pi)
# pos.orientation.x=angulos[0]
# pos.orientation.y=angulos[1]
# pos.orientation.z=angulos[2]
# pos.orientation.w=angulos[3]
# 
# robot1.go(pos,wait=True)

for i in range(8):
    print(i) 