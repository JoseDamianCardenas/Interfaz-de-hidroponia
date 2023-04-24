# Interfaz de hidroponia
GUI para el monitoreo de sensores para crecer cultivos en hidroponia, se ocupó una camara, la interfaz cuenta con la posibilidad de inicializar la cámara, tomar fotos, visualizar fotos y calcular la tasa de crecimiento de las plantas. Se usó principalmente la librería customtkinter.

![alt text](https://github.com/JoseDamianCardenas/Interfaz-de-hidroponia/blob/main/interfaz_imagen.jpg?raw=true)

En la primer columna se tiene la posibilidad de visualizar la imagen obtenida de la planta, desplegar todas las imagenes obtenidas de cada una, graficar la tasa de crecimiento entre la primer y última foto de la planta seleccionada y finalmente tenemos la opción de dejar de mostrar la imagen obtenida de la camara.

En la segunda columna tenemos la visualización de los sensores, estos se actualizan cada segundo. Además tenemos un switch para activar el registro de estos valores cada hora.

En la tercer columna tenemos el control de iluminación en el cual podemos controlar con un slider la intensidad de luz que reciben las plantas, así como el fotoperiodo (la cantidad de horas diarias que reciben luz las plantas), la hora de inicio y con eso se calcula la hora en la que dejan de recibir luz.
