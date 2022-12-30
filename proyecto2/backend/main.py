from flask import Flask, request
from flask.json import jsonify
from flask_cors import CORS
from gestor import Gestor
from playlist import Playlist
from xml.etree import ElementTree as ET
from cancion import Cancion

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

gestor = Gestor()

@app.route('/')
def home():
    return "Bienvenido a la API de la tienda de música."

@app.route('/masivaPlaylists', methods=['POST'])
def masiva_playlists():
    xml = request.data.decode("utf-8")
    datos = ET.XML(xml)
    lista_playlists = datos.findall("playlist")
    cantidad = 0
    playlists_sistema = gestor.enviar_playlists()
    for playlist in lista_playlists:
        cantidad += 1
        costo = 0
        canciones = []
        id_playlist = playlist.attrib["id"].replace(" ", "")

        for plist in playlists_sistema:
            if plist.id == id_playlist:
                return jsonify({"error":f"La playlist con id {id_playlist} ya está en el sistema."})

        nit = playlist.find("nitCliente").text.replace(" ", "")
        vynil = playlist.find("vinyl").text.replace(" ", "")
        compacto = playlist.find("compacto").text.replace(" ", "")
        categoria = playlist.find("categoria").text.replace(" ", "")
        if vynil == "True":
            costo += 500
        if compacto == "True":
            costo += 100
        print(id_playlist, nit, vynil, compacto, categoria)
        lista_canciones = playlist.findall("canciones")
        for cancion in lista_canciones:
            una = cancion.iter("cancion")
            for cancion in una:
                id_cancion = cancion.attrib["id"].replace(" ", "")
                nombre_cancion = cancion.find("nombre").text.replace(" ", "")
                anio = cancion.find("anio").text.replace(" ", "")
                artista = cancion.find("artista").text.replace(" ", "")
                genero = cancion.find("genero").text.replace(" ", "")
                if int(anio) <= 1960:
                    costo += 25
                elif int(anio) > 1960 and int(anio) <= 1990:
                    costo += 15
                elif int(anio) > 1990 and int(anio) <= 2022:
                    costo += 5
                #print(id_cancion, nombre_cancion, anio, artista, genero)
                cancione = Cancion(id_cancion, nombre_cancion, anio, artista, genero)
                canciones.append(cancione)
        gestor.agregar_playlist(id_playlist, nit, vynil, compacto, categoria, costo, canciones)
    
    #return jsonify(gestor.mostrar_playlists()), cantidad
    return jsonify({"mensaje":f"{cantidad} playlists agregadas correctamente"}), 200

@app.route('/masivaEmpresas', methods=['POST'])
def masiva_empresas():
    cantidad = 0
    emp_sistema = gestor.enviar_empresas()
    xml = request.data.decode("utf-8")
    datos = ET.XML(xml)
    lista_empresas = datos.findall("empresa")
    for empresa in lista_empresas:
        cantidad += 1
        id = empresa.attrib["id"].replace(" ", "")
        nombre = empresa.find("nombre").text.replace(" ", "")
        for emp in emp_sistema:
            if emp.nombre == nombre and emp.id == id:
                return jsonify({"error":f"La empresa {nombre} ya existe en el sistema."})

        gestor.agregar_empresa(id, nombre)
    
    #return jsonify(gestor.mostrar_empresas()), cantidad
    return jsonify({"mensaje":f"{cantidad} empresas agregadas correctamente"}), 200

