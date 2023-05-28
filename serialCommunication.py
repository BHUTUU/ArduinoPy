import serial,os, base64, random, string,sys, datetime
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from tkinter import *
from time import sleep as delay
import bhutuuImage as ImageRequired
import threading
#<<<----Argunmentation checkpost----->>>
# try:
#     fileTOWrite = sys.argv[1]
#     try:
#         fileSize = os.path.getsize(fileTOWrite)
#     except OSError as e:
#         fileSize = 0
# except:
#     fileTOWrite = None
#     fileSize = 0
# if fileTOWrite is not None:
#     if fileTOWrite.endswith('.ino'):
#         pass
#     else:
#         messagebox.showerror("Invalid file", "Invalid input file format! only '.ino' files are allowed")
#         exit(1)
# print(fileSize)
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
month = datetime.datetime.now().strftime("%B").lower()
date = str(datetime.datetime.now().strftime("%d"))
CWD = os.getcwd()
# programDir = 'C:/Program Files/ArduinoPyBhutuu'
# if not os.path.exists(programDir):
#     print("Compiler not find")
# def generate_output_filename():
#     while True:
#         random_number = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
#         output_filename = f"sketch_{random_number}"
#         if not os.path.exists(output_filename):
#             return output_filename
# tempProjectDir = generate_output_filename()
# commandForTempProject = f"arduino-cli sketch new {tempProjectDir}"
# os.system(commandForTempProject)
# realpathOfTempProject = os.path.realpath(tempProjectDir)
# filename = os.path.join(realpathOfTempProject, tempProjectDir+'.ino')
filename = None
alreadySaved = False
compiled = False
firstEdit = True
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
    global filename
    program_path = filename
    # compile_command = f"arduino-cli compile --fqbn {board} {program_path}"
    # print(compile_command)
    # os.system(compile_command)
    compiled = True
    messagebox.showinfo("Compilation", "Program compiled successfully.")

def upload_program():
    global filename
    program_path = filename
    # upload_command = f"arduino-cli upload -p {port} --fqbn {board} {program_path}"
    # print(upload_command)
    # os.system(upload_command)
    messagebox.showinfo("Upload", "Program uploaded successfully.")

def save_program():
    global filename
    global alreadySaved
    program = text_widget.get("1.0", END)
    if alreadySaved is True:
        if os.path.exists(filename):
            with open(filename, "w") as file:
                file.write(program)
                file.close()
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
                messagebox.showinfo("Save", "Program saved successfully.")
                filename = output_file_path
                alreadySaved = True

    #code to start the project......
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
compileButton = Button(headFrame, text="Compile").grid(row=0, column=0)
uploadButton = Button(headFrame, text="Upload").grid(row=0, column=1)
saveButton = Button(headFrame, text="Save", command=save_program).grid(row=0, column=2)
headFrame.grid(row=0, column=0)
text_widget = Text(winroot)
text_widget.grid(row=1, column=0, sticky="nsew")
winroot.rowconfigure(1, weight=1)
winroot.columnconfigure(0, weight=1)
if firstEdit is True:
    text_widget.insert("1.0", defaultWidget)
    firstEdit = False
winroot.mainloop()