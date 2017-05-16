
import os
from collections import deque

def calcular(tuplas_trabajo, ruta_directorio_de_output, ruta_ejecutable_lovoalign, ruta_directorio_ficheros_benchmark):
    '''Calcula los alineamientos estructurales para cada par bound/unbound'''

    #ATENCION: Las rutas de los directorios recibidos deben acabar en "\".

    #Se van a calcular los alineamientos para las 4 posibles combinaciones:

    #a) Calculo de alineamientos estructurales del ligando en estado bound con el 
    #ligando en estado unbound:
    print "Calculando alineamientos estructurales (Paso 1/4) ..."
    for i in tuplas_trabajo:
        j = i[0]
        j = j.upper()

        primera_parte_comando = "./" + ruta_ejecutable_lovoalign + " -p1 " + ruta_directorio_ficheros_benchmark + j + "_l_b.pdb" + " -p2 " + ruta_directorio_ficheros_benchmark + j 
        segunda_parte_comando = "_l_u.pdb" + " -o " + ruta_directorio_de_output + j + "l_b.pdb -rmsf " + ruta_directorio_de_output + "rmsf_" + j + "_l_b.dat" + " -all"
        comando = primera_parte_comando + segunda_parte_comando

        os.system(comando)
        print ".."


    #b) Calculo de alineamientos estructurales del ligando en estado unbound con el 
    #ligando en estado bound:
    print "Calculando alineamientos estructurales (Paso 2/4) ..."
    for i in tuplas_trabajo:
        j = i[0]
        j = j.upper()

        primera_parte_comando = "./" + ruta_ejecutable_lovoalign + " -p1 " + ruta_directorio_ficheros_benchmark + j + "_l_u.pdb" + " -p2 " + ruta_directorio_ficheros_benchmark + j + "_l_b.pdb" 
        segunda_parte_comando = " -o " + ruta_directorio_de_output + j + "l_u.pdb -rmsf " + ruta_directorio_de_output + "rmsf_" + j + "_l_u.dat" + " -all"
        comando = primera_parte_comando + segunda_parte_comando

        os.system(comando)
        print ".."


    #c) Calculo de alineamientos estructurales del receptor en estado bound con el 
    #receptor en estado unbound:
    print "Calculando alineamientos estructurales (Paso 3/4) ..."
    for i in tuplas_trabajo:
        j = i[0]
        j = j.upper()

        primera_parte_comando = "./" + ruta_ejecutable_lovoalign + " -p1 " + ruta_directorio_ficheros_benchmark + j + "_r_b.pdb" + " -p2 " + ruta_directorio_ficheros_benchmark + j
        segunda_parte_comando = "_r_u.pdb" + " -o " + ruta_directorio_de_output + j + "r_b.pdb -rmsf " + ruta_directorio_de_output + "rmsf_" + j + "_r_b.dat" +" -all"
        comando = comando = primera_parte_comando + segunda_parte_comando

        os.system(comando)
        print ".."

    #d) Calculo de alineamientos estructurales del receptor en estado unbound con el 
    #receptor en estado bound:
    print "Calculando alineamientos estructurales (Paso4/4) ..."
    for i in tuplas_trabajo:
        j = i[0]
        j = j.upper()

        primera_parte_comando = "./" + ruta_ejecutable_lovoalign + " -p1 " + ruta_directorio_ficheros_benchmark + j + "_r_u.pdb" + " -p2 " + ruta_directorio_ficheros_benchmark + j + "_r_b.pdb"
        segunda_parte_comando =  " -o " + ruta_directorio_de_output + j + "r_u.pdb -rmsf " + ruta_directorio_de_output + "rmsf_" + j + "_r_u.dat" +" -all"
        comando = primera_parte_comando + segunda_parte_comando
       
        os.system(comando)
        print ".."



def analizar(ruta_script_auxiliar_R, ruta_fich_resultado_alin, ruta_fich_output):
    '''Obtener residuos que cambien su posicion al formarse el complejo'''
 
    #Esta funcion va a utilizar el script auxiliar
    #"codigo_en_R_para_analizar_alineamiento_estructural.R", al que se le 
    #envian como parametros las rutas de los ficheros de input y output:
    com_a_ejecutar = "Rscript " + ruta_script_auxiliar_R + " " + ruta_fich_resultado_alin + " " + ruta_fich_output

    #Ejecucion del script:
    os.system(com_a_ejecutar)

    fich_output_del_analisis = open(ruta_fich_output, "r")
    residuos_relevantes = fich_output_del_analisis.read().splitlines()
    return(residuos_relevantes)
 
 












