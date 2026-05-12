from Constants import *
from Load_JSON_Module import MSG_TYPE_VALID_VALUES_LISTS_DICTIONARY as VALID_DICT, CHECK, MIN, MAX, DEFAULT_MSG_TYPE_PART as DEFAULT_PART, RANGES, VALUES, TYPE, MESSAGE_TYPE, MSG_PART_IS
from Debug_Module import DBG_Print

""" segmented_message_example_for_visualization = [ (field_name, value_type, value),
                                                    (field_name, value_type, value),
                                                    (field_name, value_type, value),
                                                    (field_name, value_type, value)]"""


# === Is Value Valid === -made by Maayan Ofir
# checks if the value of the given field is in the list of valid ranges or values
# assumes that the variable <field_value> is a numerical value(int, u_int... so on)
def Is_Value_Valid_Number(field_value, valid_ranges=[], valid_values=[]):
    DBG_Print("inside Is_Value_Valid_Number")
    DBG_Print('\n')
    try:
        #check if the value of the field is in the valid values
        if field_value in valid_values:
            return True
        
        # for every range of valid values in valid ranges
        for min_max_pair in valid_ranges:
            DBG_Print("min_max_pair")
            DBG_Print(min_max_pair)
            DBG_Print((min_max_pair[MIN], field_value, min_max_pair[MAX]))
            # check if field_value is within the bounds of that range
            if min_max_pair[MIN] <= field_value <= min_max_pair[MAX]:
                return True
    except Exception as e:
        DBG_Print("validation of number did not pass")
        DBG_Print([field_value])
        DBG_Print(e)
        DBG_Print('\n')
        raise(e) 
    return False


#
#
#
def Is_Valid_Value_Text(field_value, valid_ranges=[], valid_values=[]):
    try:
        return True 
    except:
        pass
    return False


#
#
#
def Is_Valid_Value_Bool(field_value, valid_ranges=[], valid_values=[]):
    try:
        return True 
    except:
        pass
    return False


VALIDATE_DATA_TYPE = {  "u_int": Is_Value_Valid_Number,
                        "int"  : Is_Value_Valid_Number,
                        "bool" : Is_Valid_Value_Bool,
                        "str":Is_Valid_Value_Text  }


# === Is Message Valid ===
# the function that handles the validation of the message
# receives a decode message that was split into a list, throws an exception if the message is not valid
def Is_Message_Valid(segmented_msg):
    DBG_Print("inside Is_Message_Valid")
    try:
        DBG_Print(segmented_msg)
        # if message doesn't have the field <"Message Type"> then ignore this message
        if segmented_msg[0][0] != MESSAGE_TYPE:
            DBG_Print("message type not first field in msg")
            raise(Exception)
        
        # save the message type for later use
        msg_type = str(segmented_msg[0][2])
        DBG_Print("msg type")
        DBG_Print(msg_type)
        
        # goes over every field in the message
        msg_part_index = -1
        i = 0
        while (i < len(segmented_msg)):
            # if the field is named <"Part">
            if segmented_msg[i][0] == "Part":
                msg_part_index = i
                DBG_Print("message is part")
                DBG_Print('\n')
                # if this message type doesn't have any parts then ignore this message
                if len(list(VALID_DICT[msg_type].keys())) < 2:
                    DBG_Print("part exists without any parts")
                    DBG_Print(list(VALID_DICT[msg_type].keys()))
                    DBG_Print('\n')
                    raise(Exception)
                i = len(segmented_msg)
            i += 1
        
        
        # incorporate message Parts into the validation.
        #add a check if there is parts for this field and if this message has the field with the name <"Part">
        DBG_Print("post part check")
        segmented_msg.pop(0)
        try:
            msg_part = DEFAULT_PART
            DBG_Print(segmented_msg)
            for field_name, value_type, field_value in segmented_msg:
                if field_name == MSG_PART_IS:
                    if field_value == 0:
                        msg_part = str(msg_type) + "A" 
                    elif field_value == 1:
                        msg_part = str(msg_type) + "B"
                    else:
                        DBG_Print("Part outside of recognizable range")
                        raise(Exception)
                
                DBG_Print("going through for loop")
                DBG_Print(field_name)
                DBG_Print(value_type)
                DBG_Print(field_value)
                if VALID_DICT[msg_type][msg_part][field_name][CHECK]:
                    if not VALIDATE_DATA_TYPE[value_type](field_value, VALID_DICT[msg_type][msg_part][field_name][RANGES], VALID_DICT[msg_type][msg_part][field_name][VALUES]):
                        DBG_Print("field not valid")
                        DBG_Print(field_name)
                        DBG_Print(field_value)
                        DBG_Print(value_type)
                        DBG_Print(VALID_DICT[msg_type][msg_part][field_name][RANGES])
                        DBG_Print(VALID_DICT[msg_type][msg_part][field_name][VALUES])
                        DBG_Print('\n')
                        raise(Exception)
            DBG_Print("\n out of for loop")
        except Exception as e:
            DBG_Print('\n')
            DBG_Print(VALID_DICT)
            DBG_Print('\n')
            DBG_Print("error in the for loop in Is_Message_Valid")
            DBG_Print(e)
            DBG_Print('\n')
            raise(e)
        
        #add a check of what the datatype of the field is and call the relevant function for this datatype
        # some boolean represent something other than true or false, some represent a 0 or 1, a "special" case or the normal case for example
        
    except Exception as e:
        DBG_Print("failed to validate msg")
        DBG_Print(e)
        DBG_Print('\n')
        raise(e)
