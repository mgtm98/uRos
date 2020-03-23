from .core import create_message

std_Bool        = create_message(type = "std_msgs/Bool", data = bool)
std_Byte        = create_message(type = "std_msgs/Byte", data = int)
std_Char        = create_message(type = "std_msgs/Char", data = chr)
std_ColorRGBA   = create_message(type = "std_msgs/ColorRGBA", r = float, g = float, b = float, a = float)
std_String      = create_message(type = "std_msgs/String", data = str)
std_Empty       = create_message(type = "std_msgs/Empty")
std_Int32       = create_message(type = "std_msgs/Int32", data = int)
std_Float32     = create_message(type = "std_msgs/Float32", data = float)

#TODO add the rest of ros std msgs