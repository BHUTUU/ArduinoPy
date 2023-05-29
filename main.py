import serial.tools.list_ports
import os, base64
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
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
# month = datetime.datetime.now().strftime("%B").lower()
# date = str(datetime.datetime.now().strftime("%d"))
# CWD = os.getcwd()
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
#.............................

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
            returnValue = os.system(compile_command)
            if returnValue == 0:
                compiled = True
            if silent == False:
                messagebox.showinfo("Compilation", "Program compiled successfully.")
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
            os.system(upload_command)
            messagebox.showinfo("Upload", "Program uploaded successfully.")
        else:
            messagebox.showerror("Invalid Board or Port", "Select a valid board and port before upload")

def save_program():
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

    #code to start the project......
keyboard.add_hotkey('ctrl+s', save_program)
winroot = Tk()
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
compileButton = Button(headFrame, text="Compile", command=compile_program).grid(row=0, column=0)
uploadButton = Button(headFrame, text="Upload", command=upload_program).grid(row=0, column=1)
saveButton = Button(headFrame, text="Save", command=save_program).grid(row=0, column=2)
#<<--port selection-->>
def onSelectPort(event):
    global port
    selected_port = dropdownForPort.get()
    port = selected_port
selected_port = StringVar()
selected_port.set("Select Port")
allPorts = []
dropdownForPort = ttk.Combobox(headFrame, textvariable=selected_port)
ports = serial.tools.list_ports.comports()
for port in ports:
        allPorts.append(port.device) 
dropdownForPort['value'] = tuple(allPorts)
dropdownForPort.grid(row=0, column=3)
dropdownForPort.bind("<<ComboboxSelected>>", onSelectPort)
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
winroot.mainloop()