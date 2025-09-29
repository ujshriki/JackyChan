import random

def to_six_bit_ascii(value, bit_length=168):
    """Convert an integer to 6-bit ASCII for AIS payload, ensuring 28 characters."""
    # Correct AIS 6-bit ASCII character set: '0' to 'W' and '`' to 'w'
    chars = "0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW`abcdefghijklmnopqrstuvw"
    if bit_length % 6 != 0:
        raise ValueError("Bit length must be divisible by 6")
    num_chars = bit_length // 6
    binary = bin(value)[2:].zfill(bit_length)  # Ensure exact bit length
    if len(binary) != bit_length:
        raise ValueError(f"Binary length {len(binary)} does not match expected {bit_length}")
    result = ""
    for i in range(0, bit_length, 6):
        six_bits = binary[i:i+6]
        char_index = int(six_bits, 2)
        if char_index > 63:
            raise ValueError(f"Invalid 6-bit value: {char_index}")
        result += chars[char_index]
    if len(result) != num_chars:
        raise ValueError(f"Expected {num_chars} characters, got {len(result)}")
    return result

def calculate_checksum(sentence):
    """Calculate NMEA checksum for a sentence (excluding ! and *)."""
    checksum = 0
    for char in sentence[1:sentence.find('*')]:
        checksum ^= ord(char)
    return f"{checksum:02X}"

def generate_type1_aivdm():
    """Generate a single Type 1 AIVDM sentence with random valid values."""
    msg_type = 1  # Type 1: Position Report
    repeat = 0
    mmsi = random.randint(200000000, 999999999)
    nav_status = random.randint(0, 15)
    rot = random.randint(-127, 127)
    sog = random.randint(0, 1022)
    pos_accuracy = random.randint(0, 1)
    lon = random.randint(-10800000, 10800000)
    lat = random.randint(-5400000, 5400000)
    cog = random.randint(0, 3599)
    true_heading = random.randint(0, 359) if random.random() < 0.9 else 511
    timestamp = random.randint(0, 59)
    maneuver = 0
    spare = 0
    raim = random.randint(0, 1)
    comm_state = 0

    # Convert to binary with exact bit lengths
    rot_bits = bin(rot & 0xFF)[2:].zfill(8)
    lon_bits = bin(lon & 0x0FFFFFFF)[2:].zfill(28) if lon >= 0 else bin(lon & 0x0FFFFFFF | 0x08000000)[2:].zfill(28)
    lat_bits = bin(lat & 0x07FFFFFF)[2:].zfill(27) if lat >= 0 else bin(lat & 0x07FFFFFF | 0x04000000)[2:].zfill(27)

    payload_bits = (
        bin(msg_type)[2:].zfill(6) +
        bin(repeat)[2:].zfill(2) +
        bin(mmsi)[2:].zfill(30) +
        bin(nav_status)[2:].zfill(4) +
        rot_bits +
        bin(sog)[2:].zfill(10) +
        bin(pos_accuracy)[2:].zfill(1) +
        lon_bits +
        lat_bits +
        bin(cog)[2:].zfill(12) +
        bin(true_heading)[2:].zfill(9) +
        bin(timestamp)[2:].zfill(6) +
        bin(maneuver)[2:].zfill(2) +
        bin(spare)[2:].zfill(3) +
        bin(raim)[2:].zfill(1) +
        bin(comm_state)[2:].zfill(19)
    )

    if len(payload_bits) != 168:
        raise ValueError(f"Payload length mismatch: {len(payload_bits)} bits")

    # Convert to integer for 6-bit ASCII encoding
    payload_int = int(payload_bits, 2)
    payload = to_six_bit_ascii(payload_int, 168)

    sentence = f"!AIVDM,1,1,,A,{payload},0"
    checksum = calculate_checksum(sentence)
    return f"{sentence}*{checksum}\r\n"

# Generate 100 sentences and save to file
with open("ais_test_sentences.txt", "w") as f:
    for _ in range(100):
        f.write(generate_type1_aivdm())
