# Python-Image-Editor

- A simple python based image editor.
- Divided into three files:
  - **[Macros.py](#macrospy)**
  - **[ImageEditor.py](#imageeditorpy)**
  - **[EditorUI.py](#editoruipy)**

## Macros.py

Consists of global constant values used repeatedly all through the code.

## ImageEditor.py

Consists all the functions for image editing. A generalized module for image editing.

## EditorUI.py

The UI of Image Editor which uses the functions defined in the ImageEditor.py to perform image editing in the background.

## FEATURES

---

- Save, save as to store the edited image.
- Option to restore original image, cancel changes, or apply the changes made.
- Direct access to cropping, rotating and flipping buttons.
- 4 Menu buttons for splitting channels, applying filters, adjusting various levels, and resizing.

- **Split Channel**
  - Splits the Red, Green, and Blue values of the Channel.
  - Each option shows the values of RGB in each pixel of the images as a new image.

- **Apply Filters**
  - Various filters can be applied like inverting image (negative), black and white image, edge detection, edge enhancement, pencil sketch effect, thresholding with a slider to set threshold value, erosion, and dilation.

- **Level Adjust**
  - Menu for adjusting various levels of image.
  - Includes blur, and sharpness ranging from 1 to 50.
  - Includes Brightness, Saturation, and Contrast ranging from 0 to 3.0.

- **Resize Image**
  - Displays the size of the opened image.
  - Textboxes to enter new width and height values.
  - 'Resize' button to resize the image.
  - Only resizes when both width and height are given and both are integers.

## Executables (.exe)

Converted to executable via auto-py-to-exe module of python.

Contains two executables and their respective spec files.

- **ConsoleBasedApp**
  - The executable is based on console interface. On running, a console screen will open which will then in turn run the application interface.

```bash
pyinstaller --noconfirm --onefile --console --add-data "./static/;static/" ./EditorUI.py
rm -rf build EditorUI.spec
mv dist consoleBased
```

- **WindowBasedApp**
  - The executable uses a window as an interface. It hides the console while opening the app.

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "./static/;static/" ./EditorUI.py
rm -rf build EditorUI.spec
mv dist WindowBased
```

- The **--add-data** flag in both the case tells the **pyinstaller** to include the specified file/folder in the executable file. The **static/** tells the executable where to extract the data while running. The extracted data is temporary and is deleted once app closes.
- Alternately, simply run the bash script `createExecutable.sh` to create both in one go.

```bash
bash createExecutable.sh
```
