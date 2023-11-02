from tkinter import filedialog
from tkinter import StringVar, IntVar, Tk
from tkinter.ttk import Frame, Label, Entry, Button, Checkbutton
import tkinter as tk
import os
import pathlib

# Variables initialization
global bShowImage
bShowImage = False

window = Tk()
window.title("Ofuscado caras y matrículas")
# window.iconbitmap(r'C:/PROYECTOS/DETECTION_AND_BLUR/data/logo1.ico')
inputFolder = StringVar()
modelFolder = StringVar()
outputFolder = StringVar()
labelmapFile = StringVar()
widthDim = StringVar()
heightDim = StringVar()
checkbtnVar = IntVar()

def askdirectory(field):
    file_path = filedialog.askdirectory(initialdir="C:/Datasets")
    if field=="input":
        inputFolder.set(file_path)
    elif field == "output":
        outputFolder.set(file_path)
    print(file_path)


def width_text_changed(*args):
    print(widthDim.get())


def height_text_changed(*args):
    print(widthDim.get())


def run():
    print("Input folder: " + inputFolder.get())
    print("Output folder: " + outputFolder.get())
    os.path.join(os.path.dirname(__file__))
    directory = __file__
    directory = directory.split('\\')
    curr_path = ""
    for i in range(len(directory)-1):
        # = curr_path + directory[i] + "/"
        curr_path = str(pathlib.Path().resolve())
    print(curr_path)

    #if(len(widthDim.get==())==0 or len(heightDim.get())==0):
    if checkbtnVar.get()==1:
        os.system('python ' + curr_path + '/review_images.py --input "' + inputFolder.get() +
                  '/" --fscreen True'  
                  ' --output  "' + outputFolder.get())
    else:
        os.system('python ' + curr_path + '/review_images.py --input "' + inputFolder.get() +
                  '/" --fscreen False ' +
                  ' --output  "' + outputFolder.get())

def main():

    # Selection of the folder which contains the input images
    frame1 = Frame()
    frame1.pack(side=tk.TOP)
    lbl_input = Label(frame1, text="Carpeta que contiene las imágenes")
    txtInput = Entry(frame1, width=30, textvariable=inputFolder)
    btn_input = Button(frame1, text="Explorar", command=lambda: askdirectory("input"))
    lbl_input.pack(side=tk.LEFT)
    txtInput.pack(side=tk.LEFT)
    btn_input.pack(side=tk.LEFT)

    # Selection of the folder where blurred images will be saved
    frame2 = Frame()
    frame2.pack(side=tk.TOP)
    lbl_output = Label(frame2, text="Carpeta dónde guardar las imágenes")
    txtOutput = Entry(frame2, width=30, textvariable=outputFolder)
    btn_Output = Button(frame2, text="Explorar", command=lambda: askdirectory("output"))
    lbl_output.pack(side=tk.LEFT)
    txtOutput.pack(side=tk.LEFT)
    btn_Output.pack(side=tk.LEFT)

    # Selection of the dimensions for visualizing images
    frame4 = Frame()
    frame4.pack(side=tk.TOP)
    ckbtn_fscreen = Checkbutton(frame4, text="Pantalla Completa ", variable=checkbtnVar,
                onvalue=1, offvalue=0)
    ckbtn_fscreen.pack(side=tk.LEFT)

    # Button to run process
    frame3 = Frame()
    frame3.pack(side=tk.TOP)
    btn_run = Button(frame3, text="Ejecutar",command=lambda: run())
    btn_run.pack(side=tk.LEFT)

    widthDim.trace_add('write', width_text_changed)
    heightDim.trace_add('write', height_text_changed)

    window.mainloop()


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass