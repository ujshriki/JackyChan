import json
import os
from Debug_Module import DBG_Print

MSG_TYPE_PARSE_LISTS_DICTIONARY = {}
MSG_TYPE_VALID_VALUES_LISTS_DICTIONARY = {}

FIELD_ORDER_FIELD = "Field Order File Name"

DEFAULT_MSG_TYPE_PART = "all parts"

MESSAGE_TYPE = "Message Type"
IS_MSG_DICT_A_PART = "Is a Part?"
MSG_PART_IS = "Part"
MSG_TYPE_OF_STRUCT = "Structure Of"

RANGES = "Ranges"
CHECK = "Check"
VALUES = "Values"
TYPE = "Type"
LENGTH = "Length"
MIN = "min"
MAX = "max"


#
#
#
def MSG_Json_Dict_Load(file_path):
    try:
        json_file = json.load(open(file_path))
        DBG_Print(json_file)
    except Exception as e:
        DBG_Print("failed to load json")
        DBG_Print(e)
        DBG_Print('\n')
        raise(Exception)
    return json_file


#
#
#
def Get_Field_Order(folder_path, file_name):
    try:
        field_order_file = open(folder_path+file_name, 'r')
        field_order_list = []
        
        for field_name in field_order_file:
            field_order_list.append(field_name.strip())# can replace with <rstrip()> for only removing from right of line for better performance
        
        return field_order_list
    except:
        DBG_Print("Error field order file not found or error loading said file")
        DBG_Print('\n')
        raise(Exception)


#
#
#
def Field_Dict_To_Tuple(dict_name, field_dict):
    try:
        the_tuple = (dict_name, field_dict[LENGTH], field_dict[TYPE])
    except:
        DBG_Print("ERROR in the field dict to tuple function, -- probably one of the keys is spelled wrong in the dictionary")
        DBG_Print('\n')
        raise(Exception)
    return the_tuple


#
#
#
def Create_Msg_Type_Struct_List(loaded_json_file, json_field_keys):
    struct_list = []
    try:
        DBG_Print(loaded_json_file)
        DBG_Print('\n')
        
        if(json_field_keys[0] == MESSAGE_TYPE):
            struct_list.append((MESSAGE_TYPE, loaded_json_file[MESSAGE_TYPE][LENGTH], loaded_json_file[MESSAGE_TYPE][TYPE]))
        else:
            DBG_Print("error: message type doesn't exist?")
            DBG_Print(json_field_keys)
            DBG_Print('\n')
            raise(Exception)
        
        json_field_keys.pop(0)
        for field_key in json_field_keys:
            struct_list.append(Field_Dict_To_Tuple(field_key, loaded_json_file[field_key]))
    except Exception as e:
        DBG_Print("Error in function Create_Msg_Type_Struct_List: field appending gone wrong?")
        DBG_Print(e)
        DBG_Print('\n')
        raise(Exception)
    MSG_TYPE_PARSE_LISTS_DICTIONARY[loaded_json_file[MESSAGE_TYPE][MSG_TYPE_OF_STRUCT]] = struct_list


#
#
#
def Load_Msg_Struct_Dicts(folder_path):
    json_file_names = []
    file_names = os.listdir(folder_path)
    
    for file_name in file_names:
        if file_name.endswith(".json"):
            json_file_names.append(file_name)
    
    for file_name in json_file_names:
        try:
            file_path = folder_path + file_name
            loaded_json_file = MSG_Json_Dict_Load(file_path)
            Create_Msg_Type_Struct_List(loaded_json_file, Get_Field_Order(folder_path, loaded_json_file[FIELD_ORDER_FIELD]))
        except Exception as e:
            DBG_Print("failed to load json file")
            DBG_Print(file_name)
            DBG_Print(loaded_json_file[FIELD_ORDER_FIELD])
            DBG_Print(e)
            DBG_Print('\n')



"""temporary_storage_dictionary_for_visualization_purposes_please_remove = {   1: {"all parts":{"Message Type":  {"Check":True,
                                                                                                                  "Message Type":1,
                                                                                                                  "Is a Part?": False,
                                                                                                                  "Part": ""},
                                                                                             "Repeat Indicator": {"Check" :True,
                                                                                                                  "Type"  :u_int,
                                                                                                                  "Ranges":[{"min": 0, "max": 3}],
                                                                                                                  "Values":[] },
                                                                                             "MMSI":             {"Check" :True,
                                                                                                                  "Type"  :u_int,
                                                                                                                  "Ranges":[{"min": 0, "max": 3},
                                                                                                                            {"min": 0, "max": 3},
                                                                                                                            {"min": 0, "max": 3},
                                                                                                                            {"min": 0, "max": 3},
                                                                                                                            {"min": 0, "max": 3} ],
                                                                                                                  "Values":[] },
                                                                                             "generic field":    {"Check" :None,
                                                                                                                  "Type"  :None,
                                                                                                                  "Ranges":[],
                                                                                                                  "Values":[] } } },
                                                                            2: {"all parts":{} },
                                                                            24:{"all parts":{},
                                                                                "24A":      {},
                                                                                "24B":      {} } }"""



