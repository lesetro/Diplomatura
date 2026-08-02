# =============================================================================
# DIPLOMATURA EN PYTHON - CIENCIA DE DATOS Y MACHINE LEARNING
# Trabajo Práctico N°1 — Fundamentos y Lógica de Datos en Python
# Autor: [Tu Nombre]
# =============================================================================

# 💡 TRUCO: En VS Code podés colapsar bloques de código con el triángulo
#    que aparece a la izquierda de cada función o bloque. Muy útil para
#    navegar archivos grandes.

# 💡 ATAJO ÚTIL: Ctrl + / comenta o descomenta la línea seleccionada
# 💡 ATAJO ÚTIL: Alt + ↑/↓ mueve una línea de código hacia arriba o abajo
# 💡 ATAJO ÚTIL: Ctrl + D selecciona la siguiente ocurrencia de una palabra

# =============================================================================
# OPCIÓN 1 — PROCESADOR DE BIOMETRÍA (IMC)
# Herramienta: Calcula el Índice de Masa Corporal a partir de peso y altura.
# Fórmula: IMC = peso / altura²
# Concepto de datos: Validación de entrada — dato inválido = resultado inválido
# =============================================================================

def calcular_imc():
    print("\n--- Procesador de Biometría (IMC) ---")

    # input() SIEMPRE devuelve un STRING — hay que convertir con float()
    # 💡 TÉCNICA: float() para decimales, int() para enteros
    peso = float(input("Ingresá tu peso en kg (ej: 70.5): "))
    altura = float(input("Ingresá tu altura en metros (ej: 1.75): "))

    # VALIDACIÓN — nunca confiar en lo que ingresa el usuario
    # 💡 TRUCO: siempre validar ANTES de calcular, no después
    if peso <= 0 or altura <= 0:
        print("⚠️  Error: El peso y la altura deben ser valores positivos.")
        return  # return sin valor sale de la función inmediatamente

    # Cálculo del IMC
    # 💡 TÉCNICA: altura ** 2 es "altura al cuadrado" (potencia en Python)
    imc = peso / (altura ** 2)

    # f-string: la forma moderna y legible de formatear texto en Python
    # 💡 TRUCO: {variable:.2f} muestra el número con exactamente 2 decimales
    print(f"\nResultado IMC: {imc:.2f}")

    # Clasificación por umbrales — estructura if / elif / else
    # 💡 TÉCNICA: elif evita anidar if dentro de if, el código queda más plano
    if imc < 18.5:
        print("Clasificación: Bajo peso")
    elif imc <= 25:
        print("Clasificación: Peso normal ✅")
    else:
        # Requisito del TP: mensaje especial si IMC > 25
        print("Clasificación: Sobrepeso")
        print("⚠️  Atención: Valor por encima del promedio")


# =============================================================================
# OPCIÓN 2 — SEGMENTACIÓN DE CLIENTES (PRECIO DE ENTRADA)
# Herramienta: Asigna categoría y precio según la edad del cliente.
# Concepto de datos: Segmentación — clasificar registros según rangos de valor
# =============================================================================

def precio_entrada():
    print("\n--- Segmentación de Clientes (Precio de Entrada) ---")

    # int() convierte a entero — la edad no tiene decimales
    edad = int(input("Ingresá la edad del cliente: "))

    # 💡 TÉCNICA: variables con nombres claros en snake_case
    #    Mejor: categoria_asignada que mejor: cat o CA o CATEGORIA
    if edad < 4:
        categoria_asignada = "Infantil"
        precio = 0
    elif edad <= 18:
        # 💡 TRUCO: 4 <= edad <= 18 también es válido en Python (encadenado)
        #    Equivale a: edad >= 4 and edad <= 18
        categoria_asignada = "Junior"
        precio = 400
    else:
        categoria_asignada = "Senior"
        precio = 800

    # Salida formateada exactamente como pide el TP
    print(f"\nCategoría asignada: {categoria_asignada} | Precio: ${precio}")


