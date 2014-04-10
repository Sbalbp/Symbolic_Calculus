# -*- coding: UTF-8 -*-

import math
from time import time, clock
import sys

import Enteros

baseOperaciones = 2**16

l = []

def quitaRetorno(cadena):
	if (cadena[-1] == '\n'):
		aux = cadena[0:-1]
	else:
		aux = cadena
		
	try:
		aux = int(aux)
		return aux
	except ValueError:
		print("Error. Uno de los valores en el fichero no es un entero\n")
		exit()

def inverso (n, a):
	y = 0
	v = 1
	r = n % a
	mod = n
	
	while(r != 0):
		c = n // a
		aux = y
		y = v
		v = aux - v*c
		n = a
		a = r
		r = n % a
	if (a != 1):
		print("No existe el inverso")
		return 0
	return (v%mod)

def pasoVector(num, lista):
	base = Enteros.EnteroArbitrario(baseOperaciones,10)
	num.toBase(base,10)

	long = len(lista)
	
	result = [0]*long
	for i in xrange(long):
		div = Enteros.OperacionesEnteros.division(num, Enteros.EnteroArbitrario(10,lista[i]))
		result[i] = div[1].listaToEntero()

	return result
	
def multVector(v1,v2,base):
	long = len(v1)

	r = [0]*long

	for i in xrange(long):
		r[i] = (v1[i]*v2[i])%base[i]
		
	return r
	
def calculaTablaInversos(base):
	long = len(base)

	tabla = [0]*(long-1)

	for i in xrange(long-1):
		tabla[i] = [0]*long
		for j in xrange(i+1,long):
			tabla[i][j] = inverso(base[j],base[i])
	
	return tabla
	
def calculoY(base,lista,tabla):
	long = len(base)

	y = [0]*long
	
	for i in xrange(long):
		aux = lista[i]
		for j in xrange(i):
			aux = (aux-y[j])*tabla[j][i]
		y[i] = aux%base[i]
		
	return y
	
def finalizacionModular(y,m):
	leny = len(y)

	yE = [0]*leny
	mE = [0]*len(m)
	aux = [0]*leny
	
	for i in xrange(leny):
		yE[i] = Enteros.EnteroArbitrario(baseOperaciones,y[i])
		mE[i] = Enteros.EnteroArbitrario(baseOperaciones,m[i])
		
		aux[i] = yE[i]
		for j in xrange(i):
			aux[i] = Enteros.OperacionesEnteros.multiplicacion(aux[i],mE[j])
		
	res = aux[0]
	
	for i in xrange(1,leny):
		res = Enteros.OperacionesEnteros.suma(res,aux[i])
		
	return res

# Devuelve los numeros pasados a forma de vector y la base
def inicializacionModular(a,b):
	base = []
	total = len(a.numero)+len(b.numero)
	
	acumulado = 0
	for i in l:
		base.append(i)
		aux = Enteros.EnteroArbitrario(baseOperaciones,i)
		acumulado = acumulado + len(aux.numero)
		if(acumulado > total):
			break
	
	v1 = pasoVector(a, base)
	v2 = pasoVector(b, base)
	
	tablaInversos = calculaTablaInversos(base)
	
	return [v1,v2,base,tablaInversos]

# Recibe los vectores y la base y calcula el producto
def multiplicacionModular( v1, v2, base, tablaInversos):
	prod = multVector(v1,v2,base)
	y = calculoY(base,prod,tablaInversos)
	
	return [y,base]

	
def expo(i, maxExpo):
	a = math.log(2,i)
	a = a*maxExpo
	a = a-1
	a = math.ceil(a)
	return a
	


def listaPrimos(maxExpo):
	lista = []

	try:
		f = open("primos.txt",'r')
	except IOError:
		for i in xrange(2,2**maxExpo):
	
			primo = 1
			for j in xrange(2,i):
				if(i%j == 0):
					primo = 0
			if(primo == 1):
				e = int(i**expo(i,maxExpo))
				lista.append(e)

		lista.sort()
		lista.reverse()
		
		f = open("primos.txt",'w')
		for i in lista:
			f.write(str(i))
			f.write('\n')
		
		return lista
		
	lista = f.readlines()
	lista = map(lambda x: quitaRetorno(x), lista)
	return lista
	
if sys.version_info[0] >= 3:
	print('\nERROR: Este programa debe ejecutarse con una version de Python inferior a la 3.\n')
	sys.exit()		

print('')
print(' '+'*'*64)
print(' *' + 'Calculo Simbolico 12/13 - P1: Aritmetica Entera'.center(62) + '*')
print(' '+'*'*64)
print(' *    ' + '1) Suma'.ljust(58) + '*')
print(' *    ' + '2) Resta'.ljust(58) + '*')
print(' *    ' + '3) Division'.ljust(58) + '*')
print(' *    ' + '4) Multiplicacion Escolar'.ljust(58) + '*')
print(' *    ' + '5) Multiplicacion Karatsuba'.ljust(58) + '*')
print(' *    ' + '6) Multiplicacion Modular'.ljust(58) + '*')
print(' *    ' + ''.ljust(58) + '*')
print(' *    ' + ''.ljust(58) + '*')
print(' *    ' + '7) Comparativa de tiempos'.ljust(58) + '*')
print(' *    ' + ''.ljust(58) + '*')
print(' *    ' + 'Q) Salir'.ljust(58) + '*')
print(' '+'*'*64)

i=1

entrada = None
while (entrada == None):
	entrada = raw_input('Seleccione una opcion: ').upper()
		
	if (entrada == 'Q' or i == 5):
		exit()
	elif (entrada.isdigit() and int(entrada) > 0 and int(entrada) <= 7):
		entrada = int(entrada)
	else:
		entrada = None
		i += 1
	
