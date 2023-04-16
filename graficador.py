import matplotlib.pyplot as plt

def graficar ( puntajes, puntajes_medios ):
    plt.clf() # limpia la grafica
    plt.title( 'Entrenando...' ) # titulo de la grafica
    plt.xlabel( 'Numero de juegos' ) # lo que se pinta en el eje x
    plt.ylabel( 'Puntaje' )         # lo que es pinta en el eje y
    plt.plot( puntajes )            # traza la linea de la grafica de los puntajes
    plt.plot( puntajes_medios )     # traza la linea de la grafica de los puntajes medios 
    plt.ylim( ymin=0 )              # establece valor minimo en la grafica
    plt.text( len( puntajes ) -1, puntajes[ -1 ], str( puntajes[ -1 ] ) )
    plt.text( len( puntajes_medios ) - 1, puntajes_medios[ -1  ], str( puntajes_medios[ -1 ] ) )
    plt.show()
    plt.pause( 0.1 )
    
