import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
     FigureCanvasTkAgg)
import tkinter as tk
from tkinter import messagebox, Label
import numpy as np
import random
import threading



#Variable global para almacenar las coordenadas
Xs = []

def on_click(event):
    if event.inaxes is not None:
        #Agrega las coordenadas a la lista
        if event.button == 1:
            Xs.append([1, event.xdata, event.ydata])
            plt.plot(event.xdata, event.ydata, 'ob')
            canvas.draw()
        else:
            Xs.append([1, event.xdata, event.ydata])
            plt.plot(event.xdata, event.ydata, 'or')
            canvas.draw()
    else:
        messagebox.showwarning("Fuera del plano", "Por favor haga click dentro del plano cartesiano")

def graficar_linea(n1, n2, n3, maximo):
    max_epocas = int(maximo)
    if max_epocas > 0:
        peso_1.config(text=n1)
        peso_2.config(text=n2)
        bias.config(text=n3)
        crear_grafica()

        w1 = float(n1)
        w2 = float(n2)
        b = float(n3)

        m = -w1/w2
        c = -b/w2

        plt.axline((0,c), slope=m, linewidth = 4)
        canvas.draw()
        prod_p(w1, w2, b)
        threading.Thread(target=graficar_linea, args=(w1+0.3, w2+0.5, b-0.1, max_epocas-1)).start()

    


def ini_datos():
    n1 = round(random.uniform(-1,1), 2)
    n2 = round(random.uniform(-1,1), 2)
    n3 = round(random.uniform(-1,1), 2)
    peso_1.config(text=n1)
    peso_2.config(text=n2)
    bias.config(text=n3)
    maximo = epocas.get("1.0", "end-1c")
    parametro = var_apr.get("1.0", "end-1c")
    if(is_int(maximo) and is_float(parametro)):
        if Xs:
            datos = Xs.copy()
            random.shuffle(datos)
            entr = datos[len(datos)//2:]
            prueb = datos[:len(datos)//2]

            for i in range(len(prueb)):
                plt.plot(prueb[i][1], prueb[i][2], "ok")
        
        canvas.draw()
        messagebox.showinfo("prueba", "probando")
        graficar_linea(n1, n2, n3, maximo)
    else:
        messagebox.showerror("Valores invalidos", "Las epocas deben ser enteros, el parametro de aprendizaje un flotante")
    
    

def prod_p(p1, p2, b):
    if Xs:
        W = np.array([b, p1, p2])
        X = np.array(Xs)
        y = np.dot(W, X.T) >= 0
        
        for i in range(len(y)):
            if (y[i] == 0):
                plt.plot(X[i][1], X[i][2], 'or')
            else:
                plt.plot(X[i][1], X[i][2], 'ob')
    
    canvas.draw()

def crear_grafica():
    plt.clf()
    plt.title("Practica 1")
    plt.grid("on")
    plt.xlim([-2,2])
    plt.ylim([-2,2])
    plt.xlabel(r"x1")
    plt.ylabel(r"x2")
    plt.draw()

def limpiar():
    Xs.clear()
    peso_1.config(text="0")
    peso_2.config(text="0")
    bias.config(text="0")
    crear_grafica()

def is_float(numero):
    try:
        float(numero)
        return(True)
    except:
        return False
    
def is_int(numero):
    try:
        int(numero)
        return(True)
    except:
        return False


# Initialize Tkinter and Matplotlib Figure
root = tk.Tk()
fig, ax = plt.subplots()
 
# Tkinter Application
frame = tk.Frame(root)
#frame.pack()

#Creaciones de campos de texto
Label(root, text="w1").grid(pady=5, row=0, column=0)
peso_1 = Label(root, text="0")
peso_1.grid(pady=5, row=0, column=1)


Label(root, text="w2").grid(pady=5, row=1, column=0)
peso_2 = Label(root, text="0")
peso_2.grid(pady=5, row=1, column=1)


Label(root, text="bias").grid(pady=5, row=2, column=0)
bias = Label(root, text="0")
bias.grid(pady=5, row=2, column=1)


Label(root, text="Epocas").grid(pady=5, row=0, column=2)
epocas = tk.Text(root, height = 1, width = 15)
epocas.grid(pady=5, row=0, column=3)

Label(root, text="Aprendizaje").grid(pady=5, row=1, column=2)
var_apr = tk.Text(root, height = 1, width = 15)
var_apr.grid(pady=5, row=1, column=3)


#Creación del boton
entrenar = tk.Button(root, height=1, width=15, text="Entrenar", command=lambda:ini_datos())
entrenar.grid(pady=5, padx=5, row=2, column=3)
resetear = tk.Button(root, height=1, width=15, text="Reiniciar", command=lambda:limpiar())
resetear.grid(pady=5, padx=5, row=2, column=2)
 
# Create Canvas
canvas = FigureCanvasTkAgg(fig, master=root)  
canvas.get_tk_widget().grid(row=3, column=0, columnspan=4)
 
# Plot data on Matplotlib Figure
t = np.arange(0, 2*np.pi, .01)
crear_grafica()
fig.canvas.callbacks.connect('button_press_event', on_click)
canvas.draw()
 
root.mainloop()