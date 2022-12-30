from xml.etree import ElementTree as ET
from cliente import Cliente
from lectura_empresas import LecturaEmpresas
from lectura_playlists import LecturaPlaylists

class LecturaClientes:
    def __init__(self, fichero):
        self.fichero = fichero
        self.xml_clientes = open(self.fichero, encoding="utf-8")
    
    def generar_clientes(self, archivo_playlist, archivo_empresas):
        self.ruta_p = archivo_playlist
        self.ruta_e = archivo_empresas
        #sólo para pruebas
        ruta_p = "playlist_clientes.xml"
        ruta_e = "lista_empresas.xml"
        clientes = []
        if self.xml_clientes.readable():
            self.datos = ET.fromstring(self.xml_clientes.read())
            self.lista_clientes = self.datos.findall("cliente")
            a = LecturaPlaylists(ruta_p)
            retornadas= a.generar_playlists()
            e = LecturaEmpresas(ruta_e)
            empresas = e.generar_empresas()
            for cliente in self.lista_clientes:
                asociadas = []
                pago = 0
                nit = cliente.attrib["nit"]
                nombre = cliente.find("nombre").text
                usuario = cliente.find("usuario").text
                clave = cliente.find("clave").text
                direccion = cliente.find("direccion").text
                email = cliente.find("correoElectronico").text
                #Aquí se debe buscar la empresa en la lista de empresas y agregarla al cliente
                empresa = cliente.find("empresa").text
                lista_asociadas = cliente.findall("playlistsAsociadas")
                for playlist in lista_asociadas:
                    una = playlist.iter("playlist")
                    for playlist in una:
                        id_playlist = playlist.text
                        #Aquí se debe buscar la playlist en la lista de playlists y agregarla a la lista de asociadas
                        for playlist_guardada in retornadas:
                            #La lista de asociadas no debe contener más de 3 playlists
                            if playlist_guardada.id == id_playlist and nit == playlist_guardada.nit and len(asociadas) < 3:
                                asociadas.append(playlist_guardada)
                                pago += playlist_guardada.costo
                            #si hay más de 3 playlists, se debe mostrar un mensjae de error y continuar con el siguiente cliente
                            elif playlist_guardada.id == id_playlist and nit == playlist_guardada.nit and len(asociadas) >= 3:
                                print("El cliente tiene más de 3 playlists asociadas, se guardarán sólo las primeras 3")
                                break
                        for empresa in empresas:
                            if empresa.id == id_playlist:
                                la_empresa = empresa
                        
                print(asociadas)
                nuevo_cliente = Cliente(nit, nombre, usuario, clave, direccion, email, la_empresa, pago, asociadas)
                clientes.append(nuevo_cliente)

        i = 1
        for cliente in clientes:
            print("**************************************************************************************************************************************")
            print(f"{i}. Nit: {cliente.nit}, Nombre: {cliente.nombre}, Usuario: {cliente.usuario}, Clave: {cliente.clave}, Direccion: {cliente.direccion}, Email: {cliente.email}")
            print("------------Playlists asociadas:------------")
            i += 1
            for pl in cliente.playlistsAsociadas:
                print("Costo de la playlist: ", pl.costo)
                print(pl)
                print("Canciones de la playlist:")
                for cancion in pl.canciones:
                    print(cancion)
            print("COSTO TOTAL: ", cliente.pago)    
            print("------------Empresa:------------")
            print(cliente.empresa)
            
    
if __name__ == "__main__":
    lectura = LecturaClientes("lista_clientes.xml")
    #A esta se van a enviar las rutas para que se genera tooooooodo y se enlace todo
    lectura.generar_clientes("playlist_clientes.xml", "lista_empresas.xml")