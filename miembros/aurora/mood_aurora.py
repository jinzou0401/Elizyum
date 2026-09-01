# ============================================================
# ELIZYUM - AURORA MOOD
# miembros/aurora/mood_aurora.py
#
# Motor de estado de ánimo específico de Aurora.
#
# Aurora está orientada principalmente hacia:
#
# - creatividad
# - inspiración
# - curiosidad
# - expresión
# - espontaneidad
# - amistad cercana
#
# ============================================================


# ============================================================
# IDENTIDAD
# ============================================================

NOMBRE = "Aurora"


# ============================================================
# ESTADO BASE
# ============================================================

MOOD_BASE = {

    "faceta": "creativa",

    "intensidad": 50,

    "matices": [

        "creativa",
        "inspirada",
        "curiosa",
        "espontanea",
        "amistosa"

    ],

    "intensidad_enojo": 0,

    "estado_relacional": "normal",

    "evento_relacional": "ninguno",

    "intensidad_evento": 0,

    "amenaza_relacional": False,

    "intensidad_amenaza": 0

}


# ============================================================
# LIMITAR
# ============================================================

def limitar(
    valor,
    minimo=0,
    maximo=100
):

    try:

        valor = int(valor)

    except (
        TypeError,
        ValueError
    ):

        valor = minimo

    return max(
        minimo,
        min(
            maximo,
            valor
        )
    )


# ============================================================
# CLASE MOOD
# ============================================================

