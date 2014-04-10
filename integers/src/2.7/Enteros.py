# -*- coding: UTF-8 -*-

import random
import copy

class EnteroArbitrario:

	numero = []
	
	def __init__(self, base = 10, numero = 0):
		self.base = base
		self.signo = 1
		self.l = 0
		if(numero != 0):
			self.numero = self.decToBase(numero)
	
	def decToBase(self, num):
		target = []
		while(num >= self.base):
			target.append(num%self.base)
			num = num//self.base
		target.append(num)
		
		return target
		
	def toBase(self,num, num2):
		target = []

		while(self.comparacion(num) >= 0):
			result = OperacionesEnteros.division(self,num)
			target.append(result[1].listaToEntero())
			self.numero = result[0].numero

		target.append(self.listaToEntero())

		self.numero = target
		self.base = num2
		
	def leeNumero(self, fichero = None):
	
		if(fichero == None):
			cadena = raw_input("Introduzca un valor en base 10:\n")
		else:
			try:
				f = open(fichero,'r')
			except IOError:
				print("Error. El fichero indicado no existe\n")
				exit()
			cadena = f.read()
			
		self.numero = []
		for i in cadena:
			try:
				enteroPrueba = int(i)
			except ValueError:
				print("Error. El valor introducido no es numerico\n")
				exit()
			self.numero.insert(0,int(i))
			
		if (len(self.numero) == 0):
			print("Error. No se ha introducido un numero valido\n")
			exit()
			
	def aleatorio(self, size=1):
		self.numero = []
		self.signo = 1
		
		for i in range(1,size):
			self.numero.append(random.randrange(0,self.base))
		self.numero.append(random.randrange(1,self.base))
			
	def comparacion(self, op1):
		ls = self.limpiarCeros()
		l1 = op1.limpiarCeros()
		
		self.l = ls
		op1.l = l1
	
		if (self.base != op1.base):
			return -1
		else:
		
			if ( ls < l1 ):
				return -1
			elif ( ls > l1 ):
				return 1
			else:
				for i in xrange(ls-1,-1,-1):
					if ( self.numero[i] < op1.numero[i] ):
						return -1
					elif (self.numero[i] > op1.numero[i] ):
						return 1
				return 0
				
	def limpiarCeros(self):
		i = len(self.numero)-1
		while (i>0 and self.numero[i]==0):
			self.numero.pop()
			i = i-1
			
		return i+1
		
	def listaToEntero(self):
		if(len(self.numero) == 0):
			return 0
		cadena = str(self.numero)
		cadena = cadena[::-1]
		cadena = cadena.replace('[','')
		cadena = cadena.replace(']','')
		cadena = cadena.replace(',','')
		cadena = cadena.replace(' ','')
		cadena = cadena.replace('L','')
		
		return int(cadena)
		
	def mostrar(self):
		self.numero.reverse()
		
		cadena = str(self.numero)
		
		print(cadena)
		self.numero.reverse()
				
	def sumar(self, op1):
		c = copy.deepcopy(self)
		
		carry = op1
		i = 0
		while(carry > 0):
			if(i==len(c.numero)):
				c.numero.append(0)
			temp = c.numero[i]+carry
			c.numero[i] = temp%c.base
			carry = temp//c.base
			i = i+1
			
		return c
		
	def multiplicar(self, op1):
		c = copy.deepcopy(self)
		
		carry = 0
		for i in xrange(0,len(c.numero)):
			temp = c.numero[i]*op1 + carry
			c.numero[i] = temp%c.base
			carry = temp//c.base
			
		if(carry>0):
			c.numero.append(carry)
			
		return c
			