@app.route('/masivaClientes', methods=['POST'])
def masiva_clientes():
    xml = request.data.decode("utf-8")
    datos = ET.XML(xml)
    lista_clientes = datos.findall("cliente")
    play_sistema = gestor.enviar_playlists()
    cli_sistema = gestor.enviar_clientes()
    for cliente in lista_clientes:
        asociadas = []
        pago = 0
        nit = cliente.attrib["nit"].replace(" ", "")
        nombre = cliente.find("nombre").text.replace(" ", "")
        usuario = cliente.find("usuario").text.replace(" ", "")
        #validar que el cliente no exista
        for cl in cli_sistema:
            if cl.nit == nit and cl.nombre == nombre:
                return jsonify({"error":f"El cliente {nombre} ya existe en el sistema."})

        clave = cliente.find("clave").text.replace(" ", "")
        direccion = cliente.find("direccion").text.replace(" ", "")
        email = cliente.find("correoElectronico").text.replace(" ", "")
        #Aquí se debe buscar la empresa en la lista de empresas y agregarla al cliente
        empresa = cliente.find("empresa").text.replace(" ", "")
        lista_asociadas = cliente.findall("playlistsAsociadas")

        for playlist in lista_asociadas:
            una = playlist.iter("playlist")

            
            for playlist in una:
                posibles = []
                
                id_playlist = playlist.text
                if len(asociadas)<3:
                    for p in play_sistema:
                        if p.id == id_playlist:
                            #hay que validar que la playlist no esté en otro cliente
                            posibles.append(id_playlist)
                    if len(posibles) == 1:
                        for c in cli_sistema:
                            for p in c.playlistsAsociadas:
                                if p == id_playlist:
                                    return jsonify({"error":f"La playlist con id {id_playlist} ya está asociada a otro cliente"})
                        asociadas.append(id_playlist)
                    else:
                        return jsonify({"error":f"La playlist con id {id_playlist} no existe en el sistema"})
                else:
                    return jsonify({"error":"El cliente no puede tener más de 3 playlists asociadas"})

                for playlist in play_sistema:
                    if playlist.id == id_playlist and playlist.nit == nit:
                        pago += playlist.costo

        gestor.agregar_cliente(nit, nombre, usuario, clave, direccion, email, empresa, pago, asociadas)
        gestor.gen_xmlClientes(nit, nombre, usuario, clave, direccion, email, empresa, pago, asociadas)
    
    return jsonify(gestor.mostrar_clientes()), 200
    #return jsonify({"mensaje":"Clientes agregado exitosamente"}), 200

#Esta tiene que ir a alguna playlist, entonces no probar todavía
@app.route('/agregarCancion', methods=['POST'])
def agregar_cancion():
    json=request.get_json()
    gestor.agregar_cancion(json['id'], json['nombre'],json['anio'],json['artista'],json['genero'])
    return jsonify({'ok':True, 'data':'Cancion añadida con exito'}),200

@app.route('/agregarPlaylists', methods=['POST'])
def agregar_playlist():
    xml = request.data.decode("utf-8")
    datos = ET.XML(xml)
    lista_playlists = datos.findall("playlist")
    cantidad = 0
    playlists_sistema = gestor.enviar_playlists()
    for playlist in lista_playlists:
        cantidad += 1
        costo = 0
        canciones = []
        id_playlist = playlist.attrib["id"]

        for plist in playlists_sistema:
            if plist.id == id_playlist:
                return jsonify({"error":f"La playlist con id {id_playlist} ya está en el sistema."})

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
                cancione = Cancion(id_cancion, nombre_cancion, anio, artista, genero)
                canciones.append(cancione)
        gestor.agregar_playlist(id_playlist, nit, vynil, compacto, categoria, costo, canciones)
    
    #return jsonify(gestor.mostrar_playlists()), cantidad
    return jsonify({"mensaje":f"{cantidad} playlists agregadas correctamente"}), 200

@app.route('/agregarEmpresa', methods=['POST'])
def agregar_empresa():
    json=request.get_json()
    gestor.agregar_empresa(json['id'], json['nombre'])
    return jsonify({'ok':True, 'data':'Empresa añadida con exito'}),200

@app.route('/mostrarPlaylists', methods=['GET'])
def mostrar_playlist():
    pepe = gestor.mostrar_playlists()
    if len(pepe)<1:
        return jsonify({'ok': True, 'data':'No hay playlists en el sistema.'})
    return jsonify({'ok':True, 'data':gestor.mostrar_playlists()}),200

