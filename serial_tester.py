import tkinter as tk
from tkinter import ttk, filedialog
import serial
import serial.tools.list_ports
import threading
import queue
import time

def refresh_ports():
    ports = [p.device for p in serial.tools.list_ports.comports()]
    tx_combo['values'] = ports
    rx_combo['values'] = ports

def open_file():
    fp = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if fp:
        file_path.set(fp)
        check_enable_send()

def check_enable_send(*args):
    if tx_combo.get() and rx_combo.get() and file_path.get():
        send_btn['state'] = 'normal'
    else:
        send_btn['state'] = 'disabled'

def open_serials():
    global tx_ser, rx_ser
    if tx_ser:
        tx_ser.close()
    if rx_ser:
        rx_ser.close()
    tx_port = tx_combo.get()
    rx_port = rx_combo.get()
    if tx_port and rx_port:
        try:
            tx_ser = serial.Serial(tx_port, 9600, timeout=1)
            rx_ser = serial.Serial(rx_port, 9600, timeout=0.1)
            return True
        except Exception as e:
            print(f"Error opening serial ports: {e}")
            return False
    return False

def listen_rx():
    global listening
    while listening:
        if rx_ser and rx_ser.is_open:
            try:
                line = rx_ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    rx_queue.put(line)
            except:
                pass
        time.sleep(0.01)

def update_rx():
    while not rx_queue.empty():
        line = rx_queue.get()
        right_text.insert('end', line + '\n')
        right_text.see('end')
    root.after(100, update_rx)

def send_file():
    if not open_serials():
        print("Cannot open serial ports")
        return
    global listening
    listening = True
    threading.Thread(target=listen_rx, daemon=True).start()
    root.after(100, update_rx)

    # Clear texts
    left_text.config(state='normal')
    left_text.delete('1.0', 'end')
    left_text.config(state='disabled')
    right_text.delete('1.0', 'end')

    with open(file_path.get(), 'r') as f:
        lines = f.readlines()

    left_text.config(state='normal')
    for line in lines:
        stripped = line.strip()
        if stripped:
            # Send with \r\n if not already ending with \n
            send_data = (line if line.endswith('\n') else line + '\r\n').encode('utf-8')
            tx_ser.write(send_data)
            left_text.insert('end', line)
    left_text.config(state='disabled')

def compare_texts():
    # Clear existing tags
    for tag in left_text.tag_names():
        left_text.tag_delete(tag)
    for tag in right_text.tag_names():
        right_text.tag_delete(tag)

    left_content = left_text.get('1.0', 'end').rstrip('\n')
    right_content = right_text.get('1.0', 'end').rstrip('\n')
    left_lines = left_content.split('\n')
    right_lines = right_content.split('\n')

    if len(left_lines) != len(right_lines):
        print("Line counts differ. Adjust alignment in the Received area and try again.")
        return

    for i in range(len(left_lines)):
        lline = left_lines[i].strip()
        rline = right_lines[i].strip()
        color = 'green' if lline == rline and lline else 'red'
        start = f"{i+1}.0"
        end = f"{i+2}.0"
        left_text.tag_add(color, start, end)
        right_text.tag_add(color, start, end)

    left_text.tag_config('green', foreground='green')
    left_text.tag_config('red', foreground='red')
    right_text.tag_config('green', foreground='green')
    right_text.tag_config('red', foreground='red')

# GUI setup
root = tk.Tk()
root.title("UART AIS Sentence Tester")
root.geometry("800x600")

# Top frame for controls
top_frame = ttk.Frame(root)
top_frame.pack(pady=10, fill='x')

# Tx COM
ttk.Label(top_frame, text="Tx COM:").grid(row=0, column=0, padx=5)
tx_combo = ttk.Combobox(top_frame, width=15)
tx_combo.grid(row=0, column=1, padx=5)
tx_combo.bind('<<ComboboxSelected>>', check_enable_send)

# Rx COM
ttk.Label(top_frame, text="Rx COM:").grid(row=0, column=2, padx=5)
rx_combo = ttk.Combobox(top_frame, width=15)
rx_combo.grid(row=0, column=3, padx=5)
rx_combo.bind('<<ComboboxSelected>>', check_enable_send)

# Refresh ports
refresh_btn = ttk.Button(top_frame, text="Refresh Ports", command=refresh_ports)
refresh_btn.grid(row=0, column=4, padx=5)
refresh_ports()

# File selection
ttk.Label(top_frame, text="Test File:").grid(row=1, column=0, padx=5)
file_path = tk.StringVar()
file_entry = ttk.Entry(top_frame, textvariable=file_path, width=50)
file_entry.grid(row=1, column=1, columnspan=3, padx=5)
file_path.trace('w', check_enable_send)
open_btn = ttk.Button(top_frame, text="Open Test File", command=open_file)
open_btn.grid(row=1, column=4, padx=5)

# Send button
send_btn = ttk.Button(root, text="Send", command=send_file)
send_btn.pack(pady=10)
send_btn['state'] = 'disabled'

# Text areas frame
text_frame = ttk.Frame(root)
text_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Sent (left)
ttk.Label(text_frame, text="Sent Sentences").pack(anchor='w')
left_scroll = ttk.Scrollbar(text_frame)
left_text = tk.Text(text_frame, height=20, width=50, yscrollcommand=left_scroll.set, state='disabled')
left_scroll.config(command=left_text.yview)
left_text.pack(side='left', fill='both', expand=True)
left_scroll.pack(side='left', fill='y')

# Received (right)
ttk.Label(text_frame, text="Received Sentences (Editable for Alignment)").pack(anchor='e')
right_scroll = ttk.Scrollbar(text_frame)
right_text = tk.Text(text_frame, height=20, width=50, yscrollcommand=right_scroll.set)
right_scroll.config(command=right_text.yview)
right_text.pack(side='right', fill='both', expand=True)
right_scroll.pack(side='right', fill='y')

# Compare button
compare_btn = ttk.Button(root, text="Compare", command=compare_texts)
compare_btn.pack(pady=10)

# Globals
tx_ser = None
rx_ser = None
rx_queue = queue.Queue()
listening = False

root.mainloop()