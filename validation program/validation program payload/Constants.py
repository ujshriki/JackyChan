from micropython import const

###
### === Constants ===
###

RECEIVE_PIN = const(1)
TRANCEIVE_PIN = const(0)

# === Decoding and Message Data Verification Constants ===
ASCII_CHAR_BASE_VALUE = const(48)
AIS_TABLE_LIMIT = const(39)
MAX_SIX_BIT_NUM = const(63)
AIS_OVERFLOW_DOWN_STEP = const(8)
FORMAT_6BIT_SPECIFIER = const('{:06b}') # the code that specifies how to format the conversion from the 6bit integer to the bitstring

#
INTEGER = const("int")
U_INTEGER = const("u_int")
BOOLEAN = const ("bool")
ASC_6BIT = const("ascii_6bit")


# === Position_Report_Class_A ===
# types 1-3
POS_REP_CLASS_A_PARSE_LIST  =  const([
    ("Message Type", 6, U_INTEGER),
    ("Repeat Indicator", 2, U_INTEGER),
    ("MMSI", 30, U_INTEGER),
    ("Navigation Status", 4, U_INTEGER),
    ("Rate of Turn", 8, INTEGER),
    ("Speed Over Ground", 10, U_INTEGER),
    ("Position Accuracy", 1, BOOLEAN),
    ("Longitude", 28, INTEGER),
    ("Latitude", 27, INTEGER),
    ("Course Over Ground", 12, U_INTEGER),
    ("True Heading" , 9, U_INTEGER),
    ("Time Stamp", 6, U_INTEGER),
    ("Maneuver Indicator", 2, U_INTEGER),
    ("Spare", 3, U_INTEGER), # value should always be 0
    ("RAIM flag", 1, BOOLEAN),
    ("Radio status", 19, U_INTEGER)])


# === Static and Voyage Related Data ===
# type 5
STATIC_AND_VOYAGE_RELATED_DATA_PARSE_LIST = const([
    ("Message Type", 6, U_INTEGER),
    ("Repeat Indicator", 2, U_INTEGER),
    ("MMSI", 30, U_INTEGER),
    ("AIS Version", 2, U_INTEGER),
    ("IMO Number", 30, U_INTEGER),
    ("Call Sign", 42, STR_6BIT),
    ("Vessel Name", 120, ASC_6BIT),
    ("Ship Type", 8, U_INTEGER),
    ("Dimension to Bow", 9, U_INTEGER),
    ("Dimension to Stern", 9, U_INTEGER),
    ("Dimension to Port", 6, U_INTEGER),
    ("Dimension to Starboard", 6, U_INTEGER),
    ("Position Fix Type", 4, U_INTEGER),
    ("ETA month (UTC)", 4, U_INTEGER),
    ("ETA day (UTC)", 5, U_INTEGER),
    ("ETA hour (UTC)", 5, U_INTEGER),
    ("ETA minute (UTC)", 6, U_INTEGER),
    ("Draught", 8, U_INTEGER),
    ("Destination", 120, ASC_6BIT),
    ("DTE", 1, BOOLEAN),
    ("Spare", 1, U_INTEGER)])


# === Standart Search and Rescue Aircraft Position Report ===
# type 9
STANDART_SAR_AIRCRAFT_POS_REP_PARSE_LIST = const([
    ("Message Type", 6, U_INTEGER),
    ("Repeat Indicator", 2, U_INTEGER),
    ("MMSI", 30, U_INTEGER),
    ("Altitude", 12, U_INTEGER),
    ("SOG", 10, U_INTEGER),
    ("Position Accuracy", 1, BOOLEAN),
    ("Longitude", 28, INTEGER),
    ("Latitude", 27, INTEGER),
    ("Course Over Ground", 12, U_INTEGER),
    ("Time Stamp", 6, U_INTEGER),
    ("Regional reserved", 8, U_INTEGER),
    ("DTE", 1, BOOLEAN),
    ("Spare", 3, U_INTEGER),
    ("Assigned", 1, BOOLEAN),
    ("RAIM flag", 1, BOOLEAN),
    ("Radio status", 20, U_INTEGER)])


# === Standart Class B Position Report ===
# type 18
STANDART_CLASS_B_POS_REP_PARSE_LIST = const([
    ("Message Type", 6, U_INTEGER),
    ("Repeat Indicator", 2, U_INTEGER),
    ("MMSI", 30, U_INTEGER),
    ("Regional Reserved", 8, U_INTEGER),
    ("Speed Over Ground", 10, U_INTEGER),
    ("Position Accuracy", 1, BOOLEAN),
    ("Longitude", 28, INTEGER),
    ("Latitude", 27, INTEGER),
    ("Course Over Ground", 12, U_INTEGER),
    ("True Heading", 9, U_INTEGER),
    ("Time Stamp", 6, U_INTEGER),
    ("Regional reserved", 2, U_INTEGER),
    ("CS Unit", 1, BOOLEAN),
    ("Display flag", 1, BOOLEAN),
    ("DSC Flag", 1, BOOLEAN),
    ("Band flag", 1, BOOLEAN),
    ("Message 22 flag", 1, BOOLEAN),
    ("Assigned", 1, BOOLEAN),
    ("RAIM flag", 1, BOOLEAN),
    ("Radio status", 20, U_INTEGER)])


