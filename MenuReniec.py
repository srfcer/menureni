from pymongo import MongoClient
from colorama import init, Cursor,Fore, Back, Style
import time
from time import sleep
from datetime import date

contador=0;

myClient = MongoClient("mongodb://localhost:27017")
myDb = myClient["RENIEC"]
myCollection = myDb["patron"]


#############3############################ C O N T A D O R ####################################
def set_contador(valor):
    global contador
    contador = valor
    
def get_contador():
    global contador
    return contador

#.................................Conexión y querys a base de datos.......................................................

def hacerConsulta(dni):
    query = {"DNI": dni} 
    return myCollection.find(query)

def consultaApellidosNombres(ap,am,nom):
    global contador
    # Construir el patrón de expresión regular para buscar en cualquier parte del texto
    patron_regex = f".*{nom}.*"
    # Crear un índice en el campo 'nombre'
    myCollection.create_index("AP_PAT")
    myCollection.create_index("AP_MAT")
    myCollection.create_index("NOMBRES")
    
    query = {"AP_PAT":ap, "AP_MAT":am, "NOMBRES": {"$regex":patron_regex}}
    #cantidad_resultados = myCollection.count_documents(query)
    set_contador(myCollection.count_documents(query))
    return myCollection.find(query)
   
def apellidoPnom(ap,nom):
    global contador
    # Construir el patrón de expresión regular para buscar en cualquier parte del texto
    patron_regex = f".*{nom}.*"
    # Crear un índice en el campo 'nombre'
    myCollection.create_index("AP_PAT")
    myCollection.create_index("NOMBRES")
    
    query = {"AP_PAT":ap, "NOMBRES": {"$regex":patron_regex}}
    #cantidad_resultados = myCollection.count_documents(query)
    set_contador(myCollection.count_documents(query))
    return myCollection.find(query)
    
    
def apePatnomPadre(ap,pap):
    global contador
    # Construir el patrón de expresión regular para buscar en cualquier parte del texto
    patron_regex = f".*{pap}.*"
    # Crear índices
    myCollection.create_index("AP_PAT")
    myCollection.create_index("PADRE")
    
    query = {"AP_PAT":ap, "PADRE":{"$regex":patron_regex}}
    #cantidad_resultados = myCollection.count_documents(query)
    set_contador(myCollection.count_documents(query))
    return myCollection.find(query)
        

def apePatnomMadre(ap,mom):
    global contador 
    # Construir el patrón de expresión regular para buscar en cualquier parte del texto
    patron_regex = f".*{mom}.*"
    # Crear índices
    myCollection.create_index("AP_PAT")
    myCollection.create_index("MADRE")
    
    query = {"AP_PAT":ap, "MADRE":{"$regex":patron_regex}}
    set_contador(myCollection.count_documents(query))
    return myCollection.find(query)

    
def apeMatnombres(am,nom):
    global contador 
    # Construir el patrón de expresión regular para buscar en cualquier parte del texto
    patron_regex = f".*{nom}.*"
    # Crear los índices en los campos a consultar
    myCollection.create_index("AP_MAT")
    myCollection.create_index("NOMBRES")
    
    query = {"AP_MAT":am, "NOMBRES": {"$regex":patron_regex}}
    #cantidad_resultados = myCollection.count_documents(query)
    set_contador(myCollection.count_documents(query))
    return myCollection.find(query)
    
def apeMatnomPadre(am,pap):
    global contador
    # Construir el patrón de expresión regular para buscar en cualquier parte del texto
    patron_regex = f".*{pap}.*"
    # Crear índices
    myCollection.create_index("AP_MAT")
    myCollection.create_index("PADRE")
    
    query = {"AP_MAT":am, "PADRE":{"$regex":patron_regex}}
    #cantidad_resultados = myCollection.count_documents(query)
    set_contador(myCollection.count_documents(query))
    return myCollection.find(query)

def apeMatnomMadre(am,mom):
    global contador
    # Construir el patrón de expresión regular para buscar en cualquier parte del texto
    patron_regex = f".*{mom}.*"
    # Crear índices
    myCollection.create_index("AP_MAT")
    myCollection.create_index("MADRE")
    
    query = {"AP_MAT":am, "MADRE":{"$regex":patron_regex}}
    #cantidad_resultados = myCollection.count_documents(query)
    set_contador(myCollection.count_documents(query))
    return myCollection.find(query)

