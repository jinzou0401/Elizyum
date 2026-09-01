import sys
import base64
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from emotions.emotions import EstadoEmocional
from emotions.relationships import GestorRelacion
from miembros.aurora.emotions_aurora import EmocionesAurora
from miembros.aurora import relationship_aurora


class PersistenciaRelacionesTests(unittest.TestCase):

    def test_eli_guarda_recupera_y_permanece_aislada(self):
        with tempfile.TemporaryDirectory() as carpeta:
            eli = GestorRelacion("eli", base_dir=carpeta)
            aurora = GestorRelacion("aurora", base_dir=carpeta)

            eli.procesar_contexto({
                "evento_relacional": {
                    "evento": "cumplio_promesa",
                    "intensidad": 80,
                }
            })

            eli_recargada = GestorRelacion("eli", base_dir=carpeta)
            aurora_recargada = GestorRelacion("aurora", base_dir=carpeta)

            self.assertEqual(eli_recargada.obtener(), eli.obtener())
            self.assertNotEqual(
                eli_recargada.obtener()["confianza"],
                aurora_recargada.obtener()["confianza"],
            )
            self.assertEqual(aurora_recargada.obtener(), aurora.obtener())

    def test_gestor_conserva_metadatos_del_miembro(self):
        with tempfile.TemporaryDirectory() as carpeta:
            base = {
                "confianza": 85,
                "cercania": 90,
                "comprension": 80,
                "vinculo": 88,
                "tipo_relacion": "mejor_amiga",
            }
            gestor = GestorRelacion("aurora", base=base, base_dir=carpeta)
            gestor.procesar_contexto({
                "evento_relacional": {
                    "evento": "mentira",
                    "intensidad": 70,
                }
            })

            recargado = GestorRelacion("aurora", base=base, base_dir=carpeta)
            self.assertEqual(recargado.obtener()["tipo_relacion"], "mejor_amiga")

    def test_relacion_real_de_aurora_persiste(self):
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "relacion.json"
            with patch.object(relationship_aurora, "ARCHIVO_RELACION", archivo):
                estado = relationship_aurora.RelationshipAurora()
                estado.procesar_contexto({
                    "evento_relacional": {
                        "evento": "mentira",
                        "intensidad": 100,
                    }
                })
                recargado = relationship_aurora.RelationshipAurora()

            self.assertEqual(recargado.obtener(), estado.obtener())
            self.assertLess(
                recargado.obtener()["confianza"],
                relationship_aurora.RELACION_BASE_AURORA["confianza"],
            )


class EmocionesAvanzadasTests(unittest.TestCase):

    def test_estados_independientes_y_persistentes(self):
        with tempfile.TemporaryDirectory() as carpeta:
            eli = EstadoEmocional("eli", base_dir=carpeta)
            aurora = EmocionesAurora(base_dir=carpeta)

            eli.cambiar("afecto", 20)
            aurora.cambiar("curiosidad", 10)

            eli_recargada = EstadoEmocional("eli", base_dir=carpeta)
            aurora_recargada = EmocionesAurora(base_dir=carpeta)

            self.assertEqual(eli_recargada.obtener(), eli.obtener())
            self.assertEqual(aurora_recargada.obtener(), aurora.obtener())
            self.assertNotIn("inspiracion", eli_recargada.obtener())
            self.assertEqual(aurora_recargada.obtener()["inspiracion"], 70)

    def test_decaimiento_regresa_a_la_base_sin_contagio_extra(self):
        with tempfile.TemporaryDirectory() as carpeta:
            estado = EstadoEmocional("eli", base_dir=carpeta)
            estado.establecer("felicidad", 80)
            estado.establecer("afecto", 80)

            resultado = estado.decaer(5)

            self.assertEqual(resultado["felicidad"], 75)
            self.assertEqual(resultado["afecto"], 75)
            self.assertEqual(
                EstadoEmocional("eli", base_dir=carpeta).obtener(),
                resultado,
            )

    def test_contagio_emocional_se_aplica_una_vez(self):
        with tempfile.TemporaryDirectory() as carpeta:
            estado = EstadoEmocional("eli", base_dir=carpeta)
            estado.establecer("felicidad", 70)
            afecto_antes = estado.obtener()["afecto"]

            resultado = estado.aplicar_relaciones()

            self.assertEqual(resultado["afecto"], afecto_antes + 2)