# === Extended Class B Position Report ===
# type 19
EXTENDED_CLASS_B_POS_REP_PARSE_LIST = const([
    ("Message Type", 6, U_INTEGER),
    ("Repeat Indicator", 2, U_INTEGER),
    ("MMSI", 30, U_INTEGER),
    ("Regional Reserved", 8, U_INTEGER),
    ("Speed Over Ground", 10, U_INTEGER),
    ("Position Accuracy", 1, BOOLEAN),
    ("Longitude", 28, INTEGER),
    ("Latitude", 27, INTEGER),
    ("Course Over Ground", 12, U_INTEGER),
    ("True Heading", 9, U_INTEGER),
    ("Time Stamp", 6, U_INTEGER),
    ("Regional reserved", 4, U_INTEGER),
    ("Name", 120, ASC_6BIT),
    ("Type of ship and cargo", 8, U_INTEGER),
    ("Dimension to Bow", 9, U_INTEGER),
    ("Dimension to Stern", 9, U_INTEGER),
    ("Dimension to Port", 6, U_INTEGER),
    ("Dimension to Starboard", 6, U_INTEGER),
    ("Position Fix Type", 4, U_INTEGER),
    ("RAIM flag", 1, BOOLEAN),
    ("DTE", 1, BOOLEAN),
    ("Assigned mode flag", 1, BOOLEAN),
    ("Spare", 4, U_INTEGER)])


# === Static Data Report ===
# type 24
STATIC_DATA_REPORT_A_B_FIELD = const("Part Number")
STATIC_DATA_REPORT_PART_A = const(0)
STATIC_DATA_REPORT_PART_B = const(1)

STATIC_DATA_REPORT_KEY = const(24)
STATIC_DATA_REPORT_PARSE_LIST = const([
    ("Message Type", 6, U_INTEGER),
    ("Repeat Indicator", 2, U_INTEGER),
    ("MMSI", 30, U_INTEGER),
    ("Part Number", 2, U_INTEGER),
    ("Vessel Name", 120, ASC_6BIT),
    ("Spare", 8, U_INTEGER),
    ("Ship Type", 8, U_INTEGER),
    ("Vendor ID", 18, ASC_6BIT),
    ("Unit Model Code", 4, U_INTEGER),
    ("Serial Number", 20, U_INTEGER),
    ("Call Sign", 42, ASC_6BIT),
    ("Dimension to Bow", 9, U_INTEGER),
    ("Dimension to Stern", 9, U_INTEGER)
    ("Dimension to Port", 6, U_INTEGER),
    ("Dimension to Starboard", 6, U_INTEGER),
    ("Mothership MMSI", 30, U_INTEGER),
    ("Spare", 6, U_INTEGER)])

STATIC_DATA_REPORT_KEY_B = const("24B")
STATIC_DATA_REPORT_PARSE_LIST_B = const([
    ("Message Type", 6, U_INTEGER),
    ("Repeat Indicator", 2, U_INTEGER),
    ("MMSI", 30, U_INTEGER),
    ("Part Number", 2, U_INTEGER),
    ("Vessel Name", 120, ASC_6BIT),
    ("Spare", 8, U_INTEGER),
    ("Ship Type", 8, U_INTEGER),
    ("Vendor ID", 18, ASC_6BIT),
    ("Unit Model Code", 4, U_INTEGER),
    ("Serial Number", 20, U_INTEGER),
    ("Call Sign", 42, ASC_6BIT),
    ("Dimension to Bow", 9, U_INTEGER),
    ("Dimension to Stern", 9, U_INTEGER)
    ("Dimension to Port", 6, U_INTEGER),
    ("Dimension to Starboard", 6, U_INTEGER),
    ("Mothership MMSI", 30, U_INTEGER),
    ("Spare", 6, U_INTEGER)])


# === a Dictionary of Message Type Parse Lists ===
# a dictionary that contains the lists that each contains the dimentions of the different fields of the message type they are representing
MSG_TYPE_PARSE_LISTS_DICTIONARY = const({
    1: POS_REP_CLASS_A_PARSE_LIST,
    2: POS_REP_CLASS_A_PARSE_LIST,
    3: POS_REP_CLASS_A_PARSE_LIST,
    5: STATIC_AND_VOYAGE_RELATED_DATA_PARSE_LIST,
    9: STANDART_SAR_AIRCRAFT_POS_REP_PARSE_LIST,
    18:STANDART_CLASS_B_POS_REP_PARSE_LIST,
    19:EXTENDED_CLASS_B_POS_REP_PARSE_LIST,
    STATIC_DATA_REPORT_KEY : STATIC_DATA_REPORT_PARSE_LIST,
    STATIC_DATA_REPORT_KEY_B : STATIC_DATA_REPORT_PARSE_LIST_B
    })


