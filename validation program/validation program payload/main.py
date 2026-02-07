import utime
from Constants import *
from Message_Data_Decode_Module import Decode_Msg_To_Bitstring, Seperate_Msg_Fields
from Load_JSON_Module import MSG_TYPE_PARSE_LISTS_DICTIONARY, MSG_TYPE_VALID_VALUES_LISTS_DICTIONARY, Load_Msg_Struct_Dicts, Load_Msg_Type_Valid_Values_Dicts
from Payload_Validation_Module import Is_Message_Valid
from Debug_Module import DBG_Print
from machine import UART, Pin

structure_json_folder = "/MSG_Struct/"
valid_values_json_folder = "/MSG_Valid_Value/"



# the json is an unordered data structure, if i want to keep the order of what i put in the file to load from
# then i need to find some solution

def main():
    uart = UART(0, baudrate=9600, tx=Pin(TRANCEIVE_PIN), rx=Pin(RECEIVE_PIN))
    
    Load_Msg_Struct_Dicts(structure_json_folder)
    Load_Msg_Type_Valid_Values_Dicts(valid_values_json_folder)
    message_file = open("ais_test_sentences.txt", 'r')
    while True:
        try:
            for message in message_file:
                message.strip()
                message = message.split(',') # extract the payload, could be changed so that the basic validator program will send just the payload
                DBG_Print("inside main")
                DBG_Print('\n')
                msg_bitstring = Decode_Msg_To_Bitstring(message[5], int(message[6].split('*')[0]))
                msg_fields = Seperate_Msg_Fields(msg_bitstring)
                Is_Message_Valid(msg_fields)
                print('\n')
                print("===================MESSAGE VALID!!!!!!================")
                utime.sleep(10000000)
            """
            if uart.any():
                #message = uart.read().decode()
                message = "!AIVDM,1,1,,A,1<s0QwSgpqPqe?r455kp:hJ20000,0*77"
                message = message.split(',') # extract the payload, could be changed so that the basic validator program will send just the payload
                DBG_Print(message)
                DBG_Print('\n')
                DBG_Print("inside main")
                DBG_Print(message[5])
                DBG_Print('\n')
                msg_bitstring = Decode_Msg_To_Bitstring(message[5], int(message[6].split('*')[0]))
                msg_fields = Seperate_Msg_Fields(msg_bitstring)
                Is_Message_Valid(msg_fields)
                utime.sleep(10000)"""
        except Exception as e:
            print("at end error")
            print(e)
            print('\n')
            raise(e)



if __name__ == "__main__":
    main()
