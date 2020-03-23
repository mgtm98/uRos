# uRos
_uRos is a Ros implementation for micropython boards. It uses Ros bridge to communicate with Ros Master_

## Boards Supported
_Any board with thread module enabled can use this module like esp32_

## Features Supported

- [x] Publisihng Ros Topics  
- [x] Subscribing to Ros Topics
- [x] Message Generator to create various Messages
- [ ] Standard Ros Messages 
- [ ] Ros Services
- [ ] Service Generator to create various Services

## Examples
First launch rosbridge `roslaunch rosbridge_server rosbridge_tcp.launch 
 `
1. Publish a Ros msg
```python3
from uros import *
from uros.std_msgs import std_Bool

uRos = Ros("0.0.0.0", 9090)    #creating new uRos object
msg = std_Bool(data = True)    #creating a Ros string msg object
uRos.publish("uRosTopic", msg) #publishing ros message   
```
2. Subscribe to a Ros msg
```python3
from uros import *
from uros.std_msgs import std_Bool

def callback(msgObj:Msg_I):                     # Call back function
    print(msgObj.get_data())

uRos = Ros("0.0.0.0", 9090)                     #creating new uRos object
uRos.subscribe("uRosTopic", callback, std_Bool) #Subscribing to uRosTopic  
```
 3. Create a new Ros msg Class
```python3
from uros.core import *
from uros.core import create_message

#creating new msg class
std_Point = create_message(type = "std_msgs/Point", x = int, y = int, z = int)
uRos = Ros("0.0.0.0", 9090)                     #creating new uRos object
msg = std_Point(x = 4, y = 7, z = 0)            #creating a Ros string msg object
uRos.publish("uRosTopic", msg)                  #publishing the msg object 
```

## TODO List
- Standard Ros Messages 
- Ros Services
- Service Generator to create various Services

# Author
Mohamed Gamal 
mgtm.prog@gmail.com