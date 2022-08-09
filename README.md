# Python-Image-Editor

A simple python based image editor. <br>

Divided into three files: <br>
<b>
Macros.py <br>
AppFrame.py <br>
App.py
</b>

<br>

### Macros.py
Consists of global constant values used repeatedly all through the code. <br><br>

### AppFrame.py
Consists of framework for the app. Consists of layout for save, save as, resetting, cancelling, and applying changes.

Consists of central canvas arounf which all the buttons are oriented.

Open image file and displaying image file functions are the only defined functions.

Menu options for cropping image, splitting channel, applying filters, and adjusting various levels like blur, brightness, contrast, saturation, and sharpness.

Rotating image, and flipping image icons set.

Resizing image button also available. <br><br>

### App.py
Extends <b>AppFrame.py</b> and implements the button on-click actions and scale-sliding actions for various features opened through the menu buttons.

## FEATURES
<hr>

- Save, save as to store the edited image.
- Option to restore original image, cancel changes, or apply the changes made.
- Direct access to cropping, rotating and flipping buttons.
- 4 Menu buttons for splitting channels, applying filters, adjusting various levels, and resizing.

- <b>Split Channel</b>
    - Splits the Red, Green, and Blue values of the Channel.
    - Each option shows the values of RGB in each pixel of the images as a new image.

- <b>Apply Filters</b>
    - Various filters can be applied like inverting image (negative), black and white image, edge detection, edge enhancement, pencil sketch effect, thresholding with a slider to set threshold value, erosion, and dilation.

- <b>Level Adjust</b>
    - Menu for adjusting various levels of image.
    - Includes blur, and sharpness ranging from 1 to 50.
    - Includes Brightness, Saturation, and Contrast ranging from 0 to 3.0.

- <b>Resize Image</b>
    - Displays the size of the opened image.
    - Textboxes to enter new width and height values.
    - 'Resize' button to resize the image.
    - Only resizes when both width and height are given and both are integers.