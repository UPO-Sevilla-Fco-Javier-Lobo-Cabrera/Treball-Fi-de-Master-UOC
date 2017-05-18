#!/usr/bin/env Rscript

#Este script de R generará un fichero denominado 
#"sobre_el_rechazo_de_la_hipotesis.txt", en el 
#que se imprimirá la palabra "SI" o bien la
#palabra "NO". Se dará 
#el primer caso si se rechaza que los datos de la 
#simulación problema concuerden con los del modelo
#lineal. Si no se rechaza la hipótesis, se dará
#el segundo caso.

#Paso 1:
#Lectura de parámetros del modelo lineal a partir de
#un fichero. Dicho fichero ha de contener en primer 
#lugar la desviación típica del modelo lineal y a 
#continuación los parámetros β en el orden β0, β1,
#y β2:

parametros_mod_lin <- scan(file = "modelo_lineal.txt",
                     what = double(),  n = -3, sep = "")

#Se guarda la desviación típica del modelo lineal en:
desv_tip_mod_lin <- parametros_mod_lin[1]

#Se guardan los parámetros β del modelo lineal en:
parametros_beta_mod_lin <- parametros_mod_lin[2:length(parametros_mod_lin)]

#Paso 2:
#Se procede al conteo de parámetros β del modelo lineal:
num_parametros_beta_mod_lin <- length(parametros_beta_mod_lin) 


#Paso 3:
#Lectura de datos del problema. Se espera que los datos del 
#problema estén contenidos en un fichero. Dicho fichero ha
#de contener la Kd y lambda del problema:

datos_problema <- scan(file = "problema.txt", 
                       what = double(),  n = -2, sep = "")


#Se guarda la Kd del problema en:

Kd_problema <- datos_problema[1]

#Se guarda el parámetro lambda del problema en:

lambda_problema <- datos_problema[2]



#Paso 4:
#Para testear si los datos del problema se ajustan al modelo
#lineal se va a seguir el siguiente procedimiento: 

#a)Primero se va a calcular el Kd predicho por el modelo de acuerdo
#al dato de lambda del problema. Se va a suponer que dicho Kd calculado
#es una variable aleatoria que sigue una función de 
#probabilidad normal. Esta variable aleatoria tiene como
#media el Kd predicho por el modelo. Como desviación típica tiene
#aquella característica del modelo lineal, la cual se suministró en 
#el fichero modelo_lineal.txt .

#b)A continuación, se va a realizar un test de t de Student para
#rechazar o no que el Kd del problema sea un valor probable del
#Kd predicho por el modelo.


#a)Cálculo de Kd predicho por el modelo de acuerdo
#al dato de lambda del problema:

Kd_predicho_mod_lin <- parametros_beta_mod_lin[1] + 
                              parametros_beta_mod_lin[2] * 
                             lambda_problema +
                              parametros_beta_mod_lin[3] * 
                              lambda_problema
    

#b)Test de t de Student:
#En la fórmula del estadístico t de Student se está sustituyendo 
#la cuasidesvación típica muestral por la desviación típica 
#poblacional (ya que esta última se conoce):

t <- (Kd_problema - Kd_predicho_mod_lin) /
     (desv_tip_mod_lin / sqrt(length(Kd_problema)))

#A continuación se va a calcular la probabilidad acumulada del 
#estadistico t calculado. Se desconoce el tamaño muestral. Es
#decir, no se conoce cuántas mediciones del problema se hicieron 
#para calcular su valor. Por defecto, se va a especificar un 
#tamaño muestral de n = 3 . por ello, el número de grados de
#libertad será df = n - 1 = 2.En futuras versiones del programa 
#el tamaño muestral puede podría ser también un input a introducir
#por el usuario.  

t_probabilidad_acumulada <- pt(t, df = 2)


#Si la probabilidad acumulada inferior del 5% o bien superior al
#95% entonces se rechazará la hipótesis con alfa = 0.05. Es decir,
#se rechazará que los datos del problema se ajusten al modelo lineal:


if ((t_probabilidad_acumulada < 0.05) | (t_probabilidad_acumulada > 0.95))
{
  write("SI", file = "sobre_el_rechazo_de_la_hipotesis.txt")
}else
{
  write("NO", file = "sobre_el_rechazo_de_la_hipotesis.txt")
}

