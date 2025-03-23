import serial.tools.list_ports
import os, base64, subprocess,re, sys
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
#<<<----Check is this is program is running after compiling or not------>>>
with open(sys.argv[0], 'rb') as fileCheckFormat:
    contentOfFileFormat = fileCheckFormat.read()
    try:
        contentOfFileFormat.decode('utf-8')
        compiledFile = False
    except UnicodeDecodeError:
        compiledFile = True
def openNewSession():
    if compiledFile is True:
        subprocess.Popen(sys.argv[0]) #This option will work after compilation!
    else:
        subprocess.Popen(['python', sys.argv[0]])
class ArduinoPy:
    def __init__(self, root):
        self.root = root
    filename = None
    projectpath = None
    alreadySaved = False
    compiled = False
    firstEdit = True
    silent = False
    allPorts = []
    port = None
    board = None
    boardName = None
    window_focused = True
    # Function to handle window focus events
    def on_focus(self, event):
        global window_focused
        window_focused = True
    def on_blur(self, event):
        global window_focused
        window_focused = False
    def compile_program(self):
        program_path = self.projectpath
        self.silent = True
        self.save_program()
        self.silent = False
        if self.alreadySaved:
            board = board_versions.get(self.boardName)
            if board:
                compile_command = f"arduino-cli compile --fqbn {board} {program_path}"
                print(compile_command)
                try:
                    compiledOutput = subprocess.check_output(compile_command, shell=True, universal_newlines=True)
                    self.print_to_console(compiledOutput)
                    self.compiled = True
                except subprocess.CalledProcessError as e:
                    compiledOutput = e.output
                    self.print_to_console("compilation failed!")
                    self.compiled = False
            else:
                messagebox.showerror("Invalid Board", "Select a valid board before compilation")
        else:
            messagebox.showerror("Compilation Failed", "Need to save the program before compilation.")
    def upload_program(self):
        self.compiled = False
        self.silent = True
        self.compile_program()
        self.silent = False
        if self.compiled is True:
            program_path = self.projectpath
            board = board_versions.get(self.boardName)
            if board and self.port:
                upload_command = f"arduino-cli upload -p {self.port} --fqbn {board} {program_path}"
                print(upload_command)
                try:
                    uploaded_output=subprocess.check_output(upload_command,shell=True, universal_newlines=True)
                    self.print_to_console("Uploaded successfully")
                except subprocess.CalledProcessError as e:
                    uploaded_output = e.output
                    self.print_to_console("Upload failed!")

                # messagebox.showinfo("Upload", "Program uploaded successfully.")
            else:
                messagebox.showerror("Invalid Board or Port", "Select a valid board and port before upload")
    def serialMonitor(self):
        pass
        # if self.port:
        #     command = f"arduino-cli serial -p {self.port}"
        #     def viewValues():
        #         os.Popen(command)
    def save_program(self):
        if self.window_focused:
            pass
        else:
            return
        program = self.text_widget.get("1.0", END)
        if self.alreadySaved is True:
            if os.path.exists(self.filename):
                with open(self.filename, "w") as file:
                    file.write(program)
                    file.close()
                    if self.silent is False:
                        messagebox.showinfo("Save", "Program saved successfully.")
            else:
                alreadySaved = False
                self.save_program()
        else:
            self.filename = asksaveasfilename(defaultextension=".ino", filetypes=[("Arduino Program", "*.ino")])
            if self.filename:
                if os.path.exists(self.filename):
                    with open(self.filename, "w") as file:
                        file.write(program)
                        file.close()
                        if self.silent is False:
                            messagebox.showinfo("Save", "Program saved successfully.")
                else:
                    folder_path = os.path.dirname(self.filename)
                    folder_name = os.path.splitext(os.path.basename(self.filename))[0]
                    project_directory = os.path.join(folder_path, folder_name)
                    save_command = f"arduino-cli sketch new {project_directory}"
                    os.system(save_command)
                    output_file_path = os.path.join(project_directory, f"{folder_name}.ino")
                    with open(output_file_path, "w") as file:
                        file.write(program)
                        file.close()
                    if self.silent is False:
                        messagebox.showinfo("Save", "Program saved successfully.")
                    self.filename = output_file_path
                    self.projectpath = project_directory
                    self.alreadySaved = True

    def open_project(self):
        if self.window_focused:
            pass
        else:
            return
        file_path = askopenfilename(filetypes=[("Arduino Program", "*.ino")])
        if file_path:
            with open(file_path, "r") as file:
                program = file.read()
                self.text_widget.delete("1.0", END)
                self.text_widget.insert("1.0", program)
                file.close()
            self.projectpath = os.path.dirname(file_path)
            self.filename = file_path
            self.alreadySaved = True
    def print_to_console(self, output):
        self.console_text.configure(state="normal")
        output = re.sub('\033\[\d+m', '', output)
        self.console_text.delete('1.0', END)
        self.console_text.insert(END, output)
        self.console_text.see(END)
        self.console_text.configure(state="disabled")
    def create_widget(self):
        keyboard.add_hotkey('ctrl+s', self.save_program)
        keyboard.add_hotkey('ctrl+o', self.open_project)
        self.root.bind("<FocusIn>", self.on_focus)
        self.root.bind("<FocusOut>", self.on_blur)
        self.root.title("ArduinoPy")
        self.root.geometry("800x600")
        self.root.minsize(500, 500)
        #<<--icon setup-->>
        getCahce()
        iconPhoto = PhotoImage(file='.arduinoIcon.png')
        self.root.iconphoto(False, iconPhoto)
        cleanCache()
       # <<<---Header frame--->>>
        headFrame = Frame(self.root)
        newButton = Button(headFrame, text="New", command=openNewSession).grid(row=0, column=0)
        openButton = Button(headFrame, text="Open", command=self.open_project)
        openButton.grid(row=0, column=1)
        compileButton = Button(headFrame, text="Compile", command=self.compile_program)
        compileButton.grid(row=0, column=2)
        uploadButton = Button(headFrame, text="Upload", command=self.upload_program)
        uploadButton.grid(row=0, column=3)
        saveButton = Button(headFrame, text="Save", command=self.save_program)
        saveButton.grid(row=0, column=4)
        # <<<---Port selection--->>>
        def onSelectPort(event):
            self.selected_port = dropdownForPort.get()
            self.port = self.selected_port
        self.selected_port = StringVar()
        self.selected_port.set("Select Port")
        dropdownForPort = ttk.Combobox(headFrame, textvariable=self.selected_port)
        dropdownForPort['value'] = self.allPorts
        dropdownForPort.grid(row=0, column=5)
        dropdownForPort.bind("<<ComboboxSelected>>", onSelectPort)
        def update_ports():
            ports = serial.tools.list_ports.comports()
            self.all_ports = [port.device for port in ports]
            dropdownForPort['value'] = self.all_ports
            self.root.after(1000, update_ports)
        update_ports()
        headFrame.grid(row=0, column=0)
        def onSelectBoard(event):
            self.selected_board = dropdownForBoard.get()
            self.boardName = self.selected_board
        self.selected_board = StringVar()
        self.selected_board.set("Select Board Type")
        dropdownForBoard = ttk.Combobox(headFrame, textvariable=self.selected_board)
        dropdownForBoard['value'] = boardTypes
        dropdownForBoard.grid(row=0, column=6)
        dropdownForBoard.bind("<<ComboboxSelected>>", onSelectBoard)
        serialButton = Button(headFrame, text="Serial Monitor", command=self.serialMonitor).grid(row=0, column=7)
        headFrame.grid(row=0, column=0)
        #<<<----Coding area---->>>
        self.text_widget = Text(self.root)
        self.text_widget.grid(row=1, column=0, sticky="nsew")
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        if self.firstEdit is True:
            self.text_widget.insert("1.0", defaultWidget)
            self.firstEdit = False
        #<<<----Autoclose brackets---->>>
        def on_key_release(event):
            opening_brackets = "{[("
            closing_brackets = "}])"
            if event.char and event.char in opening_brackets:
                closing_bracket = get_closing_bracket(event.char, opening_brackets, closing_brackets)
                self.text_widget.insert("insert", closing_bracket)
        def get_closing_bracket(opening_bracket, opening_brackets, closing_brackets):
            index = opening_brackets.index(opening_bracket)
            return closing_brackets[index]
        self.root.bind("<KeyRelease>", on_key_release)
        # Create a text widget for the console screen
        self.console_text = Text(self.root, height=8)
        self.console_text.grid(row=2, column=0, sticky="nsew")
        self.root.rowconfigure(2, weight=0)
        self.root.after(1000, update_ports)
if __name__ == "__main__":
    root = Tk()
    myObj = ArduinoPy(root)
    myObj.create_widget()
    root.mainloop()
