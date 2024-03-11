import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox, Label
import numpy as np
import random
import threading

#Lista de todas las coordenadas en el plano
#Cada elemento tiene: Bias, coord x, coord y
Xs = []


def on_click(event):
    #Cuando se hace un click dentro del plano, agrega la coordenada a la lista
    if event.inaxes is not None: #Checa que se encuentre dentro del plano
        bias = 1 #Bias de la entrada
        coord_x = event.xdata #Coordenada X del punto
        coord_y = event.ydata #Coordenada Y del punto
        if event.button == 1: #Checa si fue con click izquierdo
            salida = 1 #Salida deseada
            Xs.append([bias, coord_x, coord_y, salida]) #Se agrega a la lista de coordenadas
            plt.plot(coord_x, coord_y, "ob") #Se grafica el punto de color azul
            canvas.draw() #Se actualiza la figura
        else:
            #El click fue un click derecho
            salida = 0 #Salida deseada
            Xs.append([bias, coord_x, coord_y, salida]) #Se agrega a la lista de coordenadas
            plt.plot(coord_x, coord_y, "or") #Se grafica el punto de color rojo
            canvas.draw() #Se actualiza la figura
    else:
        #Se hizo click fuera del rango del plano, se muestra el warning correspondiente
        messagebox.showwarning("Fuera del plano", "Por favor haga click dentro del plano")