# =============================================================================
# OPCIÓN 3 — ANÁLISIS DE TEXTO (LOGS / NLP BÁSICO)
# Herramienta: Procesa una cadena de texto y extrae métricas básicas.
# Concepto de datos: Procesamiento de lenguaje natural — texto como dato crudo
# =============================================================================

def analizar_texto():
    print("\n--- Análisis de Texto (NLP básico) ---")

    # 💡 TÉCNICA: strip() elimina espacios en blanco al inicio y al final
    #    Muy útil para limpiar datos — hábito profesional desde el inicio
    texto = input("Ingresá una frase o texto: ").strip()

    # --- Mayúsculas ---
    # 💡 TRUCO: los strings tienen métodos propios — texto.upper(), .lower(),
    #    .replace(), .split(), .count() — no necesitás importar nada
    texto_mayusculas = texto.upper()
    print(f"\nEn mayúsculas:     {texto_mayusculas}")

    # --- Longitud ---
    # len() es una función built-in de Python — funciona con strings, listas, etc.
    longitud = len(texto)
    print(f"Longitud total:    {longitud} caracteres")

    # --- Conteo de "Python" ---
    # .lower() normaliza todo a minúsculas antes de buscar
    # 💡 TÉCNICA: siempre normalizar antes de comparar texto (case-insensitive)
    #    Es el primer paso en cualquier pipeline de NLP real
    conteo_python = texto.lower().count("python")
    print(f"Aparece 'Python':  {conteo_python} vez/veces")

    # --- Texto invertido ---
    # 💡 TRUCO PYTHON CLÁSICO: texto[::-1] es un slice con paso -1
    #    Lee el string de atrás para adelante — muy usado en entrevistas técnicas
    #    Sintaxis: [inicio:fin:paso] — si se omiten inicio y fin, toma todo
    texto_invertido = texto[::-1]
    print(f"Texto invertido:   {texto_invertido}")


# =============================================================================
# OPCIÓN 4 — MONITOR DE RENDIMIENTO (SIMULADOR DE INGRESOS MENSUALES)
# Herramienta: Analiza una serie de ingresos y calcula estadísticas básicas.
# Concepto de datos: Acumuladores — base de cualquier algoritmo de agregación
# Restricción del TP: NO usar listas ni funciones max() / min()
# =============================================================================

def simulador_ingresos():
    print("\n--- Simulador de Ingresos Mensuales ---")

    cantidad_meses = int(input("¿Cuántos meses querés procesar? "))

    # --- Inicialización de acumuladores ---
    # 💡 TÉCNICA CLAVE: siempre inicializar variables ANTES del bucle
    #    El acumulador parte en 0 y "acumula" cada valor nuevo
    total_ingresos = 0

    # Para max y min sin usar funciones built-in:
    # 💡 TRUCO: inicializar en None y manejar el primer caso aparte
    #    O inicializar ingreso_maximo en -infinito y ingreso_minimo en +infinito
    #    float('inf') es infinito en Python — cualquier número es menor que él
    ingreso_maximo = float('-inf')   # Todo número real es mayor que -infinito
    ingreso_minimo = float('inf')    # Todo número real es menor que +infinito
    mes_maximo = 0
    mes_minimo = 0

    # 💡 TÉCNICA: range(1, n+1) genera números del 1 al n (el fin es exclusivo)
    #    range(1, 4) → 1, 2, 3  (NO incluye el 4)
    for mes in range(1, cantidad_meses + 1):
        ingreso_mes = float(input(f"  Ingreso del mes {mes}: $"))

        # Acumular suma total
        total_ingresos += ingreso_mes   # Equivale a: total_ingresos = total_ingresos + ingreso_mes
        # 💡 TRUCO: += es el operador de asignación aumentada — más corto y legible

        # Detectar máximo con comparación manual (sin max())
        if ingreso_mes > ingreso_maximo:
            ingreso_maximo = ingreso_mes
            mes_maximo = mes

        # Detectar mínimo con comparación manual (sin min())
        if ingreso_mes < ingreso_minimo:
            ingreso_minimo = ingreso_mes
            mes_minimo = mes

    # Cálculo del promedio DESPUÉS del bucle
    # 💡 TÉCNICA: separar la recolección de datos del cálculo de resultados
    #    Primero juntás todos los datos, después calculás — más claro y seguro
    promedio = total_ingresos / cantidad_meses

    # --- Resultados ---
    print("\n📊 Resultados del análisis:")
    print(f"  Total acumulado:  ${total_ingresos:.2f}")
    print(f"  Promedio mensual: ${promedio:.2f}")
    print(f"  Ingreso más alto: ${ingreso_maximo:.2f} (Mes {mes_maximo})")
    print(f"  Ingreso más bajo: ${ingreso_minimo:.2f} (Mes {mes_minimo})")


