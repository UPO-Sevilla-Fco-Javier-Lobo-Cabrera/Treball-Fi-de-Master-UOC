#!/usr/bin/env Rscript

#Este script devuelve los residuos que más han cambiado significativamente su posición. 
#Para ello se va a calcular el percentil 90 de la distribución de RMSFs de los átomos 
#y se van #a seleccionar los residuos que contengan al menos un átomo con un RMSFs superior
#a dicho percentil. 

#Para recibir como comandos a través del terminal:
#i)la ruta del fichero a analizar 
#ii)la ruta del fichero de output a crear
rutas_por_comando = commandArgs(trailingOnly=TRUE)
ruta_fichero_a_analizar = rutas_por_comando[1]
ruta_fichero_output = rutas_por_comando[2]

datos_alin <- read.table(ruta_fichero_a_analizar)

percentil90 <- quantile(datos_alin$V2, probs = c(0.90))

#Variable que contendrá el conjunto de residuos con átomos que han cambiado en gran
#propoción su posición:
conjunto_res <- vector()

i <- 1

while (i <= length(datos_alin$V1))
{
  #Si el RMSF del átomo es superior al percentil 90:
  if (datos_alin$V2[i] > percentil90)
  {
    #Si el residuo que contiene dicho átomo no había sido
    #incluído en conjunto_res antes:
    if (is.element(datos_alin$V1[i], conjunto_res) == FALSE)
    {
      conjunto_res <- c(conjunto_res, datos_alin$V1[i])
    }
  }
    
  i <- i + 1
}


#Finalmente, se escriben los resultados en un fichero:
#Primero se asegura que el fichero de output ya no exista. Para ello,
#se ejecuta las siguientes dos líneas de código:
comando_para_eliminar_fichero_output_si_existia <- paste("rm ", ruta_fichero_output)
try(system(comando_para_eliminar_fichero_output_si_existia), silent = TRUE)

#Luego se crea el nuevo fichero de output:
comando_para_crear_fichero_output <- paste("touch ", ruta_fichero_output)
system(comando_para_crear_fichero_output)

#A continuación se escribe en el fichero:
for (j in conjunto_res)
{
  write(j, file = ruta_fichero_output, 
  append = TRUE, sep = "\n")  
}