def ini_datos():
    #Se asigna un valor al azar a nuestros pesos, entre -1 y 1 con 2 decimales
    n1 = round(random.uniform(-1,1), 2)
    n2 = round(random.uniform(-1,1), 2)
    n3 = round(random.uniform(-1,1), 2)
    #Se modifica el texto del label para reflejar los valores iniciales
    peso_1.config(text=n1)
    peso_2.config(text=n2)
    bias.config(text=n3)
    #Obtenemos el maximo de epocas (iteraciones) y el parametro de aprendizaje de nuestra UI
    maximo = epocas.get("1.0", "end-1c")
    parametro = var_apr.get("1.0", "end-1c")
    #Comprobamos que las epocas sean enteros y el parametro un decimal
    if(is_int(maximo) and is_float(parametro)):
        if Xs: #Checamos si Xs tiene elementos
            datos = Xs.copy() #Copiamos el contenido de la lista de coordenadas
            random.shuffle(datos) #Cambiamos el orden de la lista a uno aleatorio
            testing = datos[:len(datos)//2] #La mitad de los datos se vuelven nuestros datos de prueba
            training = [elemento for elemento in Xs if elemento not in testing] #los datos de entrenamiento son las coordenadas que no se encuentren en la lista de prueba
            for i in range(len(testing)):  #Recorremos nuestros datos de prueba
                plt.plot(testing[i][1], testing[i][2], "ok") #Encimamos un punto negro para simular que cambiamos su color

            canvas.draw() #Actualizamos los nuevos puntos de color negro
            messagebox.showinfo("Datos cargados", "Datos de prueba seleccionados") #Usamos showinfo para pausar y que el usuario note que datos se modificaron
            #Llamamos a la funcion que va a entrenar nuestro perceptron, le damos los valores iniciales y el maximo de epocas
            entrenar_perceptron(n1, n2, n3, maximo, parametro, training) 
    else:
        #En caso de que un valor fuera invalido
        messagebox.showerror("Valor invalido", "Las epocas deben ser un entero, y el parametro de aprendizaje un flotante")

def entrenar_perceptron(n1, n2, n3, maximo, parametro, entrenamiento, error = True, ):
    n1 = float(n1)
    n2 = float(n2)
    n3 = float(n3)
    max_epocas = int(maximo)
    if max_epocas == 0:
        epocas.delete("1.0", "end-1c")
        epocas.insert(tk.END, "0")
    if error == True:
        errores = []
        bandera = True
        peso_1.config(text=n1) 
        peso_2.config(text=n2)
        bias.config(text=n3)
        epocas.delete("1.0", "end-1c")
        epocas.insert(tk.END, maximo)
        plt.clf() #Borramos la linea previa, hacerlo involucra borrar todo el plano
        crear_plano() #Volvemos a crear el plano

        
        if max_epocas > 0:
            crear_linea(n1, n2, n3)
            prod_punto(n1, n2, n3)
            for i in range(len(entrenamiento)):
                fallo = calc_error(n1, n2, n3, i, entrenamiento)
                error = (entrenamiento[i][-1]) - fallo
                errores.append(error)
                parametro = float(parametro)
                n1 = n1 + parametro * error * entrenamiento[i][1]
                n2 = n2 + parametro * error * entrenamiento[i][2]
                n3 = n3 + parametro * error * entrenamiento[i][0]
        
        print(errores)
        
        if (1 in errores) or (-1 in errores):
            bandera = True
        else:
            bandera = False

        t1 = threading.Thread(target=entrenar_perceptron, args=(n1, n2, n3, max_epocas-1, parametro, entrenamiento, bandera))
        t1.start()
    max_epocas = max_epocas - 1            
    crear_linea(n1, n2, n3)
    prod_punto(n1, n2, n3)


def crear_linea(n1, n2, n3):
    w1 = n1
    w2 = n2
    b = n3
    #Valores de una recta 
    m = -w1/w2
    c = -b/w2

    #Graficamos nuestra recta
    plt.axline((0,c), slope=m, linewidth = 4)
    canvas.draw()

def prod_punto(p1, p2, b):
    if Xs:
        prueba = [sublist[:-1] for sublist in Xs]
        W = np.array([b, p1, p2])
        X = np.array(prueba)
        y = np.dot(W, X.T) >= 0
        
        for i in range(len(y)):
            if (y[i] == 0):
                plt.plot(X[i][1], X[i][2], 'or')
            else:
                plt.plot(X[i][1], X[i][2], 'ob')
    
    canvas.draw()

def calc_error(p1, p2, b, indice, training):
    W = np.array([b, p1, p2]) #Vector de pesos
    patron = training[indice] #Nuestro primer grupo de coordenadas es una epoca
    X = np.array(patron[:-1]) #Vector de entradas, eliminamos la salida deseada
 
    y = np.dot(W, X.T) >= 0 #Vemos el resultado del producto punto y checamos si es mayor a 0
    if y == 0:
        return 0
    else: #De ser mayor a 0, graficamos un punto azul y retornamos 1
        return 1

def crear_plano():
    plt.title("Practica 2") #Titulo del plano
    plt.grid("on") #Le pone un grid al plano
    plt.xlim([-2,2]) #Rango del valor de la coordenada x
    plt.ylim([-2,2]) #Rango del valor de la coordenada Y
    plt.xlabel(r"x1") #Indica cual valor es X1
    plt.ylabel(r"x2") #Indica cual valor es X2
    plt.draw() #Coloca todos los elementos en el plano

def limpiar():
    plt.clf() #EBorra todos los elementos que se encuentran en el plano
    Xs.clear() #Elimina todos los elementos de la lista de coordenadas
    #Regresa el valor de los Labels a 0 
    peso_1.config(text="0")
    peso_2.config(text="0")
    bias.config(text="0")
    crear_plano() #Restaura los elementos principales del plano

def is_float(numero):
    #Intentamos ver si es posible convertir un string a un numero flotante
    try: #De ser posible, regresa verdadero
        float(numero)
        return(True)
    except: #caso contrario, regresa falso
        return False
    
def is_int(numero):
    #Intentamos ver si es posible convertir un string a un numero entero
    try: #De ser posible, regresa verdadero
        int(numero)
        return(True)
    except: #Caso contrario, regresa falso
        return False
    

#Se inicializa Tkinter y la figura de Matplotlib
root = tk.Tk()
fig, ax = plt.subplots()

# Tkinter Application
frame = tk.Frame(root)

#Creaciones de campos de texto
#Se utiliza el label para colocar el nombre del dato a ingresar
#Como el usuario no debe modificar este valor, tambien se implementó como Label
#row y column indican la posición en base a un grid
#pady el margen respecto a los elementos que tiene encima y debajo
#Text el contenido o mensaje que muestran en pantalla 
Label(root, text="w1").grid(pady=5, row=0, column=0) #Primer peso del vector W
peso_1 = Label(root, text="0") 
peso_1.grid(pady=5, row=0, column=1) 


Label(root, text="w2").grid(pady=5, row=1, column=0) #Segundo peso del vector W
peso_2 = Label(root, text="0")
peso_2.grid(pady=5, row=1, column=1)


Label(root, text="bias").grid(pady=5, row=2, column=0) #Peso 0 del vector W
bias = Label(root, text="0")
bias.grid(pady=5, row=2, column=1) 

#Estos valores se deben ser modificables, por lo que se implementaron como cajas de texto
#Height y width es el tamaño que tienen dentro de la interfaz
Label(root, text="Epocas").grid(pady=5, row=0, column=2) #Maximo de epocas del programa
epocas = tk.Text(root, height = 1, width = 15)
epocas.grid(pady=5, row=0, column=3)

Label(root, text="Aprendizaje").grid(pady=5, row=1, column=2) #Parametro de aprendizaje
var_apr = tk.Text(root, height = 1, width = 15)
var_apr.grid(pady=5, row=1, column=3)

#Botones
#Command=lambda: indica la función que se ejecuta al presionarlos
entrenar = tk.Button(root, height=1, width=15, text="Entrenar", command=lambda:ini_datos())
entrenar.grid(pady=5, padx=5, row=2, column=3)
resetear = tk.Button(root, height=1, width=15, text="Reiniciar", command=lambda:limpiar())
resetear.grid(pady=5, padx=5, row=2, column=2)

# Se crea en cambas dentro del grid, requiere 4 columnas de espacio
canvas = FigureCanvasTkAgg(fig, master=root)  
canvas.get_tk_widget().grid(row=3, column=0, columnspan=4)

# Plot data on Matplotlib Figure
t = np.arange(0, 2*np.pi, .01)
crear_plano() #Llamamos a la función que tiene los parametros del plano
fig.canvas.callbacks.connect('button_press_event', on_click) #Detecta si hubo un click
canvas.draw() #Actualiza la figura
 
root.mainloop() #Ejecuta nuestra interfaz grafica