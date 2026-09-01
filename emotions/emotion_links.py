# ============================================================
# ELIZYUM - EMOTION LINKS
# emotions/emotion_links.py
#
# Motor central de relaciones entre emociones.
#
# Responsabilidad:
# - modificar emociones relacionadas
# - aplicar contagio emocional
# - aplicar inhibición emocional
# - mantener valores entre 0 y 100
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


def obtener_emocion(emociones, nombre):
    """
    Obtiene una emoción de forma segura.
    """

    if not isinstance(emociones, dict):
        return 0

    return limitar(
        emociones.get(
            nombre,
            0
        )
    )


# ============================================================
# RELACIONES EMOCIONALES
# ============================================================

def aplicar_relaciones_emocionales(emociones):
    """
    Aplica relaciones internas entre emociones.

    Recibe un diccionario de emociones y devuelve
    únicamente los valores modificados.

    El estado original no se modifica directamente.

    Ejemplo:

        emociones = {
            "felicidad": 80,
            "tristeza": 0,
            ...
        }

        resultado = aplicar_relaciones_emocionales(
            emociones
        )
    """

    if not isinstance(emociones, dict):
        return {}

    resultado = {}

    # ========================================================
    # OBTENER EMOCIONES
    # ========================================================

    felicidad = obtener_emocion(
        emociones,
        "felicidad"
    )

    tristeza = obtener_emocion(
        emociones,
        "tristeza"
    )

    enojo = obtener_emocion(
        emociones,
        "enojo"
    )

    sorpresa = obtener_emocion(
        emociones,
        "sorpresa"
    )

    afecto = obtener_emocion(
        emociones,
        "afecto"
    )

    curiosidad = obtener_emocion(
        emociones,
        "curiosidad"
    )

    diversion = obtener_emocion(
        emociones,
        "diversion"
    )

    # ========================================================
    # FELICIDAD → AFECTO / DIVERSIÓN
    # ========================================================

    if felicidad >= 60:

        resultado["afecto"] = limitar(
            afecto + 2
        )

        resultado["diversion"] = limitar(
            diversion + 2
        )

    # ========================================================
    # TRISTEZA → REDUCE FELICIDAD
    # ========================================================

    if tristeza >= 40:

        resultado["felicidad"] = limitar(
            felicidad - 2
        )

    # ========================================================
    # ENOJO → REDUCE FELICIDAD
    # ========================================================

    if enojo >= 40:

        resultado["felicidad"] = limitar(
            resultado.get(
                "felicidad",
                felicidad
            ) - 3
        )

        resultado["diversion"] = limitar(
            diversion - 2
        )

    # ========================================================
    # ENOJO ALTO → REDUCE AFECTO
    # ========================================================

    if enojo >= 70:

        resultado["afecto"] = limitar(
            afecto - 2
        )

    # ========================================================
    # AFECTO → FELICIDAD
    # ========================================================

    if afecto >= 70:

        resultado["felicidad"] = limitar(
            resultado.get(
                "felicidad",
                felicidad
            ) + 2
        )

    # ========================================================
    # CURIOSIDAD → SORPRESA
    # ========================================================

    if curiosidad >= 70:

        resultado["sorpresa"] = limitar(
            sorpresa + 2
        )

    # ========================================================
    # SORPRESA → CURIOSIDAD
    # ========================================================

    if sorpresa >= 60:

        resultado["curiosidad"] = limitar(
            curiosidad + 2
        )

    # ========================================================
    # DIVERSIÓN → FELICIDAD
    # ========================================================

    if diversion >= 60:

        resultado["felicidad"] = limitar(
            resultado.get(
                "felicidad",
                felicidad
            ) + 2
        )

    # ========================================================
    # TRISTEZA ALTA → REDUCE DIVERSIÓN
    # ========================================================

    if tristeza >= 70:

        resultado["diversion"] = limitar(
            resultado.get(
                "diversion",
                diversion
            ) - 3
        )

    # ========================================================
    # NORMALIZAR
    # ========================================================

    for nombre in resultado:

        resultado[nombre] = limitar(
            resultado[nombre]
        )

    return resultado


# ============================================================
# APLICAR Y DEVOLVER ESTADO COMPLETO
# ============================================================

def actualizar_emociones(emociones):
    """
    Aplica las relaciones emocionales y devuelve
    un nuevo diccionario con el estado completo.

    El diccionario original no se modifica.
    """

    if not isinstance(emociones, dict):
        return {}

    resultado = emociones.copy()

    cambios = aplicar_relaciones_emocionales(
        emociones
    )

    resultado.update(
        cambios
    )

    return resultado


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - EMOTION LINKS")
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
    print("ESTADO ORIGINAL")
    print("-" * 70)

    print(emociones)

    resultado = actualizar_emociones(
        emociones
    )

    print()
    print("-" * 70)
    print("ESTADO ACTUALIZADO")
    print("-" * 70)

    print(resultado)

    print()
    print("-" * 70)
    print("CAMBIOS")
    print("-" * 70)

    print(
        aplicar_relaciones_emocionales(
            emociones
        )
    )