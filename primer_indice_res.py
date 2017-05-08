

def buscar_primer_indice(ruta_fich):
    '''Busca el indice del primer residuo del fichero .pdb'''

    indice_res = ""
    f = open(ruta_fich, "r")
    primera_linea = f.readline()
    #Contador de secciones en blanco:
    contador = 0
    #Controlador para desplazarse por la linea:
    con = 0
    #Senal para indicar si se ha identificado ya el indice:
    senal_fin = 0
    #Senal para saber si el indice estaba en la quinta columna del 
    #fichero .pdb y no en la sexta:
    senal_indice_no_en_columna_6 = 0
    
    #Recorrer la linea:
    while senal_fin == 0:
        #Si no es el primer caracter:
        if con != 0:
            #Detectar seccion en blanco:
            if (primera_linea[con] == " ") & (primera_linea[con - 1] != " "):
                contador = contador + 1

        #Si contador == 4 y el fichero PDB no tenia identificador de cadena 
        #entonces se puede estar ante el indice del residuo:
        if contador == 4:
            #Dado que el identificador de cadena es un caracter (no es "int"):
            if primera_linea[con] in ["0","1","2","3","4","5","6","7","8","9"]:
                indice_res = indice_res + primera_linea[con]
                senal_indice_no_en_columna_6 = 1


        #Si contador == 5 y primera_linea[con] != " " se esta
        #en el indice del residuo, siempre que no estuviera
        #en la columna anterior:
        if (contador == 5) & (primera_linea[con] != " "):
           if senal_indice_no_en_columna_6 == 0:
               indice_res = indice_res + primera_linea[con]
         
        #Si ya se ha identificado el indice:
        if (contador > 5):
            senal_fin = 1
 
        con = con + 1
    
    indice_res = int(indice_res)
    return (indice_res)
      
