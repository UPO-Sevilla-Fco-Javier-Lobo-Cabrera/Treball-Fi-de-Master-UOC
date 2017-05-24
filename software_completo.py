import os

print "Bienvenido, introduzca (1) si desea solo generar un modelo lineal, (2) si desea testear unos datos frente al modelo generado, o (3) si desea testear unos datos frente a un modelo proporcionado por usted:"

decision = raw_input()

if decision == "1":
    os.system("python parte1.py")

if decision == "2":
    os.system("python parte1.py")
    os.system("python parte2.py")

if decision == "3":
    os.system("python parte2.py")