def apePatMatnomPadre(ap,am,pap):
    global contador
    # Construir el patrón de expresión regular para buscar en cualquier parte del texto
    patron_regex = f".*{pap}.*"
    # Crear índices
    myCollection.create_index("AP_PAT")
    myCollection.create_index("AP_MAT")
    myCollection.create_index("PADRE")
    
    query = {"AP_PAT":ap,"AP_MAT":am, "PADRE":{"$regex":patron_regex}}
    #cantidad_resultados = myCollection.count_documents(query)
    set_contador(myCollection.count_documents(query))
    return myCollection.find(query)
    
#===========================================R E S U L T A D O S========================================================
def mostrarResultados(resultado):
    for data in resultado:
        #print("ID:", data.get("_id"))
        print(Fore.CYAN+"DNI:", data.get("DNI"))
        print("NOMBRES:", data.get("AP_PAT"), data.get("AP_MAT"), data.get("NOMBRES"))
        print("F.NAC:", data.get("FECHA_NAC"))
        print("F.INS:", data.get("FCH_INSCRIPCION"))
        print("F.EMI:", data.get("FCH_EMISION"))
        print("F.CAD:", data.get("FCH_CADUCIDAD"))
        print("UBIGEO_N:", data.get("UBIGEO_NAC"))
        print("UBIGEO_D:", data.get("UBIGEO_DIR"))
        print("DIR:", data.get("DIRECCION"))
        print("SEXO:", data.get("SEXO"))
        print("ESTCIVIL:", data.get("EST_CIVIL"))
        print("DIG-RUC:", data.get("DIG_RUC"))
        print("MADRE:", data.get("MADRE"))
        print("PADRE:", data.get("PADRE"))

                        
        birth_date = data.get("FECHA_NAC")
        birth_date = birth_date.replace('/', ' ') 
        day, month, year = birth_date.split()
        year = int(year)
        month = int(month)
        day= int(day)

        today = date.today()

        try: 
            birth_date = date(today.year, month, day) 
        # In case the date of birth is February 29 and the current year is not leap year... 
        except ValueError: 
        # We subtract 1 from the day of birth to be 28.       
            birth_date = date(today.year, month, day-1) 
    

        # Calculation:
        #-------------
        if birth_date > today:          
            print(f"EDAD: {today.year - year -1} años") 
        else: 
            print(f"EDAD: {today.year - year} años")

        print("-" * 30)  # Línea divisoria entre documentos

#===========================================O P T I O N S========================================================
def opcion1():
    dni = input("Ingrese DNI: ")
    print(" ")
    inicio = time.time()
    resultado = hacerConsulta(dni)
    mostrarResultados(resultado)
    
    fin = time.time()
    print(f"Tiempo: {fin - inicio} segundos")
    print("-" * 30)  # Línea divisoria entre documentos
    
def opcion2():
    ap = input("Apellido Paterno: ")
    am = input("Apellido Materno: ")
    nom = input("Nombre(s): ")
    print(" ")
    inicio = time.time()
    
    resultado = consultaApellidosNombres(ap,am,nom)
    mostrarResultados(resultado)
    
    # Calcular y mostrar el tiempo transcurrido
    fin = time.time()
    tiempo_transcurrido = round(fin - inicio,2)
    print("Cantidad de Colecciones:", get_contador())
    print(f"Tiempo Consulta: {tiempo_transcurrido} segundos")
    print("-" * 30)  # Línea divisoria entre documentos
    
def opcion3(): #apellido paterno y nombres
    ap = input("Apellido Paterno: ")
    nom = input("Nombre(s): ")
    print(" ")
    inicio = time.time()
    
    resultado = apellidoPnom(ap,nom)
    mostrarResultados(resultado)
    
    # Calcular y mostrar el tiempo transcurrido
    fin = time.time()
    tiempo_transcurrido = round(fin - inicio,2)
    print("Cantidad de Colecciones:", get_contador())
    print(f"Tiempo Consulta: {tiempo_transcurrido} segundos")
    print("-" * 30)  # Línea divisoria entre documentos
    
def opcion4(): #apellido paterno y nombres de padre
    ap = input("Apellido Paterno: ")
    padre = input("Nombre de Padre: ")
    print(" ")
    inicio = time.time()
    
    resultado = apePatnomPadre(ap,padre)
    mostrarResultados(resultado)
    
    # Calcular y mostrar el tiempo transcurrido
    fin = time.time()
    tiempo_transcurrido = round(fin - inicio,2)
    print("Cantidad de Colecciones:", get_contador())
    print(f"Tiempo Consulta: {tiempo_transcurrido} segundos")
    print("-" * 30)  # Línea divisoria entre documentos

