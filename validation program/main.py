import utime
import "constants.py"
import "fragment_module.py"

# === Checksum Validator ===
# calculates the checksum of the packet
# and compares it with the checksum attached to the packet
def Is_Checksum_Valid(packet, fields):
    original_checksum = fields[FILLBIT_N_CHECKSUM_FIELD][CHECKSUM_FIELD]
    checksum = 0
    
    if original_checksum is not VALID_CHECKSUM_LENGTH:
        print("Error: checksum length not valid: ", fields[FILLBIT_N_CHECKSUM_FIELD], ' ', original_checksum)
        return STATUS_INVALID
    
    try: original_checksum = int(original_checksum, 16)
    except: print("error converting checksum to integer for calculation: error in function Is_Checksum_Valid() ", original_checksum)
    
    # goes over each character and calculates the checksum. skips over the first character which is "!" and stops before the character "*" after which is the checksum of the packet
    for ch in packet[1:packet.find('*')]:
        checksum ^= ord(ch)
    
    if checksum is not original_checksum:
        return STATUS_INVALID
    
    return STATUS_FIELD_VALID


def Fillbit_Validation(fields):
    if int(fields[FIELD_FILLBIT_N_CHECKSUM][FIELD_FILLBIT_N_CHECKSUM_FILLBIT]) is not in range(6):
        print("Error, fillbit not in valid range 0-6 ", fields[FIELD_FILLBIT_N_CHECKSUM][FIELD_FILLBIT_N_CHECKSUM_FILLBIT], '\n', fields[FIELD_FILLBIT_N_CHECKSUM])
        return STATUS_INVALID
    return STATUC_FIELD_VALID


# === Main function ===
# the main function for the validation process
# it handles what functions to call in what order, keep it as clean as possible
def Pack_Auth_vali_Check_Basic(packet):

    Purge_Old_Fragments()
    
    # checks that the packet is a string and not empty
    if not isinstance(packet, str) or not packet: ########################## re-review this part later
        return STATUS_INVALID
    
    # compares the start of sentance in the packet with the valid start of sentance in AIS packets
    if not (packet.startswith(VALID_PACKET_START_A) or packet.startswith(VALID_PACKET_START_B)): ######################## Maayan, please remember to make sure that both are valid and not just one
        return STATUS_INVALID
    
    try:
        # splitting the packet into the different message fields
        fields = packet.split(',')
        try:
            fields[FIELD_FILLBIT_N_CHECKSUM] = fields[FIELD_FILLBIT_N_CHECKSUM].split('*') # seperating the fillbit and the checksum
        except:
            print("error while splitting fillbit and checksum", fields)
            return STATUS_INVALID
    except:
        print("Error while splitting packet into fields: error occured in Pack_Auth_vali_Check_Basic() ", fields)
        return STATUS_INVALID
    # make sure the packet has the apropriate number of fields and that the checksum and fillbit were apropriately seperated
    if len(fields) < VALID_PACKET_FIELDS_NUM and len(fields[FIELD_FILLBIT_N_CHECKSUM]) is not FIELD_FILLBIT_N_CHECKSUM_LENGTH:
        return STATUS_INVALID
    
    # checks if the fillbit is in the valid range
    Fillbit_Validation(fields)
    
    # checks the checksum
    Is_Checksum_Valid(packet, fields)
    
    # Pass fields and packet to the fragmentation handler
    # check the status and do the apropriate action accourding to it
    frag_status, data = Message_Fragmentation_Check(fields, packet)
    if frag_status == STATUS_INVALID:
        return STATUS_INVALID
    elif frag_status == STATUS_SINGLE_OK:
        #Validate_Full_Message(data) ############################# FIX THIS!!!!!!!!!!!!!!!!
        return STATUS_SINGLE_OK
    elif frag_status == STATUS_MULTI_OK:
        #Validate_Full_Message(data) ############################# FIX THIS!!!!!!!!!!!!!!!!
        return STATUS_MULTI_OK
    elif frag_status == STATUS_WAITING:
        return STATUS_WAITING

if __name__ == "__main__":
    packet_collection = open('packet_collection.txt', 'r')
    
    for packet in packet_collection:
        print(Pack_Auth_vali_Check_Basic(packet.strip()))
        print(packet)
    packet_collection.close()
    
