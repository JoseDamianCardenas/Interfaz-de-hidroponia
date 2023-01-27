from time import sleep
import threading
import tkinter as tk
from tkinter import messagebox
from customtkinter import *
import cv2
import imutils
from PIL import Image
from PIL import ImageTk
import time                             #Importamos el paquete time
import math
import datetime
from tktooltip import ToolTip
import sqlite3
import matplotlib.pyplot as plt
import os.path

from w1thermsensor import W1ThermSensor #Importamos el paquete W1ThermSensor
import bme280
import smbus2

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import RPi.GPIO as GPIO
import numpy as np


set_appearance_mode("Dark")
set_default_color_theme("dark-blue")

window = CTk()
window.title('Hidroponia')
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d" %(width,height))

def cerrar_interfaz():
    continuous_threading.shutdown(0)
    leer_datos()
    GPIO.cleanup()
    window.destroy()

frame1 = CTkFrame(master=window, width=1800, height= 200)
frame1.pack(fill=BOTH, side=LEFT, expand=True)
frame2 = CTkFrame(master=window, width=100)
frame2.pack(fill=BOTH, side=LEFT)
frame2.rowconfigure(0,weight=4)
frame2.rowconfigure(1,weight=1)#label ph
frame2.rowconfigure(2,weight=1)#cuadro ph
frame2.rowconfigure(3,weight=1)
frame2.rowconfigure(4,weight=1)#temp
frame2.rowconfigure(5,weight=1)
frame2.rowconfigure(6,weight=1)
frame2.rowconfigure(7,weight=1)#hum
frame2.rowconfigure(8,weight=1)
frame2.rowconfigure(9,weight=1)
frame2.rowconfigure(10,weight=1)#temp
frame2.rowconfigure(11,weight=1)
frame2.rowconfigure(12,weight=1)
frame2.rowconfigure(13,weight=1)#cond
frame2.rowconfigure(14,weight=1)
frame2.rowconfigure(15,weight=2000)
frame2.columnconfigure(0,weight=1)
frame2.columnconfigure(1,weight=1)
frame3 = CTkFrame(master=window, width=100)
frame3.pack(fill=BOTH, side=LEFT)
framebotones = CTkFrame(frame1)
framebotones.pack(side=TOP)
frameSelPlanta = CTkFrame(frame1)
frameSelPlanta.pack(side=TOP)

espacio1=CTkLabel(frame2,text="")
espacio1.grid(row=3,column=0)
espacio2=CTkLabel(frame2,text="")
espacio2.grid(row=6,column=0)
espacio3=CTkLabel(frame2,text="")
espacio3.grid(row=9,column=0)
espacio4=CTkLabel(frame2,text="")
espacio4.grid(row=12,column=0)


i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

titulo2 = CTkLabel(frame2, text="Sensores",font=("Georgia Pro",18))
titulo2.grid(column=0,row=0,padx=10, pady=(20,25))
SaveDataLabel = CTkLabel(frame2, text="¿Guardar datos?")
#SaveDataLabel.grid(column=0,row=1,padx=5)
switch_var = StringVar(value = "off")
#def switch_event():    
SaveDataSwitch = CTkSwitch(frame2, text ="¿Guardar datos?", variable=switch_var, onvalue="on", offvalue="off",font=("Georgia Pro",12))
SaveDataSwitch.grid(column=0,row=1,sticky='e',padx=(0,20))
label1 = CTkLabel(frame2, text="pH",font=("Georgia Pro",12))
label1.grid(column=0,row=4,padx=5,pady=5)
#(column=1,row=14,sticky='e',padx=(0,20))

      
def SpH():
    
    phsensor = AnalogIn(ads, ADS.P3).value
    phsensor = round((phsensor+11149.625)/3680.709,2)
    pHSV.set(round(phsensor,1))
    window.after(1000,SpH)
    
pHSV=StringVar()

