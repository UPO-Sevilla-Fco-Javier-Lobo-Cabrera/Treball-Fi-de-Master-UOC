#Calculo de angulos chi de equilibrio e impresion en fichero de
#output llamado angulos_chi_equilibrio.

import sys
import math

from lightdock.scoring.dfire.driver import DFIREAdapter
from lightdock.pdbutil.PDBIO import parse_complex_from_file
from lightdock.structure.complex import Complex
from lightdock.rotamer.predictor import get_interface_residues, calculate_chi_angles, steric_energy
from lightdock.rotamer.library import InterfaceSurfaceLibrary


#Para hacer funcionar script es necesario pasarle dos argumentos por 
#la linea de comandos. Dichos argumentos son una ruta de fichero y
#una ruta de directorio (explicado mas adelante).


#Ruta de fichero con abreviaturas de los aas (ALA, MET, ...)
#en una columna:
ruta_abreviaturas = sys.argv[1]

f = open(ruta_abreviaturas, "r")
lista_abreviaturas_aas = f.read().splitlines()
f.close()

#Eliminacion del ultimo elemento de la lista (espacio en blanco):
lista_abreviaturas_aas.pop()


#Ruta de directorio (acabado en "\") que contiene el fichero PDB
#de cada aa:
ruta_pdbs = sys.argv[2]


#Preparacion de fichero de output:
g = open("angulos_chi_equilibrio", "w") 

#Bucle de calculo:
for i in lista_abreviaturas_aas:
	g.write(i + " ")
	i = ruta_pdbs + i + ".pdb"		
	atoms, residues, chains = parse_complex_from_file(i)
	aminoacido = Complex(chains, atoms)
	residue = aminoacido.residues[0]
	chi_angles = calculate_chi_angles(residue)

	for chi, angle in chi_angles.iteritems():
		try:
			chi_angles[chi] = math.degrees(angle)
		except TypeError:
			pass
	
	s = str(chi_angles)
	g.write(s + "\n")



g.close()




	





	

	
	
	

