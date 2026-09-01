# ============================================================
# ELIZYUM - MAIN
# main.py
#
# Punto de entrada principal de Elizyum.
#
# Motores:
#
# - Eli
# - Aurora
# - Grupo
#
# Todos permanecen activos mientras la ventana está abierta.
# ============================================================

from core.chat_engine import ChatEngine
from core.group_chat_engine import GroupChatEngine
from ui.web_app import iniciar_app


def main():

    # ========================================================
    # VENTANA PRINCIPAL
    # ========================================================

    # ========================================================
    # MOTORES INDIVIDUALES
    # ========================================================

    motor_eli = ChatEngine(
        "eli"
    )

    motor_aurora = ChatEngine(
        "aurora"
    )

    # ========================================================
    # MOTOR GRUPAL
    # ========================================================

    motor_grupo = GroupChatEngine(
        grupo="principal",
        miembros=[
            "eli",
            "aurora"
        ],
        motores={
            "eli": motor_eli,
            "aurora": motor_aurora
        }
    )
    # ========================================================
    # REGISTRO DE MOTORES
    # ========================================================

    motores = {

        "eli":
            motor_eli,

        "aurora":
            motor_aurora,

        "grupo":
            motor_grupo
    }

    # ========================================================
    # INTERFAZ
    # ========================================================

    iniciar_app(motores)

    # ========================================================
    # EJECUTAR
    # ========================================================



# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    main()