#
#
#
def Create_Msg_Type_Valid_Values_List(loaded_json_file, json_field_keys):
    valid_values_dict = {}
    dict_key = 0
    dict_part_key = DEFAULT_MSG_TYPE_PART
    
    try:        
        # if the json doesn't start as expected
        if json_field_keys[0] != MESSAGE_TYPE:
            DBG_Print("no message type")
            DBG_Print('\n')
            raise(Exception)
        
        dict_key = loaded_json_file[MESSAGE_TYPE][MESSAGE_TYPE]
        
        if isinstance(dict_key, int):
            dict_key = str(dict_key)
        
        # if this json describes the valid values for a specific part for a message type
        if loaded_json_file[MESSAGE_TYPE][IS_MSG_DICT_A_PART]:
            dict_part_key = str(dict_key) + loaded_json_file[MESSAGE_TYPE][MSG_PART_IS] # assemble the key for that message type+part combination
        else:
            dict_part_key = DEFAULT_MSG_TYPE_PART
        
        
        # if the message type has an entry in the dictionary
        if dict_key in list(MSG_TYPE_VALID_VALUES_LISTS_DICTIONARY.keys()):
            # if there *is* an entry for this message type+part combination
            if dict_part_key in list(MSG_TYPE_VALID_VALUES_LISTS_DICTIONARY[dict_key].keys()):
                # don't add this to the dictionary
                raise(Exception) # exit the try:except statement
        else:
            MSG_TYPE_VALID_VALUES_LISTS_DICTIONARY[dict_key] = {}
        
        # ensure that the field <CHECK> is a boolean true\false in <Message Type>
        if not (loaded_json_file[MESSAGE_TYPE][CHECK] == True or loaded_json_file[MESSAGE_TYPE][CHECK] == False):
            raise(Exception)
        
        
        # create the entry for the Message Type key in the new type+part combination entry
        valid_values_dict[MESSAGE_TYPE] = {CHECK: loaded_json_file[MESSAGE_TYPE][CHECK],
                                           MESSAGE_TYPE: loaded_json_file[MESSAGE_TYPE][MESSAGE_TYPE],
                                           IS_MSG_DICT_A_PART: loaded_json_file[MESSAGE_TYPE][IS_MSG_DICT_A_PART],
                                           MSG_PART_IS: loaded_json_file[MESSAGE_TYPE][MSG_PART_IS]}
        json_field_keys.pop(0)
        # creating the dictionary object to be inserted into the global dictionary that describes the valid values for the fields of the message types
        for field_key in json_field_keys:
            # ensure that the field <CHECK> is a boolean true\false
            if not (loaded_json_file[field_key][CHECK] == True or loaded_json_file[field_key][CHECK] == False):
                raise(Exception)
            
            valid_values_dict[field_key] = {CHECK: loaded_json_file[field_key][CHECK],
                                            TYPE: loaded_json_file[field_key][TYPE],
                                            RANGES: loaded_json_file[field_key][RANGES],
                                            VALUES: loaded_json_file[field_key][VALUES]}
        
        DBG_Print("loaded json new dictonary entry")
        DBG_Print(valid_values_dict)
        DBG_Print('\n')
        # add the entry for the message type+part combination to the dictionary
        MSG_TYPE_VALID_VALUES_LISTS_DICTIONARY[dict_key][dict_part_key] = valid_values_dict
    except:
        DBG_Print("Error: valid values dict creation failed?")
        DBG_Print('\n')
        raise(Exception)


#
#
#
def Load_Msg_Type_Valid_Values_Dicts(folder_path):
    json_file_names = []
    file_names = os.listdir(folder_path)
    
    #gathers names of json files in folder
    for file_name in file_names:
        if file_name.endswith(".json"):
            json_file_names.append(file_name)
    
    #tries to load every found json file in folder
    for file_name in json_file_names:
        try:
            file_path = folder_path + file_name
            loaded_json_file = MSG_Json_Dict_Load(file_path)
            Create_Msg_Type_Valid_Values_List(loaded_json_file, Get_Field_Order(folder_path, loaded_json_file[FIELD_ORDER_FIELD]))
        except Exception as e:
            DBG_Print("failed to load json file ")
            DBG_Print(file_name)
            DBG_Print(loaded_json_file[FIELD_ORDER_FIELD])
            DBG_Print(e)
            DBG_Print('\n')
