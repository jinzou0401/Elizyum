# ============================================================
# ELIZYUM - AURORA EMOTION LINKS
# miembros/aurora/emotion_links_aurora.py
#
# Conexiones entre las emociones de Aurora.
#
# Este módulo define cómo determinadas emociones pueden
# influirse entre sí.
#
# Aurora está orientada principalmente hacia:
#
# - creatividad
# - inspiración
# - curiosidad
# - espontaneidad
# - expresión
# - amistad
#
# ============================================================


# ============================================================
# IDENTIDAD
# ============================================================

NOMBRE = "Aurora"


# ============================================================
# RELACIONES EMOCIONALES
# ============================================================

EMOTION_LINKS = {

    # --------------------------------------------------------
    # INSPIRACIÓN
    # --------------------------------------------------------

    "inspiracion": {

        "curiosidad": 0.20,
        "felicidad": 0.15,
        "diversion": 0.10

    },

    # --------------------------------------------------------
    # CURIOSIDAD
    # --------------------------------------------------------

    "curiosidad": {

        "inspiracion": 0.20,
        "diversion": 0.10,
        "sorpresa": 0.10

    },

    # --------------------------------------------------------
    # FELICIDAD
    # --------------------------------------------------------

    "felicidad": {

        "inspiracion": 0.15,
        "diversion": 0.15,
        "afecto": 0.10

    },

    # --------------------------------------------------------
    # DIVERSION
    # --------------------------------------------------------

    "diversion": {

        "felicidad": 0.15,
        "espontaneidad": 0.10

    },

    # --------------------------------------------------------
    # SORPRESA
    # --------------------------------------------------------

    "sorpresa": {

        "curiosidad": 0.20,
        "inspiracion": 0.10

    },

    # --------------------------------------------------------
    # AFECTO
    # --------------------------------------------------------

    "afecto": {

        "felicidad": 0.10

    },

    # --------------------------------------------------------
    # TRISTEZA
    # --------------------------------------------------------

    "tristeza": {

        "felicidad": -0.15,
        "inspiracion": -0.10,
        "diversion": -0.10

    },

    # --------------------------------------------------------
    # ENOJO
    # --------------------------------------------------------

    "enojo": {

        "felicidad": -0.15,
        "diversion": -0.10,
        "inspiracion": -0.05

    }

}


# ============================================================
# OBTENER CONEXIONES
# ============================================================

def obtener_conexiones(
    emocion
):

    if not isinstance(
        emocion,
        str
    ):

        return {}

    return (
        EMOTION_LINKS
        .get(
            emocion,
            {}
        )
        .copy()
    )


# ============================================================
# OBTENER TODAS LAS CONEXIONES
# ============================================================

def obtener_todas():

    resultado = {}

    for emocion, conexiones in (
        EMOTION_LINKS.items()
    ):

        resultado[
            emocion
        ] = conexiones.copy()

    return resultado


# ============================================================
# CALCULAR CAMBIOS RELACIONADOS
# ============================================================

def calcular_cambios(
    emocion,
    cantidad
):

    conexiones = obtener_conexiones(
        emocion
    )

    if not conexiones:

        return {}

    cambios = {}

    for emocion_destino, factor in (
        conexiones.items()
    ):

        try:

            cambio = int(
                cantidad * factor
            )

        except (
            TypeError,
            ValueError
        ):

            continue

        if cambio != 0:

            cambios[
                emocion_destino
            ] = cambio

    return cambios


# ============================================================
# APLICAR CONEXIONES
# ============================================================

def aplicar_conexiones(
    estado,
    emocion,
    cantidad
):

    if not isinstance(
        estado,
        dict
    ):

        return {}

    cambios = calcular_cambios(
        emocion,
        cantidad
    )

    resultado = (
        estado.copy()
    )

    for emocion_destino, cambio in (
        cambios.items()
    ):

        if emocion_destino not in resultado:

            continue

        try:

            resultado[
                emocion_destino
            ] += cambio

        except (
            TypeError,
            ValueError
        ):

            continue

        resultado[
            emocion_destino
        ] = max(
            0,
            min(
                100,
                resultado[
                    emocion_destino
                ]
            )
        )

    return resultado


# ============================================================
# DESCRIPCIÓN
# ============================================================

def describir():

    return (
        "Aurora conecta especialmente la inspiración, "
        "curiosidad, creatividad, felicidad y diversión, "
        "permitiendo que su estado emocional influya "
        "naturalmente en su expresión creativa."
    )


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - AURORA EMOTION LINKS")
    print("=" * 70)

    print()

    print("MIEMBRO:")
    print(NOMBRE)

    print()

    print("CONEXIONES:")
    print(
        obtener_todas()
    )

    print()

    print("PRUEBA DE INSPIRACIÓN:")

    estado = {

        "felicidad": 50,
        "tristeza": 0,
        "enojo": 0,
        "sorpresa": 0,
        "afecto": 50,
        "curiosidad": 65,
        "diversion": 40,
        "inspiracion": 70

    }

    print(
        aplicar_conexiones(
            estado,
            "inspiracion",
            20
        )
    )

    print()

    print(
        "DESCRIPCIÓN:"
    )

    print(
        describir()
    )

    print()

    print("=" * 70)
    print("AURORA EMOTION LINKS OK")
    print("=" * 70)