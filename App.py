#!/usr/bin/env python

from PIL import Image

from tkinter import filedialog

from click import command
import Macros
from AppFrame import AppFrame


class App(AppFrame):
    def __init__(self) -> None:
        super().__init__()
        print(self.Buttons.keys())
        self.Buttons['Rotate Left'].config(command=self.__rotateLeft)
        self.Buttons['Rotate Right'].config(command=self.__rotateRight)
        self.Buttons['Flip Horizontal'].config(command=self.__flipHorizontal)
        self.Buttons['Flip Vertical'].config(command=self.__flipVertical)
        self.Buttons['Save'].config(command=self.__saveImage)
        self.Buttons['Save As'].config(command=self.__saveAsImage)
        self.Buttons['Reset Image'].config(command=self.__resetImage)
        self.Buttons['Apply Changes'].config(command=self.__applyChanges)
        self.Buttons['Cancel Changes'].config(command=self.__cancelChanges)

    def __rotateLeft(self):
        self._editing_img = self._editing_img.rotate(angle=90, expand=True)
        self._edited_img = self._edited_img.rotate(angle=90, expand=True)
        self._displayImage(self._editing_img)
        
    def __rotateRight(self):
        self._editing_img = self._editing_img.rotate(angle=-90, expand=True)
        self._edited_img = self._edited_img.rotate(angle=-90, expand=True)
        self._displayImage(self._editing_img)

    def __flipHorizontal(self):
        self._editing_img = self._editing_img.transpose(Image.Transpose.TRANSPOSE.FLIP_LEFT_RIGHT)
        self._edited_img = self._edited_img.transpose(Image.Transpose.TRANSPOSE.FLIP_LEFT_RIGHT)
        self._displayImage(self._editing_img)
        
    def __flipVertical(self):
        self._editing_img = self._editing_img.transpose(Image.Transpose.TRANSPOSE.FLIP_TOP_BOTTOM)
        self._edited_img = self._edited_img.transpose(Image.Transpose.TRANSPOSE.FLIP_TOP_BOTTOM)
        self._displayImage(self._editing_img)
    
    def __saveImage(self):
        if self._destinationFile:
            self._edited_img.save(fp=self._destinationFile)
        else:
            self.__saveAsImage()
    
    def __saveAsImage(self):
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
        self._editing_img = self._original_img.copy()
        self._edited_img = self._original_img.copy()
        self._displayImage(self._edited_img)
    
    def __applyChanges(self):
        self._edited_img = self._editing_img.copy()
        self._displayImage(self._edited_img)
    
    def __cancelChanges(self):
        self.__editing_img = self._edited_img.copy()
        self._displayImage(self.__editing_img)
    
        
if __name__ == "__main__":
    app = App()
    app.run()