class DecaimientoChatEngineTests(unittest.TestCase):

    def test_chat_engine_envia_imagen_antes_del_texto(self):
        requests_falso = types.ModuleType("requests")
        with patch.dict(sys.modules, {"requests": requests_falso}):
            from core import chat_engine

        class Respuesta:
            def raise_for_status(self):
                return None

            def json(self):
                return {"choices": [{"message": {"content": "Veo la imagen"}}]}

        class Cliente:
            def __init__(self):
                self.payload = None

            def post(self, url, json, timeout):
                self.payload = json
                return Respuesta()

        with tempfile.TemporaryDirectory() as carpeta:
            imagen = Path(carpeta) / "prueba.png"
            imagen.write_bytes(b"\x89PNG\r\n\x1a\ncontenido")
            motor = chat_engine.ChatEngine.__new__(chat_engine.ChatEngine)
            motor._construir_system_prompt = lambda: "Sistema"
            motor.messages = [{
                "role": "user",
                "content": "¿Qué observas?",
                "attachments": [{
                    "mime": "image/png",
                    "path": str(imagen),
                    "name": "prueba.png",
                }],
            }]
            cliente = Cliente()

            with patch.object(chat_engine, "requests", cliente):
                resultado = motor.obtener_respuesta(guardar=False)

        contenido = cliente.payload["messages"][1]["content"]
        self.assertEqual(resultado, "Veo la imagen")
        self.assertEqual(contenido[0]["type"], "image_url")
        self.assertEqual(contenido[1], {"type": "text", "text": "¿Qué observas?"})

    def test_chat_engine_incluye_contenido_txt(self):
        requests_falso = types.ModuleType("requests")
        with patch.dict(sys.modules, {"requests": requests_falso}):
            from core import chat_engine

        class Respuesta:
            def raise_for_status(self):
                return None

            def json(self):
                return {"choices": [{"message": {"content": "Resumen correcto"}}]}

        class Cliente:
            def post(self, url, json, timeout):
                self.payload = json
                return Respuesta()

        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "notas.txt"
            archivo.write_text("Contenido importante del documento.", encoding="utf-8")
            motor = chat_engine.ChatEngine.__new__(chat_engine.ChatEngine)
            motor._construir_system_prompt = lambda: "Sistema"
            motor.messages = [{
                "role": "user",
                "content": "Resume el archivo",
                "attachments": [{"mime": "text/plain", "path": str(archivo), "name": "notas.txt"}],
            }]
            cliente = Cliente()
            with patch.object(chat_engine, "requests", cliente):
                resultado = motor.obtener_respuesta(guardar=False)

        contenido = cliente.payload["messages"][1]["content"]
        self.assertEqual(resultado, "Resumen correcto")
        self.assertIn("ARCHIVO TXT: notas.txt", contenido)
        self.assertIn("Contenido importante", contenido)

    def test_lm_studio_reintenta_vacio_y_fija_gemma(self):
        requests_falso = types.ModuleType("requests")
        with patch.dict(sys.modules, {"requests": requests_falso}):
            from core import chat_engine

        class Respuesta:
            def __init__(self, contenido):
                self.contenido = contenido

            def raise_for_status(self):
                return None

            def json(self):
                return {
                    "choices": [{
                        "message": {"content": self.contenido},
                        "finish_reason": "stop",
                    }]
                }

        class ClienteFalso:
            def __init__(self):
                self.payloads = []
                self.respuestas = [Respuesta(""), Respuesta("Respuesta final")]

            def post(self, url, json, timeout):
                self.payloads.append(json)
                return self.respuestas.pop(0)

        cliente = ClienteFalso()
        motor = chat_engine.ChatEngine.__new__(chat_engine.ChatEngine)
        motor._construir_system_prompt = lambda: "Sistema de prueba"
        motor.messages = [{"role": "user", "content": "Hola"}]

        with patch.object(chat_engine, "requests", cliente):
            resultado = motor.obtener_respuesta(guardar=False)

        self.assertEqual(resultado, "Respuesta final")
        self.assertEqual(len(cliente.payloads), 2)
        self.assertEqual(cliente.payloads[0]["model"], "google/gemma-4-e4b")
        self.assertGreaterEqual(cliente.payloads[1]["max_tokens"], 1200)

    def test_chat_engine_selecciona_gestores_reales_y_aislados(self):
        requests_falso = types.ModuleType("requests")
        with patch.dict(sys.modules, {"requests": requests_falso}):
            from core.chat_engine import ChatEngine

        eli = ChatEngine("eli")
        aurora = ChatEngine("aurora")

        self.assertFalse(isinstance(eli.estado_relacion, types.ModuleType))
        self.assertTrue(hasattr(eli.estado_relacion, "guardar"))
        self.assertFalse(isinstance(aurora.estado_relacion, types.ModuleType))
        self.assertIsNot(eli.estado_relacion, aurora.estado_relacion)

    def test_chat_engine_decae_emocion_sin_duplicarla_en_mood(self):
        requests_falso = types.ModuleType("requests")
        with patch.dict(sys.modules, {"requests": requests_falso}):
            from core.chat_engine import ChatEngine

        class Emociones:
            def __init__(self):
                self.llamadas = 0

            def decaer(self, cantidad):
                self.llamadas += cantidad

            def obtener(self):
                return {"felicidad": 50}

        class MoodEliFalso:
            def __init__(self):
                self.emociones = object()
                self.ultimo_estado = {"faceta": "cercana"}
                self.llamadas = 0

            def decaer(self, cantidad):
                self.llamadas += cantidad

        motor = ChatEngine.__new__(ChatEngine)
        motor.estado_emocional = Emociones()
        motor.estado_mood = MoodEliFalso()
        motor.modulo_emociones = types.SimpleNamespace()

        motor.ejecutar_decaimiento()

        self.assertEqual(motor.estado_emocional.llamadas, 1)
        self.assertEqual(motor.estado_mood.llamadas, 0)
        self.assertIsNone(motor.estado_mood.ultimo_estado)


