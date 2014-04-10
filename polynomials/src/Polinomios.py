# -*- coding: UTF-8 -*-

import random
import copy
import math
import Generadores

def quitaRetorno(cadena,p):
	if (cadena[-1] == '\n'):
		aux = cadena[0:-1]
	else:
		aux = cadena
		
	try:
		if ( p > 0):
			aux = int(aux)%p
		else:
			aux = int(aux)
		return aux
	except ValueError:
		print("Error. Uno de los valores en el fichero no es un entero\n")
		exit()
		
def expo(numero):
	return int(math.floor(math.log(numero,2)+1))

class Polinomio:
	
	def __init__(self, p = 0):
		self.p = p
		self.coeficientes = []
		self.grado = -1
		
	def leePolinomio(self, fichero = None):
		self.coeficientes = []
		self.grado = -1
	
		if(fichero != None):
			try:
				f = open(fichero,'r')
			except IOError:
				print("Error. El fichero indicado no existe\n")
				exit()
			cadena = f.readlines()
			
			coeficientes = map(lambda x: quitaRetorno(x, self.p), cadena)
			
			if self.p >= 0:
				self.coeficientes = coeficientes
			else:
				i = 0
				long = len(coeficientes)
				while i<long:
					if (i+1 == long):
						aux = 0
					else:
						aux = coeficientes[i+1]
					self.coeficientes.append(complex(coeficientes[i],aux))
					i = i+2
			
			self.grado = len(self.coeficientes)-1
		else:
			print("Introduzca los valores de los coeficientes\n(Introduzca algun valor no numerico para terminar)")
			
			i = 0
			seguir = True
			
			while(seguir):
				cadena = raw_input()
			
				if cadena.isdigit() or (len(cadena) > 0 and cadena[0] == '-' and cadena[1:].isdigit()):
					cadena = int(cadena)
					if (self.p == 0):
						self.coeficientes.append(cadena)
					elif (self.p < 0):
						if (i%2 == 0):
							real = cadena
							imag = 0
						else:
							imag = cadena
							self.coeficientes.append(complex(real,imag))
					else:
						self.coeficientes.append(cadena%self.p)
					i = i+1
				else:
					seguir = False
			
			if(i%2 == 1 and self.p < 0):
				self.coeficientes.append(complex(real,imag))
			
			self.grado = len(self.coeficientes)-1
	
			
	def aleatorio(self, size=1):
		self.coeficientes = []
		self.grado = size-1
		
		for i in xrange(0,size):
			if ( self.p <= 0):
				real = random.randint(0,2**16)
				imag = random.randint(0,2**16)
				self.coeficientes.append(complex(real,imag))
			else:
				self.coeficientes.append(random.randrange(1,self.p))
		
	def multiplicar(self, multiplicador=1):
		for i in xrange(0,self.grado+1):
			if (self.p<=0):
				self.coeficientes[i] = (self.coeficientes[i]*multiplicador)
			else:
				self.coeficientes[i] = (self.coeficientes[i]*multiplicador)%self.p
			
	def mostrar(self):
		cadena = ""
		for i in xrange(0,self.grado+1):
			if(self.coeficientes[i] != 0):
				if(i!=0):
					cadena = cadena+' + '+str(self.coeficientes[i])+'*x^'+str(i)
				else:
					cadena = cadena+str(self.coeficientes[i])
		print cadena

class OperacionesPolinomios:

	@staticmethod
	def multiplicacionEscolar(op1, op2):
		resultado = Polinomio(op1.p)
		resultado.coeficientes = [0]*(op1.grado+op2.grado+1)
		
		for k in xrange(0,op2.grado+1):
			for i in xrange(0,op1.grado+1):
				resultado.coeficientes[k+i] = (op1.coeficientes[i]*op2.coeficientes[k]+resultado.coeficientes[i+k])
				
				if(resultado.p > 0):
					resultado.coeficientes[k+i] = resultado.coeficientes[k+i]%resultado.p
				
		resultado.grado = len(resultado.coeficientes)-1
		return resultado
		
	@staticmethod
	def FFT(m,raiz,op,p):
		listaA = []
		b = Polinomio(1)
		c = Polinomio(1)
		
		it = 2**(m-1)
		b.coeficientes = [0]*int(it)
		c.coeficientes = [0]*int(it)
		
	
		if (m == 0):
			listaA.append(op.coeficientes[0])
		else:
			if (op.p > 0):
				raiz2 = (raiz**2)%p
			else:
				raiz2 = (raiz**2)
			
			for i in xrange(0,it):
				try:
					b.coeficientes[i] = op.coeficientes[2*i]
					c.coeficientes[i] = op.coeficientes[2*i+1]
				except IndexError:
					pass
				
			listaB = OperacionesPolinomios.FFT(m-1,raiz2,b,p)#sin p
			listaC = OperacionesPolinomios.FFT(m-1,raiz2,c,p)#sin p
			
			listaA = [0]*(2**m)
			for i in xrange(0,it):
				if(p > 0):
					pass
					lb = listaB[i]%p
					
					sum = ((listaC[i]%p)*Generadores.potencia_modulo(raiz,i,p))%p
					listaA[i] = (lb + sum)%p
					listaA[(it)+i] = (lb - sum)%p
				else:
					listaA[i] = (listaB[i] + listaC[i]*(raiz**i))
					listaA[(2**(m-1))+i] = (listaB[i] - listaC[i]*(raiz**i))
		
		return listaA

	@staticmethod
	def multiplicacionFFT(op1,op2):
	
		if op1.p == 0 or op1.p != op2.p:
			print("Error. Los valores de p de los operandos son erroneos")
			exit()
	
		c = Polinomio(op1.p)
		m = op1.grado+op2.grado+1
		n = expo(m)
		raiz = Generadores.getRaizNesima(op1.p,2**n)
		
		if raiz == None:
			print("Error. Para el p = "+str(op1.p)+" dado no hay una raiz "+str(2**n)+"-esima")
			exit()
				
		if(op1.p > 0):		
			raizInversa = Generadores.inverso(op1.p,raiz)
			inversoExp = Generadores.inverso(op1.p,2**n)
		else:
			raizInversa = raiz**-1
			inversoExp = 2**(-n)	
		
		listaA = OperacionesPolinomios.FFT(n,raiz,op1,op1.p)		
		listaB = OperacionesPolinomios.FFT(n,raiz,op2,op2.p)
		listaC = []
		
		for i in xrange(0,2**n):
			if(op1.p > 0):
				listaC.append( (listaA[i]*listaB[i])%op1.p )
			else:
				listaC.append(listaA[i]*listaB[i])
			
		c.grado = len(listaC)-1
		c.coeficientes = listaC
		
		listaC = OperacionesPolinomios.FFT(n,raizInversa,c,c.p)
		
		c.grado = len(listaC)-1
		c.coeficientes = listaC
		c.multiplicar(inversoExp)
		
		return c