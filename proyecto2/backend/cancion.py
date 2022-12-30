class Cancion:
    def __init__(self, id, nombre, anio, artista, genero):
        self.id = id
        self.nombre = nombre
        self.anio = anio
        self.artista = artista
        self.genero = genero

    def __str__(self):
        return f"{self.id} - {self.nombre} - {self.anio} - {self.artista} - {self.genero}"