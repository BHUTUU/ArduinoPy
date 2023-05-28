import serial,os, base64, random, string
from tkinter import messagebox
from tkinter import *
from time import sleep as delay
import bhutuuImage as ImageRequired
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
def loadInternalVariables():
    CWD = os.getcwd()
    programDir = 'C:/Program Files/ArduinoPyBhutuu'
    if not os.path.exists(programDir):
        print("Compiler not find")
def generate_output_filename():
    while True:
        random_number = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        output_filename = f"sketch_{random_number}"
        if not os.path.exists(output_filename):
            return output_filename
currenProjectName = generate_output_filename()
newFileName = ""
#code to start the project......
os.system("arduino-cli sketch new "+ currenProjectName)

#.............................
def saveFile():
    saveRoot = Tk()
    saveRoot.title("Save Project")
    getCahce()
    iconPhoto = PhotoImage(file='.arduinoIcon.png')
    saveRoot.iconphoto(False, iconPhoto)
    cleanCache()
    fileNameEnterd = StringVar()
    def on_closing():
        global newFileName
        if newFileName:
            fileNameEnterd.set(newFileName)
        saveRoot.destroy()
    enteryLabel = Label(saveRoot, text="Enter Project name: ").grid(row=0, column=0)
    enterName = Entry(saveRoot,textvariable=fileNameEnterd).grid(row=0, column=1)
    saveButton = Button(saveRoot,text="Save").grid(row=2, column=2)
    cancel = Button(saveRoot,text="Cancel").grid(row=2, column=3)
    saveRoot.protocol("WM_DELETE_WINDOW", on_closing)
    saveRoot.mainloop()
    global newFileName
    newFileName = fileNameEnterd.get()
    if newFileName:
        if os.path.exists(currenProjectName):
            os.rename(currenProjectName, newFileName)
            print(os.path.isfile(currenProjectName+"/"+currenProjectName+".ino"))
            # if os.path.exists(currenProjectName+"/"+currenProjectName+".ino"):
            #     os.rename(currenProjectName+"/"+currenProjectName+".ino", currenProjectName+"/"+newFileName)+".ino"
        else:
            messagebox.showerror("Save error!","Unable to save! copy this code into your favorite text editor in order to save it.")
#save the file with new name of rename
def mainWindow():
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
    saveButton = Button(headFrame, text="Save").grid(row=0, column=2)
    headFrame.grid(row=0, column=0)
    text_widget = Text(winroot)
    text_widget.grid(row=1, column=0, sticky="nsew")
    winroot.rowconfigure(1, weight=1)
    winroot.columnconfigure(0, weight=1)
    def autosave(fileName):
        content = text_widget.get("1.0", "end-1c")
        try:
            with open(fileName, "w") as file:
                file.write(content)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    # def on_closing():
    #     if messagebox.askokcancel("Save", "Do you want to quit?"):
    #         autosave()
    #         output_filename = generate_output_filename()
    #         messagebox.showinfo("Output File", f"The output file is: {output_filename}")
    #         winroot.destroy()
        # else:
        #     winroot.destroy()
    # winroot.protocol("WM_DELETE_WINDOW", on_closing)
    # winroot.after(30000, autosave)

    winroot.mainloop()
# mainWindow()
saveFile()