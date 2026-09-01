# ============================================================
# ELIZYUM - ELI EMOTIONS
# miembros/eli/emotions_eli.py
#
# Configuración emocional específica de Eli.
# Utiliza el motor central emotions.py.
# ============================================================

from emotions.emotions import EstadoEmocional


# ============================================================
# ESTADO EMOCIONAL DE ELI
# ============================================================

class EmocionesEli(EstadoEmocional):

    def __init__(self):
        super().__init__("eli")


# ============================================================
# INSTANCIA DE ELI
# ============================================================

eli_emociones = EmocionesEli()


# ============================================================
# ACCESO RÁPIDO
# ============================================================

def obtener_emociones():
    return eli_emociones.obtener()


def cambiar_emocion(nombre, cantidad):
    return eli_emociones.cambiar(
        nombre,
        cantidad
    )


def establecer_emocion(nombre, valor):
    return eli_emociones.establecer(
        nombre,
        valor
    )


def obtener_emocion_dominante():
    return eli_emociones.emocion_dominante()


def obtener_estado_animo():
    return eli_emociones.obtener_estado_animo()


def decaer_emociones(cantidad=1):
    return eli_emociones.decaer(
        cantidad
    )


def aplicar_relaciones():
    return eli_emociones.aplicar_relaciones()


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - ELI EMOTIONS")
    print("=" * 70)

    print()

    print("Emociones de Eli:")
    print(
        obtener_emociones()
    )

    print()

    print("Emoción dominante:")
    print(
        obtener_emocion_dominante()
    )

    print()

    print("Estado de ánimo:")
    print(
        obtener_estado_animo()
    )