# =============================================================================
# PROGRAMA PRINCIPAL — BUCLE DEL MENÚ
# 💡 CONCEPTO: if __name__ == "__main__" es una guarda de ejecución
#    Significa: "ejecutá este bloque SOLO si corrés este archivo directamente"
#    Si otro archivo importa este módulo, el menú NO se ejecuta automáticamente
#    Es una buena práctica profesional SIEMPRE incluirla
# =============================================================================

if __name__ == "__main__":

    # while True crea un bucle infinito — solo se sale con break o return
    # 💡 TÉCNICA: el patrón "bucle infinito + break al salir" es muy común
    #    en menús de consola y servidores que escuchan continuamente
    while True:

        # Separador visual para que el menú sea legible entre ejecuciones
        print("\n" + "=" * 40)
        print("   === Sistema de Datos Personales ===")
        print("=" * 40)
        # 💡 TRUCO: "=" * 40 repite el carácter 40 veces — útil para separadores
        print("  1 - Calcular IMC")
        print("  2 - Precio de entrada")
        print("  3 - Analizar texto")
        print("  4 - Simulador de ingresos mensuales")
        print("  5 - Salir")
        print("=" * 40)

        opcion = input("\nElegí una opción (1-5): ").strip()
        # 💡 TRUCO: .strip() elimina si el usuario accidentalmente pone un espacio

        # 💡 TÉCNICA: usar if/elif para el menú es más claro que match/case
        #    para estudiantes. match/case existe desde Python 3.10 y es similar
        #    al switch de otros lenguajes, pero if/elif es más universal.
        if opcion == "1":
            calcular_imc()
        elif opcion == "2":
            precio_entrada()
        elif opcion == "3":
            analizar_texto()
        elif opcion == "4":
            simulador_ingresos()
        elif opcion == "5":
            print("\n👋 Cerrando el sistema. ¡Hasta la próxima!")
            break  # Sale del while True
        else:
            # Manejo de opción inválida — el programa NO se rompe
            # 💡 TÉCNICA: siempre manejar el caso "ninguna de las anteriores"
            print("⚠️  Opción inválida. Ingresá un número del 1 al 5.")

# =============================================================================
# RESUMEN DE CONCEPTOS CLAVE USADOS EN ESTE TP
# -----------------------------------------------------------------------------
# float()          → convierte string a número decimal
# int()            → convierte string a número entero
# input()          → siempre devuelve string, hay que convertir
# f-string         → f"texto {variable:.2f}" — formateo moderno
# :.2f             → 2 decimales en un float
# **               → potencia (altura ** 2 = altura²)
# strip()          → limpia espacios — hábito de limpieza de datos
# .upper()         → string a mayúsculas
# .lower()         → string a minúsculas (normalización)
# .count()         → cuenta ocurrencias de substring
# [::-1]           → invierte un string (slice con paso -1)
# +=               → acumulador (suma y reasigna)
# range(1, n+1)    → genera secuencia del 1 al n
# float('inf')     → infinito, útil para inicializar max/min
# break            → sale del bucle inmediatamente
# return           → sale de la función inmediatamente
# if __name__...   → guarda de ejecución — buena práctica siempre
# =============================================================================