# Image Manual Classification Helper

Select a directory and view and label all the image files inside the directory into up to 10 classes.

## How to use

1. Create a virtual environment (optional): `python3 -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate`
3. Install necessary libraries: `pip install -r requirements.txt`
4. Run the program using `python main.py`
5. Select directory
6. Navigate through images using left/right arrow keys
7. Press 0-9 to label the image
8. Press <kbd>Q</kbd> to quit the application. Before quitting, the application will move the images into subdirectories inside the selected directory with assigned label numbers.
9. Rename the numeric subdirectories as necessary.
