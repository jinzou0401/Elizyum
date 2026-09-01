# ============================================================
# ELIZYUM — EMPAQUETADOR DE VERSIONES
# ============================================================
#
# Archivo:
#     empaquetar_version.py
#
# Ubicación:
#     Raíz del proyecto Elizyum
#
# Uso:
#     python empaquetar_version.py 0.5
#
# Resultado:
#     versiones/
#     └── 0.5/
#         └── Elizyum_0.5.zip
#
# Función:
#     Crear una copia ZIP limpia de una versión estable
#     del proyecto, excluyendo datos personales y estados
#     dinámicos del sistema.
#
# ============================================================

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import sys
from datetime import datetime


# ============================================================
# CONFIGURACIÓN
# ============================================================

NOMBRE_PROYECTO = "Elizyum"


# ============================================================
# DIRECTORIOS EXCLUIDOS
# ============================================================
#
# Estos directorios NO serán incluidos en el ZIP.
#
# data/
#     Contiene conversaciones, memoria y estados dinámicos.
#
# versiones/
#     Contiene los ZIP de versiones anteriores.
#
# __pycache__ / entornos virtuales / configuraciones locales
#     No forman parte del código necesario para distribuir
#     una versión limpia del proyecto.
# ============================================================

EXCLUIR_DIRECTORIOS = {
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "venv",
    ".venv",
    "env",
    ".env",
    "versiones",
    "data",
}


# ============================================================
# EXTENSIONES EXCLUIDAS
# ============================================================

EXCLUIR_EXTENSIONES = {
    ".pyc",
    ".pyo",
}


# ============================================================
# ARCHIVOS EXCLUIDOS
# ============================================================

EXCLUIR_ARCHIVOS = {
    ".DS_Store",
    "Thumbs.db",
}


# ============================================================
# RAÍZ DEL PROYECTO
# ============================================================

RAIZ_PROYECTO = Path(__file__).resolve().parent


# ============================================================
# OBTENER VERSIÓN
# ============================================================

def obtener_version():

    if len(sys.argv) != 2:

        print()
        print("=" * 60)
        print("ELIZYUM — EMPAQUETADOR DE VERSIONES")
        print("=" * 60)
        print()
        print("Uso:")
        print("    python empaquetar_version.py 0.5")
        print()

        sys.exit(1)

    version = sys.argv[1].strip()

    if not version:

        print("ERROR: Debes indicar una versión.")
        sys.exit(1)

    return version


# ============================================================
# VALIDAR PROYECTO
# ============================================================

def validar_proyecto():

    archivos_importantes = [
        "main.py",
        "config.py",
        "requirements.txt",
    ]

    faltantes = []

    for archivo in archivos_importantes:

        ruta = RAIZ_PROYECTO / archivo

        if not ruta.exists():
            faltantes.append(archivo)

    if faltantes:

        print()
        print("ADVERTENCIA")
        print("-" * 60)
        print("No se encontraron algunos archivos esperados:")
        print()

        for archivo in faltantes:
            print(f"  - {archivo}")

        print()
        print("El empaquetado continuará.")
        print()


# ============================================================
# COMPROBAR EXCLUSIONES
# ============================================================

def debe_excluir(ruta: Path):

    # --------------------------------------------------------
    # Excluir directorios
    # --------------------------------------------------------

    for parte in ruta.parts:

        if parte in EXCLUIR_DIRECTORIOS:
            return True

    # --------------------------------------------------------
    # Excluir extensiones
    # --------------------------------------------------------

    if ruta.suffix.lower() in EXCLUIR_EXTENSIONES:
        return True

    # --------------------------------------------------------
    # Excluir archivos específicos
    # --------------------------------------------------------

    if ruta.name in EXCLUIR_ARCHIVOS:
        return True

    return False


# ============================================================
# RECOPILAR ARCHIVOS
# ============================================================

def recopilar_archivos():

    archivos = []

    for ruta in RAIZ_PROYECTO.rglob("*"):

        if not ruta.is_file():
            continue

        if debe_excluir(ruta):
            continue

        archivos.append(ruta)

    return sorted(archivos)


# ============================================================
# CREAR DIRECTORIO DE VERSIÓN
# ============================================================

def preparar_directorio_version(version):

    directorio_version = (
        RAIZ_PROYECTO
        / "versiones"
        / version
    )

    directorio_version.mkdir(
        parents=True,
        exist_ok=True
    )

    return directorio_version


# ============================================================
# CREAR ZIP
# ============================================================

def crear_zip(version, archivos):

    directorio_version = preparar_directorio_version(version)

    nombre_zip = f"{NOMBRE_PROYECTO}_{version}.zip"

    ruta_zip = directorio_version / nombre_zip

    # --------------------------------------------------------
    # No sobrescribir una versión existente
    # --------------------------------------------------------

    if ruta_zip.exists():

        print()
        print("=" * 60)
        print("EL ZIP YA EXISTE")
        print("=" * 60)
        print()
        print("Archivo:")
        print(f"  {ruta_zip}")
        print()
        print("Por seguridad, el archivo NO será sobrescrito.")
        print()
        print("Si realmente deseas crear una nueva copia,")
        print("elimina manualmente el ZIP anterior.")
        print()

        return None

    # --------------------------------------------------------
    # Crear ZIP
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print(f"CREANDO ELIZYUM {version}")
    print("=" * 60)
    print()

    with ZipFile(
        ruta_zip,
        "w",
        compression=ZIP_DEFLATED
    ) as zip_file:

        for archivo in archivos:

            ruta_relativa = archivo.relative_to(
                RAIZ_PROYECTO
            )

            zip_file.write(
                archivo,
                arcname=str(ruta_relativa)
            )

            print(f"  + {ruta_relativa}")

    return ruta_zip


# ============================================================
# MOSTRAR RESUMEN
# ============================================================

def mostrar_resumen(version, archivos, ruta_zip):

    if ruta_zip is None:
        return

    tamaño_mb = ruta_zip.stat().st_size / (1024 * 1024)

    print()
    print("=" * 60)
    print("EMPAQUETADO COMPLETADO")
    print("=" * 60)
    print()

    print(f"Proyecto : {NOMBRE_PROYECTO}")
    print(f"Versión  : {version}")
    print(f"Archivos : {len(archivos)}")
    print(f"Tamaño   : {tamaño_mb:.2f} MB")
    print()

    print("ZIP:")
    print(f"  {ruta_zip}")
    print()

    print(
        "Fecha de creación:",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    print()
    print("EXCLUSIONES IMPORTANTES:")
    print("  - data/")
    print("  - versiones/")
    print("  - __pycache__/")
    print("  - archivos .pyc")
    print()

    print("ESTADO: SNAPSHOT DE VERSIÓN")
    print()
    print("El ZIP ha sido creado y no será sobrescrito")
    print("automáticamente en futuras ejecuciones.")
    print()


# ============================================================
# MAIN
# ============================================================

def main():

    version = obtener_version()

    print()
    print("=" * 60)
    print("ELIZYUM — EMPAQUETADOR DE VERSIONES")
    print("=" * 60)
    print()
    print(f"Versión solicitada: {version}")
    print()

    validar_proyecto()

    archivos = recopilar_archivos()

    if not archivos:

        print()
        print("ERROR: No se encontraron archivos para empaquetar.")
        print()

        sys.exit(1)

    ruta_zip = crear_zip(
        version,
        archivos
    )

    mostrar_resumen(
        version,
        archivos,
        ruta_zip
    )


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()
