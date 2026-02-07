from micropython import const

###
### === Constants ===
###

RECEIVE_PIN = 1
TRANCEIVE_PIN = 0

# === Decoding and Message Data Verification Constants ===
ASCII_CHAR_BASE_VALUE = 48
AIS_TABLE_LIMIT = 39
MAX_SIX_BIT_NUM = 63
AIS_OVERFLOW_DOWN_STEP = 8
FORMAT_6BIT_SPECIFIER = '{:06b}' # the code that specifies how to format the conversion from the 6bit integer to the bitstring

#
INTEGER = "int"
U_INTEGER = "u_int"
BOOLEAN = "bool"
ASC_6BIT = "str"
