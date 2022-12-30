from cliente import Cliente
from playlist import Playlist
from empresa import Empresa
from cancion import Cancion
import random
from datetime import datetime
import webbrowser
import fpdf

class Gestor:
    def __init__(self):
        self.clientes = []
        self.playlists = []
        self.empresas = []
        self.canciones = []
        self.numeros_factura = []
    
    def agregar_cancion(self, id, nombre, anio, artista, genero):
        nueva_cancion = Cancion(id, nombre, anio, artista, genero)
        self.canciones.append(nueva_cancion)

    def agregar_playlist(self, id, nit, vinyl, compacto, categoria, costo, canciones = []):
        nueva_playlist = Playlist(id, nit, vinyl, compacto, categoria, costo, canciones)
        if len(self.playlists) == 0:
            self.playlists.append(nueva_playlist)
        else:
            #Si la playlist ya existe, no se agrega
            for playlist in self.playlists:
                if playlist.id == nueva_playlist.id:
                    break
            else:
                self.playlists.append(nueva_playlist)
        return True
    
    def agregar_empresa(self, id, nombre):
        nueva_empresa = Empresa(id, nombre)
        if len(self.empresas) == 0:
            self.empresas.append(nueva_empresa)
        else:
            #Si la empresa ya existe, no se agrega
            for empresa in self.empresas:
                if empresa.id == nueva_empresa.id:
                    break
            else:
                self.empresas.append(nueva_empresa)
        return True

    def agregar_cliente(self, nit, nombre, usuario, clave, direccion, email, empresa, pago, playlistsAsociadas = []):
        nuevo_cliente = Cliente(nit, nombre, usuario, clave, direccion, email, empresa, pago, playlistsAsociadas)
        self.clientes.append(nuevo_cliente)
        return True

    def mostrar_clientes(self):
        json3 = []
        
        for cliente in self.clientes:
            precio = 0
            for p in cliente.playlistsAsociadas:
                
                for psistema in self.playlists:
                    if p == psistema.id:
                        precio += psistema.costo
                    cliente.pago = precio
            client = {
                "nombre": cliente.nombre,
                "nit": cliente.nit,
                "usuario": cliente.usuario,
                "clave": cliente.clave,
                "direccion": cliente.direccion,
                "email": cliente.email,
                "empresa": cliente.empresa,
                "pago": cliente.pago,
                "playlistsAsociadas": cliente.playlistsAsociadas
            }
            json3.append(client)
        return json3
    
    def mostrar_empresas(self):
        json = []
        for empresa in self.empresas:
            empres = {
                "id": empresa.id,
                "nombre": empresa.nombre
            }
            json.append(empres)
        return json
    
    def mostrar_playlists(self):
        json = []
        
        for playlist in self.playlists:
            pl = {
                "id": playlist.id,
                "nit": playlist.nit,
                "vinyl": playlist.vinyl,
                "compacto": playlist.compacto,
                "categoria": playlist.categoria,
                "costo": playlist.costo
            }
            json2 = []
            for cancion in playlist.canciones:
                
                pl2 = {
                    "id": cancion.id,
                    "nombre": cancion.nombre,
                    "anio": cancion.anio,
                    "artista": cancion.artista,
                    "genero": cancion.genero
                }
                json2.append(pl2)
            pl["canciones"] = json2
            json.append(pl)
        return json

    def enviar_playlists(self):
        play = []
        for playlist in self.playlists:
            play.append(playlist)
        return play

    def enviar_clientes(self):
        cli = []
        for cliente in self.clientes:
            cli.append(cliente)
        return cli
    
    def enviar_empresas(self):
        emp = []
        for empresa in self.empresas:
            emp.append(empresa)
        return emp

    def eliminar_cliente(self, nit):
        for cl in self.clientes:
            if cl.nit == nit:
                self.clientes.remove(cl)
                return True
        return False 

    def gen_xmlClientes(self, nit, nombre, usuario, clave, direccion, email, empresa, pago, playlistsAsociadas = []):
        cadena = """<?xml version="1.0" encoding="UTF-8"?>"""
        cadena += """<cliente>"""
        cadena += """<nit>"""+nit+"""</nit>"""
        cadena += """<nombre>"""+nombre+"""</nombre>"""
        cadena += """<usuario>"""+usuario+"""</usuario>"""
        cadena += """<clave>"""+clave+"""</clave>"""
        cadena += """<direccion>"""+direccion+"""</direccion>"""
        cadena += """<email>"""+email+"""</email>"""
        for empresac in self.empresas:
            if empresa.id == empresac:
                nombre_empresa = empresa.nombre
        cadena += """<nombre_empresa>"""+nombre_empresa+"""</nombre_empresa>"""
        cadena += """<pago>"""+pago+"""</pago>"""
        cadena += """<playlistsAsociadas>"""
        for playlist in playlistsAsociadas:
            for playlist_sistema in self.playlists:
                if playlist.id == playlist_sistema.id:
                    cadena += """<id>"""+playlist_sistema.id+"""</id>"""
                    cadena += """<nombre>"""+playlist_sistema.nombre+"""</nombre>"""
                    cadena += """<costo>"""+playlist_sistema.costo+"""</costo>"""
        cadena += """</playlistsAsociadas>"""
        cadena += """</cliente>"""
        #generar archivo xml
        archivo = open("clientes.xml", "w")
        archivo.write(cadena)
        archivo.close()

    def generar_facturas(self, id_empresa):
        nombre_empresa = ""
        
        
        json2 = []
        num_f = random.randint(1, 1000)
        for numero in self.numeros_factura:
            while num_f == numero:
                num_f = random.randint(1, 1000)
        
        if num_f < 10:
            #9
            extra = "000"
            #0009
            num_f = str(num_f)+extra
            num_f = int(num_f)
        if num_f < 100:
            #99
            extra = "00"
            #0099
            num_f = str(num_f)+extra
            num_f = int(num_f)
        if num_f < 1000:
            #999
            extra = "0"
            #0999
            num_f = str(num_f)+extra
            num_f = int(num_f)
        if num_f == 1000:
            extra = ""
            num_f = str(num_f)+extra
            num_f = int(num_f)
        fecha = datetime.now()
        
        for empresa in self.empresas:
            print(empresa)
            clientes = []
            costo_final = 0
            if empresa.id == id_empresa:
                nombre_empresa = empresa.nombre
                for cliente in self.clientes:
                    empresac = cliente.empresa
                    #quitar espacios en blanco
                    empresac = empresac.replace(" ", "")
                    if empresac == id_empresa:
                        costo_final += cliente.pago
                        print("adentro") 
                        clientes.append(cliente)
                json = {
                    "nombre_empresa" : nombre_empresa,
                    "numero_factura" : num_f,
                    "fecha_generada" : fecha,
                    "costo" : costo_final,
                        }
                for client in clientes:
                    c = {
                        "nit_cliente" : client.nit,
                        "nombre_cliente" : client.nombre,
                        "pago" : client.pago,
                        "playlists_asociadas" : client.playlistsAsociadas
                        }
                    json2.append(c)
                json["clientes"] = json2
                #generar pdf con la factura
                pdf = fpdf()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Factura", ln=1, align="C")
                pdf.cell(200, 10, txt="Nombre de la empresa: "+nombre_empresa, ln=1, align="L")
                pdf.cell(200, 10, txt="Numero de factura: "+str(num_f), ln=1, align="L")
                pdf.cell(200, 10, txt="Fecha de generacion: "+str(fecha), ln=1, align="L")
                pdf.cell(200, 10, txt="Costo total: "+str(costo_final), ln=1, align="L")
                pdf.cell(200, 10, txt="Clientes", ln=1, align="L")
                for client in clientes:
                    pdf.cell(200, 10, txt="Nombre: "+client.nombre, ln=1, align="L")
                    pdf.cell(200, 10, txt="NIT: "+client.nit, ln=1, align="L")
                    pdf.cell(200, 10, txt="Playlists asociadas: ", ln=1, align="L")
                    for playlist in client.playlistsAsociadas:
                        pdf.cell(200, 10, txt="Nombre: "+playlist.nombre, ln=1, align="L")
                        pdf.cell(200, 10, txt="Costo: "+str(playlist.costo), ln=1, align="L")
                        for cancion in playlist.canciones:
                            pdf.cell(200, 10, txt="Cancion: "+cancion.nombre, ln=1, align="L")
                            pdf.cell(200, 10, txt="Artista: "+cancion.artista, ln=1, align="L")
                            pdf.cell(200, 10, txt="Genero: "+cancion.genero, ln=1, align="L")
                            pdf.cell(200, 10, txt="Anio: "+cancion.anio, ln=1, align="L")
                            pdf.cell(200, 10, txt="Duracion: "+cancion.duracion, ln=1, align="L")
                            pdf.cell(200, 10, txt=" ", ln=1, align="L")
                        pdf.cell(200, 10, txt=" ", ln=1, align="L")
                    pdf.cell(200, 10, txt=" ", ln=1, align="L")
                pdf.output("factura"+str(num_f)+".pdf")
                return json
            return False

    def eliminar_cancion(self, id_cancion, id_playlist):
        for playlist in self.playlists:
            print(playlist.id)
            if playlist.id == id_playlist:
                for cancion in playlist.canciones:
                    if cancion.id == id_cancion:
                        costo = 0
                        if int(cancion.anio) <= 1960:
                            costo += 25
                        elif int(cancion.anio) > 1960 and int(cancion.anio) <= 1990:
                            costo += 15
                        elif int(cancion.anio) > 1990 and int(cancion.anio) <= 2022:
                            costo += 5
                        costo_nuevo = playlist.costo - costo
                        playlist.costo = costo_nuevo
                        """for cliente in self.clientes:
                            if cliente.nit == playlist.nit:
                                costo_nuevo_cliente = cliente.pago - costo
                                cliente.pago = costo_nuevo_cliente"""
                        playlist.canciones.remove(cancion)
                        if len(playlist.canciones) < 1:
                            costo_nuevo = 0
                            playlist.costo = costo_nuevo
                            return "Ya no hay canciones"
                return True

    def documentacion(self):
        webbrowser.open_new("backend\MANUAL TÉCNICO EN - PROY 2 - 202000277.pdf")
        webbrowser.open_new("backend\MANUAL TÉCNICO ES - PROY 2 - 202000277.pdf")

    def info_estudiante(self):
        return "202000277 - Diana Berducido"