Entry1 = CTkEntry(frame2,textvariable=pHSV, justify=CENTER)
Entry1.grid(column=0,row=5,padx=5, pady=1)
ToolTip(Entry1,msg="Rango ideal de 5.5 a 6.5",delay=0,padx=10,pady=10,font=("Georgia Pro",12))
SpH()
Entry1.configure(state= DISABLED)

label2 = CTkLabel(frame2,text="Temperatura del agua (°C)",font=("Georgia Pro",12))
label2.grid(column=0,row=7,padx=5, pady=5)

def Stemp():
    temperatura = sensor.get_temperature()
    TempSV.set(round(temperatura,0))
    window.after(1000,Stemp)
    
TempSV=StringVar()

sensor = W1ThermSensor()
    
Entry2 = CTkEntry(frame2,textvariable=TempSV, justify=CENTER,font=("Georgia Pro",12))
Entry2.grid(column=0,row=8,padx=5, pady=1)
ToolTip(Entry2,msg="Rango ideal de 18 a 24°C",delay=0,padx=10,pady=10,font=("Georgia Pro",12))
Stemp()
Entry2.configure(state= DISABLED)

port = 1
#address = 0x77 # Adafruit BME280 address. Other BME280s may be different
#bus = smbus2.SMBus(port)
#bme280.load_calibration_params(bus,address)

labeltempamb=CTkLabel(frame2,text="Temperatura ambiental (°C)",font=("Georgia Pro",12))
labeltempamb.grid(column=0,row=10,padx=5, pady=1)
'''
def Stempamb():
    tempambsensor = bme280.sample(bus,address).temperature
    tempambsensor = round(tempambsensor,1)
    tempambSV.set(tempambsensor)
    window.after(1000,Stempamb)
    
tempambSV=StringVar()

EntryTempamb = CTkEntry(frame2,textvariable=tempambSV, justify=CENTER,font=("Georgia Pro",12))
EntryTempamb.grid(column=0,row=11,padx=5, pady=1)
EntryTempamb.configure(state= DISABLED)
Stempamb()
'''

label8 = CTkLabel(frame2,text="Conductividad (mS/cm)",font=("Georgia Pro",12))
label8.grid(column=0,row=13,padx=5, pady=1)

def Sconductividad():
    conducsensor = AnalogIn(ads, ADS.P2).value
    #conducsensor = round((conducsensor-127.658)/1222.464 + 0.07,2)
    conducsensor = round((conducsensor*0.000764306)-0.0265299,2)# sensor dfrobot
    #conducsensor = round((conducsensor*0.000166867)-0.115138,2)# sensor tds
    conducSV.set(conducsensor)
    window.after(1000,Sconductividad)
    
conducSV=StringVar()

Entry8 = CTkEntry(frame2,textvariable=conducSV, justify=CENTER,font=("Georgia Pro",12))
Entry8.grid(column=0,row=14, pady=1)

ToolTip(Entry8,msg="Rango ideal de 1.5 a 2.5 mS/cm",delay=0,padx=10,pady=10,font=("Georgia Pro",12))
Sconductividad()
Entry8.configure(state= DISABLED)

Datosgraf = {
    'ph' : [0, [0,14], 'pH' , 'Horas'],
    'temp' : [1, [15,25], 'Temperatura agua (°C)', 'Horas'],
    'tempa': [2, [15, 25], 'Temperatura ambiente (°C)', 'Horas'],
    'cond' : [3, [0,3], 'Conductividad (mS/cm)', 'Horas'],
    }

