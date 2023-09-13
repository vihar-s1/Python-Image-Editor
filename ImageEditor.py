#!/usr/bin/env python

from PIL import Image, ImageFilter, ImageEnhance
from numpy import asarray

from tkinter import filedialog

def rotateLeft(image: Image.Image) -> Image.Image:
    """
    - Counter-clockwise rotation by 90 degrees
    """
    if not image: return
    return image.rotate(angle=90, expand=True)


def rotateRight(image: Image.Image) -> Image.Image:
    """
    - Clockwise rotation by 90 degrees
    """
    if not image: return
    return image.rotate(angle=-90, expand=True)


def flipHorizontal(image: Image.Image) -> Image.Image:
    """
    - Left to Right Flip
    """
    if not image: return
    return image.transpose(Image.Transpose.TRANSPOSE.FLIP_LEFT_RIGHT)


def flipVertical(image: Image.Image) -> Image.Image:
    """
    - Top to Bottom Flip
    """
    if not image: return
    return image.transpose(Image.Transpose.TRANSPOSE.FLIP_TOP_BOTTOM)


def cropImage(image: Image.Image, startX: int, startY: int, endX: int, endy: int) -> Image.Image:
    """
    Cropping the image after truncating the rectangle to be inside the image
    """
    if not image: return
    # truncating crop going outside the image
    width, height = image.size
    startX, endX = max(startX, 0), min(endX, width)
    startY, endY = max(startY, 0), min(endY, height)
    
    return image.crop((startX, startY, endX, endY))


def redChannel(image: Image.Image) -> Image.Image:
    """
    Shows the red value of all the image pixels
    """
    if not image: return
        
    image = image.copy()
    red = image.convert("RGB").getdata(0)
    red = [ (r, 0, 0) for r in red ]
    image.putdata(red)
    return image


def greenChannel(image: Image.Image) -> Image.Image:
    """
    Shows the green value of all the image pixels
    """
    if not image: return
    
    image = image.copy()
    green = image.convert("RGB").getdata(1)
    green = [ (0, g, 0) for g in green ]
    image.putdata(green)
    return image


def blueChannel(image: Image.Image) -> Image.Image:
    """
    Shows the blue value of all the image pixels
    """
    if not image: return
    image = image.copy()
    blue = image.convert("RGB").getdata(2)
    blue = [ (0, 0, b) for b in blue ]
    image.putdata(blue)
    return image


def negative(image: Image.Image) -> Image.Image:
    """
    Inverts Image. Subtracting each pixel value from white pixel
    """
    if not image: return
    return image.convert("RGB").point(lambda x: 255-x)
    

def blackWhite(image: Image.Image) -> Image.Image:
    """
    Gray-Scal conversion
    """
    if not image: return
    return image.convert("L")


def detectEdge(image: Image.Image) -> Image.Image:
    """
    Detects and displays the edges of the image.
    Sharper the edge, more visibility it will have in the output.
    """
    if not image: return
    return image.filter(ImageFilter.FIND_EDGES)
    
    
def enhanceEdge(image: Image.Image) -> Image.Image:
    """
    Enhances the contrast around the edges of the image to show them more distinctly.
    """
    if not image: return
    return image.filter(ImageFilter.EDGE_ENHANCE_MORE)


def sketch(image: Image.Image) -> Image.Image:
    """
    Converts the iamge into a pencil sketch type look
    """
    if not image: return
    
    img_gray = image.convert("L")
    img_smooth = img_gray.filter(ImageFilter.GaussianBlur(150))
    try: # To suppress RunTimeWarning of divide by zero, and Invalid Value encountered
        final = asarray(img_gray) / asarray(img_smooth) * 256.0
    except Exception:
        pass
    
    return Image.fromarray(final)
    
    
def thresholding(image: Image.Image, threshold: int) -> Image.Image:
    """
    Sets each pixel to either minimum value or maximum value depending if pixel is less than or greater than threshold respectively
    """
    if not image: return
    return image.point(lambda x: 256 if x >= threshold else 0)
    
    
def erosion(image: Image.Image) -> Image.Image:
    """
    Decreases the brightness of the image
    """
    if not image: return
    return image.filter(ImageFilter.MinFilter(3))
    
    
def dilation(image: Image.Image) -> Image.Image:
    """
    Decreases the darkness of the image
    """
    if not image: return
    return image.filter(ImageFilter.MaxFilter(3))
    
    
def blurImage(image: Image.Image, value: int) -> Image.Image:
    if not image: return
    return image.filter(ImageFilter.GaussianBlur(value))
    
    
def sharpenImage(image: Image.Image, value: int) -> Image.Image:
    if not image: return
    return ImageEnhance.Sharpness(image).enhance(value)
    
    
def brightenImage(image: Image.Image, value: float) -> Image.Image:
    if not image: return
    return ImageEnhance.Brightness(image).enhance(value)
    
    
def saturateImage(image: Image.Image, value: float) -> Image.Image:
    if not image: return
    return ImageEnhance.Color(image).enhance(value)
    
    
def contrastImage(image: Image.Image, value: float) -> Image.Image:
    if not image: return
    return ImageEnhance.Contrast(image).enhance(value)
    
    
def resizeImage(image: Image.Image, size: tuple[int,int]) -> Image.Image:
    try:
        if not image: return
        image = image.resize(size)
    except:
        pass
    return image
        

def saveAsImage(image: Image.Image, destinationFile: str) -> str:
    """
        - Asks user to select the destination for saving the "image" with user-selected extension.
        - Overwrite confirmation by user required.
    """
    if not image: return
    
    filename = filedialog.asksaveasfilename(confirmoverwrite=True)
    if not filename: # filename invalid
        return
    
    extension = destinationFile.split('.')[-1]  # destination file extension
    if len(filename.split('.')) > 1: # must have name + extension  
        image.save(fp=filename)
        return filename
    else: # only name so auto append extension
        image.save(fp=filename + '.' + extension)
        return filename + '.' + extension


def saveImage(image: Image.Image, destinationFile: str) -> str:
    """
    - Saves image overwriting the last saved image location (destinationFile).
    - The first saveImage call for the given image has destinationFile as None and so defaults to saveAsImage call.
    """
    if image:
        if destinationFile:
            image.save(fp=destinationFile)
        else:
            return saveAsImage(image, ".png")
