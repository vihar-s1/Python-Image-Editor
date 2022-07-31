#!/usr/bin/env python

import tkinter

import Macros


class AppFrame:
    def __init__(self) -> None:
        self._window = tkinter.Tk(className="Python Image Editor")
        self._header = tkinter.Frame(
            self._window, bg=Macros.APP_BG, padx=Macros.PADX, pady=Macros.PADY)
        self._header.pack()
        self.Buttons = {}
        
        tkinter.Label(self._header, text="Python Image Editor", font=('Agency FB', 26, 'bold','italic'),
                      bg=Macros.APP_BG, fg=Macros.BRIGHT_GREEN).grid(row=0, column=2)

        tkinter.Label(self._header, text="", bg=Macros.APP_BG).grid(row=1, column=2)
        
        self.Buttons['Save'] = tkinter.Button(self._header, text="Save",
                       font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG)
        self.Buttons['Save'].grid(row=2, column=0)
        
        self.Buttons['Save As'] = tkinter.Button(self._header, text="Save As",
                       font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG)
        self.Buttons['Save As'].grid(row=2, column=1)
        
        self.Buttons['Reset Image'] = tkinter.Button(self._header, text="Reset Image",
                       font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG)
        self.Buttons['Reset Image'].grid(row=2, column=2)
        
        self.Buttons['Apply Changes'] = tkinter.Button(self._header, text="Apply Changes",
                       font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG)
        self.Buttons['Apply Changes'].grid(row=2, column=3)
        
        self.Buttons['Exit'] = tkinter.Button(self._header, text="Exit",
                        font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,fg=Macros.BUTTON_FG, command=self._window.quit)
        self.Buttons['Exit'].grid(row=2, column=4)

        self._app_frame = tkinter.Frame(self._window, bg=Macros.APP_BG)
        self._app_frame.pack()

        self.Buttons['Open Image'] = tkinter.Button(self._app_frame, text="Open Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                                                    fg=Macros.BUTTON_FG)
        self.Buttons['Open Image'].grid(row=0, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        self.Buttons['Crop Image'] = tkinter.Button(self._app_frame, text="Crop Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                                                    fg=Macros.BUTTON_FG)
        self.Buttons['Crop Image'].grid(row=1, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        self.Buttons['Add Text'] = tkinter.Button(self._app_frame, text="Add Text", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                                                  fg=Macros.BUTTON_FG)
        self.Buttons['Add Text'].grid(row=2, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        self.Buttons['Draw'] = tkinter.Button(self._app_frame, text="Draw", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                                              fg=Macros.BUTTON_FG)
        self.Buttons['Draw'].grid(row=3, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        self.Buttons['Apply Filters'] = tkinter.Button(self._app_frame, text="Apply Filters", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                                                       fg=Macros.BUTTON_FG)
        self.Buttons['Apply Filters'].grid(row=4, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        self.Buttons['Blur Image'] = tkinter.Button(self._app_frame, text="Blur Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                                                    fg=Macros.BUTTON_FG)
        self.Buttons['Blur Image'].grid(row=5, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        self.Buttons['Rotate Image'] = tkinter.Button(self._app_frame, text="Rotate Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                                                      fg=Macros.BUTTON_FG)
        self.Buttons['Rotate Image'].grid(row=6, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        self.Buttons['Flip Image'] = tkinter.Button(self._app_frame, text="Flip Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                                                    fg=Macros.BUTTON_FG)
        self.Buttons['Flip Image'].grid(row=7, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        

        self._canvas = tkinter.Canvas(
            self._app_frame, height=Macros.CANVAS_HEIGHT, width=Macros.CANVAS_WIDTH, background="grey")
        self._canvas.grid(row=0, column=2, rowspan=10)
        
        
        self._side_frame = tkinter.Frame(self._app_frame)
        self._side_frame.grid(row=0, column=4)
        self._side_frame.config(padx=50, pady=15, bg=Macros.APP_BG)
        
        tkinter.Label(self._side_frame, text="", bg=Macros.APP_BG).grid(row=0, column=0)

    def run(self):
        self._window.mainloop()


def main():
    app = AppFrame()
    app.run()


if __name__ == "__main__":
    main()
