import serial.tools.list_ports
import os, base64, subprocess,re
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import *
from tkinter import ttk
import bhutuuImage as ImageRequired
import threading, keyboard
#<<<---cahce management--->>>
def cleanCache():
    for i in ['.bhutuuIcon.png', '.arduinoIcon.png', '.arduinoImage.png']:
        if os.path.exists(i):
            os.remove(i)
cleanCache() # clean cache if found by any chance!
def getCahce():
    bytes_data1 = base64.b64decode(ImageRequired.bhutuuImageBytes)
    bytes_data2 = base64.b64decode(ImageRequired.arduinoIconBytes)
    bytes_data3 = base64.b64decode(ImageRequired.arduinoImageBytes)
    bhutuuImageFile = open('.bhutuuIcon.png', 'wb')
    arduinoIconFile = open('.arduinoIcon.png', 'wb')
    arduinoImageFile = open('.arduinoImage.png', 'wb')
    bhutuuImageFile.write(bytes_data1)
    arduinoIconFile.write(bytes_data2)
    arduinoImageFile.write(bytes_data3)
    bhutuuImageFile.close()
    arduinoIconFile.close()
    arduinoImageFile.close()
#<<<--- Internal variables--->>>
filename = None
projectpath = None
alreadySaved = False
compiled = False
firstEdit = True
silent = False
port = None
board = None
boardName = None
board_versions = {
    "Arduino Uno": "arduino:avr:uno",
    "Arduino Nano": "arduino:avr:nano",
    "Arduino Mega": "arduino:avr:mega",
    "Arduino Leonardo": "arduino:avr:leonardo",
    "Arduino Due": "arduino:sam:arduino_due_x",
    "Arduino Zero": "arduino:samd:arduino_zero_native",
    "Arduino MKR1000": "arduino:samd:mkr1000",
    "Arduino Nano 33 IoT": "arduino:mbed:nano33ble",
    "Arduino Nano 33 BLE": "arduino:mbed:nano33ble",
    "Arduino Nano Every": "arduino:avr:nano:cpu=atmega4809",
    "Arduino Pro Mini": "arduino:avr:pro:cpu=8MHzatmega328",
    "Arduino Yun": "arduino:avr:yun",
    "Arduino Esplora": "arduino:avr:esplora",
    "Arduino Robot": "arduino:avr:robot",
    "NodeMCU v1.0 (ESP-12E Module)": "esp8266:esp8266:nodemcuv2",
    "ESP32 Dev Module": "esp32:esp32:esp32",
    "ESP8266 Generic Module": "esp8266:esp8266:generic",
    "ESP8266 NodeMCU 1.0 (ESP-12E Module)": "esp8266:esp8266:nodemcuv2",
    "ESP8266 NodeMCU 0.9 (ESP-12 Module)": "esp8266:esp8266:nodemcu",
    "ESP8266 NodeMCU 2.0 (ESP-12E Module)": "esp8266:esp8266:nodemcuv2",
    "Wemos D1 R1": "esp8266:esp8266:d1",
    "Wemos D1 R2 & mini": "esp8266:esp8266:d1_mini",
    "Wemos D1 R32": "esp32:esp32:d1_mini32",
    "LOLIN(WEMOS) D1 mini Pro": "esp8266:esp8266:d1_mini_pro",
    "ESP32 Feather": "esp32:esp32:featheresp32",
    "ESP8266 Feather": "esp8266:esp8266:feather"
}
boardTypes = tuple(board_versions.keys())
defaultWidget = """
void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
"""
window_focused = True
# Function to handle window focus events
def on_focus(event):
    global window_focused
    window_focused = True

def on_blur(event):
    global window_focused
    window_focused = False
#...............Functions------------------->>>
def compile_program():
    global alreadySaved
    global projectpath
    global compiled
    global board
    program_path = projectpath
    silent = True
    save_program()
    silent = False
    if alreadySaved:
        board = board_versions.get(boardName)
        if board:
            compile_command = f"arduino-cli compile --fqbn {board} {program_path}"
            print(compile_command)
            compiledOutput = subprocess.check_output(compile_command, shell=True, universal_newlines=True)
            print_to_console(compiledOutput)
            # returnValue = os.system(compile_command)
            # if returnValue == 0:
            #     compiled = True
            # if silent == False:
            #     messagebox.showinfo("Compilation", "Program compiled successfully.")
        else:
            messagebox.showerror("Invalid Board", "Select a valid board before compilation")
    else:
        messagebox.showerror("Compilation Failed", "Need to savet the program before compilation.")
def upload_program():
    global silent
    global compiled
    global board
    global port
    compiled = False
    silent = True
    compile_program()
    silent = False
    if compiled is True:
        global projectpath
        program_path = projectpath
        board = board_versions.get(boardName)
        if board and port:
            upload_command = f"arduino-cli upload -p {port} --fqbn {board} {program_path}"
            print(upload_command)
            uploaded_output=subprocess.check_output(upload_command,shell=True, universal_newlines=True)
            print_to_console(uploaded_output)
            # messagebox.showinfo("Upload", "Program uploaded successfully.")
        else:
            messagebox.showerror("Invalid Board or Port", "Select a valid board and port before upload")
