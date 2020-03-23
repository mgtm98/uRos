from uros import *
from uros.std_msgs import std_Bool
def callback(msgObj:Msg_I):
    print(msgObj.get_data())

uRos = Ros("0.0.0.0", 9090)                     #creating new uRos object
uRos.subscribe("uRosTopic", callback, std_Bool) #Subscribing to uRosTopic