
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import serial
import serial.tools.list_ports
import threading
import queue
import time

class AISTester(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AIS Message Tester")
        self.geometry("1200x900")

        # AIS 6-bit dicts
        self.ais6bit_dict = {
            '@': 0,
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
            'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20,
            'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,
            '[': 27, '\\': 28, ']': 29, '^': 30, '_': 31, '`': 32,
            'a': 33, 'b': 34, 'c': 35, 'd': 36, 'e': 37, 'f': 38, 'g': 39, 'h': 40, 'i': 41, 'j': 42,
            'k': 43, 'l': 44, 'm': 45, 'n': 46, 'o': 47, 'p': 48, 'q': 49, 'r': 50, 's': 51, 't': 52,
            'u': 53, 'v': 54, 'w': 55, 'x': 56, 'y': 57, 'z': 58,
            '{': 59, '|': 60, '}': 61, '~': 62
        }
        self.ais6bit_to_char = ['?'] * 64
        self.ais6bit_to_char[0] = '@'
        for i in range(1, 27):
            self.ais6bit_to_char[i] = chr(ord('A') + i - 1)
        self.ais6bit_to_char[27] = '['
        self.ais6bit_to_char[28] = '\\'
        self.ais6bit_to_char[29] = ']'
        self.ais6bit_to_char[30] = '^'
        self.ais6bit_to_char[31] = '_'
        self.ais6bit_to_char[32] = '`'
        for i in range(33, 59):
            self.ais6bit_to_char[i] = chr(ord('a') + i - 33)
        self.ais6bit_to_char[59] = '{'
        self.ais6bit_to_char[60] = '|'
        self.ais6bit_to_char[61] = '}'
        self.ais6bit_to_char[62] = '~'
        self.ais6bit_to_char[63] = '@'

        # Available COM ports
        ports = [p.device for p in serial.tools.list_ports.comports()]

        # TX Port Combo
        tk.Label(self, text="TX Port:").grid(row=0, column=0, padx=10, pady=5)
        self.tx_var = tk.StringVar()
        self.tx_combo = ttk.Combobox(self, values=ports, textvariable=self.tx_var, width=15)
        self.tx_combo.grid(row=0, column=1, padx=10, pady=5)

        # RX Port Combo
        tk.Label(self, text="RX Port:").grid(row=0, column=2, padx=10, pady=5)
        self.rx_var = tk.StringVar()
        self.rx_combo = ttk.Combobox(self, values=ports, textvariable=self.rx_var, width=15)
        self.rx_combo.grid(row=0, column=3, padx=10, pady=5)

        # Open File Button
        self.file_btn = tk.Button(self, text="Open File", command=self.open_file)
        self.file_btn.grid(row=1, column=0, columnspan=4, pady=10)

        # Sent label and text
        tk.Label(self, text="Sent Messages", font=("Arial", 10, "bold")).grid(row=2, column=0, columnspan=2, pady=5)
        self.sent_text = ScrolledText(self, height=25, width=50, font=("Courier", 9))
        self.sent_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')

        # Last Received label and text
        tk.Label(self, text="Last Received (Raw)", font=("Arial", 10, "bold")).grid(row=2, column=2, columnspan=2, pady=5)
        self.recv_text = ScrolledText(self, height=3, width=50, font=("Courier", 10))
        self.recv_text.grid(row=3, column=2, columnspan=2, padx=10, pady=5, sticky='nsew')

        # Parsed label and text
        tk.Label(self, text="Parsed AIS Message (if OK)", font=("Arial", 10, "bold")).grid(row=4, column=2, columnspan=2, pady=5)
        self.parsed_text = ScrolledText(self, height=15, width=50, font=("Courier", 9))
        self.parsed_text.grid(row=5, column=2, columnspan=2, padx=10, pady=5, sticky='nsew')

        # Configure tags for coloring in sent_text
        self.sent_text.tag_config("green", foreground="green", font=("Courier", 9, "bold"))
        self.sent_text.tag_config("red", foreground="red", font=("Courier", 9, "bold"))

        # Buttons
        self.send_btn = tk.Button(self, text="Send Next Line", command=self.send_next, bg="lightgreen")
        self.send_btn.grid(row=6, column=0, columnspan=2, pady=10)

        self.clear_btn = tk.Button(self, text="Clear", command=self.clear)
        self.clear_btn.grid(row=6, column=2, pady=10)

        self.save_btn = tk.Button(self, text="Save Results", command=self.save_results, bg="lightblue")
        self.save_btn.grid(row=6, column=3, pady=10)

        # Variables
        self.file_path = None
        self.lines = []
        self.line_idx = 0
        self.sent = []
        self.received = []
        self.tx_ser = None
        self.rx_ser = None
        self.recv_queue = queue.Queue()
        self.running = False

        # Configure grid weights
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(5, weight=1)

    def payload_to_bits(self, payload):
        bits = ''
        for c in payload:
            val = self.ais6bit_dict.get(c, -1)
            if val == -1:
                return None
            bits += f'{val:06b}'
        return bits

    def bits_to_ascii(self, bitstr):
        s = ''
        i = 0
        while i + 6 <= len(bitstr):
            val = int(bitstr[i:i+6], 2)
            s += self.ais6bit_to_char[val] if val < 64 else '?'
            i += 6
        return s.rstrip('@')

    def parse_ais_message(self, line):
        if not line.startswith('!AIVDM'):
            return "Not an AIVDM sentence"
        if '*' not in line:
            return "Invalid NMEA format"
        msg, received_chksum = line.split('*', 1)
        # try:
        #    received_chksum = int(chksum_str[0:2], 16)
        # except ValueError:
        #    return "Invalid checksum format"
        calculated = 0
        for c in msg[1:]:
            calculated ^= ord(c)
        if calculated != received_chksum:
            return f"Checksum error: expected {calculated:02X}, got {received_chksum:02X}"
        fields = [f for f in msg.split(',') if f]
        if len(fields) < 6:
            return "Invalid number of fields"
        try:
            num_frags = int(fields[1])
            frag_num = int(fields[2])
            payload = fields[4]
            fill_bits = int(fields[5])
        except ValueError:
            return "Invalid fragment or fill bits"
        if num_frags != 1 or frag_num != 1:
            return f"Multi-fragment message ({num_frags}/{frag_num}) - cannot parse single"
        bits = self.payload_to_bits(payload)
        if not bits:
            return "Invalid characters in payload"
        try:
            msgid = int(bits[0:6], 2)
            if msgid not in [1,2,3,4,5,9,18,19,24]:
                return f"Unsupported AIS type {msgid}"
            repeat = int(bits[6:8], 2)
            mmsi = int(bits[24:54], 2)
            result = f"AIS Type {msgid} (Repeat: {repeat}) | MMSI: {mmsi}\n"
            if msgid in [1, 2, 3]:
                # Class A Position Report
                nav_status = int(bits[38:42], 2)
                rot_raw = int(bits[42:50], 2)
                sog_raw = int(bits[51:61], 2)
                sog = f"{sog_raw / 10.0:.1f}" if sog_raw < 1023 else "N/A"
                lon_raw = int(bits[62:90], 2)
                lon = (lon_raw - (1 << 28) if lon_raw >= (1 << 27) else lon_raw) / 10000000.0
                lat_raw = int(bits[90:117], 2)
                lat = (lat_raw - (1 << 27) if lat_raw >= (1 << 26) else lat_raw) / 10000000.0
                cog_raw = int(bits[117:129], 2)
                cog = f"{cog_raw / 10.0:.1f}" if cog_raw < 3600 else "N/A"
                heading_raw = int(bits[129:138], 2)
                heading = f"{heading_raw}" if 0 <= heading_raw <= 359 else "N/A"
                result += f"Position: {lat:.7f}°, {lon:.7f}°\n"
                result += f"SOG: {sog} kn | COG: {cog}° | Heading: {heading}°\n"
                result += f"Nav Status: {nav_status}\n"
            elif msgid in [18, 19]:
                # Class B Position Report
                sog_raw = int(bits[42:50], 2)
                sog = f"{sog_raw / 10.0:.1f}"
                lon_raw = int(bits[51:78], 2)
                lon = (lon_raw - (1 << 27) if lon_raw >= (1 << 26) else lon_raw) / 100000.0
                lat_raw = int(bits[78:105], 2)
                lat = (lat_raw - (1 << 27) if lat_raw >= (1 << 26) else lat_raw) / 100000.0
                cog_raw = int(bits[105:117], 2)
                cog = f"{cog_raw / 10.0:.1f}"
                heading_raw = int(bits[117:126], 2)
                heading = f"{heading_raw}" if 0 <= heading_raw <= 359 else "N/A"
                result += f"Position: {lat:.5f}°, {lon:.5f}°\n"
                result += f"SOG: {sog} kn | COG: {cog}° | Heading: {heading}°\n"
            elif msgid == 4:
                # Base Station Report
                year = int(bits[38:52], 2)
                month = int(bits[52:57], 2)
                day = int(bits[57:62], 2)
                hour = int(bits[62:67], 2)
                minute = int(bits[67:73], 2)
                second = int(bits[73:79], 2)
                lat_raw = int(bits[79:106], 2)
                lat = (lat_raw - (1 << 27) if lat_raw >= (1 << 26) else lat_raw) / 10000000.0
                lon_raw = int(bits[106:134], 2)
                lon = (lon_raw - (1 << 28) if lon_raw >= (1 << 27) else lon_raw) / 10000000.0
                result += f"Position: {lat:.7f}°, {lon:.7f}°\n"
                result += f"Time: {year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}\n"
            elif msgid == 5:
                # Static and Voyage Data Part A
                imo = int(bits[40:70], 2)
                callsign = self.bits_to_ascii(bits[70:112])
                shipname = self.bits_to_ascii(bits[112:232])
                result += f"IMO: {imo}\n"
                result += f"Ship Name: {shipname}\n"
                result += f"Callsign: {callsign}\n"
            elif msgid == 24:
                # Static Data Report Part A
                shipname = self.bits_to_ascii(bits[40:160])
                callsign = self.bits_to_ascii(bits[160:202])
                result += f"Ship Name: {shipname}\n"
                result += f"Callsign: {callsign}\n"
            elif msgid == 9:
                # SAR Aircraft Position
                result += "Standard SAR Aircraft Position Report\n"
                # Basic position parse
                lon_raw = int(bits[95:123], 2)
                lon = (lon_raw - (1 << 28) if lon_raw >= (1 << 27) else lon_raw) / 10000000.0
                lat_raw = int(bits[123:150], 2)
                lat = (lat_raw - (1 << 27) if lat_raw >= (1 << 26) else lat_raw) / 10000000.0
                result += f"Position: {lat:.7f}°, {lon:.7f}°\n"
            return result
        except Exception as e:
            return f"Parse error: {str(e)}"

    def open_serial(self):
        if not self.tx_var.get() or not self.rx_var.get():
            tk.messagebox.showerror("Error", "Please select TX and RX ports.")
            return False
        if self.tx_var.get() == self.rx_var.get():
            tk.messagebox.showerror("Error", "TX and RX ports must be different.")
            return False
        try:
            if self.tx_ser:
                self.tx_ser.close()
            if self.rx_ser:
                self.rx_ser.close()
            self.tx_ser = serial.Serial(self.tx_var.get(), 38400, timeout=1)
            self.rx_ser = serial.Serial(self.rx_var.get(), 38400, timeout=1)
            self.running = True
            threading.Thread(target=self.receiver, daemon=True).start()
            self.after(100, self.process_queue)
            return True
        except Exception as e:
            tk.messagebox.showerror("Serial Error", f"Error opening serial ports: {e}")
            return False

    def receiver(self):
        while self.running:
            try:
                line = self.rx_ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    self.recv_queue.put(line)
            except:
                if not self.running:
                    break
            time.sleep(0.001)

    def process_queue(self):
        try:
            while True:
                line = self.recv_queue.get_nowait()
                self.handle_receive(line)
        except queue.Empty:
            pass
        if self.running:
            self.after(50, self.process_queue)

    def handle_receive(self, line):
        line_num = len(self.received) + 1
        is_match = False
        tag = "red"
        if line_num <= len(self.sent):
            expected = self.sent[line_num - 1]
            if line == expected:
                is_match = True
                tag = "green"
            # Remove previous tags
            self.sent_text.tag_remove("green", f"{line_num}.0", f"{line_num}.0 lineend")
            self.sent_text.tag_remove("red", f"{line_num}.0", f"{line_num}.0 lineend")
            # Add new tag
            self.sent_text.tag_add(tag, f"{line_num}.0", f"{line_num}.0 lineend")

        # Update display (only last)
        self.recv_text.delete('1.0', 'end')
        self.parsed_text.delete('1.0', 'end')
        self.recv_text.insert('end', line + '\n')

        # Parse if match
        if is_match:
            parsed = self.parse_ais_message(line)
            self.parsed_text.insert('end', parsed + '\n')

        # Append to internal list
        self.received.append(line)

    def send_next(self):
        if not self.tx_ser or not self.rx_ser:
            if not self.open_serial():
                return
        if self.line_idx >= len(self.lines):
            tk.messagebox.showinfo("Info", "No more lines to send.")
            return

        # Handle skips
        diff = len(self.sent) - len(self.received)
        for _ in range(diff):
            line_num = len(self.received) + 1
            # Remove previous tags
            self.sent_text.tag_remove("green", f"{line_num}.0", f"{line_num}.0 lineend")
            self.sent_text.tag_remove("red", f"{line_num}.0", f"{line_num}.0 lineend")
            # Add red
            self.sent_text.tag_add("red", f"{line_num}.0", f"{line_num}.0 lineend")
            self.received.append('')
            # Update display to empty for skip
            self.recv_text.delete('1.0', 'end')
            self.parsed_text.delete('1.0', 'end')
            self.recv_text.insert('end', '\n')

        # Send next line
        line = self.lines[self.line_idx].strip()
        self.line_idx += 1
        try:
            self.tx_ser.write((line + '\r\n').encode('ascii'))
        except Exception as e:
            tk.messagebox.showerror("Send Error", f"Error sending: {e}")
            return

        # Append to sent (no tag yet)
        self.sent_text.insert('end', line + '\n')
        self.sent.append(line)

    def save_results(self):
        if not self.sent:
            tk.messagebox.showinfo("Info", "No results to save.")
            return
        # Pad received if necessary
        while len(self.received) < len(self.sent):
            line_num = len(self.received) + 1
            self.sent_text.tag_remove("green", f"{line_num}.0", f"{line_num}.0 lineend")
            self.sent_text.tag_remove("red", f"{line_num}.0", f"{line_num}.0 lineend")
            self.sent_text.tag_add("red", f"{line_num}.0", f"{line_num}.0 lineend")
            self.received.append('')

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Save Results"
        )
        if not file_path:
            return
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("AIS Message Testing Results\n")
                f.write("=" * 60 + "\n\n")
                for i in range(len(self.sent)):
                    s = self.sent[i]
                    r = self.received[i]
                    if r == '':
                        status = "TIMEOUT"
                    elif r == s:
                        status = "OK"
                    else:
                        status = "MISMATCH"
                    f.write(f"Line {i+1}:\n")
                    f.write(f"  Sent:     {s}\n")
                    f.write(f"  Received: {r if r else 'TIMEOUT'}\n")
                    f.write(f"  Status:   {status}\n")
                    if status == "OK":
                        parsed = self.parse_ais_message(s)
                        f.write(f"  Parsed:\n{parsed}\n")
                    f.write("-" * 60 + "\n\n")
            tk.messagebox.showinfo("Success", f"Results saved to {file_path}")
        except Exception as e:
            tk.messagebox.showerror("Save Error", f"Error saving file: {e}")

    def clear(self):
        self.sent_text.delete('1.0', 'end')
        self.recv_text.delete('1.0', 'end')
        self.parsed_text.delete('1.0', 'end')
        self.sent = []
        self.received = []
        self.line_idx = 0

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.file_path:
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.lines = f.readlines()
                self.line_idx = 0
                self.clear()  # Clear previous test
                tk.messagebox.showinfo("Success", f"Loaded {len(self.lines)} lines from {self.file_path}")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error loading file: {e}")

    def destroy(self):
        self.running = False
        if self.tx_ser:
            self.tx_ser.close()
        if self.rx_ser:
            self.rx_ser.close()
        super().destroy()

if __name__ == "__main__":
    app = AISTester()
    app.mainloop()