def save_program():
    global window_focused
    if window_focused:
        pass
    else:
        return
    global silent
    global projectpath
    global filename
    global alreadySaved
    program = text_widget.get("1.0", END)
    if alreadySaved is True:
        if os.path.exists(filename):
            with open(filename, "w") as file:
                file.write(program)
                file.close()
                if silent is False:
                    messagebox.showinfo("Save", "Program saved successfully.")
        else:
            alreadySaved = False
            save_program()
    else:
        filename = asksaveasfilename(defaultextension=".ino", filetypes=[("Arduino Program", "*.ino")])
        if filename:
            if os.path.exists(filename):
                with open(filename, "w") as file:
                    file.write(program)
                    file.close()
                    if silent is False:
                        messagebox.showinfo("Save", "Program saved successfully.")
            else:
                folder_path = os.path.dirname(filename)
                folder_name = os.path.splitext(os.path.basename(filename))[0]
                project_directory = os.path.join(folder_path, folder_name)
                save_command = f"arduino-cli sketch new {project_directory}"
                os.system(save_command)
                
                output_file_path = os.path.join(project_directory, f"{folder_name}.ino")
                
                with open(output_file_path, "w") as file:
                    file.write(program)
                    file.close()
                if silent is False:
                    messagebox.showinfo("Save", "Program saved successfully.")
                filename = output_file_path
                projectpath = project_directory
                alreadySaved = True
def open_project():
    global window_focused
    if window_focused:
        pass
    else:
        return
    global projectpath
    global filename
    global alreadySaved
    file_path = askopenfilename(filetypes=[("Arduino Program", "*.ino")])
    if file_path:
        with open(file_path, "r") as file:
            program = file.read()
            text_widget.delete("1.0", END)
            text_widget.insert("1.0", program)
            file.close()
        projectpath = os.path.dirname(file_path)
        filename = file_path
        alreadySaved = True
def print_to_console(output):
    console_text.configure(state="normal")
    output = re.sub('\033\[\d+m', '', output)
    console_text.delete('1.0', END)
    console_text.insert(END, output)
    console_text.see(END)
    console_text.configure(state="disabled")
keyboard.add_hotkey('ctrl+s', save_program)
keyboard.add_hotkey('ctrl+o', open_project)
#<<<<<----------gui section-------------->>>>>
winroot = Tk()
winroot.bind("<FocusIn>", on_focus)
winroot.bind("<FocusOut>", on_blur)
winroot.title("ArduinoPyBhutuu")
winroot.geometry("800x600")
winroot.minsize(500, 500)
#<<--icon setup-->>
getCahce()
iconPhoto = PhotoImage(file='.arduinoIcon.png')
winroot.iconphoto(False, iconPhoto)
cleanCache()
#<<---header frame--->>
headFrame = Frame(winroot)
openButton = Button(headFrame, text="Open", command=open_project).grid(row=0, column=0)
compileButton = Button(headFrame, text="Compile", command=compile_program).grid(row=0, column=1)
uploadButton = Button(headFrame, text="Upload", command=upload_program).grid(row=0, column=2)
saveButton = Button(headFrame, text="Save", command=save_program).grid(row=0, column=3)
#<<--port selection-->>
def onSelectPort(event):
    global port
    selected_port = dropdownForPort.get()
    port = selected_port
selected_port = StringVar()
selected_port.set("Select Port")
allPorts = []
dropdownForPort = ttk.Combobox(headFrame, textvariable=selected_port)
dropdownForPort['value'] = allPorts
dropdownForPort.grid(row=0, column=3)
dropdownForPort.bind("<<ComboboxSelected>>", onSelectPort)
def update_ports():
    ports = serial.tools.list_ports.comports()
    all_ports = [port.device for port in ports]
    dropdownForPort['value'] = all_ports
    winroot.after(1000, update_ports)
update_ports()
#<<<---board selection--->>>
def onSelectBoard(event):
    global boardName
    selected_board = dropdownForBoard.get()
    boardName = selected_board
selected_board = StringVar()
selected_board.set("Select Board Type")
dropdownForBoard = ttk.Combobox(headFrame, textvariable=selected_board)
dropdownForBoard['value'] = boardTypes
dropdownForBoard.grid(row=0, column=4)
dropdownForBoard.bind("<<ComboboxSelected>>", onSelectBoard)
headFrame.grid(row=0, column=0)
text_widget = Text(winroot)
text_widget.grid(row=1, column=0, sticky="nsew")
winroot.rowconfigure(1, weight=1)
winroot.columnconfigure(0, weight=1)
if firstEdit is True:
    text_widget.insert("1.0", defaultWidget)
    firstEdit = False
#<<--Autoclose brackets-->>
def on_key_release(event):
    opening_brackets = "{[("
    closing_brackets = "}])"
    if event.char and event.char in opening_brackets:
        closing_bracket = get_closing_bracket(event.char, opening_brackets, closing_brackets)
        text_widget.insert("insert", closing_bracket)
def get_closing_bracket(opening_bracket, opening_brackets, closing_brackets):
    index = opening_brackets.index(opening_bracket)
    return closing_brackets[index]
winroot.bind("<KeyRelease>", on_key_release)
# Create a text widget for the console screen
console_text = Text(winroot, height=8)
console_text.grid(row=2, column=0, sticky="nsew")
winroot.rowconfigure(2, weight=0)
winroot.after(1000, update_ports)
winroot.mainloop()