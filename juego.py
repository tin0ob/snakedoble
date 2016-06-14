#!/usr/bin/env python
# coding:utf-8


import pygame	#para juego
import random	#para randoms del juego
import sqlite3	#para guardar resultados
import time		#para saber la hora
from pygame.locals import *		#para tener locales
from matplotlib.pylab import hist,show #para graficar


#globales por que si no me aparece error


fondo = (0,0,0)
asd = 900,700

com1c = (255,255,0)			#color comida 1
com2c = (255,150,100)		#color comida 2
com3c = (20,40,100)			#color comida 3
com4c = (0,100,255)			#color comida 4
com5c = (20,120,220)		#color comida 5
snk1 = (255,0,0)			#color serpiente 1
snk2 = (0,0,255)			#color serpiente 2
puntaje = 0					#puntaje
conn = sqlite3.connect('puntajes.db')
conn.text_factory = str
co = conn.cursor()
##co.execute('''CREATE TABLE puntajes (user text, puntaje1 int, puntaje2 int)''') #creo tabla una vez

class comida:
	
	def __init__(self,pos,tam,col):	#constructor comida
		self.posicion = pos
		self.tamano = tam
	
		
		if col == 1:					#colores
			self.colr = com1c
		if col == 2:
			self.colr = com2c
		if col == 3:
			self.colr = com3c
		if col == 4:
			self.colr = com4c
		if col == 5:
			self.colr = com5c
	
	def aparece(self):			#aparece comida
		pygame.draw.rect(res, self.colr, (self.posicion[0], self.posicion[1], self.tamano, self.tamano))
		pygame.display.flip()
		
	def desaparece(self):		#desaparece comida
		pygame.draw.rect(res, (0,0,0),  (self.posicion[0], self.posicion[1], self.tamano, self.tamano))
		pygame.display.flip()

class snake:
	
	def __init__(self,pos,tam,col,longi,velocidad, puntaje):  	#constructor de serpiente
		self.posicion = pos								#posición de la cabeza
		self.largo = tam								#tamaño del pixel
		self.longitud = longi							#largo de serpiente
		self.velocidad = velocidad						#velocidad de serpiente
		self.puntaje = puntaje
		
		if col == 1:									#colores
			self.col = (255,0,0)
			
		if col == 2:
			self.col = (0,255,0)
		
		if col == 3:
			self.col = (0,0,255)
		
		
	def vive(self):
		pygame.draw.rect(res, self.col, (self.posicion[0], self.posicion[1], self.largo, self.largo)) #vive dandole el color al pixel creado definido en el constructor
		pygame.display.flip()	#paqueapareszca
	
	def muere(self,pot):
		pygame.draw.rect(res,(0,0,0),(pot[0],pot[1], self.largo, self.largo)) #muere porque da el negro (color de fondo)
		pygame.display.flip()	#paqueapareszca
		
	def come(self):
		self.longitud +=1		#come
	def comemas(self,a):
		self.longitud += a   	#come mas de 1
				
def choque(pos,tam):					#cálcula los choques en base a las colisiones de colores en la pantalla.
	x = pos[0] + tam / 2
	y = pos[1] + tam / 2
	colo = res.get_at((x, y))
	if colo[0:3] == com1c:				#comida 1, hace crecer
			return 1
	if colo[0:3] == com2c:				#comida 2, hace lento el juego por 30 iteraciones
			return 2
	if colo[0:3] == com3c:				#comida 3, multiplica puntaje por 3
			return 3
	if colo[0:3] == com4c:				#comida 4, multiplica puntaje por 10
			return 4
	if colo[0:3] == com5c:				#comida 5, pierdes todo el puntaje y se pone muy rapido
			return 5
	if colo[0:3] == snk1:	#eso es cuando el color es igual a la serpiente, chocar contra uno mismo
			return 6
	if colo[0:3] == snk2:
			return 7

def pantalla():		#inicializacion de pantala
	global res
	res = pygame.display.set_mode(asd)
	pygame.draw.rect(res,fondo,((0,0),(860,640)))
	
