import tkinter as tk
import subprocess

def read_serial():
    process = subprocess.Popen(['arduino-cli', 'monitor', '-p', 'COM15'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Add code to read and process the serial monitor output here
    (out, err) = process.communicate()
    return out.decode().split('\n')

def read_output():
    # Add code to read and process the serial monitor output here
    cal = read_serial()
    print(cal)

    root.after(100, read_output)

root = tk.Tk()

read_serial_button = tk.Button(root, text="Read Serial", command=read_output)
read_serial_button.pack()

root.after(0, read_output)

root.mainloop()