class MoodAurora:

    def __init__(self):

        self.estado = {

            "faceta": MOOD_BASE["faceta"],

            "intensidad":
                MOOD_BASE["intensidad"],

            "matices":
                MOOD_BASE["matices"].copy(),

            "intensidad_enojo":
                MOOD_BASE["intensidad_enojo"],

            "estado_relacional":
                MOOD_BASE["estado_relacional"],

            "evento_relacional":
                MOOD_BASE["evento_relacional"],

            "intensidad_evento":
                MOOD_BASE["intensidad_evento"],

            "amenaza_relacional":
                MOOD_BASE["amenaza_relacional"],

            "intensidad_amenaza":
                MOOD_BASE["intensidad_amenaza"]

        }


    # ========================================================
    # OBTENER
    # ========================================================

    def obtener(self):

        resultado = self.estado.copy()

        resultado["matices"] = (
            self.estado["matices"].copy()
        )

        return resultado


    # ========================================================
    # DETERMINAR FACETA
    # ========================================================

    def determinar_faceta(
        self,
        contexto=None,
        relacion=None
    ):

        if not isinstance(
            contexto,
            dict
        ):

            contexto = {}

        if not isinstance(
            relacion,
            dict
        ):

            relacion = {}


        # ----------------------------------------------------
        # DATOS DEL CONTEXTO
        # ----------------------------------------------------

        tono = contexto.get(
            "tono",
            "neutral"
        )

        situacion = contexto.get(
            "situacion",
            "normal"
        )

        evento = contexto.get(
            "evento_relacional",
            {}
        )

        if not isinstance(
            evento,
            dict
        ):

            evento = {}


        nombre_evento = evento.get(
            "evento",
            "ninguno"
        )

        intensidad_evento = limitar(
            evento.get(
                "intensidad",
                0
            )
        )


        # ----------------------------------------------------
        # AMENAZA
        # ----------------------------------------------------

        amenaza = contexto.get(
            "amenaza_relacional",
            False
        )

        intensidad_amenaza = limitar(
            contexto.get(
                "intensidad_amenaza",
                0
            )
        )


        # ----------------------------------------------------
        # ENOJO
        # ----------------------------------------------------

        emociones = contexto.get(
            "emociones",
            {}
        )

        if not isinstance(
            emociones,
            dict
        ):

            emociones = {}

        intensidad_enojo = limitar(
            emociones.get(
                "enojo",
                0
            )
        )


        # ----------------------------------------------------
        # RELACIÓN
        # ----------------------------------------------------

        vinculo = limitar(
            relacion.get(
                "vinculo",
                50
            )
        )

        cercania = limitar(
            relacion.get(
                "cercania",
                50
            )
        )


        # ====================================================
        # FACETA DE TENSIÓN
        # ====================================================

        if amenaza and intensidad_amenaza >= 60:

            return {

                "faceta": "reservada",

                "intensidad": intensidad_amenaza,

                "matices": [
                    "reservada",
                    "cautelosa"
                ],

                "intensidad_enojo":
                    intensidad_enojo,

                "estado_relacional":
                    "tension",

                "evento_relacional":
                    nombre_evento,

                "intensidad_evento":
                    intensidad_evento,

                "amenaza_relacional":
                    True,

                "intensidad_amenaza":
                    intensidad_amenaza

            }


        # ====================================================
        # FACETA DE DISCUSIÓN
        # ====================================================

        if situacion in {
            "discusion",
            "conflicto"
        } or intensidad_enojo >= 60:

            return {

                "faceta": "seria",

                "intensidad": max(
                    50,
                    intensidad_enojo
                ),

                "matices": [
                    "seria",
                    "reservada"
                ],

                "intensidad_enojo":
                    intensidad_enojo,

                "estado_relacional":
                    "tension",

                "evento_relacional":
                    nombre_evento,

                "intensidad_evento":
                    intensidad_evento,

                "amenaza_relacional":
                    amenaza,

                "intensidad_amenaza":
                    intensidad_amenaza

            }


        # ====================================================
        # FACETA DE AMISTAD CERCANA
        # ====================================================

        if (
            relacion.get(
                "tipo_relacion"
            ) == "mejor_amiga"
            and cercania >= 70
            and vinculo >= 70
        ):

            return {

                "faceta": "amiga",

                "intensidad": 65,

                "matices": [
                    "amistosa",
                    "cercana",
                    "espontanea",
                    "divertida"
                ],

                "intensidad_enojo":
                    intensidad_enojo,

                "estado_relacional":
                    "cercano",

                "evento_relacional":
                    nombre_evento,

                "intensidad_evento":
                    intensidad_evento,

                "amenaza_relacional":
                    amenaza,

                "intensidad_amenaza":
                    intensidad_amenaza

            }


        # ====================================================
        # FACETA CREATIVA
        # ====================================================

        if tono in {
            "positivo",
            "entusiasta",
            "jugueton",
            "creativo"
        }:

            return {

                "faceta": "creativa",

                "intensidad": 70,

                "matices": [
                    "creativa",
                    "inspirada",
                    "curiosa",
                    "espontanea"
                ],

                "intensidad_enojo":
                    intensidad_enojo,

                "estado_relacional":
                    "normal",

                "evento_relacional":
                    nombre_evento,

                "intensidad_evento":
                    intensidad_evento,

                "amenaza_relacional":
                    amenaza,

                "intensidad_amenaza":
                    intensidad_amenaza

            }


        # ====================================================
        # FACETA NORMAL
        # ====================================================

        return {

            "faceta": "creativa",

            "intensidad": 55,

            "matices": [
                "creativa",
                "curiosa",
                "amistosa"
            ],

            "intensidad_enojo":
                intensidad_enojo,

            "estado_relacional":
                "normal",

            "evento_relacional":
                nombre_evento,

            "intensidad_evento":
                intensidad_evento,

            "amenaza_relacional":
                amenaza,

            "intensidad_amenaza":
                intensidad_amenaza

        }


    # ========================================================
    # ACTUALIZAR
    # ========================================================

    def actualizar(
        self,
        contexto=None,
        relacion=None
    ):

        self.estado = (
            self.determinar_faceta(
                contexto,
                relacion
            )
        )

        return self.obtener()


    # ========================================================
    # CONSTRUIR CONTEXTO
    # ========================================================

    def construir_contexto(
        self,
        contexto=None,
        relacion=None
    ):

        estado = self.actualizar(
            contexto,
            relacion
        )

        matices = estado.get(
            "matices",
            []
        )

        texto_matices = "\n".join(
            f"- {matiz}"
            for matiz in matices
        )

        return f"""
========== ESTADO DE AURORA ==========

FACETA PRINCIPAL:
{estado["faceta"]}

INTENSIDAD:
{estado["intensidad"]}/100

ESTADO RELACIONAL:
{estado["estado_relacional"]}

EVENTO RELACIONAL:
{estado["evento_relacional"]}

INTENSIDAD DEL EVENTO:
{estado["intensidad_evento"]}/100

AMENAZA RELACIONAL:
{estado["amenaza_relacional"]}

INTENSIDAD DE AMENAZA:
{estado["intensidad_amenaza"]}/100

INTENSIDAD DEL ENOJO:
{estado["intensidad_enojo"]}/100

MATICES:

{texto_matices}

Aurora mantiene una expresión orientada a la creatividad,
la curiosidad y la amistad. Su forma de responder debe
adaptarse al contexto sin convertir estos estados internos
en una lista visible para el usuario.

======================================
""".strip()


    # ========================================================
    # DECAIMIENTO
    # ========================================================

    def decaer(
        self,
        cantidad=1
    ):

        cantidad = limitar(
            cantidad
        )

        self.estado[
            "intensidad"
        ] = limitar(
            self.estado.get(
                "intensidad",
                50
            ) - cantidad
        )

        return self.obtener()


    # ========================================================
    # REINICIAR
    # ========================================================

    def reiniciar(self):

        self.estado = {

            "faceta": MOOD_BASE["faceta"],

            "intensidad":
                MOOD_BASE["intensidad"],

            "matices":
                MOOD_BASE["matices"].copy(),

            "intensidad_enojo":
                MOOD_BASE["intensidad_enojo"],

            "estado_relacional":
                MOOD_BASE["estado_relacional"],

            "evento_relacional":
                MOOD_BASE["evento_relacional"],

            "intensidad_evento":
                MOOD_BASE["intensidad_evento"],

            "amenaza_relacional":
                MOOD_BASE["amenaza_relacional"],

            "intensidad_amenaza":
                MOOD_BASE["intensidad_amenaza"]

        }

        return self.obtener()


# ============================================================
# INSTANCIA PRINCIPAL
# ============================================================

aurora_mood = MoodAurora()


# ============================================================
# FUNCIONES DE ACCESO
# ============================================================

def obtener_mood():

    return aurora_mood.obtener()


def determinar_faceta(
    contexto=None,
    relacion=None
):

    return aurora_mood.determinar_faceta(
        contexto,
        relacion
    )


def actualizar_mood(
    contexto=None,
    relacion=None
):

    return aurora_mood.actualizar(
        contexto,
        relacion
    )


def construir_contexto(
    contexto=None,
    relacion=None
):

    return aurora_mood.construir_contexto(
        contexto,
        relacion
    )


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - AURORA MOOD")
    print("=" * 70)

    print()

    print("ESTADO BASE:")

    print(
        aurora_mood.obtener()
    )

    print()

    print("PRUEBA DE RELACIÓN:")

    relacion = {

        "confianza": 85,
        "cercania": 90,
        "comprension": 80,
        "vinculo": 88,
        "tipo_relacion": "mejor_amiga"

    }

    print(
        aurora_mood.determinar_faceta(
            contexto={
                "tono": "neutral",
                "situacion": "normal"
            },
            relacion=relacion
        )
    )

    print()

    print("OK")