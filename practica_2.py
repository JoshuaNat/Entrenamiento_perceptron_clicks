import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
     FigureCanvasTkAgg)
import tkinter as tk
from tkinter import messagebox, Label
import numpy as np

#Variable global para almacenar las coordenadas
Xs = []

def on_click(event):
    if event.inaxes is not None:
        #Agrega las coordenadas a la lista
        Xs.append([1, event.xdata, event.ydata])
        plt.plot(event.xdata, event.ydata, 'ok')
        canvas.draw()
    else:
        messagebox.showwarning("Fuera del plano", "Por favor haga click dentro del plano cartesiano")

def graficar_linea():
    texto1 = peso_1.get("1.0", "end-1c")
    texto2 = peso_2.get("1.0", "end-1c")
    texto3 = bias.get("1.0", "end-1c")

    if (is_float(texto1) and is_float(texto2) and is_float(texto3)):
        crear_grafica()

        w1 = float(texto1)
        w2 = float(texto2)
        b = float(texto3)

        m = -w1/w2
        c = -b/w2

        plt.axline((0,c), slope=m, linewidth = 4)
        canvas.draw()
        prod_p(w1, w2, b)
    
    else:
        messagebox.showerror("Valor invalido", "Todos los valores deben ser numeros flotantes")
        


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
    ms1 = "W1"
    ms2 = "W2"
    ms3 = "Bias"
    Xs.clear()
    peso_1.delete("1.0", "end-1c")
    peso_1.insert(tk.END, ms1)
    peso_2.delete("1.0", "end-1c")
    peso_2.insert(tk.END, ms2)
    bias.delete("1.0", "end-1c")
    bias.insert(tk.END, ms3)
    crear_grafica()

def is_float(numero):
    try:
        float(numero)
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
peso_1 = tk.Text(root, height = 1, width = 15, state="disabled").grid(pady=5, row=0, column=1)
Label(root, text="w2").grid(pady=5, row=1, column=0)
peso_2 = tk.Text(root, height = 1, width = 15, state="disabled").grid(pady=5, row=1, column=1)
Label(root, text="bias").grid(pady=5, row=2, column=0)
bias = tk.Text(root, height = 1, width = 15, state="disabled").grid(pady=5, row=2, column=1)
Label(root, text="Epocas").grid(pady=5, row=0, column=2)
epocas = tk.Text(root, height = 1, width = 15).grid(pady=5, row=0, column=3)
Label(root, text="Aprendizaje").grid(pady=5, row=1, column=2)
var_apr = tk.Text(root, height = 1, width = 15).grid(pady=5, row=1, column=3)


#Creación del boton
entrenar = tk.Button(root, height=1, width=15, text="Entrenar", command=lambda:graficar_linea())
entrenar.grid(pady=5, padx=5, row=2, column=3)
resetear = tk.Button(root, height=1, width=15, text="Reiniciar", command=lambda:limpiar())
resetear.grid(pady=5, padx=5, row=2, column=2)
 
# Create Canvas
canvas = FigureCanvasTkAgg(fig, master=root)  
#canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
 
# Plot data on Matplotlib Figure
t = np.arange(0, 2*np.pi, .01)
crear_grafica()
fig.canvas.callbacks.connect('button_press_event', on_click)
canvas.draw()
 
root.mainloop()