entero1 = Enteros.EnteroArbitrario(10)
entero2 = Enteros.EnteroArbitrario(10)
resultado = Enteros.EnteroArbitrario(baseOperaciones)

if(entrada < 7):

	#Leemos los numeros
	ruta = raw_input('Introduzca la ruta del fichero en el que se encuentra el primer entero\n(dejar en blanco para introducir por teclado)\n')
	if(len(ruta) > 0):
		entero1.leeNumero(ruta)
	else:
		entero1.leeNumero()
		
	ruta = raw_input('Introduzca la ruta del fichero en el que se encuentra el segundo entero\n(dejar en blanco para introducir por teclado)\n')
	if(len(ruta) > 0):
		entero2.leeNumero(ruta)
	else:
		entero2.leeNumero()
	
	# Pasamos los numeros a la base correspondiente
	base = Enteros.EnteroArbitrario(10,baseOperaciones)
	entero1.toBase(base,baseOperaciones)
	entero2.toBase(base,baseOperaciones)
		
	if entrada == 1:
		ti = time()
		resultado = Enteros.OperacionesEnteros.suma(entero1,entero2)
		t1 = (time() - ti)
	if entrada == 2:
		ti = time()
		resultado = Enteros.OperacionesEnteros.resta(entero1,entero2)
		t1 = (time() - ti)
	if entrada == 3:
		ti = time()
		resultDiv = Enteros.OperacionesEnteros.division(entero1,entero2)
		t1 = (time() - ti)
		
		base = Enteros.EnteroArbitrario(baseOperaciones,10)
		resultDiv[0].toBase(base,10)
		print('Cociente = ')
		resultDiv[0].mostrar()
		resultDiv[1].toBase(base,10)
		print('Resto = ')
		resultDiv[1].mostrar()
	if entrada == 4:
		ti = time()
		resultado = Enteros.OperacionesEnteros.multiplicacion(entero1,entero2)
		t1 = (time() - ti)
	if entrada == 5:
		
		if(len(entero1.numero)>len(entero2.numero)):
			mayor = len(entero1.numero)
		else:
			mayor = len(entero2.numero)
		m = math.floor(math.log(mayor,2))+1


		ti = clock()
		resultado = Enteros.OperacionesEnteros.multiplicacionKaratsuba(entero1,entero2, int(m))
		t1 = (clock() - ti)
		
	if entrada == 6:
		l = listaPrimos(16)
	
		aux = inicializacionModular(entero1,entero2)
		ti = clock()
		aux = multiplicacionModular(aux[0],aux[1],aux[2],aux[3])
		t1 = (clock() - ti)
		resultado = finalizacionModular(aux[0],aux[1])
	
	if entrada != 3:
		base = Enteros.EnteroArbitrario(baseOperaciones,10)
		resultado.toBase(base,10)
		print('\nResultado = ')
		resultado.mostrar()
		
	print ("Tiempo empleado: ",t1,".")
	
elif entrada == 7:	
	
	# Pasamos los numeros a la base correspondiente
	base = Enteros.EnteroArbitrario(10,baseOperaciones)
	entero1.toBase(base,baseOperaciones)
	entero2.toBase(base,baseOperaciones)	

	try:
		baseOperaciones = int(input("Introduzca el valor de la base:\n"))
	except ValueError:
		print("Error. La base debe ser un valor numerico mayor o igual a 10\n")
		exit()
	
	if (baseOperaciones < 10):
		print("Error. La base ha de ser mayor o igual a 10\n")
		exit()
	try:	
		digitos = int(input("Introduzca el numero de digitos de los numeros:\n"))
	except ValueError:
		print("Error. El numero de digitos debe ser un valor numerico mayor que 0\n")
		exit()
		
	if (digitos < 1):
		print("Error. El numero de digitos debe ser superior a 0\n")
		exit()
	
	try:	
		iteraciones = int(input("Introduzca el numero de repeticiones:\n"))
	except ValueError:
		print("Error. El numero de repeticiones debe ser un valor numerico mayor que 0\n")
		exit()
		
	if (iteraciones < 1):
		print("Error. El numero de iteraciones debe ser superior a 0\n")
		exit()
		
	l = listaPrimos(16)
	tme = tmk = tmm = 0
	
	for i in xrange(0,iteraciones):
		# Dos enteros aleatorios en cada iteracion
		entero1.aleatorio(digitos)
		entero2.aleatorio(digitos)
		
		
		ti = clock()
		Enteros.OperacionesEnteros.multiplicacion(entero1,entero2)
		t1 = (clock() - ti)
		tme = tme+t1
	
		# Calculo de m usada por Karatsuba
		if(len(entero1.numero)>len(entero2.numero)):
			mayor = len(entero1.numero)
		else:
			mayor = len(entero2.numero)
		m = math.floor(math.log(mayor,2))+1
		
		ti = clock()
		Enteros.OperacionesEnteros.multiplicacionKaratsuba(entero1,entero2, int(m))
		t1 = (clock() - ti)
		tmk = tmk+t1
		
		aux = inicializacionModular(entero1,entero2)
		ti = clock()
		aux = multiplicacionModular(aux[0],aux[1],aux[2],aux[3])
		t1 = (clock() - ti)
		resultado = finalizacionModular(aux[0],aux[1])
		tmm = tmm+t1
		
	tme = tme/iteraciones
	tmk = tmk/iteraciones
	tmm = tmm/iteraciones
	
	print("Tiempo medio empleado por:")
	print("Multiplicacion Escolar: ",tme)
	print("Multiplicacion de Karatsuba: ",tmk)
	print("Multiplicacion Modular: ",tmm)
	
