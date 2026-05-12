bin_message = b''
from machine import UART
from Constants import *
SEN_START = "!AIVDM"
SEN_START2 = "$AIVDM" 

def get_center(last_valid, last_invalid):
    center = 0
    distance = 0
    
    if last_valid > last_invalid:
        distance = last_valid - last_invalid # gets the distance between the last valid and invalid
        distance = distance - (distance//2) #gets the upper range of half the distance
        center = last_invalid + distance
        
    elif last_invalid > last_valid:
        distance = last_invalid - last_valid # gets the distance between the last valid and invalid
        distance = distance - (distance//2) #gets the upper range of half the distance
        center = last_invalid + distance
        
    return center


def Extract_Sentence(encoded_message):
    pointer = 0
    last_valid_char = len(encoded_message)
    last_invalid_char = 0
    is_found = False
    valid_message = b''
    sentance_start = 0
    
    while(not is_found):
        pointer = get_center(last_valid_char, last_invalid_char)
        try:
            encoded_message[pointer].decode()
            last_valid_char = pointer
            if encoded_message[pointer].decode() == SEN_START[0]:
                if encoded_message[pointer:pointer + len(SEN_START)-1].decode() == SEN_START:
                    sentance_start = pointer
                    valid_message = encoded_message[sentance_start:-1]
                    is_found = True
                elif encoded_message[pointer:pointer + len(SEN_START)-1].decode() == SEN_START2:
                    sentance_start = pointer
                    valid_message = encoded_message[sentance_start:-1]
                    is_found = True
                else:
                    sentance_start = pointer
                    valid_message = encoded_message[sentance_start:-1]
                    is_found = True
        except Exception as e:
            last_invalid_char = pointer
    
    try:
        return valid_message.decode()
    except Exception as e:
        print("healap")
        print(e)
        
    return valid_message
        