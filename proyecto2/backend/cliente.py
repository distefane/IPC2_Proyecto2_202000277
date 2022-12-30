from playlist import Playlist

class Cliente:

    playlistsAsociadas = []

    def __init__(self, nit, nombre, usuario, clave, direccion, email, empresa, pago, playlistsAsociadas = []):
        self.nit = nit
        self.nombre = nombre
        self.usuario = usuario
        self.clave = clave
        self.direccion = direccion
        self.email = email
        self.empresa = empresa
        self.playlistsAsociadas = playlistsAsociadas
        self.pago = pago

    def agregar_playlist(self, playlist):
        self.playlistsAsociadas.append(playlist)

    def mostrar_playlists(self):
        for playlist in self.playlistsAsociadas:
            print(playlist)
        
    def __str__(self):
        return f"{self.nit} - {self.nombre} - {self.usuario} - {self.clave} - {self.direccion} - {self.email} - {self.empresa} - {self.playlistsAsociadas} - {self.pago}"