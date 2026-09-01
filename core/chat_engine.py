# ============================================================
# ELIZYUM - CHAT ENGINE
# core/chat_engine.py
#
# Motor principal de conversación.
#
# Arquitectura:
#
# perfil del miembro
#        ↓
# memoria individual
#        ↓
# historial individual
#        ↓
# context_ai
#        ↓
# emociones
#        ↓
# relación
#        ↓
# mood
#        ↓
# personalidad
#        ↓
# estilo de respuesta
#        ↓
# prompt dinámico
#        ↓
# LM Studio / Gemma
#
# Compatible con:
#
# - Eli
# - Aurora
# - Memoria individual
# - Emociones individuales
# - Relación individual
# - Mood individual
# - Personalidad individual
# - GroupChatEngine
#
# ============================================================

import importlib
import base64
import types
from pathlib import Path

import requests

from config import (
    LM_STUDIO_URL,
    LM_STUDIO_MODEL,
    LM_STUDIO_MAX_TOKENS,
    TEMPERATURE
)

from mundo.context_ai import (
    analizar_contexto
)

from memory.history import (
    Historial
)

from memory.memory import (
    Memoria
)


class ChatEngine:

    # ========================================================
    # INICIALIZACIÓN
    # ========================================================

    def __init__(
        self,
        nombre="eli"
    ):

        # ----------------------------------------------------
        # IDENTIDAD
        # ----------------------------------------------------

        self.nombre = (
            str(nombre)
            .strip()
            .lower()
        )

        if not self.nombre:

            raise ValueError(
                "El nombre del miembro no puede estar vacío."
            )

        # ----------------------------------------------------
        # PERFIL
        # ----------------------------------------------------

        perfil = importlib.import_module(
            f"miembros.{self.nombre}.perfil_{self.nombre}"
        )

        self.system_prompt_base = (
            perfil.SYSTEM_PROMPT
        )

        self.reglas_personalidad = (
            perfil.REGLAS_PERSONALIDAD
        )

        # ----------------------------------------------------
        # MÓDULO DE EMOCIONES
        # ----------------------------------------------------

        self.modulo_emociones = importlib.import_module(
            f"miembros.{self.nombre}.emotions_{self.nombre}"
        )

        # ----------------------------------------------------
        # MÓDULO DE RELACIÓN
        # ----------------------------------------------------

        self.modulo_relacion = importlib.import_module(
            f"miembros.{self.nombre}.relationship_{self.nombre}"
        )

        # ----------------------------------------------------
        # MÓDULO DE MOOD
        # ----------------------------------------------------

        self.modulo_mood = importlib.import_module(
            f"miembros.{self.nombre}.mood_{self.nombre}"
        )

        # ----------------------------------------------------
        # MÓDULO DE PERSONALIDAD
        # ----------------------------------------------------

        self.modulo_personalidad = importlib.import_module(
            f"miembros.{self.nombre}.personality_{self.nombre}"
        )

        # ====================================================
        # INSTANCIA DE EMOCIONES
        # ====================================================

        self.estado_emocional = (
            self._buscar_instancia(
                self.modulo_emociones,
                (
                    "eli_emociones",
                    "aurora_emociones",
                    f"{self.nombre}_emociones"
                )
            )
        )

        if self.estado_emocional is None:

            raise ImportError(
                f"No se encontró una instancia de emociones "
                f"para {self.nombre}."
            )

        # ====================================================
        # INSTANCIA DE RELACIÓN
        # ====================================================

        self.estado_relacion = (
            self._buscar_instancia(
                self.modulo_relacion,
                (
                    "relationships",
                    "eli_relationships",
                    "aurora_relationships",
                    f"{self.nombre}_relationships"
                )
            )
        )

        # ====================================================
        # INSTANCIA DE MOOD
        # ====================================================

        self.estado_mood = (
            self._buscar_instancia(
                self.modulo_mood,
                (
                    "eli_mood",
                    "aurora_mood",
                    f"{self.nombre}_mood"
                )
            )
        )

        if self.estado_mood is None:

            raise ImportError(
                f"No se encontró una instancia de mood "
                f"para {self.nombre}."
            )

        # ====================================================
        # MEMORIA INDIVIDUAL
        # ====================================================

        self.memoria = Memoria(
            self.nombre
        )

        # ====================================================
        # HISTORIAL INDIVIDUAL
        # ====================================================

        self.historial = Historial(
            self.nombre
        )

        # ====================================================
        # ESTADOS ACTUALES
        # ====================================================

        self.emociones = (
            self._obtener_emociones()
        )

        self.relacion = (
            self._obtener_relacion()
        )

        self.ultimo_contexto = {}

        self.ultimo_mood = None

        # ====================================================
        # CARGAR ÚLTIMA CONVERSACIÓN
        # ====================================================

        ultima = (
            self.historial.ultima_conversacion()
        )

        if ultima:

            mensajes_guardados = (
                self.historial.cargar_conversacion(
                    ultima
                )
            )

            if (
                isinstance(
                    mensajes_guardados,
                    list
                )
                and mensajes_guardados
            ):

                self.messages = (
                    mensajes_guardados
                )

                self.archivo_conversacion = (
                    ultima
                )

            else:

                self.messages = [
                    {
                        "role": "system",
                        "content": self.system_prompt_base
                    }
                ]

                self.archivo_conversacion = (
                    self.historial.nombre_archivo()
                )

        else:

            self.messages = [
                {
                    "role": "system",
                    "content": self.system_prompt_base
                }
            ]

            self.archivo_conversacion = (
                self.historial.nombre_archivo()
            )

    # ========================================================
    # BUSCAR INSTANCIA
    # ========================================================

    def _buscar_instancia(
        self,
        modulo,
        nombres
    ):

        for nombre in nombres:

            if not hasattr(
                modulo,
                nombre
            ):

                continue

            objeto = getattr(
                modulo,
                nombre
            )

            # Algunos adaptadores importan el módulo central con el nombre
            # ``relationships``. Eso no es una instancia persistente y no
            # debe confundirse con el gestor real del miembro.
            if objeto is not None and not isinstance(objeto, types.ModuleType):

                return objeto

        return None

    # ========================================================
    # OBTENER EMOCIONES
    # ========================================================

    def _obtener_emociones(self):

        if hasattr(
            self.estado_emocional,
            "obtener"
        ):

            resultado = (
                self.estado_emocional.obtener()
            )

            if isinstance(
                resultado,
                dict
            ):

                return resultado

        if hasattr(
            self.modulo_emociones,
            "obtener_emociones"
        ):

            resultado = (
                self.modulo_emociones.obtener_emociones()
            )

            if isinstance(
                resultado,
                dict
            ):

                return resultado

        return {}

    # ========================================================
    # OBTENER RELACIÓN
    # ========================================================

    def _obtener_relacion(self):

        # ----------------------------------------------------
        # OBJETO
        # ----------------------------------------------------

        if self.estado_relacion is not None:

            if hasattr(
                self.estado_relacion,
                "obtener"
            ):

                resultado = (
                    self.estado_relacion.obtener()
                )

                if isinstance(
                    resultado,
                    dict
                ):

                    return resultado

            if hasattr(
                self.estado_relacion,
                "relacion"
            ):

                resultado = (
                    self.estado_relacion.relacion
                )

                if isinstance(
                    resultado,
                    dict
                ):

                    return resultado.copy()

        # ----------------------------------------------------
        # CONSTANTES DEL MÓDULO
        # ----------------------------------------------------

        posibles = (
            "RELACION_BASE_ELI",
            "RELACION_BASE_AURORA",
            "RELACION_BASE"
        )

        for nombre in posibles:

            if hasattr(
                self.modulo_relacion,
                nombre
            ):

                resultado = getattr(
                    self.modulo_relacion,
                    nombre
                )

                if isinstance(
                    resultado,
                    dict
                ):

                    return resultado.copy()

        return {}

    # ========================================================
    # COMANDOS ESPECIALES
    # ========================================================

    def procesar_comando(
        self,
        mensaje
    ):

        if not isinstance(
            mensaje,
            str
        ):

            return "no_es_comando"

        mensaje_normalizado = (
            mensaje.strip().lower()
        )

        # ----------------------------------------------------
        # OLVIDAR
        # ----------------------------------------------------

        comando_olvidar = (
            f"{self.nombre}, olvida que"
        )

        if mensaje_normalizado.startswith(
            comando_olvidar
        ):

            informacion = (
                mensaje[
                    len(comando_olvidar):
                ].strip()
            )

            if informacion:

                self.memoria.eliminar_informacion_importante(
                    informacion
                )

                return (
                    "Lo olvidaré. 🗑️\n\n"
                    f"Eliminado: {informacion}"
                )

            return None

        # ----------------------------------------------------
        # RECORDAR
        # ----------------------------------------------------

        comando_memoria = (
            f"{self.nombre}, recuerda que"
        )

        if mensaje_normalizado.startswith(
            comando_memoria
        ):

            informacion = (
                mensaje[
                    len(comando_memoria):
                ].strip()
            )

            if informacion:

                self.memoria.agregar_informacion_importante(
                    informacion
                )

                return (
                    "Lo recordaré. 🧠💜\n\n"
                    f"Guardado: {informacion}"
                )

            return None

        return "no_es_comando"

    # ========================================================
    # CONTEXTO / EMOCIONES / RELACIÓN / MOOD
    # ========================================================

    def analizar_y_actualizar_emociones(
        self,
        mensaje
    ):

        contexto = analizar_contexto(
            mensaje
        )

        if not isinstance(
            contexto,
            dict
        ):

            contexto = {}

        # ----------------------------------------------------
        # AMENAZA RELACIONAL
        # ----------------------------------------------------

        info_amenaza = contexto.get(
            "contexto_relacional",
            {}
        )

        if not isinstance(
            info_amenaza,
            dict
        ):

            info_amenaza = {}

        contexto[
            "amenaza_relacional"
        ] = info_amenaza.get(
            "amenaza_relacional",
            False
        )

        contexto[
            "intensidad_amenaza"
        ] = info_amenaza.get(
            "intensidad",
            0
        )

        # ----------------------------------------------------
        # NORMALIZAR DISTANCIA
        # ----------------------------------------------------

        if contexto.get(
            "situacion"
        ) == "distante":

            contexto[
                "situacion"
            ] = "distancia"

        if contexto.get(
            "estado_relacional"
        ) == "distante":

            contexto[
                "estado_relacional"
            ] = "distancia"

        # ----------------------------------------------------
        # EMOCIONES
        # ----------------------------------------------------

        cambios_emocionales = (
            contexto.get(
                "emociones",
                {}
            )
        )

        if not isinstance(
            cambios_emocionales,
            dict
        ):

            cambios_emocionales = {}

        for emocion, cantidad in (
            cambios_emocionales.items()
        ):

            if cantidad:

                if hasattr(
                    self.estado_emocional,
                    "cambiar"
                ):

                    self.estado_emocional.cambiar(
                        emocion,
                        cantidad
                    )

                elif hasattr(
                    self.modulo_emociones,
                    "cambiar_emocion"
                ):

                    self.modulo_emociones.cambiar_emocion(
                        emocion,
                        cantidad
                    )

        # ----------------------------------------------------
        # CONTAGIO ENTRE EMOCIONES (una sola vez por mensaje)
        # ----------------------------------------------------

        if hasattr(
            self.estado_emocional,
            "aplicar_relaciones"
        ):

            self.estado_emocional.aplicar_relaciones()

        elif hasattr(
            self.modulo_emociones,
            "aplicar_relaciones"
        ):

            self.modulo_emociones.aplicar_relaciones()

        self.emociones = (
            self._obtener_emociones()
        )

        # ----------------------------------------------------
        # RELACIÓN
        # ----------------------------------------------------

        if (
            self.estado_relacion is not None
            and hasattr(
                self.estado_relacion,
                "procesar_contexto"
            )
        ):

            self.relacion = (
                self.estado_relacion.procesar_contexto(
                    contexto
                )
            )

        elif hasattr(
            self.modulo_relacion,
            "aplicar_evento"
        ):

            evento_relacional = contexto.get(
                "evento_relacional"
            )

            if isinstance(
                evento_relacional,
                dict
            ):

                resultado = (
                    self.modulo_relacion.aplicar_evento(
                        self.relacion,
                        evento_relacional
                    )
                )

                if isinstance(
                    resultado,
                    dict
                ):

                    self.relacion = resultado

        else:

            self.relacion = (
                self._obtener_relacion()
            )

        # ----------------------------------------------------
        # MOOD
        # ----------------------------------------------------

        if hasattr(
            self.estado_mood,
            "actualizar"
        ):

            try:

                resultado_mood = (
                    self.estado_mood.actualizar(
                        contexto,
                        self.relacion
                    )
                )

                if resultado_mood is not None:

                    self.ultimo_mood = (
                        resultado_mood
                    )

            except TypeError:

                try:

                    resultado_mood = (
                        self.estado_mood.actualizar(
                            contexto
                        )
                    )

                    if resultado_mood is not None:

                        self.ultimo_mood = (
                            resultado_mood
                        )

                except Exception:

                    pass

        self.ultimo_contexto = contexto

        return contexto

    # ========================================================
    # REGISTRAR MENSAJE
    # ========================================================

    def registrar_mensaje_usuario(
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

        if not mensaje:

            raise ValueError(
                "El mensaje no puede estar vacío."
            )

        entrada = {
            "role": "user",
            "content": mensaje
        }

        if isinstance(adjuntos, list) and adjuntos:
            entrada["attachments"] = adjuntos

        self.messages.append(entrada)

        self.historial.guardar_conversacion(
            self.messages,
            self.archivo_conversacion
        )

    # ========================================================
    # DECAIMIENTO
    # ========================================================

    def ejecutar_decaimiento(self):

        if hasattr(
            self.estado_emocional,
            "decaer"
        ):

            self.estado_emocional.decaer(
                1
            )

        elif hasattr(
            self.modulo_emociones,
            "decaer_emociones"
        ):

            self.modulo_emociones.decaer_emociones(
                1
            )

        # Algunos moods (como el de Eli) poseen otra instancia del mismo
        # estado emocional. No debe decaerse dos veces ni sobrescribir el
        # archivo con una copia antigua. Los moods independientes sí pueden
        # reducir su intensidad propia.
        if hasattr(self.estado_mood, "ultimo_estado"):
            self.estado_mood.ultimo_estado = None

        if (
            hasattr(self.estado_mood, "decaer")
            and not hasattr(self.estado_mood, "emociones")
        ):
            self.estado_mood.decaer(1)

        self.emociones = (
            self._obtener_emociones()
        )

    # ========================================================
    # CONSTRUIR SYSTEM PROMPT
    # ========================================================

    def _construir_system_prompt(self):

        contexto = (
            self.ultimo_contexto
        )

        if not isinstance(
            contexto,
            dict
        ):

            contexto = {}
                # ----------------------------------------------------
        # PERSONALIDAD
        # ----------------------------------------------------

        contexto_personalidad = ""

        rasgos = None

        nombre_calculo = f"calcular_personalidad_{self.nombre}"

        if hasattr(self.modulo_personalidad, nombre_calculo):

            funcion_calculo = getattr(
                self.modulo_personalidad,
                nombre_calculo
            )

            try:

                rasgos = funcion_calculo(
                    emociones=self.emociones,
                    relacion=self.relacion,
                    mood=self.ultimo_mood
                )

            except TypeError:

                try:

                    rasgos = funcion_calculo(
                        emociones=self.emociones,
                        faceta=(self.ultimo_mood or {}).get("faceta"),
                        intensidad_faceta=(self.ultimo_mood or {}).get("intensidad", 20),
                        contexto=contexto
                    )

                except TypeError:

                    rasgos = None

        if rasgos is None and hasattr(
            self.modulo_personalidad,
            "obtener_personalidad_base"
        ):

            rasgos = self.modulo_personalidad.obtener_personalidad_base()

        nombre_construir = f"construir_contexto_personalidad_{self.nombre}"

        if isinstance(rasgos, dict):

            if hasattr(self.modulo_personalidad, nombre_construir):

                funcion_construir = getattr(
                    self.modulo_personalidad,
                    nombre_construir
                )

                try:

                    contexto_personalidad = funcion_construir(rasgos)

                except TypeError:

                    try:

                        contexto_personalidad = funcion_construir(
                            rasgos,
                            faceta=(self.ultimo_mood or {}).get("faceta"),
                            matices=(self.ultimo_mood or {}).get("matices")
                        )

                    except TypeError:

                        contexto_personalidad = ""

            elif hasattr(
                self.modulo_personalidad,
                "construir_contexto_personalidad"
            ):

                try:

                    contexto_personalidad = (
                        self.modulo_personalidad
                        .construir_contexto_personalidad(rasgos)
                    )

                except TypeError:

                    contexto_personalidad = ""
       

        # ----------------------------------------------------
        # FACETA / MOOD
        # ----------------------------------------------------

        contexto_faceta = ""

        if hasattr(
            self.estado_mood,
            "construir_contexto"
        ):

            try:

                contexto_faceta = (
                    self.estado_mood.construir_contexto(
                        contexto=contexto,
                        relacion=self.relacion
                    )
                )

            except TypeError:

                try:

                    contexto_faceta = (
                        self.estado_mood.construir_contexto(
                            contexto,
                            self.relacion
                        )
                    )

                except TypeError:

                    try:

                        contexto_faceta = (
                            self.estado_mood.construir_contexto()
                        )

                    except Exception:

                        contexto_faceta = ""

        elif hasattr(
            self.modulo_mood,
            "construir_contexto"
        ):

            try:

                contexto_faceta = (
                    self.modulo_mood.construir_contexto(
                        contexto,
                        self.relacion
                    )
                )

            except TypeError:

                contexto_faceta = ""

        # ----------------------------------------------------
        # MEMORIA
        # ----------------------------------------------------

        datos_memoria = (
            self.memoria.datos
        )

        if not isinstance(
            datos_memoria,
            dict
        ):

            datos_memoria = {}

        usuario = datos_memoria.get(
            "usuario",
            {}
        )

        preferencias = datos_memoria.get(
            "preferencias",
            {}
        )

        informacion_importante = (
            datos_memoria.get(
                "informacion_importante",
                []
            )
        )

        if not isinstance(
            usuario,
            dict
        ):

            usuario = {}

        nombre_usuario = (
            usuario.get(
                "nombre",
                ""
            )
        )

        if not nombre_usuario:

            nombre_usuario = "Usuario"

        contexto_memoria = f"""
========== MEMORIA PERMANENTE ==========

Nombre del usuario:
{nombre_usuario}

Preferencias:
{preferencias}

Información importante:
{informacion_importante}

=========================================
""".strip()

        # ----------------------------------------------------
        # VÍNCULO
        # ----------------------------------------------------

        nivel_vinculo = 50

        descripcion_vinculo = (
            "Relación en estado normal."
        )

        if (
            self.estado_relacion is not None
            and hasattr(
                self.estado_relacion,
                "obtener_nivel_vinculo"
            )
        ):

            try:

                nivel_vinculo = (
                    self.estado_relacion
                    .obtener_nivel_vinculo()
                )

            except Exception:

                pass

        elif isinstance(
            self.relacion,
            dict
        ):

            nivel_vinculo = (
                self.relacion.get(
                    "vinculo",
                    50
                )
            )

        if (
            self.estado_relacion is not None
            and hasattr(
                self.estado_relacion,
                "describir"
            )
        ):

            try:

                descripcion_vinculo = (
                    self.estado_relacion
                    .describir()
                )

            except Exception:

                pass

        elif isinstance(
            self.relacion,
            dict
        ):

            tipo_relacion = (
                self.relacion.get(
                    "tipo_relacion"
                )
            )

            if tipo_relacion:

                descripcion_vinculo = (
                    f"Relación: {tipo_relacion}."
                )

        contexto_vinculo = f"""
========== VÍNCULO CON EL USUARIO ==========

Nivel general:
{nivel_vinculo}/100

Descripción:
{descripcion_vinculo}

=============================================
""".strip()

        # ----------------------------------------------------
        # ESTILO DE RESPUESTA
        # ----------------------------------------------------

        contexto_respuesta = """
========== ESTILO DE RESPUESTA ==========

Responde de forma natural y conversacional.

Mantén las respuestas breves y directas.

En una conversación normal utiliza
normalmente entre 1 y 4 frases cortas.

Evita listas largas salvo que el usuario
las solicite.

No repitas innecesariamente la pregunta.

No desarrolles ideas que el usuario no
haya solicitado.

Si una respuesta puede darse en pocas
frases, utiliza pocas frases.

No conviertas una conversación casual
en una explicación extensa.

No escribas respuestas excesivamente largas.

=========================================
""".strip()

        # ----------------------------------------------------
        # SYSTEM PROMPT FINAL
        # ----------------------------------------------------

        partes = [
            self.system_prompt_base,
            self.reglas_personalidad,
            contexto_memoria,
            contexto_personalidad,
            contexto_vinculo,
            contexto_faceta,
            contexto_respuesta
        ]

        return "\n\n".join(
            str(parte)
            for parte in partes
            if parte
        )

    # ========================================================
    # OBTENER RESPUESTA
    # ========================================================

    def obtener_respuesta(
        self,
        mensajes=None,
        guardar=True
    ):

        system_prompt = (
            self._construir_system_prompt()
        )

        mensajes_con_contexto = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        # ----------------------------------------------------
        # HISTORIAL
        # ----------------------------------------------------

        historial_fuente = (
            self.messages
            if mensajes is None
            else mensajes
        )

        historial_fuente = list(historial_fuente)
        indices_con_imagen = {
            indice
            for indice, entrada in enumerate(historial_fuente)
            if isinstance(entrada, dict) and entrada.get("attachments")
        }
        indices_con_imagen = set(sorted(indices_con_imagen)[-2:])

        for indice, mensaje in enumerate(historial_fuente):

            if not isinstance(
                mensaje,
                dict
            ):

                continue

            role = mensaje.get(
                "role"
            )

            content = mensaje.get("content")

            if role == "system":

                continue

            if role not in {
                "user",
                "assistant"
            }:

                continue

            if not isinstance(content, (str, list)):
                continue

            if role == "user" and isinstance(content, str):
                partes = []
                textos_adjuntos = []
                adjuntos = (
                    mensaje.get("attachments", [])
                    if indice in indices_con_imagen
                    else []
                )

                if isinstance(adjuntos, list):
                    for adjunto in adjuntos[:4]:
                        if not isinstance(adjunto, dict):
                            continue

                        mime = str(adjunto.get("mime", "")).lower()
                        ruta = Path(str(adjunto.get("path", "")))

                        if mime == "text/plain":
                            try:
                                texto_archivo = ruta.read_text(encoding="utf-8")[:50000]
                            except OSError:
                                continue
                            textos_adjuntos.append(
                                f"ARCHIVO TXT: {adjunto.get('name', ruta.name)}\n{texto_archivo}"
                            )
                            continue

                        if mime not in {"image/jpeg", "image/png", "image/webp"}:
                            continue

                        try:
                            datos_imagen = base64.b64encode(ruta.read_bytes()).decode("ascii")
                        except OSError:
                            continue

                        partes.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime};base64,{datos_imagen}"
                            }
                        })

                texto_final = content
                if textos_adjuntos:
                    texto_final += "\n\n" + "\n\n".join(textos_adjuntos)

                if partes:
                    partes.append({
                        "type": "text",
                        "text": texto_final or "Analiza los archivos adjuntos."
                    })
                    content = partes
                else:
                    content = texto_final

            mensajes_con_contexto.append(
                {
                    "role": role,
                    "content": content
                }
            )

        # ----------------------------------------------------
        # LM STUDIO
        # ----------------------------------------------------

        payload = {
            "model": LM_STUDIO_MODEL,
            "messages": mensajes_con_contexto,
            "temperature": TEMPERATURE,
            "max_tokens": LM_STUDIO_MAX_TOKENS
        }

        mensaje_respuesta = ""

        for intento in range(2):
            respuesta = requests.post(
                LM_STUDIO_URL,
                json=payload,
                timeout=120
            )
            respuesta.raise_for_status()
            datos = respuesta.json()

            if not isinstance(datos, dict):
                raise ValueError("LM Studio devolvió una respuesta inválida.")

            choices = datos.get("choices")
            if not isinstance(choices, list) or not choices:
                raise ValueError("LM Studio no devolvió ninguna elección.")

            primer_resultado = choices[0]
            if not isinstance(primer_resultado, dict):
                raise ValueError("La respuesta de LM Studio tiene un formato inválido.")

            mensaje_modelo = primer_resultado.get("message")
            if not isinstance(mensaje_modelo, dict):
                raise ValueError("LM Studio no devolvió un mensaje válido.")

            contenido = mensaje_modelo.get("content")
            if isinstance(contenido, str):
                mensaje_respuesta = contenido.strip()

            if mensaje_respuesta:
                break

            if intento == 0:
                # Gemma puede terminar un intento sin texto final. El segundo
                # intento conserva el contexto, baja la variación y exige una
                # salida visible, sin guardar ni duplicar ningún turno.
                payload = {
                    **payload,
                    "temperature": min(float(TEMPERATURE), 0.4),
                    "max_tokens": max(LM_STUDIO_MAX_TOKENS, 1200),
                    "messages": mensajes_con_contexto + [
                        {
                            "role": "system",
                            "content": (
                                "Genera ahora una respuesta final visible, "
                                "breve y no vacía. No devuelvas solo "
                                "razonamiento interno."
                            )
                        }
                    ]
                }

        if not mensaje_respuesta:
            raise ValueError(
                "LM Studio devolvió una respuesta vacía después de reintentarlo."
            )

        # ----------------------------------------------------
        # GUARDAR RESPUESTA
        # ----------------------------------------------------

        if guardar:
            self.messages.append(
                {
                    "role": "assistant",
                    "content": mensaje_respuesta
                }
            )

            self.historial.guardar_conversacion(
                self.messages,
                self.archivo_conversacion
            )

        return mensaje_respuesta

    # ========================================================
    # NUEVA CONVERSACIÓN
    # ========================================================

    def nueva_conversacion(self):

        self.messages = [
            {
                "role": "system",
                "content": self.system_prompt_base
            }
        ]

        self.archivo_conversacion = (
            self.historial.nombre_archivo()
        )

        # ----------------------------------------------------
        # NO REINICIAR:
        #
        # - memoria
        # - emociones
        # - relación
        # - mood
        #
        # Estos pertenecen al miembro.
        # ----------------------------------------------------

        self.ultimo_contexto = {}


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - CHAT ENGINE")
    print("=" * 70)

    for miembro in (
        "eli",
        "aurora"
    ):

        try:

            engine = ChatEngine(
                miembro
            )

            print()
            print(
                f"MIEMBRO: {engine.nombre}"
            )

            print()
            print("EMOCIONES:")
            print(
                engine.emociones
            )

            print()
            print("RELACION:")
            print(
                engine.relacion
            )

            print()
            print("MOOD:")
            print(
                type(
                    engine.estado_mood
                ).__name__
            )

            print()
            print("PERSONALIDAD:")
            print(
                type(
                    engine.modulo_personalidad
                ).__name__
            )

            print()
            print(
                f"{miembro.upper()} CHAT ENGINE OK"
            )

        except Exception as e:

            print()
            print(
                f"ERROR EN {miembro.upper()}"
            )

            print(
                type(e).__name__,
                ":",
                e
            )

    print()
    print("=" * 70)
    print("PRUEBA FINALIZADA")
    print("=" * 70)
