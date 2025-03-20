import platform
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox

# Function to ping once
def ping_once(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = f"ping {param} 1 {host}"
    response = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    return response

# Function to ping in a thread (stoppable)
def ping_in_thread(host, stop_event):
    while not stop_event.is_set():
        response = ping_once(host)
        print(f"{host} is {'reachable' if response == 0 else 'not reachable'}.")

# Function to start pinging once
def start_pinging_once():
    target_host = host_entry.get().strip()
    if not target_host:
        messagebox.showerror("Error", "Please enter a valid domain.")
        return

    response = ping_once(target_host)
    messagebox.showinfo("Ping Result", f"{target_host} is {'reachable' if response == 0 else 'not reachable'}.")

# Function to start pinging with threads
def start_pinging_threads():
    target_host = host_entry.get().strip()
    try:
        num_threads = int(threads_entry.get().strip())
        if num_threads <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of threads.")
        return

    stop_event.clear()
    for _ in range(num_threads):
        thread = threading.Thread(target=ping_in_thread, args=(target_host, stop_event), daemon=True)
        thread.start()

# Function to stop all ping threads
def stop_pinging():
    stop_event.set()

# Create the main window
root = tk.Tk()
root.title("Ping App")
root.geometry("400x300")
root.configure(bg="black")

# Create a frame for centering
frame = tk.Frame(root, bg="black")
frame.pack(expand=True)

# Define Roboto font
font_style = ("Roboto", 12)

# Configure row/column weights for centering
for i in range(6):
    frame.grid_rowconfigure(i, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Add labels and input fields
tk.Label(frame, text="Domain:", bg="black", fg="white", font=font_style).grid(row=0, column=0, padx=10, pady=5, sticky="e")
host_entry = tk.Entry(frame, bg="#0086FF", fg="white", insertbackground="white", relief=tk.FLAT, font=font_style)
host_entry.grid(row=0, column=1, padx=10, pady=5, ipadx=10, ipady=5, sticky="ew")

tk.Label(frame, text="Threads:", bg="black", fg="white", font=font_style).grid(row=1, column=0, padx=10, pady=5, sticky="e")
threads_entry = tk.Entry(frame, bg="#0086FF", fg="white", insertbackground="white", relief=tk.FLAT, font=font_style)
threads_entry.grid(row=1, column=1, padx=10, pady=5, ipadx=10, ipady=5, sticky="ew")

# Buttons
ping_once_button = tk.Button(frame, text="Ping Once", bg="#0086FF", fg="white", relief=tk.FLAT, font=font_style, command=start_pinging_once)
ping_once_button.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

ping_threads_button = tk.Button(frame, text="Ping with Threads", bg="#0086FF", fg="white", relief=tk.FLAT, font=font_style, command=start_pinging_threads)
ping_threads_button.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

stop_threads_button = tk.Button(frame, text="Stop Ping", bg="red", fg="white", relief=tk.FLAT, font=font_style, command=stop_pinging)
stop_threads_button.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

# Stop event for stopping threads
stop_event = threading.Event()

# Run the application
root.mainloop()
