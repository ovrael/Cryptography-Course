# img_viewer.py

#from unicodedata import name
from steganography import Steganography
import PySimpleGUI as sg
import os.path
from PIL import Image, ImageTk  # Image for open, ImageTk for display


def showInformationWindow(informationText, windowTitle, size=(300, 150)):
    informationLayout = [
        [sg.Text(informationText)],
        [sg.Button("OK")]
    ]

    # Create the window
    informationWindow = sg.Window(windowTitle, informationLayout, size=size)

    # Create an event loop
    while True:
        event, values = informationWindow.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    informationWindow.close()


def showDecodeWindow():
    decodeLayout = [
        [
            sg.Text("Choose image with encoded message"),
            sg.In(size=(25, 1), enable_events=True, key="encodedFilePath"),
            sg.FileBrowse(),
        ],
        [
            [sg.Button("Reveal text", key="revealTextButton")],
        ]
    ]

    # Create the window
    decodeWindow = sg.Window("Decoding!", decodeLayout)

    # Create an event loop
    while True:
        event, values = decodeWindow.read()
        # End program if user closes window or
        # presses the OK button

        print("Event: " + event)
        if event == "OK" or event == sg.WIN_CLOSED:
            break

        elif event == "revealTextButton":
            imgPath = values["encodedFilePath"]
            message = Steganography.decode(imgPath)
            if len(message) > 0:
                showInformationWindow(
                    "Message: " + message, "Successful decoding!")
            else:
                showInformationWindow("Couldn't decode message")

    decodeWindow.close()
# First the window layout in 2 columns


file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="folder"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="fileList"
        )
    ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="tout")],
    [sg.Image(key="image")],
    [sg.Input("Write text to hide", key="textToHide")],
    [
        sg.Button("Hide text", key="hideTextButton"),
        sg.Button("Reveal text", key="revealTextButton"),
    ],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Image Viewer", layout)
imageSet = False
currentImage = None
imagePath = None

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "folder":
        imageSet = False
        folder = values["folder"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png"))
        ]
        window["fileList"].update(fnames)

    elif event == "fileList":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["folder"], values["fileList"][0]
            )
            imagePath = filename
            currentImage = Image.open(filename)
            window["tout"].update(filename)
            window["image"].update(
                data=ImageTk.PhotoImage(currentImage)
            )
            imageSet = True
        except:
            imageSet = False
            pass

    elif event == "hideTextButton":  # A file was chosen from the listbox
        try:
            if not imageSet:
                showInformationWindow(
                    "You must select an image file", "Warning")
                continue

            textToHide = values["textToHide"]
            if (len(textToHide) == 0):
                showInformationWindow(
                    "Text to hide cannot be empty", "Warning")
                continue

            result = ""

            try:
                result = Steganography.encode(imagePath, values["textToHide"])
            except Exception as e:
                showInformationWindow("Error: " + e, "Error")
                continue

            if len(result) > 0:
                showInformationWindow(
                    "File saved at: " + result, "Information")

        except:
            pass

    elif event == "revealTextButton":
        try:
            showDecodeWindow()

        except:
            pass

window.close()
