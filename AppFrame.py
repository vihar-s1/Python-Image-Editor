#!/usr/bin/env python

import tkinter
from tkinter import filedialog
from PIL import Image
from PIL.ImageTk import PhotoImage

import Macros


class AppFrame:
    def __init__(self) -> None:
        self._window = tkinter.Tk(className="Python Image Editor")
        self._header = tkinter.Frame(
            self._window, bg=Macros.APP_BG, padx=Macros.PADX, pady=Macros.PADY)
        self._header.pack()
        self.Buttons = {}

        self.__defineIcons()
        
        tkinter.Label(self._header, text="Python Image Editor", font=('Agency FB', 26, 'bold', 'italic'),
                      bg=Macros.APP_BG, fg=Macros.BRIGHT_GREEN).grid(row=0, column=2)

        tkinter.Label(self._header, text="",
                      bg=Macros.APP_BG).grid(row=1, column=2)

        self.Buttons['Save'] = tkinter.Button(self._header, text="Save",
                                              font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG)
        self.Buttons['Save'].grid(row=2, column=0)

        self.Buttons['Save As'] = tkinter.Button(self._header, text="Save As",
                                                 font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG)
        self.Buttons['Save As'].grid(row=2, column=1)

        self.Buttons['Reset Image'] = tkinter.Button(self._header, text="Reset Image",
                                                     font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG)
        self.Buttons['Reset Image'].grid(row=2, column=2)

        self.Buttons['Apply Changes'] = tkinter.Button(self._header, text="Apply Changes",
                                                       font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG)
        self.Buttons['Apply Changes'].grid(row=2, column=3)

        tkinter.Button(self._header, text="Exit", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                       fg=Macros.BUTTON_FG, command=self._window.quit).grid(row=2, column=4)

        self._app_frame = tkinter.Frame(self._window, bg=Macros.APP_BG)
        self._app_frame.pack()

        tkinter.Button(self._app_frame, text="Open Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                       fg=Macros.BUTTON_FG, command=self.__upload_image
                       ).grid(row=0, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        self.Buttons['Crop Image'] = tkinter.Button(self._app_frame, text="Crop Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                                                    fg=Macros.BUTTON_FG)
        self.Buttons['Crop Image'].grid(
            row=1, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        self.Buttons['Add Text'] = tkinter.Button(self._app_frame, text="Add Text", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                                                  fg=Macros.BUTTON_FG)
        self.Buttons['Add Text'].grid(
            row=2, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        self.Buttons['Draw'] = tkinter.Button(self._app_frame, text="Draw", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                                              fg=Macros.BUTTON_FG)
        self.Buttons['Draw'].grid(row=3, column=0, columnspan=2,
                                  padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(self._app_frame, text="Apply Filters", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, 
                       fg=Macros.BUTTON_FG, command=self.__filters).grid( row=4, column=0, columnspan=2, 
                                                                          padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        self.Buttons['Blur Image'] = tkinter.Button(self._app_frame, text="Blur Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                                                    fg=Macros.BUTTON_FG)
        self.Buttons['Blur Image'].grid(
            row=5, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        
        self.__rotate_frame = tkinter.Frame(self._app_frame, bg=Macros.APP_BG)
        self.__rotate_frame.grid(row=6, column=0, columnspan=2)
        
        self.Buttons['Rotate Left'] = tkinter.Button(self.__rotate_frame, image=self.__rotateLeftIcon, bg=Macros.BUTTON_BG,
                                                      fg=Macros.BUTTON_FG)
        self.Buttons['Rotate Left'].grid(
            row=0, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        self.Buttons['Rotate Right'] = tkinter.Button(self.__rotate_frame, image=self.__rotateRightIcon, font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
                                                      fg=Macros.BUTTON_FG)
        self.Buttons['Rotate Right'].grid(
            row=0, column=2, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        self.__flip_frame = tkinter.Frame(self._app_frame, bg=Macros.APP_BG)
        self.__flip_frame.grid(row=7, column=0, columnspan=2)
        
        self.Buttons['Flip Horizontal'] = tkinter.Button(self.__flip_frame, image=self.__flipHorizontalIcon, bg=Macros.BUTTON_BG,
                                                    fg=Macros.BUTTON_FG)
        self.Buttons['Flip Horizontal'].grid(
            row=0, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        self.Buttons['Flip Vertical'] = tkinter.Button(self.__flip_frame, image=self.__flipVerticalIcon, bg=Macros.BUTTON_BG,
                                                    fg=Macros.BUTTON_FG)
        self.Buttons['Flip Vertical'].grid(
            row=0, column=2, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        

        self._canvas = tkinter.Canvas(
            self._app_frame, height=Macros.CANVAS_HEIGHT, width=Macros.CANVAS_WIDTH, background="grey")
        self._canvas.grid(row=0, column=2, rowspan=10)

        self._side_frame = tkinter.Frame(self._app_frame, bg=Macros.APP_BG)
        self._side_frame.grid(row=0, column=4)

    def __defineIcons(self):
        self.__rotateLeftIcon = PhotoImage( Image.open('./static/rotate_left.png').resize(Macros.ICON_SIZE) )
        self.__rotateRightIcon = PhotoImage( Image.open('./static/rotate_right.png').resize(Macros.ICON_SIZE) )
        self.__flipHorizontalIcon = PhotoImage( Image.open('./static/flip_horizontal.png').resize(Macros.ICON_SIZE) )
        self.__flipVerticalIcon = PhotoImage( Image.open('./static/flip_vertical.png').resize(Macros.ICON_SIZE) )
    
    
    def __upload_image(self):
        self._canvas.delete('all')
        self._filename = filedialog.askopenfilename(filetypes=Macros.FILETYPES)
        self._destinationFile = None
        self._original_img = Image.open(self._filename)
        self._editing_img = Image.open(self._filename)
        self._edited_img = Image.open(self._filename)
        self._displayImage(self._edited_img)

    def _refresh_side_frame(self):
        self._side_frame.grid_forget()
        self._canvas.unbind("<ButtonPress>")
        self._canvas.unbind("<B1-Motion>")
        self._canvas.unbind("<ButtonRelease>")
        self._displayImage(self._edited_img)
        self._side_frame = tkinter.Frame(self._app_frame, bg=Macros.APP_BG)
        self._side_frame.grid(row=0, column=4, rowspan=10, padx=50, pady=15)

    def _displayImage(self, image: Image.Image | None):
        if not image:
            image = self._edited_img
        
        width, height = image.size
        newWidth, newHeight = width, height
        
        ratio = height / width

        if height > Macros.CANVAS_HEIGHT or width > Macros.CANVAS_WIDTH:
            if ratio < 1:
                newWidth = Macros.CANVAS_WIDTH
                newHeight = int(newWidth * ratio)
            else:
                newHeight = Macros.CANVAS_HEIGHT
                newWidth = int(newHeight * width / height)

        image = image.resize((newWidth, newHeight))
        self.display_img = PhotoImage(image=image)
        self._canvas.delete('all')
        
        self._canvas.config(width=newWidth, height=newHeight)
        self._canvas.create_image(
            newWidth/2, newHeight/2, image=self.display_img)

    def __filters(self):
        self._refresh_side_frame()
        self.Buttons['Negative'] = tkinter.Button(
            self._side_frame, text="Negative", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG
        )
        self.Buttons["Negative"].grid(row=0, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        self.Buttons['Black-White'] = tkinter.Button(
            self._side_frame, text="Black And white", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG
        )
        self.Buttons['Black-White'].grid(row=1, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        self.Buttons['Stylisation'] = tkinter.Button(
            self._side_frame, text="Stylisation", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG
        )
        self.Buttons['Stylisation'].grid(row=2, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        self.Buttons['Sketch Effect'] = tkinter.Button(
            self._side_frame, text="Sketch Effect", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG
        )
        self.Buttons['Sketch Effect'].grid(row=3, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        self.Buttons['Emboss'] = tkinter.Button(
            self._side_frame, text="Emboss", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG
        )
        self.Buttons['Emboss'].grid(row=4, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        self.Buttons['Sepia'] = tkinter.Button(
            self._side_frame, text="Sepia", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG
        )
        self.Buttons['Sepia'].grid(row=5, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        self.Buttons['Binary Thresholding'] = tkinter.Button(
            self._side_frame, text="Binary Thresholding", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG
        )
        self.Buttons['Binary Thresholding'].grid(row=6, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        self.Buttons['Erosion'] = tkinter.Button(
            self._side_frame, text="Erosion", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG
        )
        self.Buttons['Erosion'].grid(row=7, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        self.Buttons['Dilation'] = tkinter.Button(
            self._side_frame, text="Dilation", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG
        )
        self.Buttons['Dilation'].grid(row=8, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

    def run(self):
        self._window.mainloop()


def main():
    app = AppFrame()
    app.run()


if __name__ == "__main__":
    main()
