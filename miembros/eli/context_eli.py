
# ============================================================
# ELIZYUM - ELI CONTEXT
# miembros/eli/context_eli.py
#
# Adaptación del motor central de contexto para Eli.
#
# Este módulo utiliza:
#
#     mundo.context
#
# y añade únicamente la identidad/contexto específico
# necesario para Eli.
#
# ============================================================

from mundo import context


# ============================================================
# IDENTIDAD
# ============================================================

NOMBRE = "Eli"


# ============================================================
# CREAR CONTEXTO DE ELI
# ============================================================

def crear_contexto(
    datos=None
):
    """
    Crea un contexto utilizando el motor central
    y lo adapta para Eli.
    """

    contexto_eli = context.crear_contexto(
        datos
    )

    contexto_eli["miembro"] = NOMBRE

    return contexto_eli


# ============================================================
# NORMALIZAR
# ============================================================

def normalizar_contexto(
    contexto_eli=None
):
    """
    Normaliza el contexto mediante el motor central.
    """

    if not isinstance(contexto_eli, dict):
        contexto_eli = {}

    resultado = context.normalizar_contexto(
        contexto_eli
    )

    resultado["miembro"] = NOMBRE

    return resultado


# ============================================================
# OBTENER VALOR
# ============================================================

def obtener(
    contexto_eli,
    nombre,
    defecto=None
):

    contexto_eli = normalizar_contexto(
        contexto_eli
    )

    return context.obtener(
        contexto_eli,
        nombre,
        defecto
    )


# ============================================================
# OBTENER TONO
# ============================================================

def obtener_tono(
    contexto_eli
):

    return context.obtener_tono(
        normalizar_contexto(
            contexto_eli
        )
    )


# ============================================================
# OBTENER INTENCIÓN
# ============================================================

def obtener_intencion(
    contexto_eli
):

    return context.obtener_intencion(
        normalizar_contexto(
            contexto_eli
        )
    )


# ============================================================
# OBTENER SITUACIÓN
# ============================================================

def obtener_situacion(
    contexto_eli
):

    return context.obtener_situacion(
        normalizar_contexto(
            contexto_eli
        )
    )


# ============================================================
# OBTENER EVENTO RELACIONAL
# ============================================================

def obtener_evento(
    contexto_eli
):

    return context.obtener_evento(
        normalizar_contexto(
            contexto_eli
        )
    )


# ============================================================
# OBTENER AMENAZA
# ============================================================

def obtener_amenaza(
    contexto_eli
):

    return context.obtener_amenaza(
        normalizar_contexto(
            contexto_eli
        )
    )


# ============================================================
# OBTENER MARCADORES
# ============================================================

def obtener_marcadores(
    contexto_eli
):

    return context.obtener_marcadores(
        normalizar_contexto(
            contexto_eli
        )
    )


# ============================================================
# ACTUALIZAR
# ============================================================

def actualizar(
    contexto_eli,
    datos
):
    """
    Actualiza el contexto utilizando el motor central.
    """

    resultado = context.actualizar(
        contexto_eli,
        datos
    )

    resultado["miembro"] = NOMBRE

    return resultado


# ============================================================
# RESUMEN
# ============================================================

def obtener_resumen(
    contexto_eli
):

    resultado = context.obtener_resumen(
        normalizar_contexto(
            contexto_eli
        )
    )

    resultado["miembro"] = NOMBRE

    return resultado


# ============================================================
# CONTEXTO PARA ELI
# ============================================================

def construir_contexto(
    contexto_eli
):
    """
    Construye el bloque de contexto que utilizarán
    los módulos superiores de Eli.
    """

    contexto_eli = normalizar_contexto(
        contexto_eli
    )

    contexto_base = context.construir_contexto(
        contexto_eli
    )

    return f"""
========== CONTEXTO DE ELI ==========

IDENTIDAD:
{NOMBRE}

{contexto_base}

=====================================
""".strip()


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - ELI CONTEXT")
    print("=" * 70)

    contexto_eli = crear_contexto({

        "situacion": "normal",

        "tono": "afectuoso",

        "intencion": "conversacion",

        "evento_relacional": {
            "evento": "gesto_carinoso",
            "intensidad": 60
        },

        "carino": True

    })

    print()
    print("CONTEXTO DE ELI")
    print(contexto_eli)

    print()
    print("-" * 70)
    print("RESUMEN")
    print("-" * 70)

    print(
        obtener_resumen(
            contexto_eli
        )
    )

    print()
    print("-" * 70)
    print("CONTEXTO TEXTUAL")
    print("-" * 70)

    print(
        construir_contexto(
            contexto_eli
        )
    )
