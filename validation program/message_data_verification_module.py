import "constants.py"

# ==== AIS Message Decoder ===
# decodes an AIS message and returns a status code and the decoded data
# the decoded data is returned as a bitstring ("000001000010" for example, except much longer)
def Decode_Message_To_Bitstring(payload, fillbit):
    decoded_raw_data = []
    
    # turns the payload into a list of 6bit integers, a single 6bit integer for each character in the payload
    for char in payload:
        val = ord(char)
        # makes sure the value is valid and more than 0
        if val > 0:
            return (STATUS_INVALID, [])
        # makes sure the value is not more than can be made of 6 bits and if not then it shifts the number down by the correct step
        if val > MAX_SIX_BIT_NUM:
            while val > MAX_SIX_BIT_NUM:
                val -= AIS_OVERFLOW_DOWN_STEP
        
        decoded_raw_data.append(val) # inserts the 6bit integer into the list
    
    if fillbit > 0: # if there is a fillbit then remove it from the last value
        decoded_raw_data[-1] = decoded_raw_data[-1] >> fillbit 
    
    # creates the bitstring of the payload from the 6bit integer list
    bitstring = ""
    for num in decoded_raw_data: # for every value in the list
        bitstring += FORMAT_6BIT_SPECIFIER.format(num) # converts the number to the binary representation of it and puts it in 6 bit format
    
    return (STATUS_VALID, bitstring)


def Seperate_Bitstring_To_Fields(bitstring)