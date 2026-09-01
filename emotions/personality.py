# ============================================================
# ELIZYUM - PERSONALITY ENGINE
# emotions/personality.py
#
# Motor central de personalidad de Elizyum.
#
# Responsabilidad:
# - recibir estado emocional
# - recibir faceta
# - recibir contexto
# - determinar rasgos de comportamiento
# - construir instrucciones generales para un LLM
#
# Este módulo NO pertenece a ningún miembro concreto.
# ============================================================


# ============================================================
# UTILIDADES
# ============================================================

def limitar(valor, minimo=0, maximo=100):
    """
    Limita un valor al rango indicado.
    """

    try:
        valor = int(float(valor))
    except (TypeError, ValueError):
        valor = minimo

    return max(
        minimo,
        min(maximo, valor)
    )


def obtener_valor(datos, nombre, defecto=0):
    """
    Obtiene un valor numérico de forma segura.
    """

    if not isinstance(datos, dict):
        return defecto

    return limitar(
        datos.get(
            nombre,
            defecto
        )
    )


# ============================================================
# RASGOS BASE
# ============================================================

RASGOS_BASE = {
    "calidez": 50,
    "espontaneidad": 50,
    "humor": 50,
    "curiosidad": 50,
    "seriedad": 30,
    "apertura": 50,
    "cautela": 30,
    "afectividad": 50
}


# ============================================================
# OBTENER RASGOS BASE
# ============================================================

def obtener_rasgos_base():
    """
    Devuelve una copia de los rasgos base.
    """

    return RASGOS_BASE.copy()


# ============================================================
# CALCULAR RASGOS
# ============================================================

def calcular_rasgos(
    emociones=None,
    faceta=None,
    intensidad_faceta=20,
    contexto=None
):
    """
    Calcula los rasgos de comportamiento a partir
    del estado emocional y contextual.

    No modifica los datos originales.
    """

    if not isinstance(emociones, dict):
        emociones = {}

    if not isinstance(contexto, dict):
        contexto = {}

    intensidad_faceta = limitar(
        intensidad_faceta,
        0,
        100
    )

    rasgos = RASGOS_BASE.copy()

    # ========================================================
    # EMOCIONES
    # ========================================================

    felicidad = obtener_valor(
        emociones,
        "felicidad"
    )

    tristeza = obtener_valor(
        emociones,
        "tristeza"
    )

    enojo = obtener_valor(
        emociones,
        "enojo"
    )

    afecto = obtener_valor(
        emociones,
        "afecto"
    )

    curiosidad = obtener_valor(
        emociones,
        "curiosidad"
    )

    diversion = obtener_valor(
        emociones,
        "diversion"
    )

    sorpresa = obtener_valor(
        emociones,
        "sorpresa"
    )

    # ========================================================
    # INFLUENCIA EMOCIONAL
    # ========================================================

    rasgos["calidez"] += afecto // 5
    rasgos["calidez"] += felicidad // 10

    rasgos["espontaneidad"] += (
        diversion // 5
    )

    rasgos["humor"] += (
        diversion // 4
    )

    rasgos["curiosidad"] += (
        curiosidad // 5
    )

    rasgos["afectividad"] += (
        afecto // 4
    )

    rasgos["seriedad"] += (
        tristeza // 5
    )

    rasgos["seriedad"] += (
        enojo // 4
    )

    rasgos["cautela"] += (
        tristeza // 6
    )

    rasgos["cautela"] += (
        enojo // 6
    )

    rasgos["apertura"] += (
        afecto // 8
    )

    rasgos["apertura"] += (
        felicidad // 10
    )

    # ========================================================
    # SORPRESA
    # ========================================================

    if sorpresa >= 60:

        rasgos["espontaneidad"] += 5
        rasgos["curiosidad"] += 5

    # ========================================================
    # FACETAS
    # ========================================================

    if faceta == "cercana":

        rasgos["calidez"] += 15
        rasgos["afectividad"] += 15
        rasgos["apertura"] += 10

    elif faceta == "atenta":

        rasgos["curiosidad"] += 10
        rasgos["apertura"] += 5

    elif faceta == "juguetona":

        rasgos["humor"] += 15
        rasgos["espontaneidad"] += 15

    elif faceta == "coqueta":

        rasgos["calidez"] += 10
        rasgos["afectividad"] += 10
        rasgos["espontaneidad"] += 5

    elif faceta == "cortante":

        rasgos["seriedad"] += 20
        rasgos["humor"] -= 20
        rasgos["espontaneidad"] -= 10
        rasgos["apertura"] -= 10

    elif faceta == "cauta":

        rasgos["cautela"] += 20
        rasgos["seriedad"] += 10
        rasgos["espontaneidad"] -= 10

    elif faceta == "celosa":

        rasgos["cautela"] += 15
        rasgos["afectividad"] += 5
        rasgos["seriedad"] += 5

    elif faceta == "herida":

        rasgos["seriedad"] += 20
        rasgos["cautela"] += 20
        rasgos["apertura"] -= 15
        rasgos["humor"] -= 15

    elif faceta == "reconciliadora":

        rasgos["calidez"] += 15
        rasgos["apertura"] += 15
        rasgos["afectividad"] += 10
        rasgos["cautela"] += 5

    # ========================================================
    # INTENSIDAD DE FACETA
    # ========================================================

    factor = intensidad_faceta / 100

    if factor > 0:

        if faceta in {
            "cercana",
            "reconciliadora"
        }:

            rasgos["calidez"] += int(
                10 * factor
            )

        if faceta in {
            "juguetona",
            "coqueta"
        }:

            rasgos["espontaneidad"] += int(
                10 * factor
            )

        if faceta in {
            "cortante",
            "cauta",
            "herida"
        }:

            rasgos["seriedad"] += int(
                10 * factor
            )

            rasgos["cautela"] += int(
                10 * factor
            )

    # ========================================================
    # CONTEXTO
    # ========================================================

    tono = contexto.get(
        "tono",
        ""
    )

    if tono in {
        "afectuoso",
        "cariñoso",
        "carinoso"
    }:

        rasgos["calidez"] += 5
        rasgos["afectividad"] += 5

    elif tono in {
        "jugueton",
        "juguetón"
    }:

        rasgos["humor"] += 5
        rasgos["espontaneidad"] += 5

    elif tono in {
        "serio",
        "seria"
    }:

        rasgos["seriedad"] += 10

    # ========================================================
    # NORMALIZAR
    # ========================================================

    for nombre in rasgos:

        rasgos[nombre] = limitar(
            rasgos[nombre]
        )

    return rasgos


