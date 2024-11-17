class DestinoInalcanzableError(Exception):
    def __init__(self, destino):
        self.destino = destino
        self.mensaje = f"El destino {destino} no se encuentra disponible"
        super().__init__(self.mensaje)