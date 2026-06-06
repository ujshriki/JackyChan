bin_message = b''
from machine import UART
from Constants import *
SEN_START = ["!AIVDM", "$AIVDM"]
SEN_START_LEN = 6



def Find_Start_From_Point(pointer, encoded_message, encoded_message_len):
    sen_start_pos = -1 # default value for no start of sentence
    is_found = False
    sen_start = ""
    try:
        while not is_found and pointer+SEN_START_LEN <= encoded_message_len:
            try:
                sen_start = encoded_message[pointer:pointer+SEN_START_LEN].decode()
                if sen_start in SEN_START:
                    sen_start_pos = pointer
                    is_found = True
                else:
                    pointer += 1
            except:
                pointer += 1
    except Exception as e:
        print("error at find start")
        print(e)
        raise(e)
    
    return sen_start_pos


def Find_End_From_Point(pointer, encoded_message, encoded_message_len):
    sen_end_pos = -1 # default value for no start of sentence
    is_found = False
    sen_end = ""
    pointer += SEN_START_LEN
    try:
        while not is_found and pointer+3 <= encoded_message_len:
            try:
                sen_end = encoded_message[pointer:pointer+3].decode()
                if sen_end[0] == "*":
                    sen_end_pos = pointer
                    is_found = True
                else:
                    pointer += 1
            except:
                pointer += 1
    except Exception as e:
        print("error in find end")
        print(e)
        raise(e)
    
    return sen_end_pos+3


def Extract_Sentence(encoded_message):
    encoded_message_len = len(encoded_message)
    sen_start_pos = 0
    is_found = False
    valid_message = b''
    
    try:
        while not is_found:
            try:
                sen_start_pos = Find_Start_From_Point(sen_start_pos, encoded_message, encoded_message_len)
                
                #returns nothing if there is no start of sentence
                if sen_start_pos == -1:
                    print("no sentence start")
                    return b''
                
                sen_end_pos = Find_End_From_Point(sen_start_pos, encoded_message, encoded_message_len)
                
                #returns nothing if there is no end of sentence
                if sen_end_pos == -1:
                    sen_start_pos += 1
                else:
                    valid_message = encoded_message[sen_start_pos:sen_end_pos].decode()
                    is_found = True
            except Exception as e:
                print("error in extract sentence")
                print(e)
                raise(e)
    except:
        print("lead removal error")
        raise(Exception)
        
    return valid_message
        