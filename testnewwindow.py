from tkinter import Tk, Text, Button, Toplevel
class TextEditor:
    def create_text_editor(root):
        editor = Text(root)
        editor.pack()
        new_button = Button(root, text="New", command=TextEditor.open_new_editor)
        new_button.pack()

    def open_new_editor():
        new_window = Toplevel()
        TextEditor.create_text_editor(new_window)

def main():
    root = Tk()
    TextEditor.create_text_editor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
