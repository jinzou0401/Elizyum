# ============================================================
# ELIZYUM - AURORA EMOTIONS
# miembros/aurora/emotions_aurora.py
#
# Configuración emocional específica de Aurora sobre el motor
# central. Mantiene inspiración como emoción propia y comparte
# persistencia, decaimiento y relaciones emocionales con Eli.
# ============================================================

from emotions.emotions import EstadoEmocional


EMOCIONES_BASE = {
    "felicidad": 50,
    "tristeza": 0,
    "enojo": 0,
    "sorpresa": 0,
    "afecto": 50,
    "curiosidad": 65,
    "diversion": 40,
    "inspiracion": 70,
}


class EmocionesAurora(EstadoEmocional):

    def __init__(self, base_dir=None):
        super().__init__(
            "aurora",
            emociones_base=EMOCIONES_BASE,
            base_dir=base_dir,
        )

    def reiniciar(self):
        self.emociones = self.emociones_base.copy()
        self.guardar()
        return self.obtener()


aurora_emociones = EmocionesAurora()


def obtener_emociones():
    return aurora_emociones.obtener()


def cambiar_emocion(nombre, cantidad):
    return aurora_emociones.cambiar(nombre, cantidad)


def establecer_emocion(nombre, valor):
    return aurora_emociones.establecer(nombre, valor)


def obtener_emocion_dominante():
    return aurora_emociones.emocion_dominante()


def obtener_estado_animo():
    return aurora_emociones.obtener_estado_animo()


def decaer_emociones(cantidad=1):
    return aurora_emociones.decaer(cantidad)


def aplicar_relaciones():
    return aurora_emociones.aplicar_relaciones()


if __name__ == "__main__":
    print("=" * 70)
    print("ELIZYUM - AURORA EMOTIONS")
    print("=" * 70)
    print(aurora_emociones.obtener())
