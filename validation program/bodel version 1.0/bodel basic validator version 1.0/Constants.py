from micropython import const

###
### === Constants ===
###

RECEIVE_PIN = const(1)
TRANCEIVE_PIN = const(0)

### === Packet Fields constants ===
# constant examples of valid fields
VALID_START_OF_SENTANCE_A = "!AIVDM"
VALID_START_OF_SENTANCE_B = "!AIVDO"
VALID_PACKET_FIELDS_NUM = const(7)
FIELD_FILLBIT_N_CHECKSUM_LENGTH = const(2)
VALID_CHECKSUM_LENGTH = const(2)
# constants of field index in split packet
FIELD_START_OF_SENTANCE = const(0)
FIELD_FILLBIT_N_CHECKSUM = const(-1)
FIELD_CHECKSUM = const(1)
FIELD_FILLBIT = const(0)

# === Status / error codes ===
STATUS_INVALID = "INVALID"                    # check failed, non specific
STATUS_INVALID_PACKET = "INVALID_PACKET"      # type/empty check failed
STATUS_INVALID_FIELDS = "INVALID_FIELDS"      # failed to parse fragmentation fields
STATUS_FIELD_VALID = "VALID_FIELD"           # the current checked field is valid
STATUS_SINGLE_OK = "SINGLE_OK"              # single sentence validated
STATUS_MULTI_OK = "MULTI_OK"                 # multi-fragment message validated
STATUS_WAITING = "WAITING_FOR_FRAGMENTS"      # waiting for remaining fragments
STATUS_FRAGMENT_EXPIRED = "FRAGMENT_EXPIRED"  # timed out fragment

# === Decoding and Message Data Verification Constants ===
ASCII_CHAR_BASE_VALUE = const(48)
AIS_TABLE_LIMIT = const(39)
MAX_SIX_BIT_NUM = const(63)
AIS_OVERFLOW_DOWN_STEP = const(8)
FORMAT_6BIT_SPECIFIER = '{:06b}' # the code that specifies how to format the conversion from the 6bit integer to the bitstring


# === Fragment buffer Constants
FRAGMENT_TIMEOUT_SEC = const(5)
BUFFER_TIMESTAMP = "timestamp"
BUFFER_NUM_OF_FRAGMENTS = "num_of_fragments"
BUFFER_FRAGMENT = "fragment"


