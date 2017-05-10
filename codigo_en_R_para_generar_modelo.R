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

#A continuación se calculan la desviación típica y coeficientes del modelo
#y se imprimen en el archivo modelo_lineal.txt:
desviacion_tipica_modelo <- sigma(modelo_lineal)
coeficientes_del_modelo <- as.numeric(modelo_lineal$coefficients)

write(desviacion_tipica_modelo, file = "modelo_lineal.txt")
write(coeficientes_del_modelo[1], file = "modelo_lineal.txt", append = TRUE)
write(coeficientes_del_modelo[2], file = "modelo_lineal.txt", append = TRUE)
write(coeficientes_del_modelo[3], file = "modelo_lineal.txt", append = TRUE)


