# CREATING CONSOLE BASED EXECUTABLE (Helpful to see log statements)
pyinstaller --noconfirm --onefile --console --add-data "./static/;static/" ./EditorUI.py
rm -rf build EditorUI.spec
mv dist consoleBased

# CREATING WINDOW BASED EXECUTABLE (Regular Executable)
pyinstaller --noconfirm --onefile --windowed --add-data "./static/;static/" ./EditorUI.py
rm -rf build EditorUI.spec
mv dist WindowBased