def opcion5(): #apellido paterno y nombres de madre
    ap = input("Apellido Paterno: ")
    mom = input("Nombre de Madre: ")
    print(" ")
    inicio = time.time()
    
    resultado = apePatnomMadre(ap,mom)
    mostrarResultados(resultado)
    
    # Calcular y mostrar el tiempo transcurrido
    fin = time.time()
    tiempo_transcurrido = round(fin - inicio,2)
    print("Cantidad de Colecciones:", get_contador())
    print(f"Tiempo Consulta: {tiempo_transcurrido} segundos")
    print("-" * 30)  # Línea divisoria entre documentos

def opcion6(): #apellido materno y nombres
    am = input("Apellido Materno: ")
    nom = input("Nombre(s): ")
    print(" ")
    inicio = time.time()
    
    resultado = apeMatnombres(am,nom)
    mostrarResultados(resultado)
    
    # Calcular y mostrar el tiempo transcurrido
    fin = time.time()
    tiempo_transcurrido = round(fin - inicio,2)
    print("Cantidad de Colecciones:", get_contador())
    print(f"Tiempo Consulta: {tiempo_transcurrido} segundos")
    print("-" * 30)  # Línea divisoria entre documentos
    
def opcion7(): #apellido materno y nombre de Padre
    am = input("Apellido Materno: ")
    pap = input("Nombre de Padre: ")
    print(" ")
    inicio = time.time()
    
    resultado = apeMatnomPadre(am,pap)
    mostrarResultados(resultado)
    
    # Calcular y mostrar el tiempo transcurrido
    fin = time.time()
    tiempo_transcurrido = round(fin - inicio,2)
    print("Cantidad de Colecciones:", get_contador())
    print(f"Tiempo Consulta: {tiempo_transcurrido} segundos")
    print("-" * 30)  # Línea divisoria entre documentos
    
def opcion8(): #apellido materno y nombre de Madre
    am = input("Apellido Materno: ")
    mom = input("Nombre de Madre: ")
    print(" ")
    inicio = time.time()
    
    resultado = apeMatnomMadre(am,mom)
    mostrarResultados(resultado)
    
    # Calcular y mostrar el tiempo transcurrido, obtener registros o colecciones
    fin = time.time()
    tiempo_transcurrido = round(fin - inicio,2)
    print("Cantidad de Colecciones:", get_contador())
    print(f"Tiempo Consulta: {tiempo_transcurrido} segundos")
    print("-" * 30)  # Línea divisoria entre documentos

def opcion9(): #apellido materno y nombre de Madre
    ap = input("Apellido Paterno: ")
    am = input("Apellido Materno: ")
    pap = input("Nombre de Padre: ")
    
    print(" ")
    inicio = time.time()
    
    resultado = apePatMatnomPadre(ap,am,pap)
    mostrarResultados(resultado)
    
    # Calcular y mostrar el tiempo transcurrido, obtener registros o colecciones
    fin = time.time()
    tiempo_transcurrido = round(fin - inicio,2)
    print("Cantidad de Colecciones:", get_contador())
    print(f"Tiempo Consulta: {tiempo_transcurrido} segundos")
    print("-" * 30)  # Línea divisoria entre documentos
    
def menu():
    print(Fore.GREEN+"1. Buscar por DNI")
    print("2. Apellidos y Nombres")
    print("3. Apellido Paterno y Nombre(s)")
    print("4. Apellido Paterno y Nombre de Padre")
    print("5. Apellido Paterno y Nombre de Madre")
    print("6. Apellido Materno y Nombre(s)")
    print("7. Apellido Materno y Nombre de Padre")
    print("8. Apellido Materno y Nombre de Madre")
    print("9. Apellidos y Nombre de Padre")
    print("15. Salir")
    print(" ")
    opcion = int(input(Fore.RED+"Ingrese una opción: "))
    print(" ")
    
    match opcion:
        case 1:
            opcion1()
        case 2:
            opcion2()
        case 3:
            opcion3()
        case 4:
            opcion4()
        case 5:
            opcion5()
        case 6:
            opcion6()
        case 7:
            opcion7()
        case 8:
            opcion8()
        case 9:
            opcion9()
        case 15:
            print("Saliendo...") 
        case _:
            print("Opción inválida")  

#Programa principal 
menu()