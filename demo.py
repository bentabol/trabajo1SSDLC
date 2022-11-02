from config import *
from getpass import getpass
# Seguir RBAC Pattern, crear una seguridad general que englobe todo y despues capa a capa con sus funciones y validaciones individuales
# Que solicita:
# -Interfaz CLI
# -Persistencia de datos (archivo.txt o csv)
#Mas adelantes comprobar integridad

#Tengo que configurar el pasword de forma correcta que compruebe que no es una password repetida o caracteres no aceptables
#Crear otro txt que almacene los usuarios con su rol correspondiente, su nombre de usuario y su password. 
#Para parte 2 debo controlar integridad de roles y de contactos, es decir que el programa se de cuenta que han alterado el txt de los usuarios y roles y nos lo indique
#Revisar para que los metodos sean cohesivos (Ejemplo: el metodo de leer datos hacerlo separado del de guardar e3n el fichero)

class rol():
    # Clase que engloba los roles de forma de general
    
    nameRol         = None
    addContact      = None
    modifyContact   = None
    deleteContact   = None
    listContact     = None
    addUser         = None
    
    def __init__(self,_nameRol,_add, _modify,_delete,_list,_addUser):
        
        # Para crear un rol
        # Admin = rol(True,True,True,True,True) todo true ya que el admin cumple todas las funcionalidades
        self.nameRol        = _nameRol
        self.addContact     = _add
        self.modifyContact  = _modify
        self.deleteContact  = _delete
        self.listContact    = _list
        self.addUser        = _addUser
    
    def __str__(self):
        def getStatus(val,index):
            if val:
                return f"{OKGREEN}[{index}]{ENDC}"
            else:
                return f"{FAIL}[{index}]{ENDC}"
        return f"""
┌─────────────────────────────────────────────┐
│\t\t{OKBLUE}O P T I O N S{ENDC}
├─────────────────────────────────────────────┤
│\t{getStatus(self.addContact,      0)}\taddContact
│\t{getStatus(self.modifyContact,   1)}\tmodifyContact
│\t{getStatus(self.deleteContact,   2)}\tdeleteContact
│\t{getStatus(self.listContact,     3)}\tlistContact
│\t{getStatus(self.addUser,         4)}\taddUser
│\t{OKCYAN}[5]{ENDC                   }\tClose Session
└─────────────────────────────────────────────┘
"""

class User():
    
    user = None
    password = None
    userRol = None
        
    def __init__(self,_user,_pass,_rol):
        self.user       = _user
        self.password   = _pass
        self.userRol    = _rol

    def __str__(self):
        return f'{self.user},{self.password},{(self.userRol).nameRol}\n'
    
#   Se crean los roles existentes (ESTOS VAN A SER UNICOS)

# Privilegios de ADMIN == ALL
Administrador   = rol('admin',True,True,True,True,True)
# Gestor (addContact, modifyContact y listContact)
Gestor          = rol('gestor',True,True,False,True,False)
# Adistente (listContact)
Asistente       = rol('asistente',False,False,False,True,False)

roleList=[Administrador,Gestor,Asistente]

def getRol(strRol):
    if      'admin' in strRol:
        return Administrador
    elif    'gestor' in strRol:
        return Gestor
    elif    'asistente' in strRol:
        return Asistente

class Cerrojo():
    
    #Creamos los roles para en un futuro evaluarlos contra un rol entrante y usarlo de metodo de seguridad el Cerrojo
    userList = []
    
    def addUser(self,_ROL,_usuario):
        # Heredado de la clase rol el campo addUser (booleano)
        if _ROL.addUser == True:
            n = 0
            for rolesX in roleList:
                print(str(n)+" "+rolesX.nameRol)
                n +=1
            
            selectedRol = input('Ingrese el rol para el nuevo usuario: ')
            
            if (int(selectedRol)==0):
                _usuario.userRol = Administrador
            
            elif (int(selectedRol)==1):
                _usuario.userRol = Gestor
            
            elif (int(selectedRol)==2):
                _usuario.userRol = Asistente
            else:
                print(f"{FAIL}Ivalid rol selected{ENDC}")
            
            self.userList.append(_usuario)
            self.saveToFile()
    
    def login(self,_user,_pass):
        
        for UsuarioX in self.userList:
            if (UsuarioX.user == _user) & (UsuarioX.password == _pass):
                tmpUser = UsuarioX
                print(f"\n{OKGREEN}[OK]{ENDC}\tLogged as {OKCYAN}{tmpUser.userRol.nameRol}{ENDC}")
                return tmpUser
        
        print(f"{WARNING}[WARNING]{ENDC}\tUsuario o contraseña inválidos")
        return None
    
    def __init__(self):
        self.loadFromFile()
        print(f"{OKGREEN}[OK]{ENDC}\troleUsers loaded")
        
        #   Se crea un USUARIO ROOT con privilegiosde admin
        root = User('admin','1234', Administrador)
        if not self.userInList(root):
            self.userList.append(root)
            self.saveToFile()
    
    def userInList(self,_user):
        for cadaUser in self.userList:
            if cadaUser.user == _user.user:
                return True
        return False
    
    def loadFromFile(self):
        with open('Users.txt','r') as f:
                    while True:
                        line = f.readline()
                        # Linea en blanco -> \n
                        if ',' in line:
                            tmp = line.split(",")
                            tmp = User(tmp[0],tmp[1],getRol(tmp[2]))
                            self.userList.append(tmp)
                        elif len(line)<2:
                            break
                    f.close()

    def saveToFile(self):
        #llegado a este punto tenemos el Cerrojo y los usuarios con roles en la RAM -> volcar a un archivo
        with open('Users.txt','w') as f:
            for cadaUser in self.userList:
                f.write(str(cadaUser))
            f.close()

