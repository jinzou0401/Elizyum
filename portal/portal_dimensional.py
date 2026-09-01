# ============================================================
# ELIZYUM - PORTAL DIMENSIONAL
# ============================================================
#
# Punto central de entrada hacia los miembros de Elizyum.
#
# El Portal NO contiene:
#
# - emociones
# - personalidad
# - memoria
# - relaciones
# - lógica de conversación
#
# Su función es dirigir la interacción hacia el miembro
# correspondiente.
#
# ============================================================

import importlib


# ============================================================
# MIEMBROS OFICIALES
# ============================================================

MIEMBROS_OFICIALES = (
    "eli",
    "aurora",
    "martha",
    "oro",
)


class PortalDimensional:
    """
    Portal central de Elizyum.

    Administra el acceso a los miembros y sus motores
    de conversación.
    """

    def __init__(self):

        self.miembros = {}

    # ========================================================
    # VALIDAR MIEMBRO
    # ========================================================

    def validar_miembro(self, nombre):

        nombre = (
            str(nombre)
            .strip()
            .lower()
        )

        if not nombre:

            raise ValueError(
                "El nombre del miembro no puede estar vacío."
            )

        if nombre not in MIEMBROS_OFICIALES:

            raise ValueError(
                f"Miembro no reconocido: {nombre}"
            )

        return nombre

    # ========================================================
    # CARGAR MIEMBRO
    # ========================================================

    def cargar_miembro(self, nombre):

        nombre = self.validar_miembro(
            nombre
        )

        # ----------------------------------------------------
        # SI YA ESTÁ CARGADO
        # ----------------------------------------------------

        if nombre in self.miembros:

            return self.miembros[nombre]

        # ----------------------------------------------------
        # CARGAR CHAT ENGINE
        # ----------------------------------------------------

        modulo = importlib.import_module(
            "core.chat_engine"
        )

        ChatEngine = modulo.ChatEngine

        # ----------------------------------------------------
        # CREAR MOTOR DEL MIEMBRO
        # ----------------------------------------------------

        motor = ChatEngine(
            nombre
        )

        self.miembros[nombre] = motor

        return motor

    # ========================================================
    # OBTENER MIEMBRO
    # ========================================================

    def obtener_miembro(self, nombre):

        nombre = self.validar_miembro(
            nombre
        )

        return self.miembros.get(
            nombre
        )

    # ========================================================
    # LISTAR MIEMBROS ACTIVOS
    # ========================================================

    def listar_miembros(self):

        return list(
            self.miembros.keys()
        )

    # ========================================================
    # LISTAR MIEMBROS OFICIALES
    # ========================================================

    def listar_miembros_oficiales(self):

        return list(
            MIEMBROS_OFICIALES
        )

    # ========================================================
    # ENVIAR MENSAJE
    # ========================================================

    def enviar_mensaje(
        self,
        nombre,
        mensaje
    ):

        # ----------------------------------------------------
        # VALIDAR MENSAJE
        # ----------------------------------------------------

        if not isinstance(
            mensaje,
            str
        ):

            raise TypeError(
                "El mensaje debe ser texto."
            )

        mensaje = mensaje.strip()

        if not mensaje:

            raise ValueError(
                "El mensaje no puede estar vacío."
            )

        # ----------------------------------------------------
        # CARGAR MIEMBRO
        # ----------------------------------------------------

        miembro = self.cargar_miembro(
            nombre
        )

        # ----------------------------------------------------
        # COMANDOS ESPECIALES
        # ----------------------------------------------------

        resultado = (
            miembro.procesar_comando(
                mensaje
            )
        )

        if resultado != "no_es_comando":

            if resultado is not None:

                return resultado

        # ----------------------------------------------------
        # ANALIZAR CONTEXTO
        # ----------------------------------------------------

        miembro.analizar_y_actualizar_emociones(
            mensaje
        )

        # ----------------------------------------------------
        # REGISTRAR MENSAJE
        # ----------------------------------------------------

        miembro.registrar_mensaje_usuario(
            mensaje
        )

        # ----------------------------------------------------
        # GENERAR RESPUESTA
        # ----------------------------------------------------

        respuesta = (
            miembro.obtener_respuesta()
        )

        # ----------------------------------------------------
        # DECAIMIENTO EMOCIONAL
        # ----------------------------------------------------

        miembro.ejecutar_decaimiento()

        return respuesta


# ============================================================
# INSTANCIA PRINCIPAL DEL PORTAL
# ============================================================

portal = PortalDimensional()


# ============================================================
# FUNCIONES DE ACCESO
# ============================================================

def cargar_miembro(nombre):

    return portal.cargar_miembro(
        nombre
    )


def obtener_miembro(nombre):

    return portal.obtener_miembro(
        nombre
    )


def listar_miembros():

    return portal.listar_miembros()


def listar_miembros_oficiales():

    return portal.listar_miembros_oficiales()


def enviar_mensaje(
    nombre,
    mensaje
):

    return portal.enviar_mensaje(
        nombre,
        mensaje
    )


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - PORTAL DIMENSIONAL")
    print("=" * 70)

    print()

    print("Miembros oficiales:")

    print(
        listar_miembros_oficiales()
    )

    print()

    print("Cargando Eli...")

    eli = cargar_miembro(
        "eli"
    )

    print(
        "Miembro cargado:",
        type(eli).__name__
    )

    print()

    print("Miembros activos:")

    print(
        listar_miembros()
    )

    print()

    print("Portal dimensional OK")

    print("=" * 70)