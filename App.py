#!/usr/bin/env python

import tkinter
import Macros

class App:
    def __init__(self) -> None:
        self.__console = tkinter.Tk(className="Image Editor")
        self.__header = tkinter.Frame(self.__console)
        self.__header.pack()
        
        tkinter.Label(self.__header, text="").grid(row=0, column=0, columnspan=1)
        tkinter.Label(self.__header, text="Photo Editor", font=(12,)).grid(row=1, column=1, columnspan=3)
        
        tkinter.Button(self.__console, text="Open Image").pack(pady=Macros.BUTTON_PADY)
        tkinter.Button(self.__console, text="Crop Image").pack(pady=Macros.BUTTON_PADY)
        tkinter.Button(self.__console, text="Add Text").pack(pady=Macros.BUTTON_PADY)
        tkinter.Button(self.__console, text="Apply Filters").pack(pady=Macros.BUTTON_PADY)
        tkinter.Button(self.__console, text="Blur Image").pack(pady=Macros.BUTTON_PADY)
        tkinter.Button(self.__console, text="Rotate Left").pack(pady=Macros.BUTTON_PADY)
        tkinter.Button(self.__console, text="rotate Right").pack(pady=Macros.BUTTON_PADY)
        tkinter.Button(self.__console, text="Flip Horizontal").pack(pady=Macros.BUTTON_PADY)
        tkinter.Button(self.__console, text="Flip Vertical").pack(pady=Macros.BUTTON_PADY)
        
        

    def run(self):
        self.__console.mainloop()


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
