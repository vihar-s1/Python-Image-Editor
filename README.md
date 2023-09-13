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

### ImageEditor.py
Consists all the functions for image editing. A generalized module for image editing.

### EditorUI.py
The UI of Image Editor which uses the functions defined in the ImageEditor.py to perform image editing in the background.

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

## Executables (.exe)

Converted to executable via auto-py-to-exe module of python.
<hr>

Contains two executables and their respective spec files.

- <b>ConsoleBasedApp</b>
    - The executable is based on console interface. On running, a console screen will open which will then in turn run the application interface.

- <b>WindowBasedApp</b>
    - The executable uses a window as an interface. It hides the console while opening the app.

The <b>--add-data</b> flag in both the case tells the <b>pyisntaller</b> to include the specified file/folder in the executable file. The <b>static/</b> tells the executable where to extract the data while running. The extracted data is temporary and is deleted once app closes.