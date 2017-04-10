#!/usr/bin/env Rscript

#Este script de R generará un fichero denominado 
#"resultado_se_rechaza_hipótesis.txt"o bien un 
#fichero llamado
#"resultado_NO_se_rechaza_hipótesis.txt". Se dará 
#el primer caso si se rechaza que los datos de la 
#simulación problema concuerden con los del modelo
#lineal. Si no sé rechaza la hipótesis, se creará 
#el segundo fichero.

#Paso 1:
#Lectura de parámetros del modelo lineal a partir de
#un fichero. Dicho fichero ha de contener en primer 
#lugar la desviación típica del modelo lineal y a 
#continuación los parámetros β en el orden β0, β1,
#β2, β3 (los dos últimos solo en el caso 
#de que existan) :

parametros_mod_lin <- scan(file = "modelo_lineal.txt",
                     what = double(),  n = -4, sep = "")

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
#de contener la ΔG y la Δλ del problema:

datos_problema <- scan(file = "problema.txt", 
                       what = double(),  n = -2, sep = "")


#Se guarda el ΔG del problema en:

ΔG_problema <- datos_problema[1]

#Se guarda el Δλ del problema en:

Δλ_problema <- datos_problema[2]



#Paso 4:
#Para testear si los datos del problema se ajustan al modelo
#lineal se va a seguir el siguiente procedimiento: 

#a)Primero se va a calcular el ΔG predicho por el modelo de acuerdo
#al dato de Δλ del problema. Se va a suponer que dicho ΔG calculado
#es una variable aleatoria que sigue una función de 
#probabilidad normal (dicha suposición está apoyada por el
#Teorema Central del Límite*). Esta variable aleatoria tiene como
#media el ΔG predicho por el modelo. Como desviación típica tiene
#aquella característica del modelo lineal, la cual se suministró en 
#el fichero modelo_lineal.txt .

#b)A continuación, se va a realizar un test de t de Student para
#rechazar o no que el ΔG del problema sea un valor probable del
#ΔG predicho por el modelo.

#(*)La calorimetría isoterma de titulación es una técnica 
#basada en el estudio de numerosos complejos idénticos
#proteína-proteína. Por tanto, puede considerarse la medición
#final como la suma de múltiples variables aleatorias 
#independientes equivalentemente distribuidas. De este modo,
#la función de probabilidad de las mediciones de la técnica
#ha de seguir una distribución normal, de acuerdo al Teorema 
#Central del Límite.


#a)Cálculo de ΔG predicho por el modelo de acuerdo
#al dato de Δλ del problema:

if(num_parametros_beta_mod_lin == 2) #caso de modelo de recta 
{                                    #( y = b + a*x )

  ΔG_predicho_mod_lin <- parametros_beta_mod_lin[1] + 
                               parametros_beta_mod_lin[2] * 
                              Δλ_problema
}

if(num_parametros_beta_mod_lin == 3) #caso de modelo parabólico
{                               #( y = b + a*x + c*x² )

  ΔG_predicho_mod_lin <- parametros_beta_mod_lin[1] + 
                              parametros_beta_mod_lin[2] * 
                             Δλ_problema +
                              parametros_beta_mod_lin[3] * 
                              (Δλ_predicho_mod_lin_inicial^2)
    
}



if(num_parametros_beta_mod_lin == 4) #( y = b + a*x + c*x² + d*x³)
{                             
  
  ΔG_predicho_mod_lin <- parametros_beta_mod_lin[1] + 
                              parametros_beta_mod_lin[2] * 
                             Δλ_problema +
                              parametros_beta_mod_lin[3] * 
                              (Δλ_predicho_mod_lin_inicial^2) +
                              parametros_beta_mod_lin[4] * 
                              (Δλ_predicho_mod_lin_inicial^3)
  
} 


#b)Test de t de Student:
#En la fórmula del estadístico t de Student se está sustituyendo 
#la cuasidesvación típica muestral por la desviación típica 
#poblacional (ya que esta última se conoce):

t <- (ΔG_problema - ΔG_predicho_mod_lin) /
     (desv_tip_mod_lin / sqrt(length(ΔG_problema)))

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
#95% entonces se rechazará la hipótesis con alfa = 0.05 **. Es decir,
#se rechazará que los datos del problema se ajusten al modelo lineal:


if ((t_probabilidad_acumulada < 0.05) | (t_probabilidad_acumulada > 0.95))
{
  
  file.create("resultado_se_rechaza_hipótesis.txt", showWarnings = TRUE)
  
}else
{
  file.create("resultado_NO_se_rechaza_hipótesis.txt", showWarnings = TRUE)
  
}  



#(**)En una futura versión del programa, el nivel de significación 
#alfa a emplear podría ser introducido por el usuario.

