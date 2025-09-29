def decode_6bit_ascii(payload):
    """Decode AIVDM payload from 6-bit ASCII to binary string."""
    ascii_map = {chr(i + 48): i for i in range(48)}  # 0-47 for '0' to '/'
    ascii_map.update({chr(i + 56): i for i in range(48, 64)})  # 48-63 for '@' to 'O'

    binary = ""
    for char in payload:
        if char in ascii_map:
            value = ascii_map[char]
            binary += format(value, '06b')  # Convert to 6-bit binary
    return binary


def validate_ais_type1(binary):
    """Validate fields of AIS Type 1 message (Position Report)."""
    fields = [
        {"name": "Message Type", "bits": 6, "range": (1, 3), "desc": "Must be 1, 2, or 3"},
        {"name": "Repeat Indicator", "bits": 2, "range": (0, 3), "desc": "0-3"},
        {"name": "MMSI", "bits": 30, "range": (0, 999999999), "desc": "Maritime Mobile Service Identity"},
        {"name": "Navigation Status", "bits": 4, "range": (0, 15), "desc": "0-15"},
        {"name": "Rate of Turn", "bits": 8, "range": (-128, 127), "desc": "Signed, -128 to 127"},
        {"name": "Speed Over Ground", "bits": 10, "range": (0, 1023), "desc": "0-1022, 1023 = not available"},
        {"name": "Position Accuracy", "bits": 1, "range": (0, 1), "desc": "0 = low, 1 = high"},
        {"name": "Longitude", "bits": 28, "range": (-1800000, 1800000),
         "desc": "Signed, in 1/10000 min, 1810000 = not available"},
        {"name": "Latitude", "bits": 27, "range": (-900000, 900000),
         "desc": "Signed, in 1/10000 min, 910000 = not available"},
        {"name": "Course Over Ground", "bits": 12, "range": (0, 3600), "desc": "0-3599, 3600 = not available"},
        {"name": "True Heading", "bits": 9, "range": (0, 511), "desc": "0-359, 511 = not available"},
        {"name": "Timestamp", "bits": 6, "range": (0, 63), "desc": "UTC second, 60-63 = not available"},
        {"name": "Maneuver Indicator", "bits": 2, "range": (0, 3), "desc": "0-3"},
        {"name": "Spare", "bits": 3, "range": (0, 0), "desc": "Must be 0"},
        {"name": "RAIM Flag", "bits": 1, "range": (0, 1), "desc": "Receiver Autonomous Integrity Monitoring"},
        {"name": "Communication State", "bits": 19, "range": (0, 524287), "desc": "SOTDMA/ITDMA communication state"}
    ]

    results = []
    bit_pos = 0
    for field in fields:
        bits = field["bits"]
        if bit_pos + bits > len(binary):
            results.append({
                "Field": field["name"],
                "Value": None,
                "Status": f"Error: Not enough bits (requires {bits}, remaining {len(binary) - bit_pos})",
                "Description": field["desc"],
                "Bits": ""
            })
            break

        field_bits = binary[bit_pos:bit_pos + bits]
        value = int(field_bits, 2)

        if field["name"] in ["Rate of Turn", "Longitude", "Latitude"]:
            if value & (1 << (bits - 1)):
                value = value - (1 << bits)

        min_val, max_val = field["range"]
        status = "Valid" if min_val <= value <= max_val else f"Invalid (out of range: {min_val} to {max_val})"

        results.append({
            "Field": field["name"],
            "Value": value,
            "Status": status,
            "Description": field["desc"],
            "Bits": field_bits
        })

        bit_pos += bits

    return results


def parse_aivdm(aivdm_sentence):
    """Parse and validate an AIVDM sentence."""
    try:
        parts = aivdm_sentence.split(',')
        if len(parts) < 6 or parts[0] != "!AIVDM":
            return {"error": "Invalid AIVDM sentence format"}

        payload = parts[5]
        binary = decode_6bit_ascii(payload)

        if len(binary) < 6:
            return {"error": "Payload too short to determine message type"}

        msg_type = int(binary[:6], 2)
        if msg_type in [1, 2, 3]:
            return validate_ais_type1(binary)
        else:
            return {"error": f"Unsupported message type: {msg_type}"}

    except Exception as e:
        return {"error": f"Error processing AIVDM: {str(e)}"}


def main(file_path):
    """Read AIVDM messages from a file and validate each one."""
    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, 1):
                # Strip whitespace and empty lines
                aivdm_message = line.strip()
                if not aivdm_message:
                    continue

                print(f"\nProcessing message {line_number}: {aivdm_message}")
                result = parse_aivdm(aivdm_message)

                if isinstance(result, dict) and "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    fail = False
                    for field in result:
                        if "Error" in field["Status"]:
                            fail = True
                            print(
                                f"[FAIL] Field: {field['Field']}, Status: {field['Status']}, Description: {field['Description']}")
                        else:
                            print(f"[PASS] Field: {field['Field']}, Value: {field['Value']}, Status: {field['Status']}, "
                                  f"Bits: {field['Bits']}, Description: {field['Description']}")
                if fail:
                    print(f"\033[31mMessage Failed Validation\033[0m")
                else:
                    print(f"\033[32mMessage Validation Passed!\033[0m")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
    except Exception as e:
        print(f"Error reading file: {str(e)}")


if __name__ == "__main__":
    # Example file path (replace with your file path)
    file_path = "ais_test_sentences.txt"
    main(file_path)

