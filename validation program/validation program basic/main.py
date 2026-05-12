import utime
from Constants import *
from machine import UART, Pin
from Lead_Removal_Module import Extract_Sentence

# === Checksum Validator ===
# calculates the checksum of the packet
# and compares it with the checksum attached to the packet
def Is_Checksum_Valid(packet, fields):
    original_checksum = fields[FIELD_FILLBIT_N_CHECKSUM][FIELD_CHECKSUM]
    checksum = 0
    
    if not len(original_checksum) is VALID_CHECKSUM_LENGTH:
        print("Error: checksum length not valid: ", fields[FIELD_FILLBIT_N_CHECKSUM], ' ', original_checksum)
        return STATUS_INVALID
    
    try: original_checksum = int(original_checksum, 16) # try to convert the checksum into base 10 integer value from hex value
    except: print("error converting checksum to integer for calculation: error in function Is_Checksum_Valid() ", original_checksum)
    
    # goes over each character and calculates the checksum. skips over the first character which is "!" and stops before the character "*" after which is the checksum of the packet
    for ch in packet[1:packet.find('*')]:
        checksum = checksum ^ ord(ch)
    
    if not (checksum == original_checksum):
        print("invalid checksum")
        return STATUS_INVALID
    
    return STATUS_FIELD_VALID


# validates the fillbit, makes sure the fillbit is a valid value
def Fillbit_Validation(fields):
    if not int(fields[FIELD_FILLBIT_N_CHECKSUM][FIELD_FILLBIT]) in range(6):
        print("Error, fillbit not in valid range 0-6 ", fields[FIELD_FILLBIT_N_CHECKSUM][FIELD_FILLBIT], '\n', fields[FIELD_FILLBIT_N_CHECKSUM])
        return STATUS_INVALID
    return STATUS_FIELD_VALID


# === Main function ===
# the main function for the validation process
# it handles what functions to call in what order, keep it as clean as possible
def Pack_Auth_vali_Check_Basic(packet):
    
    # checks that the packet is a string and not empty
    if not isinstance(packet, str) or not packet: ########################## re-review this part later
        return STATUS_INVALID
    
    # compares the start of sentance in the packet with the valid start of sentance in AIS packets
    if not (packet.startswith("!") or packet.startswith("$")): ######################## Maayan, please remember to make sure that both are valid and not just one
        return STATUS_INVALID
    
    try:
        # splitting the packet into the different message fields
        fields = packet.split(',')
        try:
            fields[FIELD_FILLBIT_N_CHECKSUM] = fields[FIELD_FILLBIT_N_CHECKSUM].split('*') # seperating the fillbit and the checksum
        except Exception as e:
            print(e)
            print("error while splitting fillbit and checksum", fields)
            return STATUS_INVALID
    except:
        print("Error while splitting packet into fields: error occured in Pack_Auth_vali_Check_Basic() ", fields)
        return STATUS_INVALID
    # make sure the packet has the apropriate number of fields and that the checksum and fillbit were apropriately seperated
    if len(fields) < VALID_PACKET_FIELDS_NUM and len(fields[FIELD_FILLBIT_N_CHECKSUM]) is not FIELD_FILLBIT_N_CHECKSUM_LENGTH:
        return STATUS_INVALID
    
    # checks if the fillbit is in the valid range
    status = Fillbit_Validation(fields)
    
    if status == STATUS_INVALID:
        return STATUS_INVALID
    
    # checks the checksum
    status = Is_Checksum_Valid(packet, fields)
    
    if status == STATUS_INVALID:
        return STATUS_INVALID
    
    # checks if it is a fragment
    try:
        if int(fields[2]) > 1 or int(fields[1]) > 1:
            print("fragment")
            return STATUS_INVALID      # Temporary
    except Exception as e:
        print("by fragment exception ", e)
        return STATUS_INVALID                     # Temporary
    except:
        print("unknown error after fragment check")
        return STATUS_INVALID # Temporary
    
    return STATUS_SINGLE_OK


def clean_packet(packet):
    decodeable_packet =""
    
    index = 0
    while index < len(packet):
        try:
            return packet[index:-1].decode()
        except:
            index += 1
    return ""


def main():
    uart0 = UART(0, baudrate=38400, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1), invert=UART.INV_RX)
    uart1 = UART(1, baudrate=38400, bits=8, parity=None, stop=1, tx=Pin(4), rx=Pin(5), invert=UART.INV_TX)
    try:
        while(True):
            try:
                if uart0.any():
                    packet = uart0.read()
                    print(packet)
                    try:
                        packet = packet.decode()
                        try:
                            packet = packet.strip()
                        except: print("failed to strip packet")
                        print(packet)
                    except Exception as e:
                        print("failed to decode packet", e)
                        packet = Extract_Sentence(packet).strip()
                        print(packet)
                    status = Pack_Auth_vali_Check_Basic(packet)
                    print(status)
                    uart1.write(packet.encode())
                    uart1.write("\r\n".encode())
                    #if status is STATUS_SINGLE_OK:
                        #uart1.write(packet.encode())
            except Exception as e:
                print("error?", e)
                raise(e)
    except Exception as e:
        print("at end error", e)
        raise(e)
                    


while True:
    led = machine.Pin(25, Pin.OUT)
    led.value(1)
    try:
        main()
    except Exception as e:
        raise(e)
        print("error", e)
        for i in range(0,3):
            led.value(1)
            utime.sleep(0.3)
            led.value(0)
            utime.sleep(1)
    machine.reset()


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

"""if __name__ == "__main__":
    try:
        packet_collection = open('packet_collection.txt', 'r')
    
        for packet in packet_collection:
            print(Pack_Auth_vali_Check_Basic(packet.strip()))
            print(packet)
        packet_collection.close()
    except custom_excepts.Program_Filter_Exceptions as e:
        print("unexpected and unplanned for error occured: ", e)"""
    
