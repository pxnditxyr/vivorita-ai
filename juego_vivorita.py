import pygame

from enum import Enum
from random import randint
from collections import namedtuple

# Inicializa el motor de pygame
pygame.init()


TAM_BLOQUE = 25


class Direcciones( Enum ):
    DERECHA   = 1
    IZQUIERDA = 2
    ARRIBA    = 3
    ABAJO     = 4


Puntos = namedtuple( 'Puntos', 'x, y' )


class VivoritaJuego:

    def __init__ ( self, ancho=640, alto=480 ):
        self.ANCHO   = ancho
        self.ALTO    = alto

        self.puntaje = 0
        self.frutas  = None


        self.display = pygame.display.set_mode(( self.ANCHO, self.ALTO ))
        pygame.display.set_caption( 'Vivorita' )
        self.reloj = pygame.time.Clock()

        self.direccion = Direcciones.DERECHA
        self.cabeza = Puntos( self.ANCHO / 2, self.ALTO / 2 )
        
        self.vivorita = [
            self.cabeza,
            Puntos( self.cabeza.x - TAM_BLOQUE, self.cabeza.y ),
            Puntos( self.cabeza.x - ( TAM_BLOQUE * 2 ), self.cabeza.y )
        ]

    def _posicion_fruta ( self ):
        x = randint( 0, ( self.ANCHO - TAM_BLOQUE ) // TAM_BLOQUE ) * TAM_BLOQUE
        y = randint( 0, ( self.ALTO  - TAM_BLOQUE ) // TAM_BLOQUE ) * TAM_BLOQUE

        self.frutas = Puntos( x, y )

        if self.frutas in self.vivorita:
            self._posicion_fruta()

    def verificar_movimiento ( self ):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if self.direccion != Direcciones.DERECHA:
                        self.direccion = Direcciones.IZQUIERDA
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if self.direccion != Direcciones.IZQUIERDA:
                        self.direccion = Direcciones.DERECHA
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.direccion != Direcciones.ABAJO:
                        self.direccion = Direcciones.ARRIBA
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.direccion != Direcciones.ARRIBA:
                        self.direccion = Direcciones.ABAJO

    def _mover ( self, direccion ):
        x = self.cabeza.x
        y = self.cabeza.y
        if direccion == Direcciones.DERECHA:
            x += TAM_BLOQUE
        elif direccion == Direcciones.IZQUIERDA:
            x -= TAM_BLOQUE
        elif direccion == Direcciones.ARRIBA:
            y -= TAM_BLOQUE
        elif direccion == Direcciones.ABAJO:
            y += TAM_BLOQUE

        self.cabeza = Puntos( x, y )


            

