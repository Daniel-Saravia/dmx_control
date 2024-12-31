import serial
import time

# Debugging: Print status messages
def debug(message):
    print(f"[DEBUG] {message}")

# Set up the serial connection to the Enttec Open DMX USB
DMX_PORT = '/dev/ttyUSB0'  # Update this if necessary
BAUD_RATE = 250000         # DMX baud rate

try:
    debug("Initializing serial connection...")
    dmx = serial.Serial(DMX_PORT, baudrate=BAUD_RATE, stopbits=serial.STOPBITS_TWO, bytesize=serial.EIGHTBITS)
    debug(f"Serial connection established on {DMX_PORT} with baud rate {BAUD_RATE}.")
except Exception as e:
    print(f"[ERROR] Could not open serial port {DMX_PORT}: {e}")
    exit(1)

# Create a DMX packet (513 bytes: 1 start byte + 512 channels)
dmx_packet = bytearray(513)
dmx_packet[0] = 0  # Start byte (always 0 for DMX512)

# Set DMX values based on the extracted table
dmx_packet[1] = 128  # Channel 1: Pan
dmx_packet[2] = 200  # Channel 2: Pan Fine
dmx_packet[3] = 255  # Channel 3: Tilt
dmx_packet[4] = 150  # Channel 4: Tilt Fine
dmx_packet[5] = 64   # Channel 5: Color Select
dmx_packet[6] = 100  # Channel 6: Pattern
dmx_packet[7] = 50   # Channel 7: Strobe
dmx_packet[8] = 255  # Channel 8: Brightness
dmx_packet[9] = 120  # Channel 9: Tilt/Pan Speed
dmx_packet[10] = 0   # Channel 10: Automatic Mode
dmx_packet[11] = 0   # Channel 11: Other Mode

# Debugging: Print initial DMX packet
debug(f"Initial DMX packet: {list(dmx_packet[:12])}")  # Print the first 12 channels

# Send DMX data continuously
try:
    while True:
        dmx.write(dmx_packet)  # Send the DMX packet
        dmx.flush()            # Ensure the data is transmitted
        debug("DMX packet sent.")  # Log every packet transmission
        time.sleep(0.02)       # DMX refresh rate (~50Hz)
except KeyboardInterrupt:
    debug("Stopping DMX control.")
finally:
    if dmx.is_open:
        debug("Closing serial connection...")
        dmx.close()
    debug("DMX control stopped.")