def funcion():			# juego en sí
	nombre = 'asd'
	vueltas = 0
	puntaje = 0
	delay = 30 						#delay de refresco de pantalla
	x, y = 300, 300					#valores para x e y iniciales
	c, v = 500,500					#valores de c y v iniciales

	pos00 = [(x,y)]				#posición inicial de serpiente
	pos01 = [(c,v)]				#posición ininicial serpiente2
	
	snake1 = snake(pos00,8,1,15,5,0)	#constructor de snake 1
	snake2 = snake(pos01,8,2,15,5,0)	#constructor de snake 2
	
	vc = snake2.velocidad					#velocidad2 eje x
	vv = 0									#velocidad2 eje y
	vx = snake1.velocidad					#valor de velocidad para eje x
	vy = 0									#valor de velocidad para eje y

	posc00 = (random.randint(30,asd[0] - 30),random.randint(30,asd[1] - 30))	
	posc01 = (random.randint(30,asd[0] - 30), random.randint(30,asd[1] - 30))
	posc02 = (random.randint(30,asd[0] - 30), random.randint(30,asd[1] - 30))
	posc03 = (random.randint(30,asd[0] - 30), random.randint(30,asd[1] - 30))
	posc04 = (random.randint(30,asd[0] - 30), random.randint(30,asd[1] - 30))
	com5 = comida(posc04,10,5)
	com4 = comida(posc03,5,2)
	com3 = comida(posc02,15,4)
	com2 = comida(posc01,20,3)
	com1 = comida(posc00,25,1)
	com1.aparece()
	
	while True:						# funcion del juego en sí
		
		pygame.event.pump()
		teclas = pygame.key.get_pressed()	#teclas a usar y cambios en la velocidad de los ejes x e y
		if vy != - snake1.velocidad and vx != 0 and teclas[K_w]:
				vy = - snake1.velocidad
				vx = 0
		if vy != snake1.velocidad and vx != 0 and teclas[K_s]:
				vy = snake1.velocidad
				vx = 0
		if vx != - snake1.velocidad and vy != 0 and teclas[K_a]:
				vx = -snake1.velocidad
				vy = 0
		if vx != snake1.velocidad and vy != 0 and teclas[K_d]:
				vx = snake1.velocidad
				vy = 0
		if vv != -snake2.velocidad and vc != 0 and teclas[K_UP]:
				vv = -snake2.velocidad
				vc = 0
		if vv != snake2.velocidad and vc != 0 and teclas[K_DOWN]:
				vv = snake2.velocidad
				vc = 0
		if vc != -snake2.velocidad and vv != 0 and teclas[K_LEFT]:
				vc = -snake2.velocidad
				vv = 0
		if vc != snake2.velocidad and vv != 0 and teclas[K_RIGHT]:
				vc = snake2.velocidad
				vv = 0
		if teclas[K_SPACE]:			#prueba
			
				snake1.longitud += 1
				snake2.longitud += 1
				
		if teclas[K_ESCAPE]:
				break
						 
		while len(pos00) >= snake1.longitud:	#valido el largo
				snake1.muere(pos00.pop(0))  		#elimino un pixel
		while len(pos01) >= snake2.longitud:
				snake2.muere(pos01.pop(0))			#elimino pixel serp2
				
		
				
				
		x = x + vx
		y = y + vy	
		pos00.append((x,y))					#agrego pixel a posicion porque no pude hacerlo con clase
		snake1.posicion = ((x,y))			#agrego pixel a posicion de clase snake
		
		c = c + vc
		v = v + vv	
		pos01.append((c,v))					#lomismo	
		snake2.posicion = ((c,v))			#lomismo2
		
								

		
		if  x <= 5 or x > asd[0] - 15 or y <= 15 or y > asd[1] - 15 or c <= 15 or c > asd[0] - 15 or v <= 15 or v > asd[1] - 15: #comprobar pantalla
			print("saliste de la pantalla, perdiste")
			break
		
