import matplotlib.pyplot as plt
from IPython import display

plt.ion() # permite actualizar la grafica en tiempo real

def graficar ( puntajes, puntajes_medios ):
    display.clear_output( wait=True ) # limpia la pantalla
    display.display( plt.gfc() )
    plt.clf() # limpia la grafica
    plt.title( 'Entrenando...' ) # titulo de la grafica
    plt.xlabel( 'Numero de juegos' ) # lo que se pinta en el eje x
    plt.ylabel( 'Puntaje' )         # lo que es pinta en el eje y
    plt.plot( puntajes )            # traza la linea de la grafica de los puntajes
    plt.plot( puntajes_medios )     # traza la linea de la grafica de los puntajes medios 
    plt.ylim( ymin=0 )              # establece valor minimo en la grafica
    plt.text( len( puntajes ) -1, puntajes[ -1 ], str( puntajes[ -1 ] ) )
    plt.text( len( puntajes_medios ) - 1, puntajes_medios[ -1  ], str( puntajes_medios[ -1 ] ) )
    plt.show( block=False )
    plt.pause( 0.1 )
    
