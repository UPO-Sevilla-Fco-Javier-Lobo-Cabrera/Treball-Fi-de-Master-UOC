import os

def transformacion_de_unidades_a_nm(val):
    "Devuelve el valor en nanomolar a partir de datos en fM, uM .. (pe '2uM')"

    #Parte numerica de val:
    numer = ""

    #Indice para controlar las posiciones de val:
    ind = 0
    
    #Variable auxiliar:
    auxil = 0

    #Bucle para ir construyendo el valor:
    while auxil == 0:
        #Si se esta en la parte numerica de val:
        if val[ind] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", r"."]:
            numer = numer + val[ind]
            ind = ind + 1
        else:
            auxil = 1
            numer = float(numer)
            #Si se trata de milimolar:            
            if val[ind] == "m":
                numer = numer * 1000000
            #Si se trata de micromolar:            
            if val[ind] == "u":
                numer = numer * 1000
            #Si se trata de picomolar:            
            if val[ind] == "p":
                numer = numer / 1000
            #Si se trata de fentomolar:            
            if val[ind] == "f":
                numer = numer / 1000000
   
    return(numer) 
                


def coincidencias_fichero_termodinamico_y_estructuras_pdb_benchmark(ruta_fichero_termodinamico, ruta_absoluta_directorio_benchmark_structures):
    "Devuelve coincidencias entre benchmark y la base de datos termodinamica"

    #Fichero base de datos termodinamicos tipo INDEX_general_PP.2016 PDBBind:
    f=open(ruta_fichero_termodinamico,"r")
    lis = f.readlines()
    f.close()

    #Lista de ficheros pdb en directorio de benchmark structures:
    ficheros_pdb_benchmark_structures = []
    for f in os.listdir(ruta_absoluta_directorio_benchmark_structures):
        ficheros_pdb_benchmark_structures.append(f)

    #Lista de coincidencias:
    coinc = []

    for i in lis:
        #Si hay coincidencia del elemento (codigo PDB) y todavia no ha
        #sido registrado entonces se registra en coinc:
        for j in ficheros_pdb_benchmark_structures:
            if ((i[0:4].upper() in j) and (i[0:4] not in coinc)):
                coinc.append(i[0:4])

    return(coinc)
    


def coincidencias_fichero_termodinamico_y_fichero_dockground(ruta_fichero_termodinamico, ruta_fichero_dockground):
    "Devuelve coincidencias la base de datos termodinamica y DOCKGROUND"
   
    #Fichero base de datos termodinamicos tipo INDEX_general_PP.2016 PDBBind:
    f=open(ruta_fichero_termodinamico,"r")
    lis2 = f.readlines()
    f.close()
 
    #Fichero Dockground:
    f=open(ruta_fichero_dockground,"r")
    lis = f.readlines()
    f.close()

    #Lista de coincidencias:
    coinc = []
    for i in lis:
        for j in lis2:
            if i[0:4] in j:
		coinc.append(i[0:4])

    return(coinc)



def extraer_cte_disociacion(lista_complejos_pdb, ruta_fichero_termodinamico):
    "Devolver lista de tuplas PDB-Kd a partir de una lista de complejos PDB"

    #Fichero base de datos termodinamicos tipo INDEX_general_PP.2016 PDBBind:
    f=open(ruta_fichero_termodinamico,"r")
    lista1 = f.readlines()
    f.close()

    #Lista de tuplas:
    tuplas = []
    
    #Constante de disociacion
    kd = ""

    #Indice para controlar las posiciones para leer el dato de Kd:
    indice = 21

    #Bucle para obtener las tuplas:
    for i in lista_complejos_pdb:
        for j in lista1:
            if i in j:
                #Asegurar que existe una kd:
                if "Kd=" in j:
                    #Variable auxiliar:
                    aux = 0
                    #Bucle para ir construyendo kd:
                    while aux == 0:
                        #Si no se ha llegado al final del dato de kd:
                        if j[indice] != "M":
                            kd = kd + j[indice]
                            indice = indice + 1
                        else:
                            #Transformacion de unidades a nm (y ademas se 
                            #transforma kd de string a float):
                            kd = transformacion_de_unidades_a_nm(kd)
                            #Nuevo elemento en la lista de tuplas:
                            tuplas.append((i, kd))
                            #Reseteo de kd:
                            kd = ""
                            #Reseteo de indice:
                            indice = 21
                            #Cambio de aux:
                            aux = 1
    
    return(tuplas)