def graficar(sensor):
    conn = sqlite3.connect('historial_de_sensores4.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    valores=[]
    horas=[]
    for row in c.fetchall():
        valores.append(row[Datosgraf[sensor][0]])
        horas.append(row[4])
    plt.plot(horas,valores)
    plt.xlabel(Datosgraf[sensor][3])
    plt.ylabel(Datosgraf[sensor][2])
    plt.grid(True)
    plt.ylim(Datosgraf[sensor][1])
    plt.xticks(rotation=45)
    plt.show()
    conn.commit()
    conn.close()
    
icono_graph = CTkImage(Image.open(r"/home/damian/tt/icono3.png").resize((15,15),Image.ANTIALIAS))
btnGraphPH=CTkButton(frame2,text="",image=icono_graph,width=30,height=30,fg_color="gray",hover_color="white",command=lambda: graficar('ph'))
btnGraphPH.grid(column=1,row=5,sticky='e',padx=(0,20))
btnGraphTemp=CTkButton(frame2,text="",image=icono_graph,width=30,height=30,fg_color="gray",hover_color="white",command=lambda: graficar('temp'))
btnGraphTemp.grid(column=1,row=8,sticky='e',padx=(0,20))
btnGraphTempA=CTkButton(frame2,text="",image=icono_graph,width=30,height=30,fg_color="gray",hover_color="white",command=lambda: graficar('tempa'))
btnGraphTempA.grid(column=1,row=11,sticky='e',padx=(0,20))
btnGraphCond=CTkButton(frame2,text="",image=icono_graph,width=30,height=30,fg_color="gray",hover_color="white",command=lambda: graficar('cond'))
btnGraphCond.grid(column=1,row=14,sticky='e',padx=(0,20))

lblcolumna3 = CTkLabel(frame3,text="Control de iluminación",font=("Georgia Pro",18)).pack(padx=10,pady=20)

intensidad_var = StringVar()
intensidad_var.set('Intensidad 100%')
labelIntensidad = CTkLabel(frame3, textvariable=intensidad_var,font=("Georgia Pro",12))
labelIntensidad.pack(padx=10)

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)
p=GPIO.PWM(21,100)
p.start(0)
def evento_slider(value):
    intensidad_var.set('Intensidad '+str(int(value))+'%')
    
    
sliderIntensidad = CTkSlider(frame3,from_=0,to=100, width=150,command=evento_slider)
sliderIntensidad.pack(padx=10,pady=(0,16))
sliderIntensidad.set(100)


label4 = CTkLabel(frame3,text="Fotoperiodo (h)",font=("Georgia Pro",12)).pack(padx=10,pady=1)
fotoperiodo=StringVar()
fotoperiodo.set(0)
Entry4 = CTkEntry(frame3,textvariable =fotoperiodo,justify=CENTER)
Entry4.pack(padx=10,pady=(5,35))
ToolTip(Entry4,msg="Para albahaca verde se \n recomiendan 16 horas \n       de iluminación".center(25," "),delay=0,padx=10,pady=10)
valorfoto = Entry4.get()   



label5 = CTkLabel(frame3,text="Hora de inicio",font=("Georgia Pro",12)).pack(padx=10,pady=1)
horainicio=StringVar()
horainicio.set('00:00')
Entry5 = CTkEntry(frame3,textvariable =horainicio,justify=CENTER)
Entry5.pack(padx=10,pady=5)
Entry5.configure(state= DISABLED)

fecha_inicial=datetime.datetime.now()
hora_inicial=datetime.time(hour=fecha_inicial.hour,minute=fecha_inicial.minute)
lista = [hora_inicial] #.time()
for i in range(1,24):
    if i + fecha_inicial.hour > 23:
        lista.append(datetime.time(hour=i+fecha_inicial.hour-24, minute=fecha_inicial.minute))
    else:
        lista.append(datetime.time(hour=i+fecha_inicial.hour, minute=fecha_inicial.minute))
