#!/usr/bin/env Rscript

#Este script de R leerá los valores de λ y constante de disociación (Kd) a partir de los ficheros lambda.txt y kd.txt
#generados por otras partes del software. El fichero lambda.txt debe constar de una única 
#columna con los valores de lambda para cada proteína. Por su parte, el fichero Kd.txt
#ha de recoger en una única columna la constante de disociación asociada con cada complejo.


#La variable respuesta sería Kd y la variables explicativas serían lambda, lambda^2 y lambda^3 . 

#Lectura de los parámetros:

lectura_lambda <- read.table("lambda.txt")

lambda <- lectura_lambda$V1


lectura_Kd <- read.table("Kd.txt")

Kd <- lectura_Kd$V1

#Creación del modelo lineal:
lambda_cuadrado <- lambda ^2
modelo_lineal <- lm(Kd ~ lambda_cuadrado + lambda)

#A continuación se imprime el modelo lineal:
print(modelo_lineal)


