from sys import platform as platform
import socket
import json
if platform == "esp32":
    import ujson as json
    import _thread as threading
else :
    import json
    import threading

'''
    Message Interface --> Base class of all ros messages
    get_type --> static methode to get the message type (String)
    get_data --> get message object as specified in .msg in ros (dic)
    load_msg --> static methode load a message from a dic
'''
class Msg_I:
    msgType = ""
    def __init__(self):
        self.msg_object = {}

    @staticmethod
    def get_type():
        return Msg_I.msgType
    
    def get_data(self):
        return self.msg_object
    
    @staticmethod
    def load_msg(dic):
        '''
        Convert json file to a message object
        :param dic: json string representation
        :return : return a message object
        :rtype : is determined by the subclass
        '''
        raise(Exception("Un impelemented, Inherit this class in your code"))

'''
    Class Generator for Ros messages
    Usage : 
        className = create_message(type = "classNameInRos", **kwargs)
        classNameInRos --> is the class name in ros api
        kwargs --> dic containing message fields
            key is field name 
            value is the python class coresponding to it's ros implementation
    Example : 
        std_Empty = create_message(type = "std_msgs/Empty")
        std_String = create_message(type = "std_msgs/String", data = str) 
'''
def create_message(**classAttributes):
    keys = classAttributes.keys()
    if "type" not in keys:
        raise Exception("No Message Type specified")
    
    msgType = classAttributes["type"]
    del classAttributes["type"]
    
    class Message(Msg_I):
        def __init__(self, **kwargs):
            keys = kwargs.keys()
            for key in keys:
                if key not in classAttributes.keys():
                    raise Exception("No attr: "+key+" in Message: " + msgType)
            self.msg_object = kwargs

        @staticmethod
        def get_type():
            return msgType
        
        def get_data(self):
            return self.msg_object
        
        @staticmethod
        def load_msg(jsonMsg:dict):
            msg = Message()
            for key in classAttributes.keys():
                try :
                    msg.msg_object[key] = classAttributes[key](jsonMsg[key])
                except:
                    raise Exception("Conversion error from " + str(type(jsonMsg[key]))+
                        " to "+str(classAttributes[key]))
            return msg
    return Message

'''
    Ros Class can do :
        - Topics publishing and subscribing
        - TODO Services requests
    Examples:
        uRos = Ros(IP OF ROS BRIDGE, PORT OF ROS BRIDGE)
        msg = std_Bool(data = False)

        def callback(msgType):
            print(msgType.get_data())

        uRos.registerMassege(std_String, std_Int32, std_Bool)
        uRos.subscribe("TEST22",callback, std_String)
        while True:
            uRos.publish("Test33", msg)
            time.sleep(1)
'''
class Ros :
    def __init__ (self, ip:str, port:int):
        '''
        Class COnstructor
        :param ip: ip of ros bridge server
        :param port: port of ros bridge server
        '''
        self.topic_subs = {}
        self.topic_advertised = []
        self.messagesType = []
        self.socket = socket.socket()
        self.socket.connect((ip, port))
        if platform == "esp32":
            threading.start_new_thread(self.__listen, ())
        else:
            threading.Thread(target = self.__listen).start()
    
    def __listen(self):
        ''' 
        Start listening to Ros Bridge server 
        Convert messages from the server to an appropriate msg object
        call the callback func with the msg object
        '''
        while True:
            data = self.socket.recv(4096)
            dataStr = str(data)
            dataJson = json.loads(dataStr[2:-1])
            if dataJson["op"] == "publish" and dataJson["topic"] in self.topic_subs:
                jsonMsg = dataJson["msg"]
                callback = self.topic_subs[dataJson["topic"]][0]
                msgClass  = self.topic_subs[dataJson["topic"]][1]
                msgObj = msgClass.load_msg(jsonMsg)
                callback(msgObj)

    def __advertiseTopic(self, topic_name:str, msgClass:Msg_I):
        '''
        Send the advertising request before publishing a topic or subscribing to a topic
        :param topic_name: topic name to advertise
        :param msgClass: msgClass to get the message type
        '''
        data = {
            "op" : "advertise",
            "topic" : topic_name,
            "type" : msgClass.get_type()
        }
        data_str = json.dumps(data)
        self.socket.send(data_str.encode())
        self.topic_advertised.append(topic_name)

    def publish(self, topic_name:str, msg:Msg_I):
        '''
        Publisihng a msg to Ros
        :param topic_name: topic name to publish
        :param msg: ros message to advertise
        '''
        if not(msg.__class__.__base__  == Msg_I):
            raise Exception("Msg class "+str(msg.__class__)+" is not a sub class of "+str(Msg_I))
        if topic_name not in self.topic_advertised:
            self.__advertiseTopic(topic_name, msg.__class__)
        data = {
            "op" : "publish",
            "topic" : topic_name,
            "msg" : msg.get_data()
        }
        data_str = json.dumps(data)
        self.socket.send(data_str.encode())

    def subscribe(self, topic_name:str, callback, msgClass:Msg_I):
        '''
        Subscrib to a Ros topic
        :param topic_name: topic name to subscribe to
        :param callback: callback func to be called with the msg object
        :param msgClass: Ros msg class which will be passed to the callback func

        callback func have a single param which is the msg object
        '''
        if topic_name not in self.topic_advertised:
            self.__advertiseTopic(topic_name, msgClass)
        if topic_name in self.topic_subs :
            if not(callback in self.topic_subs[topic_name]) :
                self.topic_subs[topic_name].append((callback, msgClass))
        else:
            self.topic_subs[topic_name] = (callback, msgClass)
        data = {
            "op" : "subscribe",
            "topic" : topic_name,
            "type" : msgClass.get_type()
        }
        data_str = json.dumps(data)
        self.socket.send(data_str.encode())

    def unsubscribe(self, topic_name:str):
        '''
        Unsubscribe a Ros topic
        :param topic_name: topic name to subscribe to
        '''
        data = {
            "op" : "unsubscribe",
            "topic" : topic_name,
        }
        data_str = json.dumps(data)
        self.socket.send(data_str.encode())

    def registerMassege(self, *messageClassVector):
        '''
        Registers a Ros Message type
        :param messageClassVector: ros message class
        '''
        for messageClass in messageClassVector :
            if messageClass not in self.messagesType:
                self.messagesType.append(messageClass)


    