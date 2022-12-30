from xml.etree import ElementTree as ET
from empresa import Empresa

class LecturaEmpresas:
    def __init__(self, fichero):
        self.fichero = fichero
        self.xml_empresas = open(self.fichero, encoding="utf-8")

    def generar_empresas(self):
        empresas = []
        if self.xml_empresas.readable():
            self.datos = ET.fromstring(self.xml_empresas.read())
            self.lista_empresas = self.datos.findall("empresa")
            for empresa in self.lista_empresas:
                id = empresa.attrib["id"]
                nombre = empresa.find("nombre").text
                nueva_empresa = Empresa(id, nombre)
                empresas.append(nueva_empresa)

        i = 1
        for empresa in empresas:
            print(f"{i}. Nombre: {empresa.nombre}, ID: {empresa.id}")
            i += 1
    
        return empresas

if __name__ == "__main__":
    lectura = LecturaEmpresas("lista_empresas.xml")
    lectura.generar_empresas()