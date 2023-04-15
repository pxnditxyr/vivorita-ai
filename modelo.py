from numpy import dtype
import torch

from torch import nn
from torch import optim
import torch.nn.functional as Func
import os

class Modelo_Lineal ( nn.Module ):
    def __init__ ( self, num_neuronas_entrada, num_neuronas_ocultas, num_neuronas_salida ):
        super().__init__()
        self.lineal_1 = nn.Linear( num_neuronas_entrada, num_neuronas_ocultas )
        self.lineal_2 = nn.Linear( num_neuronas_ocultas, num_neuronas_salida )

    # forward es la funcion o metodo de la clase padre y se sobreescribe
    def forward ( self, datos_entrada ):
        datos_pasados_capa_1 = self.lineal_1( datos_entrada )
        datos_pasados_relu   = Func.relu( datos_pasados_capa_1 )
        salida_capa_2        = self.lineal_2( datos_pasados_relu )
        return salida_capa_2
    
    def save ( self, nombre_archivo='mi_modelo.pth' ):
        ruta_archivo = './modelo'

        if not os.path.exists( ruta_archivo ):
            os.makedirs( ruta_archivo )

        ruta_mas_nombre = os.path.join( ruta_archivo, nombre_archivo )
        torch.save( self.state_dict(), ruta_mas_nombre )


class Entrenador:
    def __init__ ( self, modelo, tasa_de_aprendizaje, gamma ):
        self.modelo = modelo
        self.tasa_de_aprendizaje = tasa_de_aprendizaje
        self.gamma = gamma

        self.optimizador = optim.Adam( modelo.parameters(), lr=self.tasa_de_aprendizaje )
        self.criterio = nn.MSELoss() # 2,3,4,2,6 -> 2^2+3^2+4^2+6^2 -> y raiz de todo
        # Medium Square Error 

    def entrenar_en_cada_paso ( self, estado, accion, recompenza, siguiente_estado, juego_terminado ):
        estado = torch.tensor( estado, dtype=torch.float )
        siguiente_estado = torch.tensor( siguiente_estado, dtype=torch.float )
        accion = torch.tensor( accion, dtype=torch.long ) # [ 0 1 0 ] -> 010 -> 101 -> 1001010101011101101101010101011010
        recompenza = torch.tensor( recompenza, dtype=torch.float )

        # [ 1, 2, 3 ].shape -> (,3) [[1,2,3],[1,2,3],[1,2,3]].shape -> (3,3)

        if len( estado.shape ) == 1:
            estado = torch.unsqueeze( estado, 0 )
            siguiente_estado = torch.unsqueeze( siguiente_estado, 0 )
            accion = torch.unsqueeze( accion, 0 )
            recompenza = torch.unsqueeze( recompenza, 0 )
            juego_terminado = ( juego_terminado, )
            # juego_terminado = True -> juego_terminado = ( True )
            # juego_terminado = True -> juego_terminado = ( True, )
            # juego_terminado = ( True, )


            # valores de q - Q values, son la medida de la utilidad para tomar una accion
            # gato   0.7 gato
            # perro  0.3 perro
            prediccion = self.modelo( estado ) # ->  derecha
            # target -> objetivo
            objetivo   = prediccion.clone()    # objetivo -> girar a la derecha

            for i in range( len( juego_terminado ) ): # ( True, )
                nuevos_valores_q = recompenza[ i ]
                if not juego_terminado[ i ]:
                    nuevos_valores_q = recompenza[ i ] + ( self.gamma * torch.max( self.modelo( siguiente_estado[ i ] ) ) )
                objetivo[ i ][ torch.argmax( accion[ i ] ).item() ] = nuevos_valores_q

            self.optimizador.zero_grad() # trabaja con los gradientes y los reinicia a 0
            perdida = self.criterio( objetivo, prediccion )
            perdida.backward() # Back propagation -> para modificar los pesos
            self.optimizador.step() # actualizara los pesos
                                                            