print(lista)
def suma():
    seleccion = CTkToplevel()
    btnSelHoras.configure(state=DISABLED)
    seleccion.title('Seleccionar hora de inicio')
    seleccion.geometry("350x185")
    
    if not valorfoto.isdigit():
        destruir_ventana()
        
        
    frame_tiempo=CTkFrame(seleccion)
    frame_tiempo.grid(row=0,column=0,padx=10,pady=20)
    hora= CTkLabel(frame_tiempo, text="Hora")
    hora.grid(row=0,column=0,padx=30,pady=20)
    valores_horas=["00"]
        
    for i in range(1,24):
        if len(str(i)) == 1:
            valores_horas.append(f'0{str(i)}')
        else:
            valores_horas.append(str(i))
        i+=1
    valores_horas=tuple(valores_horas)
    
    spin_horas=tk.Spinbox(master=frame_tiempo,values=valores_horas,justify=CENTER, width=10, state="readonly",wrap=True)
    spin_horas.grid(row=0,column=1,padx=10,pady=20)
    valores_minutos=["00"]
    
    for i in range(1,60):
        if len(str(i)) == 1:
            valores_minutos.append(f'0{str(i)}')
        else:
            valores_minutos.append(str(i))
        i+=1
    valores_minutos=tuple(valores_minutos)
    
    spin_minutos=tk.Spinbox(master=frame_tiempo,values=valores_minutos,justify=CENTER, width=10, state="readonly",wrap=True)
    spin_minutos.grid(row=0,column=2,padx=10,pady=20)
    
#spin.bind("<MouseWheel>",scroll copiar scroll
    def destruir_ventana():
        seleccion.destroy()
        btnSelHoras.configure(state=ACTIVE)
    
    def aceptar():
        valorfoto = Entry4.get()
        valorinicio=spin_horas.get()
        horainicio.set(str(valorinicio)+':'+str(spin_minutos.get()))
        try:
            suma=int(valorfoto)+int(valorinicio)
        except ValueError:
            tk.messagebox.showerror("Advertencia","Advertencia, el fotoperiodo no es un número entero")
            
        if int(valorfoto)>24:
            tk.messagebox.showerror("Advertencia","Favor de ingresar un valor de fotoperiodo no mayor a 24 h.")
            suma=0
        if suma>= 24:
            suma-=24
        if len(str(suma)) == 1:
            tiempoFin.set('0'+str(suma)+':'+str(spin_minutos.get()))
        else:
            tiempoFin.set(str(suma)+':'+str(spin_minutos.get()))
        #crear lista de horas en la cual comparar para tomar mediciones
        destruir_ventana()
    
    seleccion.protocol("WM_DELETE_WINDOW",destruir_ventana)
    btnOK=CTkButton(seleccion, text= "Aceptar",command=aceptar)
    btnOK.grid(row=1,column=0,padx=(20,10),pady=15,sticky='sw')
    btnCancel=CTkButton(seleccion, text= "Cancelar",command=destruir_ventana)
    btnCancel.grid(row=1,column=0,padx=(10,20),pady=15,sticky='se')
    
                               
btnSelHoras = CTkButton(frame3, text="Seleccionar hora", width=25, command=suma,font=("Georgia Pro",12))

btnSelHoras.pack(pady=(5,35),padx=10)

label6 = CTkLabel(frame3,text="Hora de termino",font=("Georgia Pro",12)).pack(pady=1)
tiempoFin=StringVar()
tiempoFin.set('00:00')
Entry6 = CTkEntry(frame3,textvariable=tiempoFin, justify=CENTER,font=("Georgia Pro",12))
Entry6.pack(padx=10,pady=(5,35))
Entry6.configure(state= DISABLED)

EstadoLED=0
def comparacion_encendido():
    global now
    now = datetime.datetime.now().time()
    horafinal = datetime.datetime.strptime(tiempoFin.get(),"%H:%M").time()
    hora1 = datetime.datetime.strptime(horainicio.get(),"%H:%M").time()
        #if (now < horafinal and now > hora1) or (horafinal < hora1 and now < datetime:
    if (now < horafinal and now > hora1) or (horafinal < hora1 and ((now < datetime.time(23,59,0) and now > hora1) or (now > datetime.time(0,0,0) and now <horafinal))):
            #sliderIntensidad.configure(state= ACTIVE)
        p.ChangeDutyCycle(int(sliderIntensidad.get()))
        EstadoLED=1
    else:
        p.ChangeDutyCycle(0)
        EstadoLED=0
    window.after(100,comparacion_encendido)
    #comparar la hora con las horas en las que se van a tomar las muestras
