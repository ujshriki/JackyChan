import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import serial
import serial.tools.list_ports
import threading
import queue

class AISTester(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AIS Message Tester")
        self.geometry("800x600")

        # Available COM ports
        ports = [p.device for p in serial.tools.list_ports.comports()]

        # TX Port Combo
        tk.Label(self, text="TX Port:").grid(row=0, column=0, padx=10, pady=5)
        self.tx_var = tk.StringVar()
        self.tx_combo = ttk.Combobox(self, values=ports, textvariable=self.tx_var)
        self.tx_combo.grid(row=0, column=1, padx=10, pady=5)

        # RX Port Combo
        tk.Label(self, text="RX Port:").grid(row=0, column=2, padx=10, pady=5)
        self.rx_var = tk.StringVar()
        self.rx_combo = ttk.Combobox(self, values=ports, textvariable=self.rx_var)
        self.rx_combo.grid(row=0, column=3, padx=10, pady=5)

        # Open File Button
        self.file_btn = tk.Button(self, text="Open File", command=self.open_file)
        self.file_btn.grid(row=1, column=0, columnspan=4, pady=10)

        # Text Boxes
        tk.Label(self, text="Sent Messages").grid(row=2, column=0, columnspan=2)
        self.sent_text = ScrolledText(self, height=20, width=40, font=("Courier", 10))
        self.sent_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        tk.Label(self, text="Received Messages").grid(row=2, column=2, columnspan=2)
        self.recv_text = ScrolledText(self, height=20, width=40, font=("Courier", 10))
        self.recv_text.grid(row=3, column=2, columnspan=2, padx=10, pady=5)

        # Configure tags for coloring
        self.sent_text.tag_config("green", foreground="green")
        self.sent_text.tag_config("red", foreground="red")

        # Buttons
        self.send_btn = tk.Button(self, text="Send Next Line", command=self.send_next)
        self.send_btn.grid(row=4, column=0, columnspan=2, pady=10)

        self.clear_btn = tk.Button(self, text="Clear", command=self.clear)
        self.clear_btn.grid(row=4, column=2, columnspan=2, pady=10)

        # Variables
        self.file_path = None
        self.lines = []
        self.line_idx = 0
        self.sent = []  # List of sent lines
        self.received = []  # List of received lines
        self.tx_ser = None
        self.rx_ser = None
        self.recv_queue = queue.Queue()
        self.running = False

    def open_serial(self):
        if not self.tx_var.get() or not self.rx_var.get():
            print("Please select TX and RX ports.")
            return False
        try:
            self.tx_ser = serial.Serial(self.tx_var.get(), 38400, timeout=1)
            self.rx_ser = serial.Serial(self.rx_var.get(), 38400, timeout=1)
            self.running = True
            threading.Thread(target=self.receiver, daemon=True).start()
            self.after(100, self.process_queue)
            return True
        except Exception as e:
            print(f"Error opening serial ports: {e}")
            return False

    def receiver(self):
        while self.running:
            try:
                line = self.rx_ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    self.recv_queue.put(line)
            except Exception as e:
                pass

    def process_queue(self):
        try:
            while True:
                line = self.recv_queue.get_nowait()
                self.handle_receive(line)
        except queue.Empty:
            pass
        if self.running:
            self.after(100, self.process_queue)

    def handle_receive(self, line):
        # The corresponding line number (1-based)
        line_num = len(self.received) + 1
        if line_num <= len(self.sent):
            tag = "green" if line == self.sent[line_num - 1] else "red"
            self.sent_text.tag_add(tag, f"{line_num}.0", f"{line_num}.0 lineend")
        # Append to received text
        self.recv_text.insert('end', line + '\n')
        self.received.append(line)

    def send_next(self):
        if not self.tx_ser or not self.rx_ser:
            if not self.open_serial():
                return
        if self.line_idx >= len(self.lines):
            print("No more lines to send.")
            return
        line = self.lines[self.line_idx].strip()
        self.line_idx += 1

        # Handle skips for unreceived previous lines
        diff = len(self.sent) - len(self.received)
        for _ in range(diff):
            line_num = len(self.received) + 1
            self.sent_text.tag_add("red", f"{line_num}.0", f"{line_num}.0 lineend")
            self.recv_text.insert('end', '\n')
            self.received.append('')

        # Send the line
        try:
            self.tx_ser.write((line + '\r\n').encode('utf-8'))
        except Exception as e:
            print(f"Error sending: {e}")

        # Append to sent text (no color yet)
        self.sent_text.insert('end', line + '\n')
        self.sent.append(line)

    def clear(self):
        self.sent_text.delete('1.0', 'end')
        self.recv_text.delete('1.0', 'end')
        self.sent = []
        self.received = []

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.file_path:
            with open(self.file_path, 'r') as f:
                self.lines = f.readlines()
            self.line_idx = 0
            print(f"Loaded file: {self.file_path}")

if __name__ == "__main__":
    app = AISTester()
    app.mainloop()