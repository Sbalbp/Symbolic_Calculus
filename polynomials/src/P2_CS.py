# -*- coding: UTF-8 -*-

import math
from time import time, clock
import sys
import random
import sets
import Polinomios
import Generadores


if sys.version_info[0] >= 3:
	print('\nERROR: Este programa debe ejecutarse con una version de Python inferior a la 3.\n')
	sys.exit()		

print('')
print(' '+'*'*64)
print(' *' + 'Calculo Simbolico 12/13 - P2: Multiplicacion de Polinomios'.center(62) + '*')
print(' '+'*'*64)
print(' *    ' + '1) Multiplicacion Escolar'.ljust(58) + '*')
print(' *    ' + '2) Multiplicacion por FFT'.ljust(58) + '*')
print(' *    ' + ''.ljust(58) + '*')
print(' *    ' + ''.ljust(58) + '*')
print(' *    ' + '3) Comparativa de tiempos'.ljust(58) + '*')
print(' *    ' + ''.ljust(58) + '*')
print(' *    ' + 'Q) Salir'.ljust(58) + '*')
print(' '+'*'*64)

i=1

entrada = None
while (entrada == None):
	entrada = raw_input('Seleccione una opcion: ').upper()
		
	if (entrada == 'Q' or i == 5):
		exit()
	elif (entrada.isdigit() and int(entrada) > 0 and int(entrada) <= 3):
		entrada = int(entrada)
	else:
		entrada = None
		i += 1

	
numero = Generadores.entrada_segura("Introduzca p (negativo para numeros complejos):",type_numer = True)

if numero == 0:
	print("Error. El valor de p no puede ser 0")
	exit()
	
pol1 = Polinomios.Polinomio(numero)
pol2 = Polinomios.Polinomio(numero)
	
if entrada < 3:
	#Leemos los polinomios
	ruta = raw_input('Introduzca la ruta del fichero en el que se encuentra el primer polinomio\n(dejar en blanco para introducir por teclado)\n\n')
	if(len(ruta) > 0):
		pol1.leePolinomio(ruta)
	else:
		pol1.leePolinomio()
		
	ruta = raw_input('Introduzca la ruta del fichero en el que se encuentra el segundo polinomio\n(dejar en blanco para introducir por teclado)\n\n')
	if(len(ruta) > 0):
		pol2.leePolinomio(ruta)
	else:
		pol2.leePolinomio()
		
	if entrada == 1:
		resultado = Polinomios.Polinomio(numero)
		
		ti = time()
		resultado = Polinomios.OperacionesPolinomios.multiplicacionEscolar(pol1,pol2)
		t1 = (time() - ti)
		
		print("\nResultado multiplicacion escolar: ")
		resultado.mostrar()
	else:
		resultado = Polinomios.Polinomio(numero)
		
		ti = time()
		resultado = Polinomios.OperacionesPolinomios.multiplicacionFFT(pol1,pol2)
		t1 = (time() - ti)
		
		print("\nResultado multiplicacion por FFT: ")
		resultado.mostrar()
		
	print ("Tiempo empleado: ",t1,".")
	
else:
	
	try:	
		ncoef = int(input("Introduzca el numero de coeficientes de los polinomios:\n"))
	except ValueError:
		print("Error. El numero de coeficientes debe ser un valor numerico mayor que 0\n")
		exit()
		
	if (ncoef < 1):
		print("Error. El numero de coeficientes debe ser superior a 0\n")
		exit()
	
	try:	
		iteraciones = int(input("Introduzca el numero de repeticiones:\n"))
	except ValueError:
		print("Error. El numero de repeticiones debe ser un valor numerico mayor que 0\n")
		exit()
		
	if (iteraciones < 1):
		print("Error. El numero de iteraciones debe ser superior a 0\n")
		exit()
		
	tme = tmf = 0
	
	for i in xrange(0,iteraciones):
		pol1.aleatorio(ncoef)
		pol2.aleatorio(ncoef)
		
		ti = clock()
		Polinomios.OperacionesPolinomios.multiplicacionEscolar(pol1,pol2)
		t1 = (clock() - ti)
		tme = tme+t1
		
		import profile
		ti = clock()
		Polinomios.OperacionesPolinomios.multiplicacionFFT(pol1,pol2)
		t1 = (clock() - ti)
		tmf = tmf+t1

	tme = tme/iteraciones
	tmf = tmf/iteraciones
	
	print("Tiempo medio empleado por:")
	print("Multiplicacion Escolar: ",tme)
	print("Multiplicacion por FFT: ",tmf)
