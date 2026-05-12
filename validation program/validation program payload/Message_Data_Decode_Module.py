from Constants import *
from Debug_Module import DBG_Print
from Load_JSON_Module import MSG_TYPE_PARSE_LISTS_DICTIONARY, Get_Field_Order, DEFAULT_MSG_TYPE_PART, LENGTH, TYPE, MSG_PART_IS as MSG_PART

FIELD_ORDER_FILE_PRE_MSG_TYPE = "message"
FIELD_ORDER_FILE_POST_MSG_TYPE = "structorder.txt"


# gets the message type and returns it
# gets the message type from a decoded bitstring and returns it as a char
def Get_Msg_Type(payload_bitstring):
    DBG_Print("Inside Get_Msg_Type")
    DBG_Print(str(int(payload_bitstring[0:6], 2)))
    DBG_Print('\n')
    return str(int(payload_bitstring[0:6], 2))


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
    DBG_Print("inside Decode_Msg_To_Bitstring")
    DBG_Print('\n')
    try:
        # turns the payload into a list of 6bit integers, a single 6bit integer for each character in the payload
        for char in payload:
            asc_val = ord(char) - 48
            # makes sure the value is valid and more than 0
            if asc_val < 0:
                DBG_Print("ascii value of char incorrect")
                DBG_Print('\n')
                raise(Exception)
            # makes sure the value is not more than can be made of 6 bits and if not then it shifts the number down by the correct step
            if asc_val > 40:
                asc_val -= 8
            # inserts the 6bit integer into the list
            decoded_raw_data.append(asc_val)
        
        DBG_Print("converted to 6bit values")
        
        # if there is a fillbit then remove it from the last value
        if fillbit > 0:
            DBG_Print("applying fillbit\n")
            decoded_raw_data[-1] = decoded_raw_data[-1] >> fillbit 
        
        DBG_Print("starting to convert to bitstring")
        # creates the bitstring of the payload from the 6bit integer list
        bitstring = ""
        for bin_val in decoded_raw_data: # for every value in the list
            bitstring += FORMAT_6BIT_SPECIFIER.format(bin_val) # converts the number to the binary representation of it and puts it in 6 bit format
        
        DBG_Print("converted to bitstring")
        DBG_Print(bitstring)
        DBG_Print('\n')
        return bitstring
    except Exception as e:
        DBG_Print("Error in Decode_Msg_To_Bitstring")
        DBG_Print(e)
        DBG_Print('\n')
        raise(e)


# === Parse Field ===
# converts the bitstring into it's value based on the type and returns the field name and binary and converted value
def Parse_Field(field_name, bitstring_slice, value_type):
    try:
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
        
        return (field_name, value_type, value)
    except Exception as e:
        DBG_Print("Parsing field failed")
        DBG_Print(field_name)
        DBG_Print(bitstring_slice)
        DBG_Print(value_type)
        DBG_Print(e)
        DBG_Print('\n')
        raise(Exception)


""" temporarily in comments
# === Parse Message ===
# devides the bitstring into fields based on the message type
# returns the fields containing the field's name, the binary of the value and the converted value
def Parse_Message(payload_bitstring, msg_type):
    payload_fields = []
    DBG_Print("Inside Parse_Message")
    DBG_Print('\n')
    try:
        DBG_Print("message type structure dict")
        DBG_Print(MSG_TYPE_PARSE_LISTS_DICTIONARY[msg_type])
        
        if not msg_type in list(MSG_TYPE_PARSE_LISTS_DICTIONARY.keys()):
            DBG_Print("entry keys: ", list(MSG_TYPE_PARSE_LISTS_DICTIONARY.keys()))
            DBG_Print("Error: msg type not recognised")
            DBG_Print(msg_type)
            DBG_Print('\n')
            raise(Exception)
        
        DBG_Print("starting to parse message")
        
        
        try:
            DBG_Print("1")
            # splits the bitstring based on the length of each field for this message type
            curr_pos = 0
            for field_name, field_len, value_type in MSG_TYPE_PARSE_LISTS_DICTIONARY[msg_type]:
                payload_fields.append(Parse_Field(field_name, payload_bitstring[curr_pos:curr_pos+field_len], value_type))
                DBG_Print("2")
                # differentiate message type 24A and message type 24B        
                if field_name == "Part":
                    DBG_Print("Error: message has field part, not supported currently")
                    DBG_Print('\n')
                    raise(Exception) # value of this field must be one of the two
                curr_pos += field_len
            DBG_Print(payload_fields)
            DBG_Print('\n')
        except Exception as e:
            DBG_Print("field parsing failed")
            DBG_Print(payload_fields)
            DBG_Print(e)
            DBG_Print('\n')
            raise(e)
    except Exception as e:
        DBG_Print("message parsing failed")
        DBG_Print(msg_type)
        DBG_Print(MSG_TYPE_PARSE_LISTS_DICTIONARY)
        DBG_Print(e)
        DBG_Print('\n')
        raise(e)
        
    return payload_fields"""


