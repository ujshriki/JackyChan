import "constants.py"

# === Fragment buffer ===
fragment_buffer = {}

def Purge_Old_Fragments():
    now = utime.time()
    to_delete = []
    for seq_id, entry in fragment_buffer.items():
        if now - entry[BUFFER_TIMESTAMP] > FRAGMENT_TIMEOUT_SEC:
            to_delete.append(seq_id)
    for seq_id in to_delete:
        del fragment_buffer[seq_id]


# === combines completed fragments ===
def Combine_Fragments(seq_id):
    """Combine fragments in order and return list of packets."""
    entry = fragment_buffer[seq_id]
    total = entry[BUFFER_NUM_OF_FRAGMENTS]
    packets = []
    for i in range(1, total + 1):
        packets.append(entry[BUFFER_FRAGMENT][i])
    return packets


# === Handles fragmented messages ===
# checks if the message is fragmented and handles buffering fragments and forwarding combined fragmented messages 
# returns a duple of a status code and a message
# status code like SINGLE_OK or MULTI_OK
# message either a single packet or a 
def Message_Fragmentation_Check(fields, packet):
    
    total_sentences = fields[1]
    current_sentence = fields[2]
    seq_id = fields[3]

    try:
        total_sentences = int(total_sentences)
        current_sentence = int(current_sentence)
    except ValueError:
        return (STATUS_INVALID, None)

    # Single-sentence message
    if total_sentences == 1:
        return (STATUS_SINGLE_OK, packet)

    # Multi-sentence message
    seq_key = seq_id if seq_id else "no_seq" ##################### FIX THIS!!!!!!!!!!!!!!!!!!!!!!!!!! this is when packets of fragmented messages don't come with a sequence ID which can happen for some reason, god damm it
    
    
    # Create new entry if missing
    if seq_key not in fragment_buffer:
        fragment_buffer[seq_key] = {
            BUFFER_NUM_OF_FRAGMENTS: total_sentences,
            BUFFER_FRAGMENT: {},
            BUFFER_TIMESTAMP: utime.time()
        }

    entry = fragment_buffer[seq_key]

    # Store current fragment
    entry[BUFFER_FRAGMENT][current_sentence] = packet
    entry[BUFFER_TIMESTAMP] = utime.time()

    # Check if all fragments are in # FIX THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! there are errors, syntax and others i think
    #if len(entry[BUFFER_FRAGMENT]) == entry[BUFFER_NUM_OF_FRAGMENTS]:
        #combined = combine_fragments(seq_key)
        #del fragment_buffer[seq_key]
        #return (STATUS_MULTI_OK, combined)

    return (STATUS_WAITING, None)