# Persona para Contacto
class Persona():
    #Datos de cada persona dentro de la agenda
    id=None
    Nombre = None
    Apellido = None
    NroTelefono = None
    
    def __init__(self, nombre, apellido, numero):
        self.Nombre=nombre
        self.Apellido=apellido
        self.NroTelefono=numero        

    def __str__(self):
        def eval(stringX):
            if len(stringX)<8:
                return '\t\t'
            else:
                return '\t'
        return f"{self.Nombre}{eval(self.Nombre)}{self.Apellido}{eval(self.Apellido)}{self.NroTelefono}"

def dialogoCrearPersona():
   nombre = input("Nombre: ")
   apellido = input("Apellido: ")
   numero = input("Numero: ")
   return Persona(nombre,apellido,numero)

#Clase agenda  
class Agenda():
      
    # Cerrojo
    cerrojo = Cerrojo()
    path = None
    Contactos = []
    
    def __init__(self,_path=None):
        if _path!=None:
            self.path = _path
    
    #Se supone que esperamos una persona (contacto)
    def addContact(self, _ROL):
        tmp = dialogoCrearPersona()
        result = input(f"quiere confirmar añadir a {tmp.Nombre} a la agenda yes/no: ")
        if result == "yes":
            #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
            #Si el rol es valido se sincroniza la agenda si no lo es, se aborta
            if _ROL.addContact:
                print(f'{OKGREEN}[OK]{ENDC}\t{tmp.Nombre} added to Contacts')
                self.Contactos.append(tmp)
                self.sync()
            else:
                self.notRole()
        else:
            print(f"{FAIL}operacion abortada por el usuario{ENDC}")
    
    #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
    def modifyContact(self, _ROL=None):
        print("Dialogo Modificar Persona:")
        modificado = False
        if _ROL.modifyContact:
            
            def getContacts(findContact):
                listC = []
                for cadaContact in self.Contactos:
                    if findContact in cadaContact.Nombre:
                        listC.append(cadaContact)
                return listC
            
            listaTmp = getContacts(input("Buscar contacto: "))
            
            #Imprimimos los contactos coincidentes
            for option, contacto in enumerate(listaTmp):
                print(f"Result option: [{option}]\n{contacto}")
            
            selectOption = int(input("Seleccionamos el Contacto que queremos modificar: "))
            
            if selectOption in  range(0,len(listaTmp)):
                ContactoTmp = dialogoCrearPersona()
                index = self.Contactos.index(listaTmp[selectOption])
                self.Contactos[index] = ContactoTmp
                modificado = True
            else:
                print(f"{OKGREEN}Opcion incorrecta. Abort{ENDC}")
            
            if modificado:
                print(f"{OKGREEN}Success{ENDC}")
                self.sync()
            else:
                print(f"{FAIL}Fallo en intento modificar usuario{ENDC}")
                
        else:
            print(f"{FAIL}[FAIL]{ENDC}\t{_ROL.nameRol} no tiene derechos para ejecutar esa Accion")
            return False
    
    #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
    def deleteContact(self, llave=None):
        print("Dialogo Eliminar Persona:")
        nombre = input("Indique el nombre a eliminar en la agenda: ")
        eliminado = False
        
        if llave.deleteContact:
            if ((nombre!=None)):
                cont = 0
                for cadaContacto in self.Contactos:
                    if cadaContacto.Nombre == nombre:
                        tmp = cadaContacto
                        self.Contactos.pop(cont)
                        eliminado = True
                    cont+=1
            if eliminado:
                print("Success")
                self.sync()
            else:
                print("Fail")
        else:
            print(f"{llave.nameRol} no tiene derechos para ejecutar esa Accion")
         
    #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
    def listContact(self, _ROL):
        print("Dialogo Listar Agenda: ")
        if _ROL.listContact:
            print(HEADER_LISTAR)
            for cadaContacto in self.Contactos:
                print(cadaContacto)
        else:
            print(f"{_ROL.nameRol} no tiene derechos para ejecutar esa Accion")
    
    #Specyfic Layer
    def addUser(self,_ROL):
        print("Dialogo añadir usuario:")
         #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
        _user = input("usuario: ")
        _pass = getpass("password: ")
        _pass2 = getpass("Confirme:\npassword: ")
        if _pass == _pass2:
            usuario = User(_user,_pass,None)
            self.cerrojo.addUser(_ROL,usuario)
            self.sync()
        else:
            #capa de seguridad que solicita de nuevo la password por posibles errores
            print("Passwords no coincide")        
    
    #Specyfic Layer
    def notRole(self):
        print(f"{FAIL}[FAIL]{ENDC}\tRol invalido")
    
    #Specyfic Layer
    def sync(self):
        with open (self.path,'w') as f:
            for x in self.Contactos:
                f.write(x.Nombre+","+x.Apellido+","+x.NroTelefono+"\n")
            f.close()
    
    def loadFromfile(self, _ROL):
        if type(_ROL) == rol:
            
            with open(self.path,'r') as f:
                    while True:
                        line = f.readline()
                        # Linea en blanco -> \n
                        if ',' in line:
                            tmp = line.split(",")
                            tmp = Persona(tmp[0],tmp[1],tmp[2])
                            self.Contactos.append(tmp)
                        elif line == '':
                            break
                    print(f"{OKGREEN}[OK]{ENDC}\tContactos cargados del fichero")
                    f.close()    