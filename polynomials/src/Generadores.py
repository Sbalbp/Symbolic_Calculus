# -*- coding: UTF-8 -*-

import math
from time import time, clock
import sys
import random
import sets
import Polinomios

# Calcula el inverso de a en Zn
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

# Calcula un generador en Zp
def getGenerador(p):
	listaPrimos = factorizacion_fermat(p-1)
	
	if listaPrimos == None:
		print("Error. Valor invalido")
		exit()
		
	n = listaPrimos.count(2)
	
	setPrimos = set(listaPrimos)
	try:
		setPrimos.remove(1)
	except KeyError:
		pass
		
	for numero in xrange(2,p):
		esGenerador = True
		for factor in setPrimos:
			pot = potencia_modulo(numero,(p-1)/factor,p)
			if pot == 1:
				esGenerador = False
				break
		if esGenerador:			
			return [numero,n]
		
	return None
	
# Calcula una raiz de grado n en Zp
def getRaizNesima(p,n):
	if (p < 0):
		return complex(math.cos((math.pi*2)/n), math.sin((math.pi*2)/n))

	gen = getGenerador(p)
	gen1 = gen[0]
	gen2 = gen[1]
	
	if ((gen1 == None) or (((p-1)%n)!= 0)):
		return None
	
	return potencia_modulo(gen1,(p-1)/n,p)

# Devuelve si N es primo o no
def primalidad_probabilistica(N = None, rondas = None, evitar_salida = False):
	if not N: N = entrada_segura('Introduzca el valor de N :', type_numer = True)
	if not rondas:
		rondas = input('Introduzca cantidad máxima de rondas O porcentaje de probabilidad (con %):')

		if rondas[-1] == '%':
			probabilidad = float(rondas[:-1])
			rondas = 0
			while (1 - (1/4)**rondas)*100.0 < probabilidad:
				rondas += 1
				
		elif rondas.isdigit():
			rondas = int(rondas)
		else:
			if not evitar_salida: print("Error en entrada.")
			return False

	probabilidad = 	1 - (1/4)**rondas

	# Mecanismo básico
	if N % 10 not in [1,3,7,9]: return False
	if N < 10:
		if N in [3,5,7]: return True
		else: return False

	# Comprobación de demasiadas rondas
	if rondas >= int(N * 0.4):
		if not evitar_salida: print ("Demasiadas rondas para un número pequeño")
		return False

	usados = []
	for _ in range(rondas):
		a_escogido = False
		while not a_escogido:
			a = random.randint(3, N-1) # No sirve que sea 1, ni que sea igual a N-1
			# Comprobaciones de selección de a
			if (a not in usados) and (a % 10 in [1,3,7,9]):
				usados.append(a)
				a_escogido = True

		# Descomposición de N-1
		s = 0
		r = N-1
		while (r % 2 == 0):
			s += 1
			r = r // 2

		b = potencia_modulo(a, r, N)
		if b in [N-1, 1]: continue

		siguiente_ronda = False
		for i in range(1, s):
			#b = modulo(a, r**(2*i), N)
			b = (b ** 2)%N
			if b == N-1:
				siguiente_ronda = True
				break
			elif b == 1:
				break


		if not siguiente_ronda: return False

	# No tengo motivos para creer que no sea primo
	if not evitar_salida: print("Probabilidad: {0}%".format(probabilidad*100.0))
	return True	
	
# Devuelve el valor de la potencia a**b mod p
def potencia_modulo(a = None, b = None, p = None):

	if not a: a = entrada_segura('Introduzca el valor de a (base):', type_numer = True)
	if b==None: b = entrada_segura('Introduzca el valor de b (exponente):', type_numer = True)
	if not p: p = entrada_segura('Introduzca el valor de p (módulo):', type_numer = True)
	
	r = 1
	
	while b != 0:
		if b % 2 == 1:
			r = (r*a)%p
			b = (b-1)//2
		else:
			b = b// 2
		a = (a*a)%p
	
	return r
	
def isqrt(x):
	if x < 0:
		raise ValueError('ERROR. Raíz cuadrada de un número negativo.')

	n = int(x)
	if n == 0: return 0

	a, b = divmod(n.bit_length(), 2)
	x = 2**(a+b)

	while True:
		y = (x + n//x)//2
		if y >= x: return x
		x = y
		
def is_square(n):
	referencia = isqrt(n)
	if referencia ** 2 == n: return True
	return False

# Devuelve la factorizacion de n como producto de primos
def factorizacion_fermat(n = None):

	if not n: return None
	
	if primalidad_probabilistica(n,10,True):
		return [int(n)]
		
	resultado = []
		
	while (n%2 == 0):
		resultado.append(2)
		n = n//2
		
	if n==1:
		resultado.append(1)
		return resultado
	
	x = isqrt(n)+1
	y = x*x-n

	while(not is_square(y)):
		x = x+1
		y = x*x-n
		
	y = isqrt(y)
	
	if(x+y == n or x-y == n):
		resultado.append(int(n))
		return resultado
	
	resultado.extend(factorizacion_fermat(x+y))
	resultado.extend(factorizacion_fermat(x-y))
	
	return resultado
	
def entrada_segura(mensaje, paciencia = None, type_numer = False, type_list = False):
	a = None
	veces = 0
	
	if not (type_numer or type_list): return None
	
	while (a == None):
		if paciencia and veces > paciencia: exit
		a = raw_input(mensaje + ' ')
		if type_numer and (a.isdigit() or (a[0] == '-' and a[1:].isdigit())):
			a = int(a)
		elif type_list and a in type_list:
			pass
		else:
			print ('Valor invalido.')
			a = None
			
	return a
	