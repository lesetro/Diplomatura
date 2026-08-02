# TP1 - Diplomatura en Ciencias de Datos y Machine Learning

# punto 1- Procesador de Biometria (IMC)
def calcular_imc():
    print("\nCalcular IMC ")
    peso_texto = input("Ingresa tu peso en kg: ")
    altura_texto = input("Ingresa tu altura en metros: ")
    if not peso_texto.replace('.', '', 1).isdigit() or not altura_texto.replace('.', '', 1).isdigit():
        print("Error: ingresa numeros validos, digitos con punto decimal")
        return
    peso = float(peso_texto)
    altura = float(altura_texto)
    if peso <= 0 or altura <= 0:
        print("Error: los valores deben ser positivos mayores a cero, digitos con punto")
        return
    imc = peso / (altura ** 2)
    print(f"Tu IMC es: {imc:.2f}")
    if imc > 25:
        print("Atencion: Valor por encima del promedio")

# punto 2-Segmentacion de Clientes (Precio de entrada)
def precio_entrada():
    print("\n Precio de Entrada ")
    edad_texto = input("Ingresa la edad: ")
    if not edad_texto.isdigit():
        print("Error: ingresa un numero valido")
        return
    edad = int(edad_texto)
    if edad < 4:
        categoria = "Infantil"
        precio = 0
    elif edad <= 18:
        categoria = "Junior"
        precio = 400
    else:
        categoria = "Senior"
        precio = 800
    print(f"Categoria asignada: {categoria} | Precio: ${precio}")

# punto 3- Analisis de texto
def analizar_texto():
    print("\n Analisis de Texto ")
    texto = input("Ingresa una frase: ")
    print(f"Mayusculas: {texto.upper()}")
    print(f"Longitud: {len(texto)} caracteres")
    print(f"Aparece 'Python': {texto.lower().count('python')} vez/veces")
    print(f"Texto invertido: {texto[::-1]}")

# punto 4- Simulador de Ingresos Mensuales
def simulador_ingresos():
    print("\n Simulador de Ingresos Mensuales ")
    cantidad_meses_texto = input("Cuantos meses vas a ingresar? ")
    
    # Validando que sea entero positivo (sin puntos)
    if not cantidad_meses_texto.isdigit():
        print("Error: ingresa un número entero válido (sin puntos decimales)")
        return
    
    cantidad_meses = int(cantidad_meses_texto)
    if cantidad_meses <= 0:
        print("Error: el numero de meses debe ser mayor a cero")
        return
    
    total = 0
    mes_maximo = 1  
    mes_minimo = 1
    ingreso_maximo = None
    ingreso_minimo = None
    
    for mes in range(1, cantidad_meses + 1):
        # Bucle para validar el ingreso de CADA mes
        while True:
            ingreso_texto = input(f"Ingreso del mes {mes}: $")
            
            # Validar formato
            if not ingreso_texto.replace('.', '', 1).isdigit():
                print("Error: ingresa un número válido (solo dígitos y un punto)")
                continue  # Vuelve a preguntar el mismo mes
            
            ingreso = float(ingreso_texto)
            
            if ingreso < 0:
                print("Error: el ingreso no puede ser negativo")
                continue  # Vuelve a preguntar el mismo mes
            
            
            break  # Sale del while y continúa con el siguiente mes
        
        total += ingreso
        
        # Lógica para máximos y mínimos
        if mes == 1:
            ingreso_maximo = ingreso
            ingreso_minimo = ingreso
        else:
            if ingreso > ingreso_maximo:
                ingreso_maximo = ingreso
                mes_maximo = mes
            if ingreso < ingreso_minimo:
                ingreso_minimo = ingreso
                mes_minimo = mes
    
    promedio = total / cantidad_meses
    print(f"Total acumulado:  ${total:.2f}")
    print(f"Promedio mensual: ${promedio:.2f}")
    print(f"Ingreso mas alto: ${ingreso_maximo:.2f} (mes {mes_maximo})")
    print(f"Ingreso mas bajo: ${ingreso_minimo:.2f} (mes {mes_minimo})")

# Menu principal
while True:
    print("\n Sistema de Datos Personales ")
    print("1 - Calcular IMC")
    print("2 - Precio de entrada")
    print("3 - Analizar texto")
    print("4 - Simulador de ingresos mensuales")
    print("5 - Salir")
    opcion = input("Elegi una opcion: ")
    if opcion == "1":
        calcular_imc()
    elif opcion == "2":
        precio_entrada()
    elif opcion == "3":
        analizar_texto()
    elif opcion == "4":
        simulador_ingresos()
    elif opcion == "5":
        print("Saliendo del sistema...")
        break
    else:
        print("Opcion invalida. Ingresa un numero del 1 al 5")