def comparacion_escritura():
    global lista
    global hora_actual
    
    hora_actual=datetime.time(hour=now.hour,minute=now.minute)
    if switch_var.get() == "on" and hora_actual in lista:
        escribir_datos()
    window.after(60000,comparacion_escritura)        

comparacion_encendido()
comparacion_escritura()
def iniciar():
    global cap
    cap = cv2.VideoCapture(-1)
    btnIniciar.configure(state=DISABLED)#evitamos que el usuario seleccione botones que no debería para evitar errores
    btnVisualizar.configure(state=DISABLED)
    visualizar()
    
def visualizar():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.flip(frame,0)
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            
            #img = CTkImage(dark_image=frame,size=(200,200))
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
        else:
            lblVideo.image = ""
            cap.release()

def finalizar():
    global cap
    cap.release()#Si hay problemas con esto ponerlo dentro de un try
    btnIniciar.configure(state=ACTIVE)
    btnCapturar.configure(state=ACTIVE)
    btnVisualizar.configure(state=ACTIVE)
    

def tomarfoto():
    global cap
    ret, frame = cap.read()
    frame = cv2.flip(frame,0)
    i=1
    while (os.path.isfile(segmented_button_var.get()+"-"+str(i)+".jpg")):#checar si ya existe la imagen
        i+=1
    else:
        cv2.imwrite(segmented_button_var.get()+"-"+str(i)+".jpg",frame) #si no existe la imagen, escribir la imagen sin sobreescribir
    
def visualizarfoto():
    btnIniciar.configure(state=DISABLED)
    btnCapturar.configure(state=DISABLED)
    #btnFinalizar.configure(state=DISABLED)
    i=1
    lista_de_fotos=[]
    while (os.path.isfile(segmented_button_var.get()+"-"+str(i)+".jpg")):#checar si ya existe la imagen
        lista_de_fotos.append(ImageTk.PhotoImage(Image.open(segmented_button_var.get()+"-"+str(i)+".jpg")))
        i+=1
    #Creamos ventana donde vamos a ver las fotos de la planta seleccionada
    ventana_fotos = CTkToplevel()
    ventana_fotos.title(segmented_button_var.get())
    global lblFotos
    lblFotos = tk.Label(ventana_fotos,image=lista_de_fotos[0])
    lblFotos.grid(row=0,column=0,columnspan=3)
    def sig(image_number):
        global lblFotos
        global btnSig
        global btnAnt
        lblFotos.grid_forget()
        lblFotos = tk.Label(ventana_fotos,image=lista_de_fotos[image_number-1])
        btnSig = CTkButton(ventana_fotos, text=">>", command=lambda: sig(image_number+1),font=("Georgia Pro",12))
        btnAnt = CTkButton(ventana_fotos, text="<<", command=lambda: ant(image_number-1),font=("Georgia Pro",12))
        
        if image_number == len(lista_de_fotos):
            btnSig=CTkButton(ventana_fotos, text=">>",state=DISABLED,font=("Georgia Pro",12))
        lblFotos.grid(row=0,column=0,columnspan=3)
        btnAnt.grid(row=1,column=0)
        btnSig.grid(row=1,column=2)
    def ant(image_number):
        global lblFotos
        global btnSig
        global btnAnt
        lblFotos.grid_forget()
        lblFotos = tk.Label(ventana_fotos,image=lista_de_fotos[image_number-1])
        btnSig = CTkButton(ventana_fotos, text=">>", command=lambda: sig(image_number+1),font=("Georgia Pro",12))
        btnAnt = CTkButton(ventana_fotos, text="<<", command=lambda: ant(image_number-1),font=("Georgia Pro",12))
        
        if image_number == 1:
            btnAnt=CTkButton(ventana_fotos, text="<<",state=DISABLED,font=("Georgia Pro",12))
            
        lblFotos.grid(row=0,column=0,columnspan=3)
        btnAnt.grid(row=1,column=0)
        btnSig.grid(row=1,column=2)
        
    btnSig = CTkButton(ventana_fotos, text=">>", command=lambda: sig(2),font=("Georgia Pro",12))
    btnAnt = CTkButton(ventana_fotos, text="<<", command=ant,state=DISABLED,font=("Georgia Pro",12))    
    btnAnt.grid(row=1,column=0)
    btnSig.grid(row=1,column=2)
    
    
