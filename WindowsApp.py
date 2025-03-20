import subprocess
import threading
import tkinter as tk
import multiprocessing

multiprocessing.freeze_support()

# Function to ping once
def ping_once(host):
    param = '-n'
    ping_exe = r"C:\Windows\System32\ping.exe"
    command = [ping_exe, param, "1", host]

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        response = subprocess.run(command, stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL, shell=False, startupinfo=startupinfo)
        return response.returncode == 0
    except Exception:
        return False

# Function to start a single ping
def start_pinging_once():
    global command_count
    target_host = host_entry.get().strip()
    if not target_host:
        status_label.config(text="Error: Enter a valid domain.", fg="red")
        return

    response = ping_once(target_host)
    command_count += 1
    status_label.config(text=f"{target_host} is {'reachable' if response else 'not reachable'} | Commands: {command_count}", fg="white")

# Function to continuously ping in a thread
def ping_worker(host, stop_event):
    global command_count
    param = '-n'
    ping_exe = r"C:\Windows\System32\ping.exe"
    command = [ping_exe, param, "1", host]

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    while not stop_event.is_set():
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=startupinfo)
        process.wait()  
        command_count += 1
        status_label.config(text=f"{host} is {'reachable' if process.returncode == 0 else 'not reachable'} | Commands: {command_count}", fg="white")

# Function to start multiple pinging threads
def start_pinging_threads():
    target_host = host_entry.get().strip()
    try:
        num_threads = int(threads_entry.get().strip())
        if num_threads <= 0:
            raise ValueError
    except ValueError:
        status_label.config(text="Error: Enter a valid number of threads.", fg="red")
        return

    stop_event.clear()
    for _ in range(num_threads):
        thread = threading.Thread(target=ping_worker, args=(target_host, stop_event), daemon=True)
        thread.start()

# Function to stop all ping threads
def stop_pinging():
    stop_event.set()
    status_label.config(text="Ping stopped.", fg="yellow")

# PyInstaller-friendly main function
def main():
    global root, host_entry, threads_entry, stop_event, status_label, command_count
    command_count = 0

    root = tk.Tk()
    root.title("Ping App")
    root.geometry("400x300")
    root.configure(bg="black")

    frame = tk.Frame(root, bg="black")
    frame.pack(expand=True)

    font_style = ("Roboto", 12)

    tk.Label(frame, text="Domain:", bg="black", fg="white", font=font_style).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    host_entry = tk.Entry(frame, bg="#0086FF", fg="white", insertbackground="white", relief=tk.FLAT, font=font_style)
    host_entry.grid(row=0, column=1, padx=10, pady=5, ipadx=10, ipady=5, sticky="ew")

    tk.Label(frame, text="Threads:", bg="black", fg="white", font=font_style).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    threads_entry = tk.Entry(frame, bg="#0086FF", fg="white", insertbackground="white", relief=tk.FLAT, font=font_style)
    threads_entry.grid(row=1, column=1, padx=10, pady=5, ipadx=10, ipady=5, sticky="ew")

    ping_once_button = tk.Button(frame, text="Ping Once", bg="#0086FF", fg="white", relief=tk.FLAT, font=font_style, command=start_pinging_once)
    ping_once_button.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

    ping_threads_button = tk.Button(frame, text="Ping With Thread", bg="#0086FF", fg="white", relief=tk.FLAT, font=font_style, command=start_pinging_threads)
    ping_threads_button.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

    stop_threads_button = tk.Button(frame, text="Stop Ping", bg="red", fg="white", relief=tk.FLAT, font=font_style, command=stop_pinging)
    stop_threads_button.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

    status_label = tk.Label(frame, text="Status: Waiting for input", bg="black", fg="white", font=font_style)
    status_label.grid(row=5, column=0, columnspan=2, pady=10)

    stop_event = threading.Event()
    root.mainloop()

if __name__ == "__main__":
    main()
