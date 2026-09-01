
# ============================================================
# ELIZYUM - ELI RELATIONSHIP
# miembros/eli/relationship_eli.py
#
# Adaptación del motor relacional central para Eli.
#
# Este módulo NO duplica el motor de relaciones.
# Utiliza:
#
#     emotions.relationships
#
# y añade únicamente las reglas específicas de Eli.
#
# Flujo:
#
# relationships.py
#        ↓
# relationship_eli.py
#        ↓
# mood.py
#        ↓
# mood_eli.py
# ============================================================

from emotions import relationships


# ============================================================
# VALORES BASE DE ELI
# ============================================================

RELACION_BASE_ELI = {
    "confianza": 75,
    "cercania": 65,
    "comprension": 60,
    "vinculo": 70
}


# ============================================================
# CREAR RELACIÓN DE ELI
# ============================================================

def crear_relacion():

    return relationships.crear_relacion(
        confianza=RELACION_BASE_ELI["confianza"],
        cercania=RELACION_BASE_ELI["cercania"],
        comprension=RELACION_BASE_ELI["comprension"],
        vinculo=RELACION_BASE_ELI["vinculo"]
    )


# ============================================================
# NORMALIZAR
# ============================================================

def normalizar_relacion(relacion=None):

    if not isinstance(relacion, dict):
        relacion = crear_relacion()

    resultado = relationships.normalizar_relacion(
        relacion
    )

    return resultado


# ============================================================
# OBTENER VALOR
# ============================================================

def obtener_valor(
    relacion,
    nombre,
    defecto=50
):

    relacion = normalizar_relacion(
        relacion
    )

    return relationships.obtener_valor(
        relacion,
        nombre,
        defecto
    )


# ============================================================
# CAMBIAR VALOR
# ============================================================

def cambiar_valor(
    relacion,
    nombre,
    cantidad
):

    relacion = normalizar_relacion(
        relacion
    )

    return relationships.cambiar_valor(
        relacion,
        nombre,
        cantidad
    )


# ============================================================
# ESTABLECER VALOR
# ============================================================

def establecer_valor(
    relacion,
    nombre,
    valor
):

    relacion = normalizar_relacion(
        relacion
    )

    return relationships.establecer_valor(
        relacion,
        nombre,
        valor
    )


# ============================================================
# EVENTOS ESPECÍFICOS DE ELI
# ============================================================

def aplicar_evento(
    relacion,
    evento
):
    """
    Aplica primero el motor relacional central.

    Después permite añadir reglas específicas de Eli
    sin modificar relationships.py.
    """

    relacion = normalizar_relacion(
        relacion
    )

    resultado = relationships.aplicar_evento(
        relacion,
        evento
    )

    return resultado


# ============================================================
# ESTADO RELACIONAL DE ELI
# ============================================================

def determinar_estado(
    relacion
):

    relacion = normalizar_relacion(
        relacion
    )

    return relationships.determinar_estado(
        relacion
    )


# ============================================================
# RESUMEN RELACIONAL DE ELI
# ============================================================

def obtener_resumen(
    relacion
):

    relacion = normalizar_relacion(
        relacion
    )

    return relationships.obtener_resumen(
        relacion
    )


# ============================================================
# CONTEXTO PARA ELI
# ============================================================

def construir_contexto_relacional(
    relacion
):
    """
    Construye un contexto textual que podrá utilizar
    mood_eli.py o personality_eli.py.

    Los valores internos se mantienen separados del
    comportamiento del motor central.
    """

    relacion = normalizar_relacion(
        relacion
    )

    resumen = obtener_resumen(
        relacion
    )

    return f"""
========== RELACIÓN DE ELI ==========

ESTADO RELACIONAL:
{resumen["estado"]}

CONFIANZA:
{resumen["confianza"]}/100

CERCANÍA:
{resumen["cercania"]}/100

COMPRENSIÓN:
{resumen["comprension"]}/100

VÍNCULO:
{resumen["vinculo"]}/100

=====================================
""".strip()


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - ELI RELATIONSHIP")
    print("=" * 70)

    relacion = crear_relacion()

    print()
    print("RELACIÓN INICIAL")
    print(
        obtener_resumen(
            relacion
        )
    )

    print()
    print("-" * 70)
    print("EVENTO: gesto_carinoso")
    print("-" * 70)

    relacion = aplicar_evento(
        relacion,
        {
            "evento": "gesto_carinoso",
            "intensidad": 60
        }
    )

    print(
        obtener_resumen(
            relacion
        )
    )

    print()
    print("-" * 70)
    print("EVENTO: mentira")
    print("-" * 70)

    relacion = aplicar_evento(
        relacion,
        {
            "evento": "mentira",
            "intensidad": 80
        }
    )

    print(
        obtener_resumen(
            relacion
        )
    )

    print()
    print("-" * 70)
    print("CONTEXTO PARA ELI")
    print("-" * 70)

    print(
        construir_contexto_relacional(
            relacion
        )
    )
# ============================================================
# INSTANCIA PERSISTENTE DE ELI
# ============================================================

from emotions.relationships import GestorRelacion

eli_relationships = GestorRelacion(
    "eli",
    base=RELACION_BASE_ELI
)