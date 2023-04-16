import random
import numpy as np
import torch
from collections import deque

from juego_vivorita import VivoritaJuegoIA, Direcciones, Puntos
from modelo import Modelo_Lineal, Entrenador
from graficador import graficar

MEMORIA_MAXIMA = 100000
TAM_LOTES = 1000

TAZA_DE_APRENDIZAJE = 0.001

class Agente:
    
    def __init__ ( self ):
        self.numero_juegos = 0
        self.epsilon = 0 # aleatoriedad
        self.gamma   = 0.9 # tasa de decremento o descuento
        # 2 ^ 2 -> 4 --> 1/2^2 -> 1/4

        # 1 gato -> 100% / sesgo 
        # 0 perro -> 0%

        # 0.99 gato
        # 0.01 perro

        self.memoria = deque( maxlen=MEMORIA_MAXIMA )

        self.modelo = Modelo_Lineal( num_neuronas_entrada=11, num_neuronas_ocultas=256, num_neuronas_salida=3 )
        self.entrenador = Entrenador( self.modelo, TAZA_DE_APRENDIZAJE, self.gamma )

        
    def obtener_estado ( self, juego ):
        cabeza_vivora = juego.vivorita[ 0 ]

        punto_izquierda = Puntos( cabeza_vivora.x - 20, cabeza_vivora.y )
        punto_derecha   = Puntos( cabeza_vivora.x + 20, cabeza_vivora.y )
        punto_arriba    = Puntos( cabeza_vivora.x, cabeza_vivora.y - 20 )
        punto_abajo     = Puntos( cabeza_vivora.x, cabeza_vivora.y + 20 )

        direccion_izquierda = juego.direccion == Direcciones.IZQUIERDA
        direccion_derecha   = juego.direccion == Direcciones.DERECHA
        direccion_arriba    = juego.direccion == Direcciones.ARRIBA
        direccion_abajo     = juego.direccion == Direcciones.ABAJO

        estado = [
            # Caso Siga
            ( direccion_derecha and juego.ha_chocado( punto_derecha ) ) or
            ( direccion_izquierda and juego.ha_chocado( punto_izquierda ) ) or
            ( direccion_arriba and juego.ha_chocado( punto_arriba ) ) or
            ( direccion_abajo and juego.ha_chocado( punto_abajo ) ),

            # Caso giro horario
            ( direccion_arriba and juego.ha_chocado( punto_derecha ) ) or
            ( direccion_abajo and juego.ha_chocado( punto_izquierda ) ) or
            ( direccion_izquierda and juego.ha_chocado( punto_arriba ) ) or
            ( direccion_derecha and juego.ha_chocado( punto_abajo ) ),

            # Caso giro Anti-horario
            ( direccion_abajo and juego.ha_chocado( punto_derecha ) ) or
            ( direccion_arriba and juego.ha_chocado( punto_izquierda ) ) or
            ( direccion_derecha and juego.ha_chocado( punto_arriba ) ) or
            ( direccion_izquierda and juego.ha_chocado( punto_abajo ) ),

            # Direccion de Movimiento
            direccion_izquierda,
            direccion_derecha,
            direccion_arriba,
            direccion_abajo,

            # lugar de la fruta

            juego.fruta.x < juego.cabeza.x, # fruta esta a la izquierda
            juego.fruta.x > juego.cabeza.x, # fruta esta a la derecha
            juego.fruta.y < juego.cabeza.y, # fruta esta arriba
            juego.fruta.y > juego.cabeza.y, # fruta esta abajo
        ]
        # estado [ True, True, True, True, False, False, False, True, False, True, False ]

        # estado [ 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0 ]
        return np.array( estado, dtype=int )
        


    def recordar ( self, estado, accion, recompenza, siguiente_estado, juego_terminado ):
        # [
            # ( [ 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0 ], [ 1, 0, 0 ], -2, [ 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0 ], True ),
            # ( [ 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0 ], [ 1, 0, 0 ], -2, [ 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0 ], True ),
            # ( [ 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0 ], [ 1, 0, 0 ], -2, [ 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0 ], True ),
            # ( [ 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0 ], [ 1, 0, 0 ], -2, [ 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0 ], True ),
            # ( [ 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0 ], [ 1, 0, 0 ], -2, [ 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0 ], True )
        # ]
        self.memoria.append(( estado, accion, recompenza, siguiente_estado, juego_terminado ))

    def entrenar_memoria_largo_plazo ( self ):
        if len( self.memoria ) > TAM_LOTES:
            ejemplos_aleatorios = random.sample( self.memoria, TAM_LOTES )
        else:
            ejemplos_aleatorios = self.memoria

        estados, acciones, recompenzas, siguientes_estados, juegos_terminados = zip( *ejemplos_aleatorios )
        self.entrenador.entrenar_en_cada_paso( estados, acciones, recompenzas, siguientes_estados, juegos_terminados )
            


    def entrenar_memoria_corto_plazo ( self, estado_anterior, accion, recompenza, nuevo_estado, juego_terminado ):
        self.entrenador.entrenar_en_cada_paso( estado_anterior, accion, recompenza, nuevo_estado, juego_terminado )

    def obtener_accion ( self, estado ):
        self.epsilon = 90 - self.numero_juegos
        movimiento_final = [ 0, 0, 0 ]
        if random.randint( 0, 200 ) < self.epsilon:
            movimiento = random.randint( 0, 2 )
            movimiento_final[ movimiento ] = 1
        else:
            estado_0 = torch.tensor( estado, dtype=torch.float )
            # [ 
            prediccion = self.modelo( estado_0 )
            # [ 0.8, 0.15, 0.05 ]
            # [ [ 0, 0.8 ], [ 1, 0.15 ], [ 2, 0.05 ] ]
            movimiento = torch.argmax( prediccion ).item()
            # [ 0.8 ] ->  0, 1, 2
            # [ 1 0 0 ] [ 0 1 0 ] [ 0 0 1 ]
            movimiento_final[ int( movimiento ) ] = 1
            # [ 0 0 1 ]
        return movimiento_final

            


def entrenar ():
    puntajes_a_graficar = []
    puntajes_medios_a_graficar = []
    puntaje_total = 0
    puntaje_record = 0
    agente = Agente()
    juego = VivoritaJuegoIA()

    while True:
        estado_anterior = agente.obtener_estado( juego )

        accion = agente.obtener_accion( estado_anterior )

        recompenza, juego_terminado, puntaje_obtenido = juego.verificar_movimiento( accion )

        nuevo_estado = agente.obtener_estado( juego )

        agente.entrenar_memoria_corto_plazo( estado_anterior, accion, recompenza, nuevo_estado, juego_terminado )
        agente.recordar( estado_anterior, accion, recompenza, nuevo_estado, juego_terminado )
        
        if juego_terminado:
            
            juego.reiniciar_juego()
            agente.numero_juegos += 1
            agente.entrenar_memoria_largo_plazo()

            if puntaje_obtenido > puntaje_record:
                puntaje_record = puntaje_obtenido
            print( f"\tJuego Nro: { agente.numero_juegos }\n\tPuntaje: { puntaje_obtenido }\n\tPuntaje Record: { puntaje_record } " )
            puntajes_a_graficar.append( puntaje_obtenido )
            puntaje_total += puntaje_obtenido
            puntaje_medio = puntaje_total / agente.numero_juegos
            puntajes_medios_a_graficar.append( puntaje_medio )
            # graficar( puntajes_a_graficar, puntajes_medios_a_graficar )



if __name__ == '__main__':
    entrenar()
