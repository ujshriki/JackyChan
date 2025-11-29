import utime
from Constants import *
from Message_Data_Decode_Module import Decode_Msg_To_Bitstring, Seperate_Msg_Fields
from machine import UART, Pin




def main():
    uart = UART(0, baudrate=9600, tx=Pin(TRANCEIVE_PIN), rx=Pin(RECEIVE_PIN))
    
    while True:
        try:
            if uart.any():
                message = uart.read().decode()
                msg_bitstring = Decode_Msg_To_Bitstring(message)
                msg_fields = Seperate_Msg_Fields(msg_bitstring)
                
                print(packet)
        except Exception as e:
            print("at end error", e)



if __name__ == "__main__":
    main()
