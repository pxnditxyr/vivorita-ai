import pygame

from enum import Enum
from random import randint
from collections import namedtuple

# Inicializa el motor de pygame
pygame.init()
fuente = pygame.font.SysFont( 'freeserif', 25 )

TAM_BLOQUE            = 20
VELOCIDAD             = 1

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


Puntos = namedtuple( 'Puntos', 'x, y' )

class VivoritaJuego:

    def __init__ ( self, ancho=640, alto=480 ):
        self.ANCHO   = ancho
        self.ALTO    = alto

        self.puntaje = 0
        self.fruta   = None


        self.pantalla = pygame.display.set_mode(( self.ANCHO, self.ALTO ))
        pygame.display.set_caption( 'Vivorita' )
        self.reloj = pygame.time.Clock()

        self.direccion = Direcciones.DERECHA
        self.cabeza = Puntos( self.ANCHO / 2, self.ALTO / 2 )
        
        self.vivorita = [
            self.cabeza,
            Puntos( self.cabeza.x - TAM_BLOQUE, self.cabeza.y ),
            Puntos( self.cabeza.x - ( TAM_BLOQUE * 2 ), self.cabeza.y )
        ]

        self._crear_fruta()

    def _crear_fruta ( self ):
        x = randint( 0, ( self.ANCHO - TAM_BLOQUE ) // TAM_BLOQUE ) * TAM_BLOQUE
        y = randint( 0, ( self.ALTO  - TAM_BLOQUE ) // TAM_BLOQUE ) * TAM_BLOQUE

        self.fruta = Puntos( x, y )

        if self.fruta in self.vivorita:
            self._crear_fruta()


    def _ha_chocado ( self ):
        if self.cabeza in self.vivorita[ 1: ]:
            return True

        if self.cabeza.x > ( self.ANCHO - TAM_BLOQUE ) or self.cabeza.x < 0 or self.cabeza.y > ( self.ALTO - TAM_BLOQUE ) or self.cabeza.y < 0:
            return True
        
        return False
    

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
        
        self._mover( self.direccion )
        self.vivorita.insert( 0, self.cabeza )

        juego_terminado = False        

        if self._ha_chocado():
            juego_terminado = True
            return juego_terminado, self.puntaje

        if self.cabeza == self.fruta:
            self.puntaje += 1
            self._crear_fruta()
        else:
            self.vivorita.pop()

        self._actualizar_pantalla()
        self.reloj.tick( VELOCIDAD )

        return juego_terminado, self.puntaje

if __name__ == '__main__':
    juego = VivoritaJuego()

    i = 0

    while True:
        juego_terminado, puntaje = juego.verificar_movimiento()
        if juego_terminado:
            break

    print( f"Puntaje: { puntaje }" )
    pygame.quit()



