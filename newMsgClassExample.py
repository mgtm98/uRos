from uros.core import *
from uros.core import create_message

#creating new msg class
std_Point = create_message(type = "std_msgs/Point", x = int, y = int, z = int)
uRos = Ros("0.0.0.0", 9090)                     #creating new uRos object
msg = std_Point(x = 4, y = 7, z = 0)            #creating a Ros string msg object
uRos.publish("uRosTopic", msg)                  #publishing the msg object