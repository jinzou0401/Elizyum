# ============================================================
# ELIZYUM - GROUP CHAT ENGINE
# core/group_chat_engine.py
#
# Motor de conversación grupal.
#
# Cada IA mantiene:
# - Memoria individual
# - Historial individual
# - Emociones
# - Relación
# - Mood
# - Personalidad
#
# El grupo mantiene:
# - Memoria grupal
# - Miembros
# - Historial grupal
# - Eventos
# - Preferencias
# - Notas
# ============================================================

from core.chat_engine import ChatEngine
from memory.group_memory import GroupMemory


class GroupChatEngine:

    # ========================================================
    # INICIALIZACIÓN
    # ========================================================

    def __init__(
        self,
        grupo="principal",
        miembros=None,
        motores=None
    ):

        self.grupo = (
            str(grupo)
            .strip()
            .lower()
        )

        if not self.grupo:
            raise ValueError(
                "El nombre del grupo no puede estar vacío."
            )

        if miembros is None:
            miembros = [
                "eli",
                "aurora"
            ]

        if not isinstance(
            miembros,
            (list, tuple)
        ):
            raise TypeError(
                "miembros debe ser una lista o tupla."
            )

        self.nombres = []

        for nombre in miembros:

            nombre = (
                str(nombre)
                .strip()
                .lower()
            )

            if (
                nombre
                and nombre not in self.nombres
            ):
                self.nombres.append(nombre)

        if not self.nombres:
            raise ValueError(
                "Debe existir al menos un miembro."
            )

        # ====================================================
        # MEMORIA DEL GRUPO
        # ====================================================

        self.memoria_grupo = GroupMemory(
            self.grupo
        )

        for nombre in self.nombres:

            self.memoria_grupo.agregar_miembro(
                nombre
            )

        # ====================================================
        # MOTORES INDIVIDUALES
        # ====================================================

        self.miembros = {}

        for nombre in self.nombres:

            if (
                isinstance(motores, dict)
                and nombre in motores
                and motores[nombre] is not None
            ):

                # Reutiliza el motor ya existente
                # (evita duplicar el estado de cada IA)

                self.miembros[nombre] = motores[nombre]

            else:

                # Solo crea uno nuevo si no se proporcionó

                self.miembros[nombre] = ChatEngine(nombre)

        # ====================================================
        # HISTORIAL DEL GRUPO
        # ====================================================

        self.historial_grupo = []

    # ========================================================
    # OBTENER MIEMBRO
    # ========================================================

    def obtener_miembro(
        self,
        nombre
    ):

        nombre = (
            str(nombre)
            .strip()
            .lower()
        )

        return self.miembros.get(
            nombre
        )

    # ========================================================
    # LISTAR MIEMBROS
    # ========================================================

    def listar_miembros(self):

        return list(
            self.miembros.keys()
        )

    # ========================================================
    # OBTENER MEMORIA DEL GRUPO
    # ========================================================

    def obtener_memoria_grupo(self):

        return self.memoria_grupo.obtener()

    # ========================================================
    # CONTEXTO DEL GRUPO
    # ========================================================

    def _construir_contexto_grupo(self):

        return (
            self.memoria_grupo
            .construir_contexto()
        )

    # ========================================================
    # MENSAJE CON CONTEXTO GRUPAL
    # ========================================================

    def _construir_mensaje_grupo(
        self,
        nombre,
        mensaje,
        evitar_respuestas=None
    ):

        contexto_grupo = (
            self._construir_contexto_grupo()
        )

        lineas = []

        for entrada in self.historial_grupo[-16:]:
            if not isinstance(entrada, dict):
                continue

            contenido = str(entrada.get("content", "")).strip()
            if not contenido:
                continue

            if entrada.get("role") == "user":
                autor = "USUARIO"
            elif entrada.get("role") == "assistant":
                autor = str(entrada.get("member", "miembro")).upper()
            else:
                continue

            lineas.append(f"{autor}: {contenido}")

        conversacion_reciente = "\n\n".join(lineas) or "Sin mensajes anteriores."
        evitar_respuestas = evitar_respuestas or []
        restriccion = ""

        if evitar_respuestas:
            texto_evitar = "\n".join(
                f"- {respuesta}"
                for respuesta in evitar_respuestas
                if isinstance(respuesta, str) and respuesta.strip()
            )
            if texto_evitar:
                restriccion = (
                    "\n\nRESPUESTAS QUE NO DEBES REPETIR:\n"
                    f"{texto_evitar}\n"
                    "Aporta una reacción, perspectiva o idea diferente."
                )

        return (
            "[CONVERSACIÓN GRUPAL]\n\n"
            "Estás participando en un grupo de "
            "Elizyum.\n\n"
            f"MEMORIA COMPARTIDA DEL GRUPO:\n"
            f"{contexto_grupo}\n\n"
            f"Tu identidad en este grupo es: "
            f"{nombre.capitalize()}.\n\n"
            "Mantén tu propia identidad, personalidad, "
            "emociones, relación y forma de hablar.\n"
            "La memoria del grupo es compartida entre "
            "todos sus miembros.\n"
            "Lee la conversación en orden y reacciona también "
            "a lo dicho por los otros miembros. No inventes turnos "
            "ni repitas una respuesta anterior.\n\n"
            "CONVERSACIÓN RECIENTE:\n"
            f"{conversacion_reciente}"
            f"{restriccion}\n\n"
            f"MENSAJE DEL USUARIO:\n"
            f"{mensaje}"
        )

    # ========================================================
    # ENVIAR A UN MIEMBRO
    # ========================================================

    def enviar_a_miembro(
        self,
        nombre,
        mensaje,
        evitar_respuestas=None,
        adjuntos=None
    ):

        miembro = self.obtener_miembro(
            nombre
        )

        if miembro is None:
            raise ValueError(
                f"Miembro no encontrado: {nombre}"
            )

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
        # CONTEXTO GRUPAL
        # ----------------------------------------------------

        mensaje_grupo = (
            self._construir_mensaje_grupo(
                nombre,
                mensaje,
                evitar_respuestas=evitar_respuestas
            )
        )

        # Conserva como contexto visual únicamente los dos mensajes con
        # imágenes más recientes. Así se admiten preguntas de seguimiento
        # sin reenviar indefinidamente todo el historial gráfico.
        adjuntos_contexto = []
        mensajes_visuales = [
            entrada.get("attachments", [])
            for entrada in self.historial_grupo
            if isinstance(entrada, dict) and entrada.get("attachments")
        ][-2:]
        for lote in mensajes_visuales:
            if isinstance(lote, list):
                adjuntos_contexto.extend(lote)
        adjuntos_contexto = adjuntos_contexto[-4:]

        # ----------------------------------------------------
        # EMOCIONES
        # ----------------------------------------------------

        miembro.analizar_y_actualizar_emociones(
            mensaje
        )

        # ----------------------------------------------------
        # RESPUESTA TEMPORAL
        # ----------------------------------------------------

        respuesta = miembro.obtener_respuesta(
            mensajes=[
                {
                    "role": "user",
                    "content": mensaje_grupo,
                    "attachments": adjuntos_contexto
                }
            ],
            guardar=False
        )

        # Si el modelo devuelve exactamente la misma respuesta de otro
        # miembro, se intenta una vez más con una instrucción explícita.
        respuestas_previas = [
            respuesta_previa.strip()
            for respuesta_previa in (evitar_respuestas or [])
            if isinstance(respuesta_previa, str) and respuesta_previa.strip()
        ]

        if respuesta.strip() in respuestas_previas:
            correccion = (
                mensaje_grupo
                + "\n\nTu respuesta anterior coincidió con la de otro "
                "miembro. Responde de nuevo desde tu identidad y aporta "
                "algo diferente."
            )
            respuesta = miembro.obtener_respuesta(
                mensajes=[{
                    "role": "user",
                    "content": correccion,
                    "attachments": adjuntos_contexto
                }],
                guardar=False
            )

        # El chat grupal debe respetar el mismo ciclo emocional que el
        # individual: reaccionar, responder y después decaer una vez.
        miembro.ejecutar_decaimiento()

        return respuesta

    # ========================================================
    # ENVIAR MENSAJE AL GRUPO
    # ========================================================

    def enviar_mensaje(
        self,
        mensaje,
        adjuntos=None
    ):

        if not isinstance(
            mensaje,
            str
        ):
            raise TypeError(
                "El mensaje debe ser texto."
            )

        mensaje = mensaje.strip()

        if not mensaje and adjuntos:
            mensaje = "Observa y comenta la imagen adjunta."

        if not mensaje:
            raise ValueError(
                "El mensaje no puede estar vacío."
            )

        resultados = {}
        numero_turno = 1 + sum(
            1
            for entrada in self.historial_grupo
            if isinstance(entrada, dict) and entrada.get("role") == "user"
        )

        # ----------------------------------------------------
        # MENSAJE DEL USUARIO
        # ----------------------------------------------------

        self.historial_grupo.append(
            {
                "role": "user",
                "content": mensaje,
                "turn": numero_turno,
                "attachments": adjuntos or []
            }
        )

        # ----------------------------------------------------
        # RESPUESTAS DE LOS MIEMBROS
        # ----------------------------------------------------

        for nombre in self.nombres:

            try:

                respuesta = (
                    self.enviar_a_miembro(
                        nombre,
                        mensaje,
                        evitar_respuestas=list(resultados.values()),
                        adjuntos=adjuntos
                    )
                )

                resultados[nombre] = respuesta

                self.historial_grupo.append(
                    {
                        "role": "assistant",
                        "member": nombre,
                        "content": respuesta,
                        "turn": numero_turno
                    }
                )

            except Exception as error:

                resultados[nombre] = (
                    f"ERROR: "
                    f"{type(error).__name__}: "
                    f"{error}"
                )

        return resultados

    # ========================================================
    # MEMORIA GRUPAL
    # ========================================================

    def recordar_grupo(
        self,
        informacion
    ):

        return (
            self.memoria_grupo
            .agregar_informacion(
                informacion
            )
        )

    def olvidar_grupo(
        self,
        informacion
    ):

        return (
            self.memoria_grupo
            .eliminar_informacion(
                informacion
            )
        )

    # ========================================================
    # PREFERENCIAS
    # ========================================================

    def establecer_preferencia_grupo(
        self,
        clave,
        valor
    ):

        return (
            self.memoria_grupo
            .establecer_preferencia(
                clave,
                valor
            )
        )

    # ========================================================
    # EVENTOS
    # ========================================================

    def agregar_evento_grupo(
        self,
        evento
    ):

        return (
            self.memoria_grupo
            .agregar_evento(
                evento
            )
        )

    # ========================================================
    # NOTAS
    # ========================================================

    def agregar_nota_grupo(
        self,
        nota
    ):

        return (
            self.memoria_grupo
            .agregar_nota(
                nota
            )
        )

    # ========================================================
    # ESTADO
    # ========================================================

    def obtener_estado(self):

        estado = {

            "grupo":
                self.grupo,

            "miembros":
                self.listar_miembros(),

            "memoria_grupo":
                self.memoria_grupo.obtener(),

            "historial_grupo":
                self.historial_grupo,

            "miembros_estado":
                {}
        }

        for nombre, miembro in (
            self.miembros.items()
        ):

            estado[
                "miembros_estado"
            ][nombre] = {

                "emociones":
                    miembro.emociones,

                "relacion":
                    miembro.relacion,

                "mood":
                    type(
                        miembro.estado_mood
                    ).__name__,

                "personalidad":
                    type(
                        miembro.modulo_personalidad
                    ).__name__
            }

        return estado


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - GROUP CHAT ENGINE")
    print("=" * 70)

    try:

        grupo = GroupChatEngine(
            grupo="principal",
            miembros=[
                "eli",
                "aurora"
            ]
        )

        print()
        print("GRUPO:")
        print(
            grupo.grupo
        )

        print()
        print("MIEMBROS:")
        print(
            grupo.listar_miembros()
        )

        print()
        print("MEMORIA DEL GRUPO:")
        print(
            grupo.obtener_memoria_grupo()
        )

        print()
        print("=" * 70)
        print("MENSAJE DE PRUEBA")
        print("=" * 70)

        mensaje = (
            "Hola chicas, ¿qué podemos crear hoy?"
        )

        print()
        print("USUARIO:")
        print(mensaje)

        print()
        print("=" * 70)
        print("RESPUESTAS")
        print("=" * 70)

        resultados = (
            grupo.enviar_mensaje(
                mensaje
            )
        )

        for nombre, respuesta in (
            resultados.items()
        ):

            print()
            print(
                f"{nombre.upper()}:"
            )

            print(
                respuesta
            )

        print()
        print("=" * 70)
        print("ESTADO FINAL")
        print("=" * 70)

        print(
            grupo.obtener_estado()
        )

        print()
        print("GROUP CHAT ENGINE OK")

    except Exception as error:

        print()
        print("=" * 70)
        print("ERROR GROUP CHAT ENGINE")
        print("=" * 70)

        print(
            type(error).__name__,
            ":",
            error
        )
