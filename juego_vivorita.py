import pygame
from enum import Enum
from random import randint
from collections import namedtuple
import numpy as np

pygame.init()
fuente = pygame.font.SysFont( 'freeserif', 25 )

TAM_BLOQUE            = 20
VELOCIDAD             = 200

COLOR_CABEZA_VIVORITA = ( 33, 0, 98 )
COLOR_VIVORITA        = ( 87, 108, 188 )
AUX                   = ( 36, 89, 83 )
COLOR_VIVORITA_DENTRO = ( 122, 168, 116 )
COLOR_FONDO           = (  0, 159, 189 )
COLOR_FRUTA           = ( 47, 15, 93 )
COLOR_PUNTAJE         = ( 66, 66, 66 )

COLOR_CABEZA_VIVORITA_DENTRO = ( 26, 95, 122 )


class Direcciones( Enum ):
    DERECHA   = 1
    IZQUIERDA = 2
    ARRIBA    = 3
    ABAJO     = 4


Puntos = namedtuple( 'Puntos', 'x, y' ) # tupla nombrada, ( 'Nombre', 'atributo1, atributo2, ...' )

class VivoritaJuegoIA:

    def __init__ ( self, ancho=640, alto=480 ):
        self.ANCHO   = ancho
        self.ALTO    = alto

        self.pantalla = pygame.display.set_mode(( self.ANCHO, self.ALTO ))
        pygame.display.set_caption( 'Vivorita' )
        self.reloj = pygame.time.Clock()

        self.reiniciar_juego()

        
    def reiniciar_juego ( self ):
        self.direccion = Direcciones.DERECHA
        self.cabeza = Puntos( self.ANCHO / 2, self.ALTO / 2 )

        self.vivorita = [
            self.cabeza,
            Puntos( self.cabeza.x - TAM_BLOQUE, self.cabeza.y ),
            Puntos( self.cabeza.x - ( TAM_BLOQUE * 2 ), self.cabeza.y )
        ]

        self.puntaje = 0
        self.fruta   = None
        self._crear_fruta()

        # Aumentando
        self.iteracion_frame = 0


    def _crear_fruta ( self ):
        x = randint( 0, ( self.ANCHO - TAM_BLOQUE ) // TAM_BLOQUE ) * TAM_BLOQUE
        y = randint( 0, ( self.ALTO  - TAM_BLOQUE ) // TAM_BLOQUE ) * TAM_BLOQUE

        self.fruta = Puntos( x, y )

        if self.fruta in self.vivorita:
            self._crear_fruta()


    def ha_chocado ( self, bloque=None ):

        if bloque is None:
            bloque = self.cabeza

        if bloque in self.vivorita[ 1: ]:
            return True

        if bloque.x > ( self.ANCHO - TAM_BLOQUE ) or bloque.x < 0 or bloque.y > ( self.ALTO - TAM_BLOQUE ) or bloque.y < 0:
            return True
        
        return False
    

    def _mover ( self, accion ):
        
        # Aumentando: [ siga, derecha, izq ]
        cambio_sentido_horario = [ Direcciones.DERECHA, Direcciones.ABAJO, Direcciones.IZQUIERDA, Direcciones.ARRIBA ]
        indice_direccion = cambio_sentido_horario.index( self.direccion ) # 3


        # [ 1, 0, 0 ] => siga
        # [ 0, 1, 0 ] => giro horario ==> derecha -> abajo -> izquierda -> arriba
        # [ 0, 0, 1 ] => giro antihorario ==> derecha -> arriba -> izquierda -> abajo

        if np.array_equal( accion, [ 1, 0, 0 ] ):
            nueva_direccion = cambio_sentido_horario[ indice_direccion ]
        elif np.array_equal( accion, [ 0, 1, 0 ] ):
            nueva_direccion = cambio_sentido_horario[ ( indice_direccion + 1 ) % 4 ] # %4 por si la posicion es 3 entonces el siguiente seria (3+1)%4 = 0
        else:
            nueva_direccion = cambio_sentido_horario[ ( indice_direccion - 1 ) % 4 ]

        self.direccion = nueva_direccion

        x = self.cabeza.x
        y = self.cabeza.y

        if self.direccion == Direcciones.DERECHA:
            x += TAM_BLOQUE
        elif self.direccion == Direcciones.IZQUIERDA:
            x -= TAM_BLOQUE
        elif self.direccion == Direcciones.ARRIBA:
            y -= TAM_BLOQUE
        elif self.direccion == Direcciones.ABAJO:
            y += TAM_BLOQUE

        self.cabeza = Puntos( x, y )

    def _actualizar_pantalla ( self ):

        self.pantalla.fill( COLOR_FONDO )
        pygame.draw.rect( self.pantalla, COLOR_CABEZA_VIVORITA, pygame.Rect( self.vivorita[ 0 ].x, self.vivorita[ 0 ].y, TAM_BLOQUE, TAM_BLOQUE ) )
        pygame.draw.rect( self.pantalla, COLOR_CABEZA_VIVORITA_DENTRO, pygame.Rect( self.vivorita[ 0 ].x + 4, self.vivorita[ 0 ].y + 4, 12, 12 ) )
        for bloque_cuerpo in self.vivorita[ 1: ]:
            pygame.draw.rect( self.pantalla, COLOR_VIVORITA, pygame.Rect( bloque_cuerpo.x, bloque_cuerpo.y, TAM_BLOQUE, TAM_BLOQUE ) )
            pygame.draw.rect( self.pantalla, COLOR_VIVORITA_DENTRO, pygame.Rect( bloque_cuerpo.x + 4, bloque_cuerpo.y + 4, 12, 12 ) )

        x_fruta = 0
        y_fruta = 0
        if self.fruta:
            x_fruta = self.fruta.x
            y_fruta = self.fruta.y
        pygame.draw.rect( self.pantalla, COLOR_FRUTA, pygame.Rect( x_fruta, y_fruta, TAM_BLOQUE, TAM_BLOQUE ) )
        texto = fuente.render( f"Puntaje: { self.puntaje }", True, COLOR_PUNTAJE )
        self.pantalla.blit( texto, ( 0, 0 ) )
        pygame.display.flip()


    # Aumentando
    def verificar_movimiento ( self, accion ):
        self.iteracion_frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        self._mover( accion )
        self.vivorita.insert( 0, self.cabeza )

        juego_terminado = False        
        recompenza = 0

        if self.ha_chocado() or self.iteracion_frame > 100 * len( self.vivorita ):
            juego_terminado = True
            recompenza = -2
            return recompenza, juego_terminado, self.puntaje

        if self.cabeza == self.fruta:
            self.puntaje += 1
            recompenza = 2
            self._crear_fruta()
        else:
            self.vivorita.pop()

        self._actualizar_pantalla()
        self.reloj.tick( VELOCIDAD )

        return recompenza, juego_terminado, self.puntaje
