import utime
from Constants import *
from Message_Data_Decode_Module import Decode_Msg_To_Bitstring, Seperate_Msg_Fields
from Load_JSON_Module import MSG_TYPE_PARSE_LISTS_DICTIONARY, MSG_TYPE_VALID_VALUES_LISTS_DICTIONARY, Load_Msg_Struct_Dicts, Load_Msg_Type_Valid_Values_Dicts
from Payload_Validation_Module import Is_Message_Valid
from Debug_Module import DBG_Print
from machine import UART, Pin





# the json is an unordered data structure, if i want to keep the order of what i put in the file to load from
# then i need to find some solution

def main():
    uart = UART(0, baudrate=38400, tx=Pin(TRANCEIVE_PIN), rx=Pin(RECEIVE_PIN), invert=UART.INV_RX)
    uart1 = UART(1, baudrate=38400, tx=Pin(4), rx=Pin(5), invert=UART.INV_TX)
    Load_Msg_Struct_Dicts(structure_json_folder)
    Load_Msg_Type_Valid_Values_Dicts(valid_values_json_folder)
    DBG_Print("\n\n\n")
    DBG_Print(MSG_TYPE_PARSE_LISTS_DICTIONARY)
    DBG_Print("\n\n\n")
    DBG_Print(MSG_TYPE_VALID_VALUES_LISTS_DICTIONARY)
    
    while True:
        try:
            if uart.any():
                message_og = uart.read()
                print(message_og)
                try:
                    message_og = message_og.decode()
                except Exception as e:
                    DBG_Print(e)
                    DBG_Print("decode fail")
                message_og.strip()
                message = message_og.split(',') # extract the payload, could be changed so that the basic validator program will send just the payload
                DBG_Print("inside main")
                DBG_Print('\n')
                DBG_Print(message)
                msg_bitstring = Decode_Msg_To_Bitstring(message[5], int(message[6].split('*')[0]))
                msg_fields = Seperate_Msg_Fields(msg_bitstring)
                Is_Message_Valid(msg_fields)
                #uart1.write(message_og)
                uart1.write((message_og+"\r\n").encode())
                print('\n')
                print("===================MESSAGE VALID!!!!!!================")
        except Exception as e:
            print("at end error")
            print(e)
            print('\n')



# if __name__ == "__main__":
#     while True:
#         led = machine.Pin(25, Pin.OUT)
#         led.value(1)
#         try:
#             main()
#         except Exception as e:
#             raise(e)
#             print("error", e)
#             for i in range(0,3):
#                 led.value(1)
#                 utime.sleep(0.3)
#                 led.value(0)
#                 utime.sleep(1)
#        led.value(0)



while True:
    led = machine.Pin(25, Pin.OUT)
    led.value(1)
    try:
        main()
    except Exception as e:
        for i in range(0,3):
            led.value(1)
            utime.sleep(0.3)
            led.value(0)
            utime.sleep(1)
        print("error", e)
        #raise(e)




