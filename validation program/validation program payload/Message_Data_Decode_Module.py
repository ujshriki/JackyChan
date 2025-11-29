from Constants import *

# gets the message type and returns it
# gets the message type from a decoded bitstring and returns it
def Get_Msg_Type(payload_bitstring):
    return int(payload_bitstring[0:5], 2)

# gets a bitstring and returns the integer value of it
def Bitstr_To_UInt(bitstr):
    return int(bitstr, 2) # returns the integer of the bitstring given

# gets a bitstring and returns the signed integer value of it
# if negetive it returs the negetive number the bitstring represents
# if positive it returns the positive number the bitstring represents
def Bitstr_To_Int(bitstr):
    if bitstr[0] == '1':# if negative
        return -((~int(bitstr, 2) & # converts the bitstring into integer and inverts the value of every bit
                                    ((1 << len(bitstr)) - 1)) + 1) # creates a mask to keep only the first len(bitstr) bits of the result from the line above and adds a 1 to correct the result 
    return int(bitstr, 2) # if positive

    

# ==== AIS Message Decoder ===
# decodes an AIS message and returns the decoded data
# the decoded data is returned as a bitstring ("000001000010" for example, except much longer)
def Decode_Msg_To_Bitstring(payload, fillbit):
    decoded_raw_data = []
    
    # turns the payload into a list of 6bit integers, a single 6bit integer for each character in the payload
    for char in payload:
        asc_val = ord(char)
        # makes sure the value is valid and more than 0
        if asc_val > 0:
            return []
        # makes sure the value is not more than can be made of 6 bits and if not then it shifts the number down by the correct step
        if asc_val > MAX_SIX_BIT_NUM:
            while asc_val > MAX_SIX_BIT_NUM:
                asc_val -= AIS_OVERFLOW_DOWN_STEP
        # inserts the 6bit integer into the list
        decoded_raw_data.append(asc_val)
        
    # if there is a fillbit then remove it from the last value
    if fillbit > 0: 
        decoded_raw_data[-1] = decoded_raw_data[-1] >> fillbit 
    
    # creates the bitstring of the payload from the 6bit integer list
    bitstring = ""
    for bin_val in decoded_raw_data: # for every value in the list
        bitstring += FORMAT_6BIT_SPECIFIER.format(bin_val) # converts the number to the binary representation of it and puts it in 6 bit format
    
    return bitstring


# === Parse Field ===
# converts the bitstring into it's value based on the type and returns the field name and binary and converted value
def Parse_Field(field_name, bitstring_slice, value_type):
    # if field is unsigned integer
    if value_type == U_INTEGER:
        value = Bitstr_To_UInt(bitstring_slice) # turn into unsigned integer
    # if field is signed integer
    elif value_type == INTEGER:
        value = Bitstr_To_Int(bitstring_slice) # turn into signed integer
    # if field is boolean and is length of 1 bit
    elif value_type == BOOLEAN and len(bitstring_slice) == 1:
        value = Bitstr_To_UInt(bitstring_slice) # turn into unsigned integer representing a boolean
    # if field is string interpret the values into string
    elif value_type == ASC_6BIT:
        value = ""
        curr_pos = 0
        
        # goes over every 6 bits that together represent a single character of the string
        for char_pos in range(0, len(bitstring_slice), 6):
            char_val = int(bitstring_slice[char_pos:char_pos+6], 2) # converts them to their ascii value
            
            # corrects the ascii value to 8 bits
            if char_val < 40:
                value.append(chr(char_val + 48))
            else:
                value.append(chr(char_val + 56))
    else:
        raise(Exception)
    
    return (field_name, bitstring_slice, value)


# === Parse Message ===
# devides the bitstring into fields based on the message type
# returns the fields containing the field's name, the binary of the value and the converted value
def Parse_Message(payload_bitstring, msg_type):
    payload_fields = []
    
    try:
        # splits the bitstring based on the length of each field for this message type
        curr_pos = 0
        
        for field_name, field_len, value_type in MSG_TYPE_PARSE_LISTS_DICTIONARY[msg_type]:
            payload_fields.append(Parse_Field(field_name, payload_bitstring[curr_pos:curr_pos+field_len-1], value_type))
            
            # differentiate message type 24A and message type 24B        
            if msg_type == STATIC_DATA_REPORT_KEY and field_name == STATIC_DATA_REPORT_A_B_FIELD:
                if payload_fields[-1][-1] == STATIC_DATA_REPORT_PART_A:
                    msg_type = STATIC_DATA_REPORT_KEY
                elif payload_fields[-1][-1] == STATIC_DATA_REPORT_PART_A:
                    msg_type = STATIC_DATA_REPORT_KEY_B
                else:
                    raise(Exception) # value of this field must be one of the two
            
            curr_pos += curr_field_len
    except:
        raise(Exception)
        
    return payload_fields


def Seperate_Msg_Fields(payload_bitstring):
    payload_fields = Parse_Message(payload_bitstring, Get_Msg_Type(payload_bitstring))
    
    return payload_fields




