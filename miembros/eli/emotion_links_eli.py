# ============================================================
# ELIZYUM - ELI EMOTION LINKS
# miembros/eli/emotion_links_eli.py
#
# Adaptador emocional específico de Eli.
#
# Flujo:
#
# emociones de Eli
#       ↓
# emotions.emotion_links
#       ↓
# emotion_links_eli
#       ↓
# estado emocional de Eli
#
# Este archivo NO contiene el motor central.
# ============================================================

from emotions.emotion_links import (
    aplicar_relaciones_emocionales,
    actualizar_emociones,
    limitar
)


# ============================================================
# IDENTIDAD
# ============================================================

NOMBRE = "Eli"


# ============================================================
# APLICAR RELACIONES
# ============================================================

def aplicar_relaciones_eli(emociones):
    """
    Aplica las relaciones emocionales centrales
    al estado emocional de Eli.

    Devuelve únicamente los valores modificados.
    """

    if not isinstance(emociones, dict):
        return {}

    return aplicar_relaciones_emocionales(
        emociones
    )


# ============================================================
# ACTUALIZAR ESTADO
# ============================================================

def actualizar_estado_emocional_eli(emociones):
    """
    Actualiza el estado emocional completo de Eli
    utilizando el motor central de Elizyum.
    """

    if not isinstance(emociones, dict):
        return {}

    return actualizar_emociones(
        emociones
    )


# ============================================================
# APLICAR CAMBIOS A UN ESTADO EXISTENTE
# ============================================================

def aplicar_cambios_eli(emociones):
    """
    Aplica los cambios emocionales directamente
    sobre una copia del estado recibido.

    El diccionario original no se modifica.
    """

    if not isinstance(emociones, dict):
        return {}

    resultado = emociones.copy()

    cambios = aplicar_relaciones_eli(
        emociones
    )

    resultado.update(
        cambios
    )

    return resultado


# ============================================================
# OBTENER RESUMEN
# ============================================================

def obtener_resumen_emocional_eli(emociones):
    """
    Genera un resumen simple del estado emocional de Eli.
    """

    if not isinstance(emociones, dict):
        emociones = {}

    resultado = {}

    for nombre, valor in emociones.items():

        resultado[nombre] = limitar(
            valor
        )

    return {
        "miembro": NOMBRE,
        "emociones": resultado
    }


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - ELI EMOTION LINKS")
    print("=" * 70)

    emociones = {

        "felicidad": 80,

        "tristeza": 0,

        "enojo": 0,

        "sorpresa": 20,

        "afecto": 70,

        "curiosidad": 60,

        "diversion": 60
    }

    print()
    print("-" * 70)
    print("MIEMBRO")
    print("-" * 70)

    print(NOMBRE)

    print()
    print("-" * 70)
    print("ESTADO ORIGINAL")
    print("-" * 70)

    print(emociones)

    print()
    print("-" * 70)
    print("CAMBIOS DEL MOTOR CENTRAL")
    print("-" * 70)

    print(
        aplicar_relaciones_eli(
            emociones
        )
    )

    print()
    print("-" * 70)
    print("ESTADO ACTUALIZADO DE ELI")
    print("-" * 70)

    print(
        actualizar_estado_emocional_eli(
            emociones
        )
    )

    print()
    print("-" * 70)
    print("RESUMEN")
    print("-" * 70)

    print(
        obtener_resumen_emocional_eli(
            emociones
        )
    )