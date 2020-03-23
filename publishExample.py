from uros import *
from uros.std_msgs import std_Bool

uRos = Ros("0.0.0.0", 9090)                     #creating new uRos object
msg = std_Bool(data = True)    #creating a Ros string msg object
uRos.publish("uRosTopic", msg)                  #publishing the msg object