@app.route('/mostrarClientes', methods=['GET'])
def mostrar_clientes():
    pepe = gestor.mostrar_clientes()
    if len(pepe)<1:
        return jsonify({'ok': True, 'data':'No hay clientes en el sistema.'})
    return jsonify({'ok':True, 'data':gestor.mostrar_clientes()}),200

@app.route('/mostrarEmpresas', methods=['GET'])
def mostrar_empresas():
    pepe = gestor.mostrar_empresas()
    if len(pepe)<1:
        return jsonify({'ok': True, 'data':'No hay empresas en el sistema.'})
    return jsonify({'ok':True, 'data':gestor.mostrar_empresas()}),200

@app.route('/eliminarCliente', methods = ['DELETE'])
def eliminar_cliente():
    json = request.get_json()
    nit_cliente = json['nit']
    if gestor.eliminar_cliente(json['nit']) is True:
        return jsonify({'ok':True, 'data':f'Cliente con nit {nit_cliente} eliminado con exito'}),200
    return jsonify({'ok':False, 'data':f'Cliente con nit {nit_cliente} no existe en el sistema'}),404

@app.route('/eliminarCancion', methods = ['DELETE'])
def eliminar_cancion():
    json = request.get_json()
    id_playlist = json['id_playlist']
    id_cancion = json['id_cancion']
    pepe = gestor.eliminar_cancion(id_cancion, id_playlist)
    if pepe is True:
        return jsonify({'ok':True, 'data':f'Cancion con id {id_cancion} de playlist con id {id_playlist} eliminada con exito'}),200
    elif pepe == "No hay canciones":
        return jsonify({'ok':False, 'data':f'Cancion con id {id_cancion} de playlist con id {id_playlist} eliminada con exito. Ahora la playlist se encuentra vacía.'}),404
    return jsonify({'ok':False, 'data':f'Cancion o playlist no existen'}),404

@app.route('/generarFactura', methods = ['GET'])
def generar_factura(): 
    json = request.get_json()
    id_empresa = json['id_empresa']
    if gestor.generar_facturas(id_empresa) is False:
        return jsonify({'ok':False, 'data':f'Empresa con id {id_empresa} no existe en el sistema'}),404
    return jsonify({'ok':True, 'data':gestor.generar_facturas(id_empresa)})

@app.route('/informacion_estudiante', methods = ['GET'])
def informacion_estudiante():
    return jsonify({'ok':True, 'data':'Diana Berducido - 202000277'}),200

@app.route('/documentacion', methods = ['GET'])
def documentacion():
    gestor.documentacion()
    return jsonify({'ok':True, 'data':'Documentacion generada con exito'}),200

#a través de parametros en URL
"""@app.route('/eliminarCliente/', methods = ['DELETE'])
def eliminar_clienteURL():
    nit = request.args.get("nit")
    if gestor.eliminar_cliente(nit) is True:
        return jsonify({'ok':True, 'data':f'Cliente con nit {nit} eliminado con exito'}),200
    return jsonify({'ok':False, 'data':f'Cliente con nit {nit} no existe en el sistema'}),404

@app.route('/eliminarCancion', methods = ['DELETE'])
def eliminar_cancionURL():
    id_cancion = request.args['id_cancion']
    id_playlist = request.args['id_playlist']
    pepe = gestor.eliminar_cancion(id_cancion, id_playlist)
    if pepe is True:
        return jsonify({'ok':True, 'data':f'Cancion con id {id_cancion} de playlist con id {id_playlist} eliminada con exito'}),200
    elif pepe == "No hay canciones":
        return jsonify({'ok':False, 'data':f'Cancion con id {id_cancion} de playlist con id {id_playlist} eliminada con exito. Ahora la playlist se encuentra vacía.'}),404
    return jsonify({'ok':False, 'data':f'Cancion o playlist no existen'}),404"""

if __name__ == '__main__':
    app.run(debug=True)