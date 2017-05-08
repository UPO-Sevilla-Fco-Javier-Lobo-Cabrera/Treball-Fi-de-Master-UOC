
import sys
import math


def leer_fichero_angulos_chi_equilibrio():
    '''Crear una lista de listas con la informacion de 
    angulos_chi_equilibrio''' 

    #A partir del fichero angulos_chi_equilibrios se va a crear una    
    #lista de listas denominada "informacion". Cada elemento de 
    #"informacion" es una lista que contendra en primer lugar
    #la abreviatura en mayusculas de aminoacido, luego su 
    #angulo chi x2, luego su angulo chi x3, luego su angulo chi x1
    #y por ultimo su angulo chi x4.

    g = open("angulos_chi_equilibrio", "r")

    informacion = []

    lista_lineas_del_fichero = g.read().splitlines()


    for i in lista_lineas_del_fichero:
        elemento = []
        elemento.append(i[0:3])
	
        #Para empezar a leer cada linea desde los angulos chi:
        indice = 11

        #Para contar los angulos chi registrados:
        contador = 0
	
        while (contador < 4):
            #Si dentro de dos posiciones hay una "N" entonces el 
            #angulo chi es "None":
            if (i[indice] == "N"):
                elemento.append("None")
		#Posicionamiento del indice en el siguiente angulo chi:
                if ((indice + 12) < len(i)):
                    indice = indice + 12
                else:
                    break
            else:
                #En la variable "almacen" se va a ir construyendo el 
                #angulo chi en cuestion:
                almacen = ""
                while ((i[indice] != ",") and (i[indice] != "}")):
                    almacen = almacen + i[indice]
                    if ((indice + 1) < len(i)):
                        indice = indice + 1
                    else:
                        break
		
                #Pasar de string a float:
                almacen = float(almacen)
                #Anadir a elemento:
                elemento.append(almacen)
                #Desplazar indice:
                if ((indice + 8) < len(i)):
                    indice = indice + 8
                else:
                    break

            contador = contador + 1 
        informacion.append(elemento)

    g.close()

    return informacion




def contribucion_residuo(nombre_res, angulos_chi, informac):
    '''Calcular la contribucion a lambda de un residuo'''

    #El primer parametro de entrada ha de ser la abreviatura del 
    #aminoacido en cuestion en 3 letras (y mayusculas)

    #El segundo parametro de entrada ha de ser un diccionario gene-
    #rado por la funcion predictor.calculate_chi_angles . Contiene
    #los angulos chi obtenidos del residuo a estudiar.
	
    #El tercer parametro de entrada ha de ser una lista de listas
    #retornada por la funcion leer_fichero_angulos_chi_equilibrio .
    #Contiene los angulos chi de equilibrio de cada uno de los
    #20 aminoacidos.

    claves_angulos_chi = ["x2", "x3", "x1", "x4"]
    contribucion = 0.0
    #La variable i sera una lista con el nombre del residuo primero
    #y los angulos chi de equilibrio caracteristicos a continuacion:
    for i in informac:
        #Indice para controlar las posiciones de la variable i:
        indi = 1
        #Si se halla el residuo a comparar:
        if (nombre_res == i[0]):
            #Calculo para cada chi:
            for j in claves_angulos_chi:
                #if (angulos_chi[j] no es ningun numero por no existir ese
                #ese angulo chi:
                if (angulos_chi[j] != "None") & (angulos_chi[j] is not None):
                    #Primer caso:
                    if ((angulos_chi[j] >= 0) and (i[indi] >= 0)):
                        distancia = abs(angulos_chi[j] - i[indi])
                        contribucion  =  contribucion + distancia
                    #Segundo caso:
                    elif ((angulos_chi[j] <= 0) and (i[indi] <= 0)):
                        distancia = abs(angulos_chi[j] - i[indi])
                        contribucion  =  contribucion + distancia
                    #Tercer caso:
                    else:
                        #Si no se han dado los casos anteriores 
                        #se ha de tener un angulo positivo y
                        #otro negativo. El calculo entonces de la
                        #distancia es similar a calcular la distancia
                        #minima entre dos agujas de un reloj, estando una
                        #en el hemisferio derecho del reloj y la otra
                        #en el izquierdo. Las "12" serian -180 grados 
                        #(o 180), las "6" equivaldria a un angulo de 0
                        #grados, "menos cuarto" e "y cuarto" serian -90 
                        #y 90 grados respectivamente:
                        if (angulos_chi[j] > 0):
                            #Si se ha dado esta condicion es que i[indi] < 0:
                            arco_inferior_reloj = (180 - angulos_chi[j]) + (180 + i[indi])
                            arco_superior_reloj = (0 + angulos_chi[j]) + (0 - i[indi]) 
                            if (arco_inferior_reloj <= arco_superior_reloj):
                                #Es decir, por ejemplo las "9 y 5 min":
                                distancia = (180 - angulos_chi[j]) + (180 + i[indi])
                                contribucion  =  contribucion + distancia
                            else:
                                #Es decir, por ejemplo las "8 y 20 min":
                                distancia = (0 + angulos_chi[j]) + (0 - i[indi])
                                contribucion  =  contribucion + distancia
                        else:
                           #Si se ha dado esta condicion es que i[indi] > 0. 
                           #El codigo es como el anterior intercambiando 
                           #el orden de angulos_chi[j] y i[indi]:
                           arco_inferior_reloj = (180 - i[indi]) + (180 + angulos_chi[j])
                           arco_superior_reloj = (0 + i[indi]) + (0 - angulos_chi[j])
                           if (arco_inferior_reloj <= arco_superior_reloj):
                               #Es decir, por ejemplo las "8 y 5 min":
                               distancia = (180 - i[indi]) + (180 + angulos_chi[j])
                               contribucion  =  contribucion + distancia
                           else:
                               #Es decir, por ejemplo las "8 y 20 min":
                               distancia = (0 + i[indi]) + (0 - angulos_chi[j])
                               contribucion  =  contribucion + distancia

				#Para pasar al siguiente angulo chi:		
                indi = indi + 1

            #Como ya se ha hallado el residuo a comparar:
            break

    return contribucion