class ConversacionGrupalTests(unittest.TestCase):

    class MemoriaGrupoFalsa:
        def construir_contexto(self):
            return "Memoria de prueba"

    class MiembroFalso:
        def __init__(self, respuestas):
            self.respuestas = list(respuestas)
            self.prompts = []
            self.entradas = []
            self.analisis = 0
            self.decaimientos = 0

        def analizar_y_actualizar_emociones(self, mensaje):
            self.analisis += 1

        def obtener_respuesta(self, mensajes=None, guardar=True):
            self.prompts.append(mensajes[0]["content"])
            self.entradas.append(mensajes[0])
            self.assert_no_guardar = guardar
            return self.respuestas.pop(0)

        def ejecutar_decaimiento(self):
            self.decaimientos += 1

    def crear_grupo(self, eli, aurora):
        requests_falso = types.ModuleType("requests")
        with patch.dict(sys.modules, {"requests": requests_falso}):
            from core.group_chat_engine import GroupChatEngine

        grupo = GroupChatEngine.__new__(GroupChatEngine)
        grupo.grupo = "principal"
        grupo.nombres = ["eli", "aurora"]
        grupo.miembros = {"eli": eli, "aurora": aurora}
        grupo.memoria_grupo = self.MemoriaGrupoFalsa()
        grupo.historial_grupo = []
        return grupo

    def test_miembros_escuchan_turnos_y_no_contaminan_historial_individual(self):
        eli = self.MiembroFalso(["Idea de Eli", "Eli responde después"])
        aurora = self.MiembroFalso(["Idea de Eli", "Perspectiva de Aurora", "Aurora continúa"])
        grupo = self.crear_grupo(eli, aurora)

        primero = grupo.enviar_mensaje("¿Qué construimos?")
        segundo = grupo.enviar_mensaje("Continúen")

        self.assertEqual(primero["aurora"], "Perspectiva de Aurora")
        self.assertIn("ELI: Idea de Eli", aurora.prompts[0])
        self.assertIn("AURORA: Perspectiva de Aurora", eli.prompts[1])
        self.assertEqual(segundo["eli"], "Eli responde después")
        self.assertTrue(all(valor is False for valor in [eli.assert_no_guardar, aurora.assert_no_guardar]))
        self.assertEqual(eli.analisis, 2)
        self.assertEqual(aurora.analisis, 2)
        self.assertEqual(eli.decaimientos, 2)
        self.assertEqual(aurora.decaimientos, 2)
        self.assertEqual([m["turn"] for m in grupo.historial_grupo], [1, 1, 1, 2, 2, 2])

    def test_imagen_grupal_llega_a_eli_y_aurora(self):
        eli = self.MiembroFalso(["Eli observa"])
        aurora = self.MiembroFalso(["Aurora observa"])
        grupo = self.crear_grupo(eli, aurora)
        adjunto = {"mime": "image/png", "path": "imagen.png", "name": "imagen.png"}

        grupo.enviar_mensaje("Miren esta imagen", adjuntos=[adjunto])

        self.assertEqual(eli.entradas[0]["attachments"], [adjunto])
        self.assertEqual(aurora.entradas[0]["attachments"], [adjunto])


