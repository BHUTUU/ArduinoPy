from tkinter import Tk, Text, INSERT, END

def on_key_release(event):
    if event.char in "{[(":
        closing_bracket = get_closing_bracket(event.char)
        st.insert(INSERT, closing_bracket)
        st.insert(INSERT, "|")

def get_closing_bracket(opening_bracket):
    if opening_bracket == "(":
        return ")"
    elif opening_bracket == "[":
        return "]"
    elif opening_bracket == "{":
        return "}"

root = Tk()
st = Text(root)
st.bind("<KeyRelease>", on_key_release)
st.pack()
root.mainloop()
