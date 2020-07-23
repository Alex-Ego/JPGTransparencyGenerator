import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import Transparency as tp

root= tk.Tk()
root.title("Generador de transparencias para iconos")

X = 600
Y = 300

import_file_path = "No has subido ningun archivo"

canvas1 = tk.Canvas(root, width = X, height = Y, relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='Generador de transparencias para iconos')
label2 = tk.Label(root, text='Ingresa una imagen con el fondo blanco para eliminarlo')
label1.config(font=('helvetica', 20))
label2.config(font=('helvetica', 15))
canvas1.create_window(X//2, 50, window=label1)
canvas1.create_window(X//2, 80, window=label2)

def check_img():
    global im1
    try:
        if im1:
            return True
    except:
        return False

def getIMG():
    global im1
    global import_file_path
    try:
        import_file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg")])
        im1 = Image.open(import_file_path)
        cleaner = tk.Label(root, text="                                                                                             ")
        cleaner.config(font=('helvetica', 10))
        canvas1.create_window(X//2, Y-120, window=cleaner)
        img_status = tk.Label(root, text=import_file_path)
        img_status.config(font=('helvetica', 10))
        canvas1.create_window(X//2, Y-120, window=img_status)
    except AttributeError:
        pass
    

browseButton_IMG = tk.Button(text="Importar Imagen", command=getIMG, bg='royalblue', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(X//2, Y-150, window=browseButton_IMG)
img_status_default = tk.Label(root, text="No has subido ningun archivo")
img_status_default.config(font=('helvetica', 10))
canvas1.create_window(X//2, Y-120, window=img_status_default)

def convertToPNG ():
    if check_img() == True:
        #try:
        #global import_file_path
        export_file_path = filedialog.asksaveasfilename(filetypes=[("Transparent PNG", ".png")])
        print(export_file_path)
        transparent_img = tp.EliminarFondo(import_file_path, export_file_path)
        #except:
        #    pass

saveAsButton_PNG = tk.Button(text='Eliminar fondo', command=convertToPNG, bg='royalblue', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(X//2, Y-80, window=saveAsButton_PNG)

root.mainloop()
