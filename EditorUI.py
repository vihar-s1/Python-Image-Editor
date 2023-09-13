#!/usr/bin/env python

import tkinter, os
from tkinter import filedialog
from PIL import Image
from PIL.ImageTk import PhotoImage

import Macros
import ImageEditor

import sys
from os import path

# Function needed to make sure that .exe version uses static files integrated in it
# and does not need to be provided explicitly.
# The .exe when running, creates a temporary folder and stores images in that folder.
def resource_path(relative_path: str):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception as e:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)


class ImageEditorUI:
    def __init__(self) -> None:
        # Three different stages of images to be able to do reset image, apply changes and cancel changes
        self.__original_img = self.__editing_img = self.__edited_img = None
        # for "save", "save as" functionalities
        self.__filename = self.__destinationFile = None
        
        # App Name
        self.__window = tkinter.Tk(className="Python Image Editor")
        self.__window.config(bg=Macros.APP_BG)
        
        # Header for showing app name and header buttons
        self.__header = tkinter.Frame(self.__window, bg=Macros.APP_BG, padx=Macros.PADX, pady=Macros.PADY)
        self.__header.pack()
        
        # all the icons used for right-left rotate and flipping action clubbed together
        self.__defineIcons()
        
        tkinter.Label(
            self.__header, text="Python Image Editor", font=('Agency FB', 26, 'bold', 'italic'),
            bg=Macros.APP_BG, fg=Macros.BRIGHT_GREEN
        ).grid(row=0, column=0)
        tkinter.Label(self.__header, text="  ", bg=Macros.APP_BG).grid(row=1, column=2)
        
        self.__header_buttons = tkinter.Frame(self.__header, bg=Macros.APP_BG, padx=Macros.PADX, pady=Macros.PADY)
        self.__header_buttons.grid(row=2, column=0)
        
        # Defining and placing header buttons in the header frame with horizontal padding for spacing inbetween
        # SAVE BUTTON
        tkinter.Button(
            self.__header_buttons, text="Save", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG,
            command=self.__saveImage
        ).grid(row=0, column=0, padx=Macros.PADX)
        
        # SAVE AS BUTTON
        tkinter.Button(
            self.__header_buttons, text="Save As", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG,
            command=self.__saveAsImage
        ).grid(row=0, column=1, padx=Macros.PADX)
        
        # RESET IMAGE
        tkinter.Button(
            self.__header_buttons, text="Reset Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG,
            command=self.__resetImage
        ).grid(row=0, column=2, padx=Macros.PADX)
        
        # APPLY CHANGES
        tkinter.Button(
            self.__header_buttons, text="Apply Changes", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG,
            command=self.__applyChanges
        ).grid(row=0, column=3, padx=Macros.PADX)
        
        # CANCEL CHANGES
        tkinter.Button(
            self.__header_buttons, text="Cancel Changes", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG,
            command=self.__cancelChanges
        ).grid(row=0, column=4, padx=Macros.PADX)
        
        # ...tkinter.tk.quit exits the initialized object
        # ...basically exiting the main window --> quit the program
        tkinter.Button(
            self.__header_buttons, text="Exit Editor", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
            fg=Macros.BUTTON_FG, command=self.__exitEditor
        ).grid(row=0, column=5, padx=Macros.PADX)
        
        # All the buttons and frames and canvas used for creating the App Frame will be children of the __app_frame
        self.__app_frame = tkinter.Frame(self.__window, bg=Macros.APP_BG)
        self.__app_frame.pack()
        
        #. Defining Menu Buttons for opening, cropping, and resizing the image, rotate, flip, splitting channel, and so on
        tkinter.Button(
            self.__app_frame, text="Open Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
            fg=Macros.BUTTON_FG, command=self.__upload_image
        ).grid(row=0, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        #. CROP IMAGE
        tkinter.Button(
            self.__app_frame, text="Crop Image", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
            fg=Macros.BUTTON_FG, command=self.__cropImage
        ).grid(
            row=1, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        
        #. SPLIT CHANNEL
        tkinter.Button(
            self.__app_frame, text="Split Channel", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
            fg=Macros.BUTTON_FG, command=self.__splitChannel
        ).grid(
            row=2, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        
        #. APPLY FILTERS
        tkinter.Button(
            self.__app_frame, text="Apply Filters", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
            fg=Macros.BUTTON_FG, command=self.__filters
        ).grid(
            row=3, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        
        #. LEVEL ADJUST
        tkinter.Button(
            self.__app_frame, text="Level Adjust", font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
            fg=Macros.BUTTON_FG, command=self.__levelAdjust
        ).grid(
            row=4, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        
        self.__rotate_frame = tkinter.Frame(self.__app_frame, bg=Macros.APP_BG)
        self.__rotate_frame.grid(row=5, column=0, columnspan=2)
        
        #. ROTATE LEFT
        tkinter.Button(
            self.__rotate_frame, image=self.__rotateLeftIcon, font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
            text="Left\nRotate", fg=Macros.BUTTON_FG, command=self.__rotateLeft
        ).grid(
            row=0, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        
        #. ROTATE RIGHT
        tkinter.Button(
            self.__rotate_frame, image=self.__rotateRightIcon, font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
            text="Right\nRotate", fg=Macros.BUTTON_FG, command=self.__rotateRight
        ).grid(
            row=0, column=2, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        
        self.__flip_frame = tkinter.Frame(self.__app_frame, bg=Macros.APP_BG)
        self.__flip_frame.grid(row=6, column=0, columnspan=2)
        
        #. FLIP HORIZONTAL
        tkinter.Button(
            self.__flip_frame, image=self.__flipHorizontalIcon, font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
            text="Horizontal\Flip", fg=Macros.BUTTON_FG, command=self.__flipHorizontal
        ).grid(
            row=0, column=0, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        
        #. FLIP VERTICAL
        tkinter.Button(
            self.__flip_frame, image=self.__flipVerticalIcon, font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG,
            text="Vertical\Flip", fg=Macros.BUTTON_FG, command=self.__flipVertical
        ).grid(
            row=0, column=2, columnspan=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY
        )
        
        #. RESIZE BUTTON
        tkinter.Button(
            self.__app_frame, text="Resize Image", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG,
            bg=Macros.BUTTON_BG, command=self.__resetImage
        )
        
        #. Creating canvas
        # The canvas will hold and display the image opened
        # The canvas size will be a static object i.e. it won't change with the size of the image, the image will change with the size of the canvas
        # To prevent that, we constantly reshape the canvas while displaying the image using the displayImage method.
        self.__canvas = tkinter.Canvas(
            self.__app_frame, height=Macros.CANVAS_HEIGHT, width=Macros.CANVAS_WIDTH, background="grey")
        self.__canvas.grid(row=0, column=2, rowspan=10)

        #. The side frame or the "right side frame" will be used to display the various options given by different menu buttons
        # Eg. various filters available on clicking 'Apply Filters' button,
        # saturation, brightness etc, on clicking 'Level Adjust' button
        self.__side_frame = tkinter.Frame(self.__app_frame, bg=Macros.APP_BG)
        self.__side_frame.grid(row=0, column=4)
        
    
    def __saveImage(self):
        if not self.__edited_img: return
        if self.__destinationFile:
            ImageEditor.saveImage(self.__edited_img, self.__destinationFile)
        else:
            filename = ImageEditor.saveImage(self.__edited_img, None)
            if filename:
                self.__destinationFile = filename
    
    def __saveAsImage(self):
        if not self.__edited_img: return
        self.__destinationFile = ImageEditor.saveAsImage(self.__edited_img, self.__destinationFile)
    
    
    def __refresh_side_frame(self):
        """
        - Refreshes the side frame, removing all the buttons on it
        - Used to display the various options available under a menu button
        - Refreshing ensures buttons do not overlap and one menu option's buttons
            are not visible along side other menu option's buttons
        """
        self.__side_frame.grid_forget()
        self.__canvas.unbind("<ButtonPress>")
        self.__canvas.unbind("<B1-Motion>")
        self.__canvas.unbind("<ButtonRelease>")
        if self.__edited_img:
            self.__displayImage(self.__edited_img)
        self.__side_frame = tkinter.Frame(self.__app_frame, bg=Macros.APP_BG)
        self.__side_frame.grid(row=0, column=4, rowspan=10, padx=Macros.PADX, pady=Macros.PADY)
    
        
    def __displayImage(self, image: Image.Image):
        """
        - resizes the image to fit inside Macros.CANVAS_WIDTH x MACROS.CANVAS_HEIGHT. The canvas is also resized to the same dimensions.
        - Actual image is not resized, copy of image to display is made, which is then resized to ensure actual image remains unaltered.
        - Aspect ratio is maintained while resizing. Keeps track of the resizing ratio (height/NewHeight) which is used during cropping.
        """
        if not image: image = self.__edited_img
        
        width, height = image.size
        newWidth, newHeight = width, height
        ratio = height / width
        
        if height > Macros.CANVAS_HEIGHT or width > Macros.CANVAS_WIDTH:
            if ratio < 1:
                newWidth = Macros.CANVAS_WIDTH
                newHeight = int(newWidth * ratio)
            else:
                newHeight = Macros.CANVAS_HEIGHT
                newWidth = int(newHeight / ratio)
        
        self.__scaledRatio = height / newHeight
        
        image = image.resize((newWidth, newHeight))
        self.display_img = PhotoImage(image=image)
        self.__canvas.delete('all')
    
        self.__canvas.config(width=newWidth, height=newHeight)
        self.__canvas.create_image(newWidth/2, newHeight/2, image=self.display_img)
        
    
    def __defineIcons(self):
        """
        - Defining the icons used for some of the buttons.
        - Need to be along the rest of the console and frames definition because PIL.Imagetk.PhotoImage is tkinter supporting photoImage
        whick only works when atleast one tkintertk instance exists, 'self.__window' in this instance
        """
        try:
            self.__rotateLeftIcon = PhotoImage( Image.open( resource_path('static\\rotate_left.png') ).resize(Macros.ICON_SIZE) ) 
            self.__rotateRightIcon = PhotoImage( Image.open( resource_path('static\\rotate_right.png') ).resize(Macros.ICON_SIZE) )
            self.__flipHorizontalIcon = PhotoImage( Image.open( resource_path('static\\flip_horizontal.png') ).resize(Macros.ICON_SIZE) )
            self.__flipVerticalIcon = PhotoImage( Image.open( resource_path('static\\flip_vertical.png') ).resize(Macros.ICON_SIZE) )
        except:
            self.__rotateLeftIcon = self.__rotateRightIcon = self.__flipHorizontalIcon = self.__flipVerticalIcon = None
            
    
    def __exitEditor(self):
        if self.__edited_img:
            self.__edited_img.close()
            self.__editing_img.close()
            self.__original_img.close()
        self.__window.quit()
        
    
    def __resetImage(self):
        """Sets editing and edited image as original image"""
        if not self.__original_img: return
        self.__editing_img = self.__original_img.copy()
        self.__edited_img = self.__original_img.copy()
        self.__displayImage(self.__edited_img)
            

    def __applyChanges(self):
        """
        - Applies the current implemented changes
        - Sets edited_img to editing_img
        """
        if self.__editing_img:
            self.__edited_img = self.__editing_img.copy()
            self.__displayImage(self.__edited_img)
    
    
    def __cancelChanges(self):
        """
        - Discards the current implemented changes
        - Sets editing_img to edited_img
        """
        if self.__edited_img:
            self.__editing_img = self.__edited_img.copy()
            self.__displayImage(self.__editing_img)
            
    
    def __upload_image(self):
        """
        - Opening/Uploading image on the canvas
        - canvas.delete("all") clears the canvas first
        - Three copies are created while the destinationFile will be created
            during first call to save or all calls to save as
        """
        self.__filename = filedialog.askopenfilename(filetypes=Macros.FILETYPES)
        self.__destinationFile = None
        if os.path.isfile(self.__filename):
            self.__original_img = Image.open(self.__filename)
            self.__editing_img = Image.open(self.__filename)
            self.__edited_img = Image.open(self.__filename)
            self.__canvas.delete("all")
            self.__displayImage(self.__edited_img)
    

    def __cropImage(self):
        """
        - Crop image action divided in three stages
            - start() --> locks the top-left corner for crop when left-mouse button is clicked
            - crop() --> constantly resets the rectangle border displayed around the to-be-cropped image as cursor drags the bottom-right corner
            - end() --> locks the bottom-right corner for crop when left-mouse button is released
        """
        self.__refresh_side_frame()
        tkinter.Label(
            self.__side_frame, text="Click and drag\non image to crop", font=Macros.BUTTON_FONT,
            bg=Macros.APP_BG, fg=Macros.BUTTON_FG
        ).grid (row=0, column=0)
        
        self.rectangleId = 0
        self.startX, self.startY, self.endX, self.endY = 0, 0, 0, 0
        
        def start(event):
            self.startX, self.startY = event.x, event.y
            
        def crop(event):
            if self.rectangleId:
                self.__canvas.delete(self.rectangleId)
                
            self.endX, self.endY = event.x, event.y
            self.rectangleId = self.__canvas.create_rectangle(self.startX, self.startY, self.endX, self.endY, width=1)
        
        def end(event):
            self.endX, self.endY = event.x, event.y
            
            self.startX, self.endX = int(min(self.startX, self.endX) * self.__scaledRatio), int(max(self.startX, self.endX) * self.__scaledRatio)
            self.startY, self.endY = int(min(self.startY, self.endY) * self.__scaledRatio), int(max(self.startY, self.endY) * self.__scaledRatio)
            
            # Truncating cropping going outside the image
            width, height = self.__edited_img.size
            self.startX, self.endX = max(self.startX, 0), min(self.endX, width)
            self.startY, self.endY = max(self.startY, 0), min(self.endY, height)
            
            self.__editing_img = self.__edited_img.crop((self.startX, self.startY, self.endX, self.endY))
            self.__displayImage(self.__editing_img)
            
        self.__canvas.bind("<ButtonPress>", start)
        self.__canvas.bind("<B1-Motion>", crop)
        self.__canvas.bind("<ButtonRelease>", end)


    def __rotateLeft(self):
        """Counter-Clockwise rotation by 90 degrees"""
        if self.__editing_img:
            self.__editing_img = ImageEditor.rotateLeft(self.__editing_img)
            self.__edited_img = ImageEditor.rotateLeft(self.__edited_img)
            self.__displayImage(self.__editing_img)


    def __rotateRight(self):
        """Clockwise rotation by 90 degrees"""
        if self.__editing_img:
            self.__editing_img = ImageEditor.rotateRight(self.__editing_img)
            self.__edited_img = ImageEditor.rotateRight(self.__editing_img)
            self.__displayImage(self.__editing_img)


    def __flipHorizontal(self):
        """Left to Right Flip"""
        if self.__editing_img:
            self.__editing_img = ImageEditor.flipHorizontal(self.__editing_img)
            self.__edited_img = ImageEditor.flipHorizontal(self.__edited_img)
            self.__displayImage(self.__editing_img)


    def __flipVertical(self):
        """Top to Bottom Flip"""
        if self.__editing_img:
            self.__editing_img = ImageEditor.flipVertical(self.__editing_img)
            self.__edited_img = ImageEditor.flipVertical(self.__edited_img)
            self.__displayImage(self.__editing_img)


    def __splitChannel(self):
        """
        - Converts the given image into RGB type and then splits the red values, blue values and green values of the image based on selection.
        - Red Channel  Button shows the image when all green and blue pixels are set to 0.
        - green Channel  Button shows the image when all blue and red pixels are set to 0.
        - blue Channel  Button shows the image when all red and green pixels are set to 0.
        """
        self.__refresh_side_frame()
        
        # Added to ensurethat the dimensions of editing and edited images are same
        # When taking a particular channel value of pixels from edited image and putting it in editing image
        self.__editing_img = self.__edited_img.copy()
        
        tkinter.Button(self.__side_frame, text='Red Channel', font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__redChannel
                       ).grid(row=0, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        tkinter.Button(self.__side_frame, text='Green Channel', font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__greenChannel
                       ).grid(row=1, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        tkinter.Button(self.__side_frame, text='Blue Channel', font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__blueChannel
                       ).grid(row=2, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

    def __redChannel(self):
        """Shows the red value of all the image pixels"""
        if self.__edited_img:
            self.__editing_img = ImageEditor.redChannel(self.__edited_img)
            self.__displayImage(self.__editing_img)
 
    def __greenChannel(self):
        """Shows the green value of all the image pixels"""
        if self.__edited_img:
            self.__editing_img = ImageEditor.greenChannel(self.__edited_img)
            self.__displayImage(self.__editing_img)
    
    def __blueChannel(self):
        """Shows the blue value of all the image pixels"""
        if self.__edited_img:
            self.__editing_img = ImageEditor.blueChannel(self.__edited_img)
            self.__displayImage(self.__editing_img)
            
            
    def __filters(self):
        """Displays options for various filters available under 'Apply Filters' Menu Button"""
        self.__refresh_side_frame()
        
        tkinter.Button(
            self.__side_frame, text="Negative", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__negative
        ).grid(row=0, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self.__side_frame, text="Black And white", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__blackWhite
        ).grid(row=1, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self.__side_frame, text="Detect Edge", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__detectEdge
        ).grid(row=2, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self.__side_frame, text="Enhance Edge", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__enhanceEdge
        ).grid(row=3, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self.__side_frame, text="Pencil Sketch", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__sketch
        ).grid(row=4, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Scale(
            self.__side_frame, label="Thresholding", from_=0, to=256, font=Macros.BUTTON_FONT, orient='horizontal',
            fg=Macros.BUTTON_FG,bg=Macros.BUTTON_BG, command=self.__thresholding
        ).grid(row=5, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self.__side_frame, text="Erosion", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__erosion
        ).grid(row=6, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Button(
            self.__side_frame, text="Dilation", font=Macros.BUTTON_FONT, fg=Macros.BUTTON_FG, bg=Macros.BUTTON_BG, command=self.__dilation
        ).grid(row=7, column=2, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

    def __negative(self):
        """Inverts image. Subtracting each pixel value from white pixel"""
        if self.__edited_img:
            self._editing_img = ImageEditor.negative(self.__edited_img)
            self.__displayImage(self._editing_img)
    
    def __blackWhite(self):
        """Gray-Scale Conversion"""
        if self.__edited_img:
            self.__editing_img = ImageEditor.blackWhite(self.__edited_img)
            self.__displayImage(self.__editing_img)
            
    def __detectEdge(self):
        """
        - Detects and displays the edges of the image.
        - sharper the edge more clearly visible it will be.
        """
        if self.__edited_img:
            self.__editing_img = ImageEditor.detectEdge(self.__edited_img)
            self.__displayImage(self.__editing_img)
            
    def __enhanceEdge(self):
        """Enhances the contrast around the edges of the image to show them more distinctly."""
        if self.__edited_img:
            self.__editing_img = ImageEditor.enhanceEdge(self.__edited_img)
            self.__displayImage(self.__editing_img)
    
    def __sketch(self):
        """Converts the image into what it can look like as a pencil sketching"""
        if self.__edited_img:
            self.__editing_img = ImageEditor.sketch(self.__edited_img)
            self.__displayImage(self.__editing_img)
        
    def __thresholding(self, threshold):
        """Sets each pixel to either minimum value or maximum value based on a certain threshold value"""
        if self.__edited_img:
            self.__editing_img = ImageEditor.thresholding(self.__edited_img, int(threshold))
            self.__displayImage(self.__editing_img)
    
    def __erosion(self):
        """Decreases the amount of bright pixels from the image"""
        if self.__edited_img:
            self.__editing_img = ImageEditor.erosion(self.__edited_img)
            self.__displayImage(self.__editing_img)
            
    def __dilation(self):
        """Decreases the amount of dark pixels from the image"""
        if self.__edited_img:
            self.__editing_img = ImageEditor.dilation(self.__edited_img)
            self.__displayImage(self.__editing_img)
           
    
    def __levelAdjust(self):
        """
        - Adjust various levels of the image like brightness, saturation, contrast and more.
        - All level Scales' action commands have self-explanatory names
        """
        self.__refresh_side_frame()
        
        tkinter.Scale(self.__side_frame, from_=1, to=50, label='Blur', orient='horizontal',
                      font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG, command=self.__blurImage
                      ).grid(row=0, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        tkinter.Scale(self.__side_frame, from_=1, to=50, label='Sharpness', orient='horizontal',
                      font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG, command=self.__sharpenImage
                      ).grid(row=1, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        tkinter.Scale(self.__side_frame, from_=0.0, resolution=0.1, to=3.0, label='Brightness', orient='horizontal',
                      font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG, command=self.__brightenImage
                      ).grid(row=2, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

        tkinter.Scale(self.__side_frame, from_=0.0, resolution=0.1, to=3.0, label='Saturation', orient='horizontal',
                      font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG, command=self.__saturateImage
                      ).grid(row=3, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)
        
        tkinter.Scale(self.__side_frame, from_=0.0, resolution=0.1, to=3.0, label='Contrast', orient='horizontal',
                      font=Macros.BUTTON_FONT, bg=Macros.BUTTON_BG, fg=Macros.BUTTON_FG, command=self.__contrastImage
                      ).grid(row=4, column=0, padx=Macros.PADX, pady=Macros.PADY, sticky=Macros.BUTTON_STICKY)

    def __blurImage(self, value):
        if self.__edited_img:
            self.__editing_img = ImageEditor.blurImage(self.__edited_img, int(value))
            self.__displayImage(self.__editing_img)
            
    def __sharpenImage(self, value):
        if self.__edited_img:
            self.__editing_img = ImageEditor.sharpenImage(self.__edited_img, int(value))
            self.__displayImage(self.__editing_img)
    
    def __brightenImage(self, value):
        if self.__edited_img:
            self.__editing_img = ImageEditor.brightenImage(self.__edited_img, float(value))
            self.__displayImage(self.__editing_img)
            
    def __saturateImage(self, value):
        if self.__edited_img:
            self.__editing_img = ImageEditor.saturateImage(self.__edited_img, float(value))
            self.__displayImage(self.__editing_img)
            
    def __contrastImage(self, value):
        if self.__edited_img:
            self.__editing_img = ImageEditor.contrastImage(self.__edited_img, float(value))
            self.__displayImage(self.__editing_img)
            

    def run(self):
        """Executes self.__window.mainloop()"""
        self.__window.mainloop()


def main():
    app = ImageEditorUI()
    app.run()


if __name__ == "__main__":
    main()