class HistorialGrupalTests(unittest.TestCase):

    class GrupoFalso:
        def __init__(self):
            self.historial_grupo = []

        def enviar_mensaje(self, mensaje, adjuntos=None):
            self.historial_grupo.extend([
                {"role": "user", "content": mensaje, "turn": 1, "attachments": adjuntos or []},
                {"role": "assistant", "member": "eli", "content": "Eli responde", "turn": 1},
                {"role": "assistant", "member": "aurora", "content": "Aurora responde", "turn": 1},
            ])
            return {"eli": "Eli responde", "aurora": "Aurora responde"}

    def cargar_api(self):
        webview_falso = types.ModuleType("webview")
        with patch.dict(sys.modules, {"webview": webview_falso}):
            from ui.web_app import ElizyumAPI
        return ElizyumAPI

    def test_guarda_recupera_y_crea_nueva_conversacion_grupal(self):
        ElizyumAPI = self.cargar_api()

        with tempfile.TemporaryDirectory() as carpeta:
            grupo = self.GrupoFalso()
            api = ElizyumAPI({"grupo": grupo}, base_dir=carpeta)
            api.enviar_mensaje("grupo", "Primer mensaje")
            primera_id = api.obtener_conversacion_actual("grupo")

            grupo_reabierto = self.GrupoFalso()
            api_reabierta = ElizyumAPI({"grupo": grupo_reabierto}, base_dir=carpeta)

            self.assertEqual(grupo_reabierto.historial_grupo, grupo.historial_grupo)
            self.assertEqual(api_reabierta.obtener_conversacion_actual("grupo"), primera_id)

            api_reabierta.nueva_conversacion("grupo")
            self.assertEqual(grupo_reabierto.historial_grupo, [])
            api_reabierta.enviar_mensaje("grupo", "Segunda conversación")
            segunda_id = api_reabierta.obtener_conversacion_actual("grupo")

            self.assertNotEqual(primera_id, segunda_id)
            recuperada = api_reabierta.cargar_conversacion("grupo", primera_id)
            self.assertEqual(recuperada[0]["content"], "Primer mensaje")

    def test_imagen_se_valida_guarda_y_prepara_para_historial(self):
        ElizyumAPI = self.cargar_api()
        png_minimo = b"\x89PNG\r\n\x1a\n" + b"datos-de-prueba"
        data_url = "data:image/png;base64," + base64.b64encode(png_minimo).decode("ascii")

        with tempfile.TemporaryDirectory() as carpeta:
            api = ElizyumAPI({"grupo": self.GrupoFalso()}, base_dir=carpeta)
            guardados = api._guardar_adjuntos("grupo", [{
                "name": "captura.png",
                "data_url": data_url,
            }])
            preparados = api._adjuntos_para_ui(guardados)

            self.assertEqual(len(guardados), 1)
            self.assertTrue(Path(guardados[0]["path"]).exists())
            self.assertEqual(preparados[0]["name"], "captura.png")
            self.assertTrue(preparados[0]["url"].startswith("file:"))

    def test_txt_se_valida_guarda_y_prepara_para_historial(self):
        ElizyumAPI = self.cargar_api()
        contenido = "Ideas para Elizyum".encode("utf-8")
        data_url = "data:text/plain;base64," + base64.b64encode(contenido).decode("ascii")

        with tempfile.TemporaryDirectory() as carpeta:
            api = ElizyumAPI({"grupo": self.GrupoFalso()}, base_dir=carpeta)
            guardados = api._guardar_adjuntos("grupo", [{
                "name": "ideas.txt",
                "data_url": data_url,
            }])
            preparados = api._adjuntos_para_ui(guardados)

            self.assertEqual(guardados[0]["type"], "text")
            self.assertEqual(Path(guardados[0]["path"]).read_text(encoding="utf-8"), "Ideas para Elizyum")
            self.assertEqual(preparados[0]["type"], "text")


if __name__ == "__main__":
    unittest.main()