# === Parse Message ===
# devides the bitstring into fields based on the message type
# returns the fields containing the field's name, the binary of the value and the converted value
def Parse_Message(payload_bitstring, msg_type, key_ordered):
    payload_fields = []
    DBG_Print("Inside Parse_Message")
    DBG_Print('\n')
    try:
        DBG_Print("message type structure dict")
        DBG_Print(MSG_TYPE_PARSE_LISTS_DICTIONARY[msg_type])
        
        if not msg_type in list(MSG_TYPE_PARSE_LISTS_DICTIONARY.keys()):
            DBG_Print("entry keys: ", list(MSG_TYPE_PARSE_LISTS_DICTIONARY.keys()))
            DBG_Print("Error: msg type not recognised")
            DBG_Print(msg_type)
            DBG_Print('\n')
            raise(Exception)
        
        DBG_Print("starting to parse message")
        
        
        try:
            DBG_Print("1")
            # splits the bitstring based on the length of each field for this message type
            curr_pos = 0 # start from beginning
            field_len = 0 # placeholder value
            value_type = INTEGER # placeholder value
            field_name = "" # empty field name
            msg_part = DEFAULT_MSG_TYPE_PART # default part
            
            while key_ordered: # goes throught all the field names specified in the key order list
                field_name = key_ordered.pop(0)
                field_len = MSG_TYPE_PARSE_LISTS_DICTIONARY[msg_type][msg_part][LENGTH]
                value_type = MSG_TYPE_PARSE_LISTS_DICTIONARY[msg_type][msg_part][TYPE]
                
                field_tuple = Parse_Field(field_name, payload_bitstring[curr_pos:curr_pos+field_len], value_type)
                
                # differentiate message type 24A and message type 24B        
                if field_name == MSG_PART:
                    if field_tuple[2] == 0:
                        presumed_msg_part = str(msg_type) + "A" 
                    elif field_tuple[2] == 1:
                        presumed_msg_part = str(msg_type) + "B"
                    else:
                        DBG_Print("Part outside of recognizable range")
                        raise(Exception)
                    
                    if presumed_msg_part in MSG_TYPE_PARSE_LISTS_DICTIONARY[msg_type].keys():
                        msg_part = presumed_msg_part
                        new_key_ordered = Get_Field_Order(structure_json_folder, FIELD_ORDER_FILE_PRE_MSG_TYPE + msg_part + FIELD_ORDER_FILE_POST_MSG_TYPE)
                        key_ordered = new_key_ordered[new_key_ordered.index(MSG_PART):]
                    
                
                payload_fields.append(field_tuple)
                DBG_Print("2")
                
                
                curr_pos += field_len
            DBG_Print(payload_fields)
            DBG_Print('\n')
        except Exception as e:
            DBG_Print("field parsing failed")
            DBG_Print(payload_fields)
            DBG_Print(e)
            DBG_Print('\n')
            raise(e)
    except Exception as e:
        DBG_Print("message parsing failed")
        DBG_Print(msg_type)
        DBG_Print(MSG_TYPE_PARSE_LISTS_DICTIONARY)
        DBG_Print(e)
        DBG_Print('\n')
        raise(e)
        
    return payload_fields


#
#
#
def Seperate_Msg_Fields(payload_bitstring):
    DBG_Print("inside Seperate_Msg_Fields")
    DBG_Print('\n')
    try:
        msg_type = Get_Msg_Type(payload_bitstring)
        key_ordered = Get_Field_Order(structure_json_folder, FIELD_ORDER_FILE_PRE_MSG_TYPE + str(msg_type) + FIELD_ORDER_FILE_POST_MSG_TYPE)
        payload_fields = Parse_Message(payload_bitstring, msg_type, key_ordered)
    except Exception as e:
        DBG_Print("Failed to seperate msg fields")
        DBG_Print(e)
        DBG_Print('\n')
        raise(e)
    return payload_fields
