from xml.etree import ElementTree as ET
from playlist import Playlist
from cancion import Cancion

class LecturaPlaylists:
    def __init__(self, fichero):
        self.fichero = fichero
        self.xml_playlists = open(self.fichero, encoding="utf-8")
        
    def generar_playlists(self):
        global playlists1
        playlists1 = []
        if self.xml_playlists.readable():
            self.datos = ET.fromstring(self.xml_playlists.read())
            self.lista_playlists = self.datos.findall("playlist")
            for playlist in self.lista_playlists:
                costo = 0
                canciones = []
                id_playlist = playlist.attrib["id"]
                nit = playlist.find("nitCliente").text
                vynil = playlist.find("vinyl").text
                compacto = playlist.find("compacto").text
                categoria = playlist.find("categoria").text
                if vynil == "True":
                    costo += 500
                if compacto == "True":
                    costo += 100
                print(id_playlist, nit, vynil, compacto, categoria)
                lista_canciones = playlist.findall("canciones")
                for cancion in lista_canciones:
                    una = cancion.iter("cancion")
                    for cancion in una:
                        id_cancion = cancion.attrib["id"]
                        nombre_cancion = cancion.find("nombre").text
                        anio = cancion.find("anio").text
                        artista = cancion.find("artista").text
                        genero = cancion.find("genero").text
                        if int(anio) <= 1960:
                            costo += 25
                        elif int(anio) > 1960 and int(anio) <= 1990:
                            costo += 15
                        elif int(anio) > 1990 and int(anio) <= 2022:
                            costo += 5
                        #print(id_cancion, nombre_cancion, anio, artista, genero)
                        nueva_cancion = Cancion(id_cancion, nombre_cancion, anio, artista, genero)
                        canciones.append(nueva_cancion)
                        nueva_playlist = Playlist(id_playlist, nit, vynil, compacto, categoria, costo, canciones)
                if len(playlists1) == 0:
                    playlists1.append(nueva_playlist)
                else:
                    #Si la playlist ya existe, no se agrega
                    for playlist in playlists1:
                        if playlist.id == nueva_playlist.id:
                            break
                    else:
                        playlists1.append(nueva_playlist)
        i = 1
        for playlist in playlists1:
            print(f"{i}. ID: {playlist.id}, Nit: {playlist.nit}, Vinyl: {playlist.vinyl}, Compacto: {playlist.compacto}, Categoria: {playlist.categoria}, Costo: {playlist.costo}")
            for cancion in playlist.canciones:
                print(cancion)
            i += 1
        return playlists1
    
if __name__ == "__main__":
    lectura = LecturaPlaylists("playlist_clientes.xml")
    lectura.generar_playlists()