#!/usr/bin/env python

from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageMath
import tkinter
from tkinter import filedialog

from numpy import asarray, invert
import numpy
import Macros
from AppFrame import AppFrame


class App(AppFrame):
    def __init__(self) -> None:
        super().__init__()
        print(self.Buttons.keys())
        self.Buttons['Save'].config(command=self.__saveImage)
        self.Buttons['Save As'].config(command=self.__saveAsImage)
        self.Buttons['Reset Image'].config(command=self.__resetImage)
        self.Buttons['Apply Changes'].config(command=self.__applyChanges)
        self.Buttons['Cancel Changes'].config(command=self.__cancelChanges)
        
        self.Buttons['Crop Image'].config(command=self.__cropImage)
        self.Buttons['Apply Filters'].config(command=self.__filters)
        self.Buttons['Level Adjust'].config(command=self.__levelAdjust)
        self.Buttons['Rotate Left'].config(command=self.__rotateLeft)
        self.Buttons['Rotate Right'].config(command=self.__rotateRight)
        self.Buttons['Flip Horizontal'].config(command=self.__flipHorizontal)
        self.Buttons['Flip Vertical'].config(command=self.__flipVertical)
        
    def __rotateLeft(self):
        if self._editing_img:
            self._editing_img = self._editing_img.rotate(angle=90, expand=True)
            self._edited_img = self._edited_img.rotate(angle=90, expand=True)
            self._displayImage(self._editing_img)
        
    def __rotateRight(self):
        if self._editing_img:
            self._editing_img = self._editing_img.rotate(angle=-90, expand=True)
            self._edited_img = self._edited_img.rotate(angle=-90, expand=True)
            self._displayImage(self._editing_img)

    def __flipHorizontal(self):
        if self._editing_img:
            self._editing_img = self._editing_img.transpose(Image.Transpose.TRANSPOSE.FLIP_LEFT_RIGHT)
            self._edited_img = self._edited_img.transpose(Image.Transpose.TRANSPOSE.FLIP_LEFT_RIGHT)
            self._displayImage(self._editing_img)
        
    def __flipVertical(self):
        if self._editing_img:
            self._editing_img = self._editing_img.transpose(Image.Transpose.TRANSPOSE.FLIP_TOP_BOTTOM)
            self._edited_img = self._edited_img.transpose(Image.Transpose.TRANSPOSE.FLIP_TOP_BOTTOM)
            self._displayImage(self._editing_img)
        
    def __saveImage(self):
        if self._edited_img:
            if self._destinationFile:
                self._edited_img.save(fp=self._destinationFile)
            else:
                self.__saveAsImage()
    
    def __saveAsImage(self):
        if self._edited_img:
            filename = filedialog.asksaveasfilename(confirmoverwrite=True)
            extension = self._filename.split('.')[-1]
            if len(filename.split('.')) != 1:
                extension = filename.split('.')[-1]
                self._edited_img.save(fp=filename)
                self._destinationFile = filename
            else:
                self._edited_img.save(fp=filename + '.' + extension)
                self._destinationFile = filename + '.' + extension
    
    def __resetImage(self):
        if self._original_img:
            self._editing_img = self._original_img.copy()
            self._edited_img = self._original_img.copy()
            self._displayImage(self._edited_img)
    
    def __applyChanges(self):
        if self._editing_img:
            self._edited_img = self._editing_img.copy()
            self._displayImage(self._edited_img)
    
    def __cancelChanges(self):
        if self._edited_img:
            self.__editing_img = self._edited_img.copy()
            self._displayImage(self.__editing_img)
    
    def __cropImage(self):
        pass
    
    def __filters(self):
        self._refresh_side_frame()
        
        tkinter.Button(
            self._side_frame, text="Negative", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__negative
        ).grid(row=0, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self._side_frame, text="Black And white", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__blackWhite
        ).grid(row=1, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self._side_frame, text="Stylisation", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__stylization
        ).grid(row=2, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self._side_frame, text="Pencil Sketch", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__sketch
        ).grid(row=3, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Scale(
            self._side_frame, label="Thresholding", from_=0, to=256, font=Macros.BUTTON_FONT, orient='horizontal',
            fg=Macros.BUTTON_FG,bg=Macros.BUTTON_BG, command=self.__thresholding
        ).grid(row=4, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self._side_frame, text="Erosion", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__erosion
        ).grid(row=5, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self._side_frame, text="Dilation", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__dilation
        ).grid(row=6, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

    def __negative(self):
        if self._edited_img:
            self._editing_img = self._edited_img.convert('RGB').point(lambda x: 255-x)
            self._displayImage(self._editing_img)
    
    def __blackWhite(self):
        if self._edited_img:
            self._editing_img = self._edited_img.convert('L')
            self._displayImage(self._editing_img)
            
    def __stylization(self):
        pass
    
    def __sketch(self):
        if self._edited_img:
            img_gray = self._edited_img.convert('L')
            img_invert = img_gray.point(lambda x: 255-x)
            img_smooth = img_invert.filter(ImageFilter.GaussianBlur(200))
            invert_smooth = img_smooth.point(lambda x: 255-x)
            final = asarray(img_gray) / asarray(invert_smooth) * 256
            self._editing_img = Image.fromarray(final)
            self._displayImage(self._editing_img)
            
            
    def __sepia(self):
        pass
    
    def __thresholding(self, value):
        if self._edited_img:
            value = int(value)
            self._editing_img = self._edited_img.point(lambda x: 256 if x >= value else 0)
            self._displayImage(self._editing_img)
    
    def __erosion(self):
        if self._edited_img:
            self._editing_img = self._edited_img.filter(ImageFilter.MinFilter(3))
            self._displayImage(self._editing_img)
            
    
    def __dilation(self):
        if self._edited_img:
            self._editing_img = self._edited_img.filter(ImageFilter.MaxFilter(3))
            self._displayImage(self._editing_img)
    
    def __levelAdjust(self):
        self._refresh_side_frame()
        
        tkinter.Scale(self._side_frame, from_=1, to=50, label='Blur', orient='horizontal',
                      font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG, command=self.__blurImage
                      ).grid(row=0, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        tkinter.Scale(self._side_frame, from_=1, to=50, label='Sharpness', orient='horizontal',
                      font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG, command=self.__sharpenImage
                      ).grid(row=1, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        tkinter.Scale(self._side_frame, from_=0.0, resolution=0.1, to=3.0, label='Brightness', orient='horizontal',
                      font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG, command=self.__brightenImage
                      ).grid(row=2, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Scale(self._side_frame, from_=0.0, resolution=0.1, to=3.0, label='Saturation', orient='horizontal',
                      font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG, command=self.__saturateImage
                      ).grid(row=3, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

    
    def __blurImage(self, value):
        if self._edited_img:
            value = int(value)
            self._editing_img = self._edited_img.filter(ImageFilter.GaussianBlur(value))
            self._displayImage(self._editing_img)
            
    def __sharpenImage(self, value):
        if self._edited_img:
            value = int(value)
            self._editing_img = ImageEnhance.Sharpness(self._edited_img).enhance(value)
            self._displayImage(self._editing_img)
    
    def __brightenImage(self, value):
        if self._edited_img:
            self._editing_img = ImageEnhance.Brightness(self._edited_img).enhance(float(value))
            self._displayImage(self._editing_img)
            
    def __saturateImage(self, value):
        if self._edited_img:
            self._editing_img = ImageEnhance.Color(self._edited_img).enhance(float(value))
            self._displayImage(self._editing_img)
        
if __name__ == "__main__":
    app = App()
    app.run()
