"""Has some of widgets which I wanted
"""
from tkinter import Entry, Label, END

class Form:
    def __init__(self, master, text= "", entryText= "", width= 200) -> None:
        def deleter(event) -> None:
            if self.__entry["fg"] == "grey" and self.__entry.get() == entryText:
                self.__entry.delete(0, END)
                self.__entry.configure(fg= "black")
            else:
                return
        def setter(event) -> None:
            if self.__entry.get() == "":
                self.__entry.insert(0, entryText)
                self.__entry.configure(fg= "grey")
        self.__master = master
        self.__text = text
        self.__entryText = entryText
        self.__width = width
        self.__entry = Entry(master, fg= "grey")
        self.__entry.bind("<FocusIn>", deleter)
        self.__entry.bind("<FocusOut>", setter)
        self.__master.bind("<Button-1>", lambda event: event.widget.focus_set())
        self.__entry.insert(0, entryText)
        self.__label = Label(master, text= text + " :")
    def place(self, x= 0, y= 0, anchor= None) -> None:
        self.__label.place(x= x, y= y, anchor= anchor)
        self.__entry.place(x= x + 50, y= y, anchor= anchor, width= self.__width)
    def get(self) -> str:
        return self.__entry.get()

if __name__ == "__main__":
    from tkinter import Tk
    root = Tk()
    a = Form(root, text= "This is a form", entryText= "Guide text")
    a.place(x= 100, y= 100)
    root.mainloop()