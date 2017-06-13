import requests
from Config.cConfig import cConfig as  oConfig
from Config.cConfig import CCNDespacho as Enum

class Simulator:
     
    def CCN_Status():
        try:
            host= oConfig.HostCCN()
            status=oConfig.ComandMaquina(Enum.Status)
            response=requests.get(host,status, verify=False,timeout=0.1)
            print('esper')
            if(response.status_code==200):
                print(response.text)
                return response.text
   
        except OSError as err:
           # print("OS error: {0}".format(err))
            return 'KO'
        except ValueError:
            #print("Could not convert data to an integer.")
            return 'KO'
        except:
            #print("Unexpected error:", sys.exc_info()[0])
            return 'KO'
            raise

    def CCN_Preparar(Carril):
        try:
            host= oConfig.HostCCN()+'('+Carril+')'
            status=oConfig.ComandMaquina(Enum.Preparar)
            response=requests.get(host,status, verify=False,timeout=0.1)
            print('esper')
            if(response.status_code==200):
                print(response.text)
                return response.text
   
        except OSError as err:
            print("OS error: {0}".format(err))
            return 'KO'
        except ValueError:
            print("Could not convert data to an integer.")
            return 'KO'
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return 'KO'
            raise
    def CCN_Despachar(Carril):
        try:
            host= oConfig.HostCCN()+'('+Carril+')'
            status=oConfig.ComandMaquina(Enum.Despachar)
            response=requests.get(host,status, verify=False,timeout=0.1)
            print('esper')
            if(response.status_code==200):
                print(response.text)
                return response.text
   
        except OSError as err:
            print("OS error: {0}".format(err))
            return 'KO'
        except ValueError:
            print("Could not convert data to an integer.")
            return 'KO'
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return 'KO'
            raise