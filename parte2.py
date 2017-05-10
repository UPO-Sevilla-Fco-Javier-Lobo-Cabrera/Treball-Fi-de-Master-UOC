
from lightdock.pdbutil.PDBIO import parse_complex_from_file
from lightdock.structure.complex import Complex
from lightdock.rotamer.predictor import calculate_chi_angles
import sys
import os
import extraer_informacion_bases_de_datos
import alineamientos_estruc
import func_lambda
import primer_indice_res

print "Bienvenido:"

try:
    f = open("datos_input", "r")
except:
    print "Este programa necesita de un fichero de input llamado datos_input localizado en el mismo directorio que este script de Python. En dicho fichero, han de incluirse los siguientes datos, uno en cada linea: \nRuta del fichero con la informacion de la constante de disociacion que este en el formato de INDEX_general_PP.2016 de la base de datos PDBbind. \nRuta del directorio que contiene las estructuras del ligando y receptor en estados unbound y bound siguiendo la nomenclatura de la base de datos benchmark. \nRuta del directorio que contiene los modulos de Python y scripts de R en general utilizados, asi como el fichero de angulos chi de equilibrio. \nRuta del script de R en particular para analizar los alineamientos estructurales. \nRuta del ejecutable de lovoalign.\nAtencion: las rutas de los directorios deben acabar en barra invertida (backslash)."
    sys.exit()

datos_fich_input = f.read().splitlines()
f.close()


#Ruta del fichero con la constante de disociacion:
f_ter = datos_fich_input[0]
#Las rutas de los directorios deben acabar en "/":
#Ruta del directorio de estructuras pdb:
d_ben = datos_fich_input[1]
#El directorio de trabajo (d_trab) contiene los modulos de Python y R:
d_trab = datos_fich_input[2]
#Ruta del codigo en R auxiliar para analizar alineamiento estructural:
r_lin = datos_fich_input[3]
#Ruta del ejecutable de lovoalign. Nota: Si al ejecutar el programa se
#observa error de Fortran "Sementation fault" entonces acudir al directorio
#de lovoalign => src/sizes.f90 y disminuir maxatom por ejemplo a 3500
#y maxfile a 5000, volver a compilar y probar con el nuevo ejecutable. Sin
#embargo, es posible que asi queden algunos complejos sin analizar por superar
#o bien el ligando o bien el receptor ese numero de atomos.
r_lov = datos_fich_input[4]


#Lista de claves de "ligando_bound", "ligando_unbound", "receptor_bound"
#y "receptor_unbound":
l_clav = ["l_b", "l_u", "r_b", "r_u"]
#Variable para contener los angulos chi mas estables de los
#residuos individualmente:
chi_equ = func_lambda.leer_fichero_angulos_chi_equilibrio()
#c va a contener las coincidencias de las bases de datos:
c = []
#tuplas va a contener las coincidencias de las bases de datos con la 
#constante de disociacion especifica de cada una:
tuplas = []
#resul_fin va a ser otra lista de tuplas. En este caso va a contener los
#pares valor de lambda del complejo-constante de disociacion del complejo:
resul_fin = []


#Verficiacion de que el complejo indicado en el archivo de la constante de 
#disociacion y el indicado por los ficheros de estructura son los mismos:
print "Comprobando concordancia de los datos.."
c = extraer_infor_bases_de_datos.coincidencias_fichero_termodinamico_y_estructuras_pdb_benchmark(f_ter, d_ben)
if len(c) == 0:
    print "El nombre del complejo no coincide."
    sys.exit()


#Extraccion de informacion termodinamica (ctes de disociacion):"
print "\nExtrayendo informacion termodinamica.."
tuplas = extraer_infor_bases_de_datos.extraer_cte_disociacion(c, f_ter)


#Si no existe el fichero de angulos chi de equilibrio en el directorio
#de trabajo se avisa al usuario y se termina el programa:
listar_elementos_directorio_trabajo = "ls " + d_trab
elementos_directorio_trabajo = os.popen(listar_elementos_directorio_trabajo).read()
if "angulos_chi_equilibrio" not in elementos_directorio_trabajo:
    print "No existe el fichero de angulos chi de equilibrio. Para crearlo use el script calculador_de_chi_angles_de_equilibrio_para_cada_aminoacido.py"
    sys.exit()

