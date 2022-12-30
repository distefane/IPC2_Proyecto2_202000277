from cancion import Cancion

class Playlist:
    canciones = []
    def __init__(self, id, nit, vinyl, compacto, categoria, costo, canciones = []):
        self.id = id
        self.nit = nit
        self.vinyl = vinyl
        self.compacto = compacto
        self.categoria = categoria
        self.canciones = canciones
        self.costo = costo
    
    def agregar_cancion(self, cancion):
        self.canciones.append(cancion)
    
    def __str__(self):
        return f"Playlist: {self.id} - {self.nit} - {self.vinyl} - {self.compacto} - {self.categoria}"

    def mostrar_canciones(self):
        for cancion in self.canciones:
            print(cancion)
