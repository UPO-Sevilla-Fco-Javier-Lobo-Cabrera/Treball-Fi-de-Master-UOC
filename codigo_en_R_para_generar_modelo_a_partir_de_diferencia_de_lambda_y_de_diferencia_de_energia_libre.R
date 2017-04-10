#!/usr/bin/env Rscript

#Este script está diseñado para ser ejecutado desde una terminal 
#(véase http://stackoverflow.com/questions/18306362/run-r-script-from-command-line)
#o en este caso, desde un programa en python que posibilite su ejecución mediante
#el empleo del método os.system() .

#Este script de R leerá los valores de Δλ y ΔG a partir de los ficheros diferencia_lambda.txt y gibbs.txt
#generados por otras partes del software. El fichero fichero_lambda.txt debe constar de una única 
#columna con los valores de Δλ para cada proteína. Por su parte, el fichero gibbs.txt
#ha de recoger en una única columna las variaciones de energía libre de Gibbs (ΔG) asociadas
#para cada proteína. Como en cada complejo existen dos proteínas, los valores del fichero
#gibbs.txt serán repetitivos de dos en dos. PE:
#5.987
#5.987
#7.665
#7.665
#...





#La variable respuesta sería ΔG y la variables explicativas serían Δλ, Δλ^2 y Δλ^3 . 


#Lectura de los parámetros:

lectura_Δλ <- read.table("RUTA_DONDE_ESTE_EL_PROGRAMA_DE_PYTHON/diferencia_lambda.txt")

Δλ <- lectura_Δλ$V1


lectura_ΔG <- read.table("RUTA_DONDE_ESTE_EL_PROGRAMA_DE_PYTHON/gibbs.txt")

ΔG <- lectura_ΔG$V1


#Creación de los modelos lineales:

modelo_lineal_a <- lm(ΔG ~ Δλ)

modelo_lineal_b <- lm(ΔG ~ Δλ^2)

modelo_lineal_c <- lm(ΔG ~ Δλ + Δλ^2 + Δλ^3)



#A continuación se procede al cálculo de R² para cada modelo:

r_cuadrado_modelo_lineal_a <- summary(modelo_lineal_a)$r.squared

r_cuadrado_modelo_lineal_c <- summary(modelo_lineal_b)$r.squared

r_cuadrado_modelo_lineal_c <- summary(modelo_lineal_c)$r.squared












