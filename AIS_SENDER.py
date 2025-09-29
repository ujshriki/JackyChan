import serial
import pyais
from pyais import NMEAMessage
from pyais.messages import MessageType1

# Create a sample AIS message (Message Type 1)
msg = MessageType1.create(
    mmsi=123456789,
    nav_status=0,
    rot=0,
    sog=10.2,
    position_accuracy=1,
    x=12.3456,
    y=45.6789,
    cog=89.0,
    true_heading=90,
    timestamp=60
)

# Encode the message into NMEA format
nmea_sentences = pyais.messages.decode(msg)

# Open the serial port
with serial.Serial(port="COM3", baudrate=38400, timeout=1) as ser:
    for sentence in nmea_sentences:
        ser.write((sentence + '\r\n').encode('ascii'))
        print(f"Sent: {sentence}")
