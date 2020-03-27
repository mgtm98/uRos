from uros import *
from uros.std_msgs import std_Bool

count = 0
def callback(msgObj:Msg_I):
    global count
    print(msgObj.get_data())
    count = count + 1
    if count == 5:
        uRos.unsubscribe("uRosTopic")
        print("Unsubscribed")

uRos = Ros("0.0.0.0", 9090)                     #creating new uRos object
uRos.subscribe("uRosTopic", callback, std_Bool) #Subscribing to uRosTopic