# ============================================================
# OBTENER ESTILO DOMINANTE
# ============================================================

def obtener_estilo(rasgos):
    """
    Determina los rasgos predominantes.
    """

    if not isinstance(rasgos, dict):
        rasgos = {}

    categorias = {
        "calida": rasgos.get("calidez", 0),
        "espontanea": rasgos.get("espontaneidad", 0),
        "humoristica": rasgos.get("humor", 0),
        "curiosa": rasgos.get("curiosidad", 0),
        "seria": rasgos.get("seriedad", 0),
        "abierta": rasgos.get("apertura", 0),
        "cauta": rasgos.get("cautela", 0),
        "afectiva": rasgos.get("afectividad", 0)
    }

    ordenados = sorted(
        categorias.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        nombre
        for nombre, valor in ordenados
        if valor >= 50
    ]


# ============================================================
# CONSTRUIR CONTEXTO DE PERSONALIDAD
# ============================================================

def construir_contexto_personalidad(
    rasgos,
    faceta=None,
    matices=None
):
    """
    Construye un bloque de contexto para un LLM.

    No contiene identidad específica de ningún miembro.
    """

    if not isinstance(rasgos, dict):
        rasgos = {}

    if not isinstance(matices, list):
        matices = []

    estilo = obtener_estilo(
        rasgos
    )

    if estilo:

        texto_estilo = "\n".join(
            f"- {item}"
            for item in estilo
        )

    else:

        texto_estilo = (
            "- comportamiento equilibrado"
        )

    if matices:

        texto_matices = "\n".join(
            f"- {matiz}"
            for matiz in matices
        )

    else:

        texto_matices = (
            "- sin matices secundarios relevantes"
        )

    return f"""
========== CONTEXTO DE PERSONALIDAD ==========

FACETA:
{faceta or "normal"}

RASGOS:

- Calidez: {limitar(rasgos.get("calidez", 50))}/100
- Espontaneidad: {limitar(rasgos.get("espontaneidad", 50))}/100
- Humor: {limitar(rasgos.get("humor", 50))}/100
- Curiosidad: {limitar(rasgos.get("curiosidad", 50))}/100
- Seriedad: {limitar(rasgos.get("seriedad", 30))}/100
- Apertura: {limitar(rasgos.get("apertura", 50))}/100
- Cautela: {limitar(rasgos.get("cautela", 30))}/100
- Afectividad: {limitar(rasgos.get("afectividad", 50))}/100


ESTILO DOMINANTE:

{texto_estilo}


MATICES:

{texto_matices}


REGLAS:

- Adaptar el comportamiento al contexto.
- Mantener coherencia entre emociones y personalidad.
- Las emociones no obligan a una respuesta concreta.
- El contexto conversacional puede modificar el estilo.
- No inventar hechos.
- No mencionar valores internos.
- No mencionar nombres técnicos de facetas.
- Mantener un comportamiento natural.
- Evitar exageraciones emocionales.
- No convertir estas reglas en una lista dentro de la respuesta.

================================================
""".strip()


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - PERSONALITY ENGINE")
    print("=" * 70)

    emociones = {

        "felicidad": 70,
        "tristeza": 0,
        "enojo": 0,
        "sorpresa": 20,
        "afecto": 80,
        "curiosidad": 70,
        "diversion": 60
    }

    rasgos = calcular_rasgos(
        emociones=emociones,
        faceta="cercana",
        intensidad_faceta=40,
        contexto={
            "tono": "afectuoso"
        }
    )

    print()
    print("-" * 70)
    print("RASGOS")
    print("-" * 70)

    print(rasgos)

    print()
    print("-" * 70)
    print("ESTILO")
    print("-" * 70)

    print(
        obtener_estilo(
            rasgos
        )
    )

    print()
    print("-" * 70)
    print("CONTEXTO PARA LLM")
    print("-" * 70)

    print(
        construir_contexto_personalidad(
            rasgos,
            faceta="cercana",
            matices=[
                "afectuosa",
                "confiada"
            ]
        )
    )