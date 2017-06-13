import sys
import socket
import configparser
from enum import Enum

class CCNDespacho(Enum):
    Status = 1
    Preparar = 2
    Despachar = 3

class cConfig:
    configuracion = configparser.ConfigParser()
    configuracion.read('Config.cfg')
    Rabbit = configuracion['ConexionRabbit']
    General=configuracion['General']
    Http=configuracion['ComandHTTP']
    ResulLectura=""
    def ConexionRabbit():
        return cConfig.Rabbit['CadenaConexion']

    def GetIP():
        nombre_equipo = socket.gethostname()
        direccion_equipo = socket.gethostbyname(nombre_equipo)
        return "1921681126" ##direccion_equipo.replace(".", "")

    def NameQueue():        
        return cConfig.GetIP()

    def IN_NameQueue():     
        return cConfig.General['Prefix_IN']+ cConfig.GetIP()
   
    def OUT_NameQueue():      
        return cConfig.General['Prefix_OUT']+ cConfig.GetIP()

    def HostCCN():
        return cConfig.Http['HostCCN']
    def PortCCN():
        return cConfig.Http['PortCCN']
    def PortMone():
        return cConfig.Http['PortMone']
    def ComandMaquina(comad):
        if (comad==CCNDespacho.Status):
            return cConfig.Http['eStatus']
        if (comad==CCNDespacho.Preparar):
            return cConfig.Http['eSelect']
        if (comad==CCNDespacho.Despachar):
            return cConfig.Http['eDespacho']



