#!/usr/bin/env python

from PIL import Image, ImageFilter, ImageEnhance
import tkinter
from tkinter import filedialog

from numpy import asarray
import Macros
from AppFrame import AppFrame


class App(AppFrame):
    def __init__(self) -> None:
        '''
        - Assigns commands to the buttons from AppFrame.py
        '''
        super().__init__()
        
        self.Buttons['Save'].config(command=self.__saveImage)
        self.Buttons['Save As'].config(command=self.__saveAsImage)
        self.Buttons['Reset Image'].config(command=self.__resetImage)
        self.Buttons['Apply Changes'].config(command=self.__applyChanges)
        self.Buttons['Cancel Changes'].config(command=self.__cancelChanges)
        
        self.Buttons['Crop Image'].config(command=self.__cropImage)
        self.Buttons['Split Channel'].config(command=self.__splitChannel)
        self.Buttons['Apply Filters'].config(command=self.__filters)
        self.Buttons['Level Adjust'].config(command=self.__levelAdjust)
        self.Buttons['Rotate Left'].config(command=self.__rotateLeft)
        self.Buttons['Rotate Right'].config(command=self.__rotateRight)
        self.Buttons['Flip Horizontal'].config(command=self.__flipHorizontal)
        self.Buttons['Flip Vertical'].config(command=self.__flipVertical)
        self.Buttons['Resize'].config(command=self.__resize)
        
    def __rotateLeft(self):
        '''
        - Counter-clockwise rotation by 90 degrees
        '''
        if self._editing_img:
            self._editing_img = self._editing_img.rotate(angle=90, expand=True)
            self._edited_img = self._edited_img.rotate(angle=90, expand=True)
            self._displayImage(self._editing_img)
        
    def __rotateRight(self):
        '''
        - Clockwise rotation by 90 degrees
        '''
        if self._editing_img:
            self._editing_img = self._editing_img.rotate(angle=-90, expand=True)
            self._edited_img = self._edited_img.rotate(angle=-90, expand=True)
            self._displayImage(self._editing_img)

    def __flipHorizontal(self):
        '''
        - Left to Right Flip
        '''
        if self._editing_img:
            self._editing_img = self._editing_img.transpose(Image.Transpose.TRANSPOSE.FLIP_LEFT_RIGHT)
            self._edited_img = self._edited_img.transpose(Image.Transpose.TRANSPOSE.FLIP_LEFT_RIGHT)
            self._displayImage(self._editing_img)
        
    def __flipVertical(self):
        '''
        - Top to Bottom Flip
        '''
        if self._editing_img:
            self._editing_img = self._editing_img.transpose(Image.Transpose.TRANSPOSE.FLIP_TOP_BOTTOM)
            self._edited_img = self._edited_img.transpose(Image.Transpose.TRANSPOSE.FLIP_TOP_BOTTOM)
            self._displayImage(self._editing_img)
        
    def __saveImage(self):
        '''
        - Saves image overwriting the last saved image location (_destinationFile).
        - The first __saveImage call for the given image has _destinationFile as None and so defaults to __saveAsImage call.
        '''
        if self._edited_img:
            if self._destinationFile:
                self._edited_img.save(fp=self._destinationFile)
            else:
                self.__saveAsImage()
    
    def __saveAsImage(self):
        '''
        - Asks user to select the destination for saving the edited_img with user-selected extension.
        - Overwrite confirmation by user required.
        '''
        if self._edited_img:
            filename = filedialog.asksaveasfilename(confirmoverwrite=True)
            if not filename:
                return
            extension = self._filename.split('.')[-1]
            if len(filename.split('.')) != 1:
                extension = filename.split('.')[-1]
                self._edited_img.save(fp=filename)
                self._destinationFile = filename
            else:
                self._edited_img.save(fp=filename + '.' + extension)
                self._destinationFile = filename + '.' + extension
    
    def __resetImage(self):
        '''
        - sets editing and edited image as original image
        '''
        if self._original_img:
            self._editing_img = self._original_img.copy()
            self._edited_img = self._original_img.copy()
            self._displayImage(self._edited_img)
    
    def __applyChanges(self):
        '''
        - applies the current implemented changes
        - sets edited_img to editing_img
        '''
        if self._editing_img:
            self._edited_img = self._editing_img.copy()
            self._displayImage(self._edited_img)
    
    def __cancelChanges(self):
        '''
        - discards the current implemented changes
        - sets editing_img to edited_img
        '''
        if self._edited_img:
            self._editing_img = self._edited_img.copy()
            self._displayImage(self._editing_img)
    
    def __cropImage(self):
        '''
        - crop image action divided in three stages
            - start() --> locks the top-left corner for the final cropped image when left-mouse button is clicked
            - crop() --> constantly resets the rectangle border displayed around the to-be-cropped image as cursor drags the bottom-right corner
            - end() --> locks the botom-right corner for the final cropped image when left-mouse button is released, and then crops the image
        '''
        self._refresh_side_frame()
        tkinter.Label(self._side_frame, text="Click and drag\non image to crop", font=Macros.BUTTON_FONT,
                      bg=Macros.APP_BG, fg=Macros.BUTTON_FG).grid(row=0, column=0)
        
        self.rectangleID = 0
        self.startX, self.startY, self.endX, self.endY = 0, 0, 0, 0
        
        def start(event):
            self.startX, self.startY = event.x, event.y
        
        def crop(event):
            if self.rectangleID:
                self._canvas.delete(self.rectangleID)
            
            self.endX, self.endY = event.x, event.y
            self.rectangleID = self._canvas.create_rectangle(self.startX, self.startY, self.endX, self.endY, width=1)
            
        def end(event):
            self.endX, self.endY = event.x, event.y
            
            self.startX, self.endX = int(min(self.startX, self.endX) * self._ratio), int(max(self.startX, self.endX) * self._ratio)
            self.startY, self.endY = int(min(self.startY, self.endY) * self._ratio), int(max(self.startY, self.endY) * self._ratio)
            
            # Truncating cropping going outside the image
            width, height = self._edited_img.size
            self.startX, self.endX = max(self.startX, 0), min(self.endX, width)
            self.startY, self.endY = max(self.startY, 0), min(self.endY, height)
            
            self._editing_img = self._edited_img.crop((self.startX, self.startY, self.endX, self.endY))
            self._displayImage(self._editing_img)
        
        self._canvas.bind("<ButtonPress>", start)
        self._canvas.bind("<B1-Motion>", crop)
        self._canvas.bind("<ButtonRelease>", end)
            
    
    def __splitChannel(self):
        '''
        - Converts the given image into RGB type and then splits the red values, blue values and green values of the image based on selection.
        - Red Channel  Button shows the image when all green and blue pixels are set to 0.
        - green Channel  Button shows the image when all blue and red pixels are set to 0.
        - blue Channel  Button shows the image when all red and green pixels are set to 0.
        '''
        self._refresh_side_frame()
        
        # Added to ensure that the dimensions of editing and edited images are same 
        # when taking a particular channel value of pixels from edited image and putting it in editing image.
        self._editing_img = self._edited_img.copy()
        
        tkinter.Button(self._side_frame, text='Red Channel', font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__redChannel
                       ).grid(row=0, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        tkinter.Button(self._side_frame, text='Green Channel', font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__greenChannel
                       ).grid(row=1, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        tkinter.Button(self._side_frame, text='Blue Channel', font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__blueChannel
                       ).grid(row=2, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
    def __redChannel(self):
        '''
        - Shows the red value of all the image pixels
        '''
        if self._edited_img:
            red = self._edited_img.convert("RGB").getdata(0)
            red = [ (r, 0, 0) for r in red ]
            self._editing_img.putdata(red)
            self._displayImage(self._editing_img)
        
    def __greenChannel(self):
        '''
        - Shows the green value of all the image pixels
        '''
        if self._edited_img:
            green = self._edited_img.convert("RGB").getdata(1)
            green = [ (0, g, 0) for g in green ]
            self._editing_img.putdata(green)
            self._displayImage(self._editing_img)
        
    def __blueChannel(self):
        '''
        - Shows the blue value of all the image pixels
        '''
        if self._edited_img:
            blue = self._edited_img.convert("RGB").getdata(2)
            blue = [ (0, 0, b) for b in blue ]
            self._editing_img.putdata(blue)
            self._displayImage(self._editing_img)
    
    
    def __filters(self):
        '''
        - Displays option for various filters available under 'Apply Filters' Menu Button
        '''
        self._refresh_side_frame()
        
        tkinter.Button(
            self._side_frame, text="Negative", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__negative
        ).grid(row=0, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self._side_frame, text="Black And white", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__blackWhite
        ).grid(row=1, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self._side_frame, text="Detect Edge", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__detectEdge
        ).grid(row=2, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self._side_frame, text="Enhance Edge", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__enhanceEdge
        ).grid(row=3, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self._side_frame, text="Pencil Sketch", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__sketch
        ).grid(row=4, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Scale(
            self._side_frame, label="Thresholding", from_=0, to=256, font=Macros.BUTTON_FONT, orient='horizontal',
            fg=Macros.BUTTON_FG,bg=Macros.BUTTON_BG, command=self.__thresholding
        ).grid(row=5, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self._side_frame, text="Erosion", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__erosion
        ).grid(row=6, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self._side_frame, text="Dilation", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__dilation
        ).grid(row=7, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

    def __negative(self):
        '''
        - Inverts image. Subtracting each pixel value from white pixel
        '''
        if self._edited_img:
            self._editing_img = self._edited_img.convert('RGB').point(lambda x: 255-x)
            self._displayImage(self._editing_img)
    
    def __blackWhite(self):
        '''
        - Gray-scale conversion
        '''
        if self._edited_img:
            self._editing_img = self._edited_img.convert('L')
            self._displayImage(self._editing_img)
            
    def __detectEdge(self):
        '''
        - Detects and displays the edges of the image.
        - sharper the edge more clearly visible it will be.
        '''
        if self._edited_img:
            self._editing_img = self._edited_img.filter(ImageFilter.FIND_EDGES)
            self._displayImage(self._editing_img)
            
    def __enhanceEdge(self):
        '''
        - Enhances the contrast around the edges of the image to show them more distinctly.
        '''
        if self._edited_img:
            self._editing_img = self._edited_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
            self._displayImage(self._editing_img)
    
    def __sketch(self):
        '''
        - Converts the image into what it can look like as a pencil sketching
        '''
        if self._edited_img:
            img_gray = self._edited_img.convert('L')
            img_smooth = img_gray.filter(ImageFilter.GaussianBlur(150))
            try: # To suppress RuntimeWarning of divide by zero, and invalid value encountered
                final = asarray(img_gray) / asarray(img_smooth) * 256.0
            except Exception:
                pass
            self._editing_img = Image.fromarray(final)
            self._displayImage(self._editing_img)
        
    
    def __thresholding(self, threshold):
        '''
        - sets each pixel to either minimum value or maximum value based on a certain threshold value
        '''
        if self._edited_img:
            threshold = int(threshold)
            self._editing_img = self._edited_img.point(lambda x: 256 if x >= threshold else 0)
            self._displayImage(self._editing_img)
    
    def __erosion(self):
        '''
        Decreases the amount of bright pixels from the image
        '''
        if self._edited_img:
            self._editing_img = self._edited_img.filter(ImageFilter.MinFilter(3))
            self._displayImage(self._editing_img)
            
    
    def __dilation(self):
        '''
        Decreases the amount of dark pixels from the image
        '''
        if self._edited_img:
            self._editing_img = self._edited_img.filter(ImageFilter.MaxFilter(3))
            self._displayImage(self._editing_img)
    
    def __levelAdjust(self):
        '''
        - Adjust various levels of the image like brightness, saturation, contrast and more.
        - All level Scales' action commands have self-explanatory names
        '''
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
        
        tkinter.Scale(self._side_frame, from_=0.0, resolution=0.1, to=3.0, label='Contrast', orient='horizontal',
                      font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG, command=self.__contrastImage
                      ).grid(row=4, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

    
    def __blurImage(self, value):
        if self._edited_img:
            self._editing_img = self._edited_img.filter(ImageFilter.GaussianBlur(int(value)))
            self._displayImage(self._editing_img)
            
    def __sharpenImage(self, value):
        if self._edited_img:
            self._editing_img = ImageEnhance.Sharpness(self._edited_img).enhance(int(value))
            self._displayImage(self._editing_img)
    
    def __brightenImage(self, value):
        if self._edited_img:
            self._editing_img = ImageEnhance.Brightness(self._edited_img).enhance(float(value))
            self._displayImage(self._editing_img)
            
    def __saturateImage(self, value):
        if self._edited_img:
            self._editing_img = ImageEnhance.Color(self._edited_img).enhance(float(value))
            self._displayImage(self._editing_img)
            
    def __contrastImage(self, value):
        if self._edited_img:
            self._editing_img = ImageEnhance.Contrast(self._edited_img).enhance(float(value))
            self._displayImage(self._editing_img)
            

    def __resize(self):
        '''
        - Resizing options displayed in the side frame.
        - Displays current size of the image and an input for new width and new height.
        - Resizes the image on clicking the Resize button by calling __resizeImage function
        '''
        if self._editing_img:
            self._refresh_side_frame()
            self._displayImage(self._editing_img)
            width, height = self._editing_img.size
            
            tkinter.Label(self._side_frame, text='Current Size:',  font=Macros.BUTTON_FONT, bg=Macros.APP_BG, fg=Macros.BUTTON_FG
                          ).grid(row=0, column=0, sticky=Macros.BUTTON_STICKY)
            
            tkinter.Label(self._side_frame, text=f'{width} X {height}',  font=Macros.BUTTON_FONT, bg=Macros.APP_BG, fg=Macros.BUTTON_FG
                          ).grid(row=1, column=0, sticky=Macros.BUTTON_STICKY)
            
            tkinter.Label(self._side_frame, text='',  font=Macros.BUTTON_FONT, bg=Macros.APP_BG, fg=Macros.BUTTON_FG
                          ).grid(row=2, column=0, sticky=Macros.BUTTON_STICKY)
            
            self.sizeFrame = tkinter.Frame(self._side_frame)
            self.sizeFrame.grid(row=3, column=0)
            
            self.widthBox = tkinter.Entry(self.sizeFrame, font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG, width=5)
            self.widthBox.grid(row=0, column=0, sticky=Macros.BUTTON_STICKY)
            
            tkinter.Label(self.sizeFrame, text='X',  font=Macros.BUTTON_FONT, bg=Macros.APP_BG, fg=Macros.BUTTON_FG
                          ).grid(row=0, column=1, sticky=Macros.BUTTON_STICKY)
            
            self.heightBox = tkinter.Entry(self.sizeFrame, font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG, width=5)
            self.heightBox.grid(row=0, column=2, sticky=Macros.BUTTON_STICKY)
            
            tkinter.Label(self._side_frame, text='',  font=Macros.BUTTON_FONT, bg=Macros.APP_BG, fg=Macros.BUTTON_FG
                          ).grid(row=4, column=0, sticky=Macros.BUTTON_STICKY)
            
            tkinter.Button(self._side_frame, text='Resize', bg=Macros.APP_BG, fg=Macros.BUTTON_FG,
                           font=Macros.BUTTON_FONT, command=self.__resizeImage).grid(row=5, column=0)
            

    def __resizeImage(self):
        '''
        - Resizes the image if input for both width and height is given and both are integer values.
        - The resize performed is soft resize, i.e., aspect ratio on resizing is not maintained. 
            - The image will get stretched to fill the new aspect ratio.
        '''
        if self.widthBox.get() and self.heightBox.get():
            width, height = self.widthBox.get(), self.heightBox.get()
            try:
                width = int(width.strip())
                height = int(height.strip())
                self._editing_img = self._edited_img.resize(size=(width, height))
            except Exception as e:
                pass
            self.__resize()
            
if __name__ == "__main__":
    app = App()
    app.run()
