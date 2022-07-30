#!/usr/bin/env python

import tkinter
from tkinter import PhotoImage
from tkinter.font import Font
from PIL import Image

import Macros


class App:
    def __init__(self) -> None:
        self.__window = tkinter.Tk(className="Python Image Editor")
        self.__header = tkinter.Frame(
            self.__window, bg=Macros.APP_BG, padx=Macros.PADX, pady=Macros.PADY)
        self.__header.pack()

        
        tkinter.Label(self.__header, text="Python Image Editor", font=('Agency FB', 22, 'bold','italic'),
                      bg=Macros.APP_BG, fg=Macros.BRIGHT_GREEN, pady=Macros.PADY).grid(row=1, column=2)

        tkinter.Button(self.__header, text="Save",
                       font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG).grid(row=2, column=0)
        tkinter.Button(self.__header, text="Save As",
                       font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG).grid(row=2, column=1)
        tkinter.Button(self.__header, text="Reset Image",
                       font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG).grid(row=2, column=2)
        tkinter.Button(self.__header, text="Apply Changes",
                       font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG).grid(row=2, column=3)
        tkinter.Button(self.__header, text="Exit",
                        font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG, command=self.__window.quit).grid(row=2, column=4)

        self.__app_frame = tkinter.Frame(self.__window, bg=Macros.APP_BG)
        self.__app_frame.pack()

        tkinter.Button(self.__app_frame, text="Open Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG).grid(
            row=0, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        tkinter.Button(self.__app_frame, text="Crop Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG).grid(
            row=1, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        tkinter.Button(self.__app_frame, text="Add Text", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG).grid(
            row=2, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        tkinter.Button(self.__app_frame, text="Draw", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG).grid(
            row=3, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        tkinter.Button(self.__app_frame, text="Apply Filters", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG).grid(
            row=4, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        tkinter.Button(self.__app_frame, text="Blur Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG).grid(
            row=5, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        tkinter.Button(self.__app_frame, text="Rotate", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG).grid(
            row=6, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        tkinter.Button(self.__app_frame, text="Flip", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG).grid(
            row=7, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )

        self.__canvas = tkinter.Canvas(
            self.__app_frame, height=600, width=1000, background="grey")
        self.__canvas.grid(row=0, column=2, rowspan=10)

    def run(self):
        self.__window.mainloop()


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
