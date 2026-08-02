"""
Práctico N° 5 - Diplomatura en Python para Ciencia de Datos y ML

Este programa automatiza el proceso de Ingesta, Limpieza, Validación,
Gestión y Persistencia de datos de clientes desde un archivo de texto plano.
"""

import re
import logging
import csv
import json
import os

# =============================================================================
# CONFIGURACIÓN DE RUTAS . Creamos las carpetas y los archivos donde se trabajara
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

ARCHIVO_INGESTA = os.path.join(RAW_DIR, "ingesta_cruda.txt")
ARCHIVO_LOG = os.path.join(LOGS_DIR, "sistema.log")
ARCHIVO_CSV = os.path.join(PROCESSED_DIR, "clientes_limpios.csv")
ARCHIVO_JSON = os.path.join(PROCESSED_DIR, "clientes_limpios.json")

# =============================================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGGING
# =============================================================================
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(ARCHIVO_LOG, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# VARIABLES GLOBALES
# =============================================================================
clientes_limpios = []
emails_registrados = set()
estadisticas = {
    "total_lineas": 0,
    "registros_validos": 0,
    "registros_descartados": 0,
    "emails_gmail": 0
}

# =============================================================================
# PARTE 1: INGESTA ROBUSTA
# =============================================================================
def cargar_archivo(ruta_archivo):
    """
    Lee el archivo fuente con manejo de errores de codificación.
    Retorna lista de líneas o None si hay error.
    """
    logger.info(f"Iniciando carga del archivo: {ruta_archivo}")
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
            logger.info(f"Archivo cargado exitosamente. {len(lineas)} líneas leídas.")
            return lineas
            
    except FileNotFoundError:
        logger.error(f"ERROR: El archivo '{ruta_archivo}' no existe.")
        return None
            
    except Exception as e:
        logger.error(f"Error inesperado al leer el archivo: {e}")
        return None

# =============================================================================
# PARTE 2: MOTOR DE LIMPIEZA - REGEX
# =============================================================================
def es_linea_sistema(linea):
    """
    Detecta líneas de sistema que deben ignorarse:
    - Encabezados (### INICIO..., ### FIN...)
    - Separadores (----)
    - Errores del sistema (##### Error...)
    - Logs del sistema (### LINEA DE SISTEMA...)
    """
    linea_limpia = linea.strip()
    
    # Líneas vacías
    if linea_limpia == "":
        return True
    
    # Encabezados y pies de archivo
    if linea_limpia.startswith('###') or linea_limpia.endswith('###'):
        return True
    
    # Separadores
    if re.match(r'^-{5,}$', linea_limpia):
        return True
    
    # Errores del sistema
    if 'Error' in linea_limpia and '#####' in linea_limpia:
        return True
    
    if linea_limpia.startswith('Registro Corrupto'):
        return True
    
    return False

def extraer_nombre(linea):
    """
    Extrae el nombre del cliente limpiando prefijos y formateando en Title Case.
    Maneja múltiples formatos de entrada y separadores.
    """
    # Remover prefijos comunes
    prefijos = [
        r'^ID:\s*\d+\s*-\s*',
        r'^Cliente Nuevo:\s*',
        r'^Cliente:\s*',
        r'^Contacto:\s*',
        r'^Socio:\s*',
        r'^Cli:\s*',
        r'^Dato Incompleto\s*-\s*Cliente:\s*',
    ]
    
    linea_limpia = linea.strip()
    for prefijo in prefijos:
        linea_limpia = re.sub(prefijo, '', linea_limpia, flags=re.IGNORECASE)
    
    # Remover comillas del nombre
    linea_limpia = linea_limpia.replace('"', '')
    
    # Separar por cualquier separador seguido de teléfono, email o número
    # Patrones que indican fin del nombre
    patron_fin_nombre = r'\s*[-|;/,]\s*(?:Tel|Cel|tel|Mail|\d{3}[\s.-]|\(\d{3}\)|\d{10})|@|\d{3}\s*[-;|/,]'
    partes = re.split(patron_fin_nombre, linea_limpia, maxsplit=1, flags=re.IGNORECASE)
    
    if partes and partes[0].strip():
        nombre = partes[0].strip()
        # Limpiar caracteres especiales y guiones bajos
        nombre = nombre.replace('_', ' ')
        nombre = re.sub(r'^[^a-záéíóúñA-ZÁÉÍÓÚÑ]+|[^a-záéíóúñA-ZÁÉÍÓÚÑ]+$', '', nombre)
        # Limpiar "sin telefono" u otras frases residuales
        nombre = re.sub(r'\s+sin\s+telefono.*$', '', nombre, flags=re.IGNORECASE)
        if nombre and len(nombre) > 1:
            return nombre.title()
    
    return None

def extraer_telefono(linea):
    """
    Extrae y normaliza el teléfono a exactamente 10 dígitos.
    Usa lookbehind negativo (?<![a-zA-Z]) para ignorar dígitos que
    forman parte de palabras o usernames (ej: perez88@mail.com).
    """
    # Busca bloques numéricos que NO estén precedidos por una letra
    bloques = re.findall(r'(?<![a-zA-Z])\d[\d\s\-().]*\d', linea)

    for bloque in bloques:
        digitos = re.sub(r'\D', '', bloque)
        if len(digitos) == 10:
            return digitos
        if len(digitos) > 10:
            return digitos[-10:]  # por si hay ID numérico al inicio

    return None

def extraer_email(linea):
    """
    Extrae y valida el email con formato usuario@dominio.extension.
    Convierte a minúsculas para normalización.
    """
    # Patrón para email válido (debe tener extensión de al menos 2 caracteres)
    patron_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    match = re.search(patron_email, linea)
    
    if match:
        return match.group().lower()
    
    return None

# =============================================================================
# PARTE 3 Y 4: PROCESAMIENTO Y VALIDACIÓN
# =============================================================================
def procesar_linea(linea, numero_linea):
    """
    Procesa una línea individual aplicando las reglas de limpieza y validación.
    
    Criterios:
    - Email es obligatorio y debe ser único
    - Teléfono faltante se marca como 'Desconocido'
    - Se conserva solo el primer registro de emails duplicados
    """
    global emails_registrados, estadisticas
    
    # Ignorar líneas de sistema
    if es_linea_sistema(linea):
        logger.info(f"Línea {numero_linea} ignorada: línea de sistema o vacía")
        estadisticas["registros_descartados"] += 1
        return None
    
    # Extraer datos
    nombre = extraer_nombre(linea)
    telefono = extraer_telefono(linea)
    email = extraer_email(linea)
    
    # Validación: debe tener nombre
    if not nombre:
        logger.warning(f"Línea {numero_linea} descartada: no se pudo extraer nombre - {linea.strip()[:50]}")
        estadisticas["registros_descartados"] += 1
        return None
    
    # Validación: debe tener email válido
    if not email:
        logger.warning(f"Línea {numero_linea} descartada: email inválido o faltante - {nombre}")
        estadisticas["registros_descartados"] += 1
        return None
    
    # Validación: email no duplicado
    if email in emails_registrados:
        logger.warning(f"Línea {numero_linea} descartada: email duplicado ({email}) - {nombre}")
        estadisticas["registros_descartados"] += 1
        return None
    
    # Registrar email
    emails_registrados.add(email)
    
    # Teléfono faltante se marca como Desconocido
    if not telefono:
        telefono = "Desconocido"
        logger.info(f"Línea {numero_linea}: teléfono marcado como Desconocido para {nombre}")
    
    # Contar emails de Gmail
    if email.endswith('@gmail.com'):
        estadisticas["emails_gmail"] += 1
    
    estadisticas["registros_validos"] += 1
    
    return {
        "nombre": nombre,
        "telefono": telefono,
        "email": email
    }

def cargar_y_limpiar():
    """Función principal que carga el archivo y procesa todas las líneas."""
    global clientes_limpios, emails_registrados, estadisticas
    
    # Reiniciar datos
    clientes_limpios = []
    emails_registrados = set()
    estadisticas = {
        "total_lineas": 0,
        "registros_validos": 0,
        "registros_descartados": 0,
        "emails_gmail": 0
    }
    
    lineas = cargar_archivo(ARCHIVO_INGESTA)
    
    if lineas is None:
        print("\n❌ No se pudo cargar el archivo. Revisa el log para más detalles.")
        return False
    
    estadisticas["total_lineas"] = len(lineas)
    
    for i, linea in enumerate(lineas, start=1):
        cliente = procesar_linea(linea, i)
        if cliente:
            clientes_limpios.append(cliente)
    
    print(f"\n✅ Proceso completado:")
    print(f"   - Líneas procesadas: {estadisticas['total_lineas']}")
    print(f"   - Registros válidos: {estadisticas['registros_validos']}")
    print(f"   - Registros descartados: {estadisticas['registros_descartados']}")
    
    logger.info(f"Carga completada: {estadisticas['registros_validos']} válidos, "
                f"{estadisticas['registros_descartados']} descartados")
    
    return True

# =============================================================================
# FUNCIONES DEL MENÚ
# =============================================================================
def buscar_cliente():
    """Busca un cliente por nombre (insensible a mayúsculas/minúsculas)."""
    if not clientes_limpios:
        print("\n⚠️  No hay clientes cargados. Primero usa la opción 1.")
        return
    
    nombre_buscar = input("\nIngresa el nombre a buscar: ").strip().lower()
    
    encontrados = [c for c in clientes_limpios if nombre_buscar in c["nombre"].lower()]
    
    if encontrados:
        print(f"\n🔍 Se encontraron {len(encontrados)} resultado(s):\n")
        for c in encontrados:
            print(f"   Nombre: {c['nombre']}")
            print(f"   Teléfono: {c['telefono']}")
            print(f"   Email: {c['email']}")
            print("   " + "-" * 30)
    else:
        print(f"\n❌ No se encontró ningún cliente con '{nombre_buscar}'")

def mostrar_estadisticas():
    """Muestra estadísticas del proceso de carga."""
    if estadisticas["total_lineas"] == 0:
        print("\n⚠️  No hay datos cargados. Primero usa la opción 1.")
        return
    
    total = estadisticas["total_lineas"]
    validos = estadisticas["registros_validos"]
    descartados = estadisticas["registros_descartados"]
    gmail = estadisticas["emails_gmail"]
    
    porcentaje_gmail = (gmail / validos * 100) if validos > 0 else 0
    
    print("\n📊 ESTADÍSTICAS DEL DATASET:")
    print("=" * 40)
    print(f"   Total líneas leídas:     {total}")
    print(f"   Registros válidos:       {validos}")
    print(f"   Registros descartados:   {descartados}")
    print(f"   Emails de Gmail:         {gmail} ({porcentaje_gmail:.1f}%)")
    print("=" * 40)

def eliminar_cliente():
    """Elimina un cliente de la lista por email."""
    global clientes_limpios, emails_registrados
    
    if not clientes_limpios:
        print("\n⚠️  No hay clientes cargados.")
        return
    
    email_eliminar = input("\nIngresa el email del cliente a eliminar: ").strip().lower()
    
    for i, cliente in enumerate(clientes_limpios):
        if cliente["email"] == email_eliminar:
            eliminado = clientes_limpios.pop(i)
            emails_registrados.discard(email_eliminar)
            estadisticas["registros_validos"] -= 1
            if email_eliminar.endswith('@gmail.com'):
                estadisticas["emails_gmail"] -= 1
            print(f"\n✅ Cliente eliminado: {eliminado['nombre']}")
            logger.info(f"Cliente eliminado: {eliminado['nombre']} ({email_eliminar})")
            return
    
    print(f"\n❌ No se encontró cliente con email '{email_eliminar}'")

def mostrar_clientes():
    """Muestra todos los clientes cargados."""
    if not clientes_limpios:
        print("\n⚠️  No hay clientes cargados.")
        return
    
    print(f"\n📋 LISTADO DE CLIENTES ({len(clientes_limpios)} registros):")
    print("=" * 70)
    for i, c in enumerate(clientes_limpios, start=1):
        print(f"{i:2}. {c['nombre']:<25} | {c['telefono']:<12} | {c['email']}")
    print("=" * 70)

# =============================================================================
# PARTE 5: PERSISTENCIA
# =============================================================================
def guardar_csv():
    """Exporta los datos a formato CSV (separador coma, UTF-8)."""
    try:
        with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
            campos = ["nombre", "telefono", "email"]
            writer = csv.DictWriter(archivo, fieldnames=campos)
            writer.writeheader()
            writer.writerows(clientes_limpios)
        logger.info(f"Datos exportados a CSV: {ARCHIVO_CSV}")
        return True
    except Exception as e:
        logger.error(f"Error al guardar CSV: {e}")
        return False

def guardar_json():
    """Exporta los datos a formato JSON como respaldo estructurado."""
    try:
        with open(ARCHIVO_JSON, 'w', encoding='utf-8') as archivo:
            json.dump(clientes_limpios, archivo, indent=2, ensure_ascii=False)
        logger.info(f"Datos exportados a JSON: {ARCHIVO_JSON}")
        return True
    except Exception as e:
        logger.error(f"Error al guardar JSON: {e}")
        return False

def guardar_y_salir():
    """Guarda los datos en ambos formatos y termina el programa."""
    if not clientes_limpios:
        print("\n⚠️  No hay datos para guardar.")
        confirmar = input("¿Deseas salir de todos modos? (s/n): ").strip().lower()
        if confirmar == 's':
            logger.info("Programa terminado sin guardar datos")
            return True
        return False
    
    print("\n💾 Guardando datos...")
    
    exito_csv = guardar_csv()
    exito_json = guardar_json()
    
    if exito_csv and exito_json:
        print(f"   ✅ CSV guardado en: {ARCHIVO_CSV}")
        print(f"   ✅ JSON guardado en: {ARCHIVO_JSON}")
        print("\n¡Hasta luego! 👋")
        logger.info("Programa terminado exitosamente")
        return True
    else:
        print("   ⚠️  Hubo errores al guardar. Revisa el log.")
        return False

# =============================================================================
# MENÚ PRINCIPAL
# =============================================================================
def mostrar_menu():
    """Muestra el menú de opciones."""
    print("\n" + "=" * 50)
    print("   SISTEMA DE GESTIÓN DE CLIENTES")
    print("=" * 50)
    print("   1. Cargar y Limpiar datos")
    print("   2. Buscar cliente")
    print("   3. Ver estadísticas")
    print("   4. Eliminar cliente")
    print("   5. Mostrar todos los clientes")
    print("   6. Guardar y Salir")
    print("=" * 50)

def main():
    """Función principal con el bucle del menú interactivo."""
    logger.info("=" * 50)
    logger.info("INICIO DEL PROGRAMA")
    logger.info("=" * 50)
    
    print("\n🚀 Bienvenido al Sistema de Gestión de Clientes")
    
    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción (1-6): ").strip()
        
        if opcion == "1":
            cargar_y_limpiar()
        elif opcion == "2":
            buscar_cliente()
        elif opcion == "3":
            mostrar_estadisticas()
        elif opcion == "4":
            eliminar_cliente()
        elif opcion == "5":
            mostrar_clientes()
        elif opcion == "6":
            if guardar_y_salir():
                break
        else:
            print("\n❌ Opción no válida. Por favor ingresa un número del 1 al 6.")

if __name__ == "__main__":
    main()
