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
Icon images are saved in static folder...all four images are needed for them to be displayed.

<b>left rotate icon name: </b> <i>rotate_left.png</i><br>
<b>right rotate icon name: </b> <i>rotate_right.png</i><br>
<b>horizontal flip icon name: </b> <i>flip_horizontal.png</i><br>
<b>vertical flip icon name: </b> <i>flip_veritcal.png</i><br>

Resizing image button also available. <br><br>

The <b>resource_path</b> is defined so that when the project is compiled into a .exe file, the images are not needed to be explicitly provided.
On running the executable, it extracts the additional files/folders into the system's temporary folder. The <b>resource_path</b> checks this for temporary folder and if it exists, it returns base path as the temp folder, otherwise, the current folder is returned as the base folder for the additional files/folders.

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

## Executables (.exe)
<hr>

Contains two executables and their respective spec files.

- <b>ConsoleBasedApp</b>
    - The executable is based on console interface. On running, a console screen will open which will then in turn run the application interface.
    - The command to compile the executable as console based executable is as follows:
    
    ![](https://user-images.githubusercontent.com/96971096/187042709-32bbefc9-e23b-43fd-928c-9ca3177494ea.png)

- <b>WindowBasedApp</b>
    - THe executable uses a window as an interface. It hides the console while opening the app.
    - The command to compile the executable as window based executable is as follows:

   ![](https://user-images.githubusercontent.com/96971096/187042767-68656c6c-e16f-49f5-abf9-3c79d7ff72e2.png)

The <b>--add-data</b> flag in both the case tells the <b>pyisntaller</b> to include the specified file/folder in the executable file. The <b>static/</b> tells the executable where to extract the data while running. The extracted data is temporary and is deleted once app closes.