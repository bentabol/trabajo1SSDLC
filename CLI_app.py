from demo import *

user,password,USER,ROL = None,None,None,None

def login():
   print(TITLE)
   global user,password
   print(f"{HEADER}======== LOGIN ========{ENDC}")
   user        = input("login: ")
   password    = getpass("pass: ")

#[1]* Aun teniendo el path si el login no es válido, no se cargan los contactos
miAgenda = Agenda(_path='Contacts.txt')
login()
USER = miAgenda.cerrojo.login(user,password)

while True:
   
   #Si el login en el cerrojo devuelve un Usuario lo guardamos
   if type(USER)==User:
      ROL = USER.userRol
      #[1]* Con un login valido se carga completamente los contactos de la agenda
      miAgenda.loadFromfile(ROL)
      
      print(ROL)
      
      option = input("Selecciona opción: ")
      
      # Add Contact
      if int(option) == 0:
         miAgenda.addContact(_ROL=ROL)
            
      elif int(option) == 1:
         miAgenda.modifyContact(_ROL=ROL)
      
      elif int(option) == 2:
         #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
         miAgenda.deleteContact(llave=ROL)

      elif int(option) == 3:
         #Capa especifica de seguridad que se encarga de validar si el rol es el correcto
         miAgenda.listContact(_ROL=ROL)
         
      elif int(option) == 4:
         miAgenda.addUser(_ROL=ROL)
         
      elif int(option) == 5:
         
         print(f"Ended Session: {user}")
         del user, password
         del USER, ROL
         USER, user,password, ROL = None, None, None, None
         
   # Se devuelve None si el login falla
   else:
      login()
      USER = miAgenda.cerrojo.login(user,password)