#Si no existe un directorio llamado fich_temporales (corresponde a 
#los alineamientos estructurales) en el directorio de trabajo se crea:
if "fich_temporales" not in elementos_directorio_trabajo:
    crear_directorio = "mkdir " + d_trab + "fich_temporales"
    os.system(crear_directorio)
    print "\nAlineamientos estructurales.."
    os.system("sleep 2")
    alineamientos_estruc.calcular(tuplas, "fich_temporales/", r_lov, d_ben)

#Si no existe un directorio llamado "otros_arch_temps" (contiene ficheros
#generados por el script de R de analisis de los alineamientos estructurales)
#en el directorio de trabajo se crea:
if "otros_arch_temps" not in elementos_directorio_trabajo:
    crear_directorio = "mkdir " + d_trab + "otros_arch_temps"
    os.system(crear_directorio)



print "\n\n\nAnalizando resultados de los alineamientos.."


for i in tuplas:
    #Si no se han podido realizar previamente los cuatro alineamientos del complejo
    #(es decir, si no existen todos los ficheros .dat correspondientes) se salta
    #esa iteracion (ademas mediante la variable senal se cuentan dichos saltos):
    aux1 = d_trab + "fich_temporales/" + "rmsf_" + i[0].upper() + "_l_b.dat"
    aux2 = d_trab + "fich_temporales/" + "rmsf_" + i[0].upper() + "_l_u.dat"
    aux3 = d_trab + "fich_temporales/" + "rmsf_" + i[0].upper() + "_r_b.dat" 
    aux4 = d_trab + "fich_temporales/" + "rmsf_" + i[0].upper() + "_r_u.dat"
    if (os.path.isfile(aux1) & os.path.isfile(aux2) & os.path.isfile(aux3) & os.path.isfile(aux4) == False):
        senal = senal + 1
        print "No se han podido realizar los alineamientos estructurales necesarios."
        sys.exit()  

    
    #Si en cambio se han podido realizar los cuatro alineamientos del complejo:
    
    #Se actualiza primero el contador del complejo que se esta analizado:
    contad = contad + 1
    print "Analizando complejo " + str(contad) + ".."

    #Reseteo de los valores de lambda para cada una de las cuatro proteinas:
    lam_ligando_bound = 0.0
    lam_ligando_unbound = 0.0
    lam_receptor_bound = 0.0
    lam_receptor_unbound = 0.0

    #Senal para saber si el complejo ha podido ser analizado (un valor igual a 
    #cero indica que todo va funcionando):
    senal_analisis_comp = 0
    #Para cada una de las cuatro proteinas en cuestion("ligando_bound",
    #"ligando_unbound", "receptor_bound" y "receptor_unbound"):    
    for j in l_clav:
        #Ruta del fichero pdb de la proteina en cuestion:
        ruta_pdb = d_ben + i[0].upper() + "_" + j + ".pdb"
        #Generacion del objeto Complex:
        atoms, residues, chains = parse_complex_from_file(ruta_pdb)
        try:
            proteina_complejo = Complex(chains, atoms)
        except:
            senal_analisis_comp = 1

        #Ruta del fichero con los resultados del alineamiento de la proteina
        #en cuestion con su par bound/unbound:
        alin = d_trab + "fich_temporales/" + "rmsf_" + i[0].upper() + "_" + j + ".dat"
        #res_cam va a contener los indices de lor residuos que cambian de
        #posicion en la proteina en cuestion:
        res_cam = alineamientos_estruc.analizar(r_lin, alin, d_trab + "otros_arch_temps/" + i[0] + j + ".out")
     
        #Adaptacion de res_cam a la nomenclatura de indices de
        #lightdock.structure.complex. Como la indexacion en
        #lightdock.structure.complex es 0, 1, 2, ... es necesario
        #restar la diferencia existente. Ademas, en este paso
        #se va a convertir los elementos de res_cam de strings a integers:
        try:
            diferencia = primer_indice_res.buscar_primer_indice(ruta_pdb)
            w = 0
            #print res_cam
            while w < len(res_cam):
                res_cam[w] = int(res_cam[w]) - diferencia
                w = w + 1
            #print res_cam
        except:
            senal_analisis_comp = 1


        #Calculo de la contribucion de lambda de la proteina en cuestion.
        #Para ello, se van analizando los angulos chi de cada uno de
        #los residuos indexados por res_cam:

        #Contador de residuos que no han podido ser analizados. Si supera el umbral
        #de 1/10 de los residuos que cambian de esa proteina entonces el conjunto de
        #4 alineamientos al que pertenece la proteina no es contabilizado
        #(senal_analisis_comp valdria 1):
        residuos_con_errores = 0
        #Calculo de la contribucion de lambda de la proteina en cuestion:
        for h in res_cam:
            #Senal de que ha habido un error analizando ese residuo:
            senal_error = 0
            #Creacion del objeto residuo:
            try:
                residuo = proteina_complejo.residues[h]
            except:
                residuos_con_errores = residuos_con_errores + 1
                senal_error = 1
            #Calculo de los angulos chi del residuo:
            try:
                ang_chi = calculate_chi_angles(residuo)
            except:
               if senal_error == 0:
                    residuos_con_errores = residuos_con_errores + 1 
                    senal_error = 1
            #Calculo de la contribucion a lambda del residuo:
            try:
                res_la = func_lambda.contribucion_residuo(residuo.name, ang_chi, chi_equ)
            except:
                if senal_error == 0:
                    residuos_con_errores = residuos_con_errores + 1 
                    senal_error = 1        

            #Actualizacion de los valores de lambda de la proteina 
            #en cuestion si el residuo ha podido ser analizado:
            if senal_error == 0:
                if j == "l_b":
                    lam_ligando_bound = lam_ligando_bound + res_la
                if j == "l_u":
                    lam_ligando_unbound = lam_ligando_unbound + res_la
                if j == "r_b":
                    lam_receptor_bound = lam_receptor_bound + res_la
                if j == "r_u":
                    lam_receptor_unbound = lam_receptor_unbound + res_la

                
        #Si para la proteina en cuestion 1/10 de los residuos que debian ser
        #analizados no han podido ser analizados, entonces se descarta el 
        #complejo del que forma parte la proteina para el ouput del programa:   
        if residuos_con_errores >= (len(res_cam)/10):
            senal_analisis_comp = 1
    
    #Calculo del valor de lambda del complejo (si todo ha funcionado
    #correctamente):
    if senal_analisis_comp == 0:
        lam_comp = lam_ligando_unbound + lam_receptor_unbound - (lam_ligando_bound + lam_receptor_bound)
        #Actualizacion de la lista de tuplas de resultados 
        #(lam_comp, cte_disociacion del complejo):
        par_lam_comp_cte_disoc = (lam_comp, i[1])
        resul_fin.append(par_lam_comp_cte_disoc)
        #Actualizacion del contador de complejos analizados:
        comp_analizados = comp_analizados + 1

#Creacion de uno de los ficheros que va a utilizar el script codigo_en_R_para_prueba_de_hipotesis_con_el_modelo_y_datos_del_problema.R:            
g = open("problema.txt", "w")
for i in resul_fin:
    g.write(str(i[1]))
    g.write("\n")
    g.write(str(i[0]))
g.close()


#Ejecucion del script 
#codigo_en_R_para_prueba_de_hipotesis_con_el_modelo_y_datos_del_problema.R:
os.system("Rscript codigo_en_R_para_prueba_de_hipotesis_con_el_modelo_y_datos_del_problema.R")

#Lectura del output del script ejecutado para concluir sobre el rechazo o no rechazo de los 
#datos del problema al modelo:
h = open("sobre_el_rechazo_de_la_hipotesis.txt", "r")
output_final = h.read().splitlines()
h.close()
if output_final[0] == "NO":
    print "No se rechaza la hipotesis de que los datos del problema se ajusten al modelo."
else:
    print "Se rechaza la hipotesis de que los datos del problema se ajusten al modelo."








