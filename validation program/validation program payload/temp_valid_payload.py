from Constants import *

POS_REP_CLASS_A_VALID_RANGE  =  const([
    ("Message Type", 1, 3),
    ("Repeat Indicator", 0, 15),
    ("MMSI", 30, ),
    ("Navigation Status", 4, ),
    ("Rate of Turn", 8, ),
    ("Speed Over Ground", 10, ),
    ("Position Accuracy", 1, ),
    ("Longitude", 28, ),
    ("Latitude", 27, ),
    ("Course Over Ground", 12, ),
    ("True Heading" , 9, ),
    ("Time Stamp", 6, ),
    ("Maneuver Indicator", 2, ),
    ("Spare", 3, ), # value should always be 0
    ("RAIM flag", 1, ),
    ("Radio status", 19, )])



STATIC_AND_VOYAGE_RELATED_DATA_VALID_RANGE = const([
    ("Message Type", 6,),
    ("Repeat Indicator", 2,),
    ("MMSI", 30,),
    ("AIS Version", 2,),
    ("IMO Number", 30,),
    ("Call Sign", 42,),
    ("Vessel Name", 120,),
    ("Ship Type", 8,),
    ("Dimension to Bow", 9,),
    ("Dimension to Stern", 9,),
    ("Dimension to Port", 6,),
    ("Dimension to Starboard", 6,),
    ("Position Fix Type", 4,),
    ("ETA month (UTC)", 4,),
    ("ETA day (UTC)", 5,),
    ("ETA hour (UTC)", 5,),
    ("ETA minute (UTC)", 6,),
    ("Draught", 8,),
    ("Destination", 120,),
    ("DTE", 1,),
    ("Spare", 1,)])



STANDART_SAR_AIRCRAFT_POS_REP_VALID_RANGE = const([
    ("Message Type", 6,),
    ("Repeat Indicator", 2,),
    ("MMSI", 30,),
    ("Altitude", 12,),
    ("SOG", 10,),
    ("Position Accuracy", 1,),
    ("Longitude", 28,),
    ("Latitude", 27,),
    ("Course Over Ground", 12,),
    ("Time Stamp", 6,),
    ("Regional reserved", 8,),
    ("DTE", 1,),
    ("Spare", 3,),
    ("Assigned", 1,),
    ("RAIM flag", 1,),
    ("Radio status", 20,)])



STANDART_CLASS_B_POS_REP_VALID_RANGE = const([
    ("Message Type", 6,),
    ("Repeat Indicator", 2,),
    ("MMSI", 30,),
    ("Regional Reserved", 8,),
    ("Speed Over Ground", 10,),
    ("Position Accuracy", 1,),
    ("Longitude", 28,),
    ("Latitude", 27,),
    ("Course Over Ground", 12,),
    ("True Heading", 9,),
    ("Time Stamp", 6,),
    ("Regional reserved", 2,),
    ("CS Unit", 1,),
    ("Display flag", 1,),
    ("DSC Flag", 1,),
    ("Band flag", 1,),
    ("Message 22 flag", 1,),
    ("Assigned", 1,),
    ("RAIM flag", 1,),
    ("Radio status", 20,)])



EXTENDED_CLASS_B_POS_REP_VALID_RANGE = const([
    ("Message Type", 6,),
    ("Repeat Indicator", 2,),
    ("MMSI", 30,),
    ("Regional Reserved", 8,),
    ("Speed Over Ground", 10,),
    ("Position Accuracy", 1,),
    ("Longitude", 28,),
    ("Latitude", 27,),
    ("Course Over Ground", 12,),
    ("True Heading", 9,),
    ("Time Stamp", 6,),
    ("Regional reserved", 4,),
    ("Name", 120,),
    ("Type of ship and cargo", 8,),
    ("Dimension to Bow", 9,),
    ("Dimension to Stern", 9,),
    ("Dimension to Port", 6,),
    ("Dimension to Starboard", 6),
    ("Position Fix Type", 4,),
    ("RAIM flag", 1,),
    ("DTE", 1,),
    ("Assigned mode flag", 1,),
    ("Spare", 4,)])



STATIC_DATA_REPORT_VALID_RANGE = const([
    ("Message Type", 6,),
    ("Repeat Indicator", 2,),
    ("MMSI", 30,),
    ("Part Number", 2,),
    ("Vessel Name", 120,),
    ("Spare", 8,),
    ("Ship Type", 8,),
    ("Vendor ID", 18,),
    ("Unit Model Code", 4,),
    ("Serial Number", 20,),
    ("Call Sign", 42,),
    ("Dimension to Bow", 9,),
    ("Dimension to Stern", 9,)
    ("Dimension to Port", 6,),
    ("Dimension to Starboard", 6,),
    ("Mothership MMSI", 30,),
    ("Spare", 6,)])



VALID_PAYLOAD_RANGE_DICT = const({
    1: POS_REP_CLASS_A_VALID_RANGE,
    2: POS_REP_CLASS_A_VALID_RANGE,
    3: POS_REP_CLASS_A_VALID_RANGE,
    5: STATIC_AND_VOYAGE_RELATED_DATA_VALID_RANGE,
    9: STANDART_SAR_AIRCRAFT_POS_REP_VALID_RANGE,
    18:STANDART_CLASS_B_POS_REP_VALID_RANGE,
    19:EXTENDED_CLASS_B_POS_REP_VALID_RANGE,
    24:STATIC_DATA_REPORT_VALID_RANGE
    })




def Validate_Parsed_Message(message, msg_type):
    try:
        for msg_field_name, _ignored, msg_field_value in msg and list_field_name, field_min_valid, field_max_valid in VALID_PAYLOAD_RANGE_DICT[msg_type]:
            
            if field_min_valid <= msg_field_value <= field_max_valid:
                
            else:
                raise(Exception)
            
    except:
        raise(Exception)
    
    