def graficar_crecimiento():
    btnIniciar.configure(state=DISABLED)
    btnCapturar.configure(state=DISABLED)
cap = None


btnIniciar = CTkButton(framebotones, text="Iniciar", width=45, command=iniciar,font=("Georgia Pro",12))
btnIniciar.pack(side=LEFT,padx=20)
btnCapturar = CTkButton(framebotones, text="Tomar Foto", width=45, command= tomarfoto,font=("Georgia Pro",12))
btnCapturar.pack(side=LEFT,pady=10,padx=20)
btnVisualizar = CTkButton(framebotones, text="Visualizar", width=45, command= visualizarfoto,font=("Georgia Pro",12))
btnVisualizar.pack(side=LEFT,pady=10,padx=20)
btnVisualizar = CTkButton(framebotones, text="Graficar", width=45, command= graficar_crecimiento,font=("Georgia Pro",12))
btnVisualizar.pack(side=LEFT,pady=10,padx=20)
btnFinalizar = CTkButton(framebotones, text="Finalizar", width=45, command=finalizar,font=("Georgia Pro",12))
btnFinalizar.pack(side=LEFT,padx=20,pady=10)

selPlantaLabel = CTkLabel(frameSelPlanta, text="Selección de planta",font=("Georgia Pro",12)).pack()
segmented_button_var = StringVar(value="A1")
btnsSelPlanta =CTkSegmentedButton(frameSelPlanta,values=["A1","A2","B1","B2"], variable=segmented_button_var,font=("Georgia Pro",12)) 
btnsSelPlanta.pack()
lblVideo = tk.Label(frame1,text="") #Se usa label de la lib original de tkinter ya que la de CTk ya no es compatible en la version 5
lblVideo.pack()
lblVideo.configure(bg="#212121")#se buscó un color que fuera similar al del fondo para tapar el color blanco que es el default
# Base de datos

# Creación de base de datos o conexión a una base de datos
conn = sqlite3.connect('historial_de_sensores4.db')

# Creación de cursor
c = conn.cursor()

# Creación de tabla
'''
c.execute("""CREATE TABLE addresses(
        pH real,
        temp real,
        temp_ambiental real,
        conductividad real,
        hora text,
        luz text
        )""")
'''

def escribir_datos():
    conn = sqlite3.connect('historial_de_sensores4.db')
    c = conn.cursor()
    c.execute("INSERT INTO addresses VALUES(:ph,:temp, :temp_ambiental, :conductividad, :hora, :luz)",
              {
                  'ph': Entry1.get(),
                  'temp': Entry2.get(),
                  'temp_ambiental': EntryTempamb.get(),
                  'conductividad': Entry8.get(),
                  'hora': str(hora_actual),
                  'luz': EstadoLED
              }
              )
    conn.commit()
    conn.close()
    
def leer_datos():
    conn = sqlite3.connect('historial_de_sensores4.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    print(records)
    conn.commit()
    conn.close()
    

    
    
conn.commit()
conn.close()    

window.protocol("WM_DELETE_WINDOW",cerrar_interfaz)

window.mainloop()