#########################################################################################
#########################################################################################
###########################CHOCLO INEFICIENTE DE IFS PARA CHOQUES########################
#########################################################################################
#########################################################################################

		
		if choque(snake1.posicion,snake1.largo) == 1:				#comida 1, + uno de puntaje, si se come desaparece y aparece en otro lado,
			snake1.comemas(3)											#invocando la clase
			com1.desaparece()
			com1.posicion = ((random.randint(20,asd[0]-15),random.randint(20,asd[1] - 15)))
			com1.aparece()
			snake1.puntaje += 1
			
		if choque(snake2.posicion,snake2.largo) == 1:						#lo mismo ineficientemente para la serpiente 2
			snake2.comemas(3)
			com1.desaparece()
			com1.posicion = ((random.randint(20,asd[0] - 20),random.randint(20,asd[1] - 20)))
			com1.aparece()
			snake2.puntaje += 1
		
		if choque(snake1.posicion,snake1.largo) == 3:						#otra comida que multiplica el puntaje
			snake1.comemas(5)
			com2.desaparece()
			com2.posicion = ((random.randint(20,asd[0] - 20),random.randint(20,asd[1] - 20)))
			snake1.puntaje = snake1.puntaje + 5
			
		if choque(snake2.posicion,snake2.largo) == 3:						#lo mismo para snk2
			snake2.comemas(5)
			com2.desaparece()
			com2.posicion = ((random.randint(20,asd[0] - 20),random.randint(20,asd[1] - 20)))
			snake2.puntaje = snake2.puntaje + 5
		
		if choque(snake1.posicion,snake1.largo) == 4:						#super comida que te multiplica por 10 
			snake1.comemas(6)
			com3.desaparece()
			com3.posicion = ((random.randint(20,asd[0] - 20),random.randint(20,asd[1] - 20)))
			snake1.puntaje = snake1.puntaje* 5
			
		if choque(snake2.posicion,snake2.largo) == 4:						#super ineficiencia
			snake2.comemas(6)
			com3.desaparece()
			com3.posicion = ((random.randint(20,asd[0] - 20),random.randint(20,asd[1] - 20)))
			snake2.puntaje = snake2.puntaje* 5
			
		if choque(snake1.posicion,snake1.largo) == 5:						#super comida que te borra el puntaje y se pone rapido 
			snake1.comemas(12)
			com5.desaparece()
			com5.posicion = ((random.randint(20,asd[0] - 20),random.randint(20,asd[1] - 20)))
			snake1.puntaje = snake1.puntaje * 100
			snake1.velocidad += 1
			
		if choque(snake2.posicion,snake2.largo) == 5:						#super ineficiencia
			snake2.comemas(12)
			com5.desaparece()
			com5.posicion = ((random.randint(20,asd[0] - 20),random.randint(20,asd[1] - 20)))
			snake2.puntaje = snake2.puntaje * 100
			snake2.velocidad += 1
			
		if choque(snake1.posicion,snake1.largo) == 2:						#super comida que hace lento el juego
			snake1.comemas(-5)
			com4.desaparece()
			com4.posicion = ((random.randint(20,asd[0] - 20),random.randint(20,asd[1] - 20)))
			snake1.velocidad = snake1.velocidad + 5
			snake1.puntaje = snake1.puntaje* 1000
			#if snake1.velocidad <= 5:
			#	snake1.velocidad = 7
			
		if choque(snake2.posicion,snake2.largo) == 2:						#super ineficiencia
			snake2.comemas(-5)
			com4.desaparece()
			com4.posicion = ((random.randint(20,asd[0] - 20),random.randint(20,asd[1] - 20)))
			snake2.velocidad = snake2.velocidad + 5
			snake2.puntaje = snake2.puntaje * 1000
			#if snake2.velocidad <= 5:
			#	snake2.velocidad = 7
			
		if choque(snake1.posicion,snake1.largo) == 6 or choque(snake2.posicion, snake2.largo) == 7 or choque(snake2.posicion,snake2.largo) == 6 or choque(snake1.posicion, snake1.largo) == 7:						#choque contra ti mismo o la otra serpiente
			print("chocaste")
			break	
		

		
		snake1.vive()				#dibujo snake1
		snake2.vive()				#dibujo snake2
		
		
		if snake1.puntaje % 3 == 1:			#modular para comida 2
			com2.aparece()
		
		if snake2.puntaje % 7 == 2:		#modular para comida 3
			com3.aparece()
		
		if vueltas != 0 and vueltas % 300 == 0: #condicion comida 4
			com5.aparece()
				
		if vueltas == 1500 or vueltas == 3000: 			#condicion comida 5
			com4.aparece()
		
		vueltas += 1					#contador de ciclos dados por el juego
		pygame.time.delay(delay)			#dileeeei
		
		
#########################################################################################
##########################################imprimir puntajes##############################
#########################################################################################

	print("el puntaje de snake1 fue:") 
	print(snake1.puntaje)
	print("el puntaje de snake2 fue:")
	print(snake2.puntaje)
	print("sobreviviste a: ")
	print(vueltas)
	print("vueltas")
	
	dia = time.strftime("%c")
	co.execute("INSERT INTO puntajes (user, puntaje1, puntaje2) VALUES (?, ?, ?)", (dia,snake1.puntaje,snake2.puntaje))
	conn.commit()
	co.execute("SELECT * FROM puntajes")
	datos = co.fetchall()
	asd2 = list()
	for dato in datos:
		asd2.append(dato)
		#print(asd2)
		print(dato)


	
	conn.close()

def fin():
	pygame.quit()							#chao
		
try:										#corro juego
	pantalla()								
	funcion()
 	
finally:
	fin()
	#v=range(0,21)							# a implementar con los datos de la base de datos.
	#data=[]
	#for i in range(1000):
	#	data.append(random.choice(v))

	#hist(data,21, (0,20))
	#show()		#gráfico a preparar
			
	