class OperacionesEnteros:

	@staticmethod
	def suma(op1, op2):
	
		# Si un operando es nagativo se devuelve una resta
		if(op1.signo == -1):
			return OperacionesEnteros.resta(op2,op1)
		if(op2.signo == -1):
			return OperacionesEnteros.resta(op1,op2)
	
		c = EnteroArbitrario(op1.base)
		
		l1 = len(op1.numero)
		l2 = len(op2.numero)
	
		if(l1 >= l2):
			mayor = op1
			menor = op2
			lm = l1
			ln = l2
		else:
			mayor = op2
			menor = op1
			lm = l2
			ln = l1
		dif = abs(l1-l2)
			
		c.numero = [0]*(lm)
			
		carry = 0
		for i in xrange(0,lm):
			temp = mayor.numero[i]+carry
			if(i < ln):
				temp = temp+menor.numero[i]
			c.numero[i] = temp%c.base
			carry = temp//c.base
		if (carry > 0):
			c.numero.append(carry)
		
		return c
		
	@staticmethod
	def resta(op1, op2):
		c = EnteroArbitrario(op1.base)
	
		if(op1.comparacion(op2) >= 0):
			mayor = op1
			menor = op2
			lg = op1.l
			lp = op2.l
		else:
			mayor = op2
			menor = op1
			lg = op2.l
			lp = op1.l
			c.signo = -1
			
		c.numero = [0]*(lg)
		
		carry = 0
		for i in xrange(0,lg):
			if ( i >= lp ):
				if(mayor.numero[i] >= carry):
					c.numero[i] = mayor.numero[i]-carry
					carry = 0
				else:
					c.numero[i] = mayor.base+mayor.numero[i]-carry
					carry = 1
			else:
				if(mayor.numero[i] >= menor.numero[i]+carry):
					c.numero[i] = mayor.numero[i]-menor.numero[i]-carry
					carry = 0
				else:
					c.numero[i] = mayor.base+mayor.numero[i]-menor.numero[i]-carry
					carry = 1
		
		return c

	@staticmethod
	def multiplicacion(op1, op2):
		c = EnteroArbitrario(op1.base)
		if(op1.signo != op2.signo):
			c.signo = -1

		c.numero = [0]
		i = 0
		while(i < len(op1.numero)+len(op2.numero)-1):
			c.numero.append(0)
			i = i+1
			
		
		for k in xrange(0,len(op2.numero)):
			carry = 0
			i = 0
			for i in xrange(0,len(op1.numero)):
				temp = op1.numero[i]*op2.numero[k]+c.numero[i+k]+carry
				c.numero[i+k] = temp%op1.base
				carry = temp//op1.base
				
			c.numero[k+len(op1.numero)] = carry
			k = k+1
		
		return c

	@staticmethod
	def division(op1, op2):
		m = len(op1.numero)
		n = len(op2.numero)
	
		resto = EnteroArbitrario(op1.base)
		cociente = EnteroArbitrario(op1.base)
		
		cociente.numero = [0]*m
		if(op1.signo != op2.signo):
			resto.signo = -1
			cociente.signo = -1
			
		if op1.comparacion(op2) < 0:
			resto = copy.deepcopy(op1)
			return [cociente, resto]
		
		resto.numero = op1.numero[m-n+1:m]

		for j in range(m-n,-1,-1):
			resto.numero.insert(0,op1.numero[j])
		
			if ( resto.comparacion(op2) >= 0 ):
			
				resto.numero.append(0)
				q = (resto.numero[n]*resto.base+resto.numero[n-1])//op2.numero[n-1]
				
				while ( resto.comparacion( op2.multiplicar(q) ) < 0):
					q = q-1
				
				resto = OperacionesEnteros.resta(resto,op2.multiplicar(q))
				cociente.numero[j] = q
			else:
				cociente.numero[j] = 0
						
		cociente.limpiarCeros()
		resto.limpiarCeros()
		return [cociente, resto]	


	@staticmethod
	def multiplicacionKaratsuba(op1, op2, m):
		a1 = EnteroArbitrario(op1.base)
		a0 = EnteroArbitrario(op1.base)
		b1 = EnteroArbitrario(op1.base)
		b0 = EnteroArbitrario(op1.base)
		suma_t = EnteroArbitrario(op1.base)
		total = EnteroArbitrario(op1.base)
	
		if (m==0):
			return OperacionesEnteros.multiplicacion(op1,op2)
		else:
		
			while (len(op1.numero) < 2**m or len(op1.numero)%2 != 0):
				op1.numero.append(0)
			while (len(op2.numero) < 2**m or len(op2.numero)%2 != 0):
				op2.numero.append(0)
				
			l1 = len(op1.numero)
			l2 = len(op2.numero)
			
			a1.numero = op1.numero[l1//2:l1] 
			a0.numero = op1.numero[0:l1//2] 
			b1.numero = op2.numero[l2//2:l2] 
			b0.numero = op2.numero[0:l2//2] 
			
			t1 = OperacionesEnteros.multiplicacionKaratsuba(a1,b1,m-1) 
			t2 = OperacionesEnteros.multiplicacionKaratsuba(OperacionesEnteros.resta(a1,a0),OperacionesEnteros.resta(b0,b1),m-1) 
			t3 = OperacionesEnteros.multiplicacionKaratsuba(a0,b0,m-1) 
			
			suma_t = OperacionesEnteros.suma(t1, OperacionesEnteros.suma(t2,t3)) 
			
			aux1 = [0]*(2**(m-1))
			aux2 = [0]*(2**m)
			
			aux1.extend(suma_t.numero)
			suma_t.numero = aux1
			aux2.extend(t1.numero)
			t1.numero = aux2
			
			total = OperacionesEnteros.suma(suma_t, OperacionesEnteros.suma(t1,t3))
			
			if(op1.signo != op2.signo):
				total.signo = -1
			
			return total
