# ============================================================
# ELIZYUM - MOOD ELI
# miembros/eli/mood_eli.py
#
# Adaptador del motor central de ánimo para Eli.
#
# El motor central está en:
#
#     emotions/emotions.py
#     emotions/mood.py
#
# Este archivo NO contiene la lógica central.
# ============================================================

from emotions.mood import (
    obtener_estado_faceta,
    construir_contexto_faceta
)

from miembros.eli.emotions_eli import eli_emociones


# ============================================================
# CONFIGURACIÓN DE ELI
# ============================================================

NOMBRE = "eli"


# ============================================================
# ESTADO EMOCIONAL DE ELI
# ============================================================

class MoodEli:
    """
    Motor de ánimo específico de Eli.

    Utiliza los motores centrales de Elizyum.
    """

    def __init__(self):

        self.emociones = eli_emociones

        self.ultimo_estado = None


    # ========================================================
    # EMOCIONES
    # ========================================================

    def obtener_emociones(self):

        return self.emociones.obtener()


    # ========================================================
    # CAMBIAR EMOCIÓN
    # ========================================================

    def cambiar_emocion(
        self,
        nombre,
        cantidad
    ):

        return self.emociones.cambiar(
            nombre,
            cantidad
        )


    # ========================================================
    # ESTABLECER EMOCIÓN
    # ========================================================

    def establecer_emocion(
        self,
        nombre,
        valor
    ):

        return self.emociones.establecer(
            nombre,
            valor
        )


    # ========================================================
    # ESTADO DE ÁNIMO
    # ========================================================

    def obtener_estado_animo(self):

        return self.emociones.obtener_estado_animo()


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

        estado = obtener_estado_faceta(
            emociones=self.obtener_emociones(),
            contexto=contexto,
            relacion=relacion
        )

        self.ultimo_estado = estado

        return estado


    # ========================================================
    # CONSTRUIR CONTEXTO PARA GEMMA
    # ========================================================

    def construir_contexto(
        self,
        contexto=None,
        relacion=None
    ):
        """
        Construye el contexto emocional y relacional
        de Eli para el LLM.
        """

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

        estado = self.determinar_faceta(
            contexto=contexto,
            relacion=relacion
        )

        return construir_contexto_faceta(
            estado,
            contexto=contexto
        )


    # ========================================================
    # ÚLTIMO ESTADO
    # ========================================================

    def obtener_ultimo_estado(self):

        if self.ultimo_estado is None:

            return self.determinar_faceta()

        return self.ultimo_estado.copy()


    # ========================================================
    # DECAIMIENTO
    # ========================================================

    def decaer(
        self,
        cantidad=1
    ):

        resultado = self.emociones.decaer(
            cantidad
        )

        self.ultimo_estado = None

        return resultado


# ============================================================
# INSTANCIA PRINCIPAL DE ELI
# ============================================================

eli_mood = MoodEli()


# ============================================================
# FUNCIONES DE ACCESO
# ============================================================

def obtener_emociones():

    return eli_mood.obtener_emociones()


def cambiar_emocion(
    nombre,
    cantidad
):

    return eli_mood.cambiar_emocion(
        nombre,
        cantidad
    )


def establecer_emocion(
    nombre,
    valor
):

    return eli_mood.establecer_emocion(
        nombre,
        valor
    )


def obtener_estado_animo():

    return eli_mood.obtener_estado_animo()


def determinar_faceta(
    contexto=None,
    relacion=None
):

    return eli_mood.determinar_faceta(
        contexto,
        relacion
    )


def construir_contexto(
    contexto=None,
    relacion=None
):

    return eli_mood.construir_contexto(
        contexto,
        relacion
    )


def obtener_ultimo_estado():

    return eli_mood.obtener_ultimo_estado()


def decaer(
    cantidad=1
):

    return eli_mood.decaer(
        cantidad
    )


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - MOOD ELI")
    print("=" * 70)

    estado = determinar_faceta()

    print()
    print("ESTADO:")
    print(estado)

    print()
    print("CONTEXTO:")
    print(construir_contexto())

    print()
    print("=" * 70)
    print("MOOD ELI OK")
    print("=" * 70)