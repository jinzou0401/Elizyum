import json
import base64
import binascii
import re
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import webview


class ElizyumAPI:
    MIME_IMAGENES = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }
    MIME_ARCHIVOS = {"text/plain": ".txt"}
    MAX_IMAGEN = 8 * 1024 * 1024
    MAX_TEXTO = 2 * 1024 * 1024
    MAX_ADJUNTOS = 4

    def __init__(self, motores, base_dir=None):
        self.motores = motores
        self.base_dir = (
            Path(base_dir)
            if base_dir is not None
            else Path(__file__).resolve().parent.parent
        )
        self.estado_ui_archivo = self.base_dir / "data" / "ui_state.json"
        self.grupo_dir = self.base_dir / "data" / "groups" / "principal" / "conversations"
        self.adjuntos_dir = self.base_dir / "data" / "attachments"
        self.grupo_dir.mkdir(parents=True, exist_ok=True)
        self.grupo_archivo = self._ultimo_archivo(self.grupo_dir)
        if self.grupo_archivo:
            self.motores["grupo"].historial_grupo = self._leer_mensajes(self.grupo_archivo)

    def obtener_estado_ui(self):
        estado_base = {"chat_activo": "eli", "seleccionadas": {"eli": "", "aurora": "", "grupo": ""}}
        try:
            datos = json.loads(self.estado_ui_archivo.read_text(encoding="utf-8"))
            if isinstance(datos, dict):
                estado_base["chat_activo"] = datos.get("chat_activo", "eli")
                estado_base["seleccionadas"].update(datos.get("seleccionadas", {}))
        except Exception:
            pass
        return estado_base

    def guardar_estado_ui(self, nombre, identificador=""):
        nombre = str(nombre).lower()
        estado = self.obtener_estado_ui()
        estado["chat_activo"] = nombre if nombre in self.motores else "eli"
        estado["seleccionadas"][nombre] = str(identificador or "")
        self.estado_ui_archivo.parent.mkdir(parents=True, exist_ok=True)
        self.estado_ui_archivo.write_text(json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8")
        return estado

    def obtener_conversacion_actual(self, nombre):
        nombre = str(nombre).lower()
        if nombre == "grupo":
            return self.grupo_archivo.name if self.grupo_archivo else ""
        archivo = getattr(self.motores[nombre], "archivo_conversacion", None)
        return Path(archivo).name if archivo else ""

    def _ultimo_archivo(self, carpeta):
        archivos = sorted(carpeta.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        return archivos[0] if archivos else None

    def _leer_mensajes(self, archivo):
        try:
            datos = json.loads(archivo.read_text(encoding="utf-8"))
            return datos.get("messages", []) if isinstance(datos, dict) else []
        except Exception:
            return []

    def _guardar_adjuntos(self, nombre, adjuntos):
        if not adjuntos:
            return []
        if not isinstance(adjuntos, list) or len(adjuntos) > self.MAX_ADJUNTOS:
            raise ValueError("Puedes adjuntar hasta 4 imágenes por mensaje.")

        guardados = []
        destino = self.adjuntos_dir / nombre
        destino.mkdir(parents=True, exist_ok=True)

        for adjunto in adjuntos:
            if not isinstance(adjunto, dict):
                raise ValueError("Adjunto no válido.")

            nombre_original = Path(str(adjunto.get("name", "imagen"))).name[:120]
            data_url = str(adjunto.get("data_url", ""))
            coincidencia = re.fullmatch(
                r"data:(image/(?:jpeg|png|webp)|text/plain);base64,([A-Za-z0-9+/=\r\n]+)",
                data_url,
            )
            if not coincidencia:
                raise ValueError("Solo se permiten imágenes JPG, PNG, WebP o archivos TXT.")

            mime, contenido_base64 = coincidencia.groups()
            try:
                contenido = base64.b64decode(contenido_base64, validate=True)
            except (binascii.Error, ValueError):
                raise ValueError("La imagen adjunta está dañada.")

            limite = self.MAX_TEXTO if mime == "text/plain" else self.MAX_IMAGEN
            if not contenido or len(contenido) > limite:
                raise ValueError("Las imágenes admiten 8 MB y los TXT 2 MB como máximo.")

            if mime == "text/plain":
                try:
                    contenido.decode("utf-8")
                except UnicodeDecodeError:
                    raise ValueError("El archivo TXT debe estar guardado en UTF-8.")

            firma_valida = (
                (mime == "image/jpeg" and contenido.startswith(b"\xff\xd8\xff"))
                or (mime == "image/png" and contenido.startswith(b"\x89PNG\r\n\x1a\n"))
                or (
                    mime == "image/webp"
                    and contenido.startswith(b"RIFF")
                    and contenido[8:12] == b"WEBP"
                )
            )
            if mime != "text/plain" and not firma_valida:
                raise ValueError("El contenido no corresponde al formato de imagen indicado.")

            extension = {**self.MIME_IMAGENES, **self.MIME_ARCHIVOS}[mime]
            archivo = destino / f"{uuid4().hex}{extension}"
            archivo.write_bytes(contenido)
            guardados.append({
                "type": "text" if mime == "text/plain" else "image",
                "name": nombre_original,
                "mime": mime,
                "path": str(archivo),
            })

        return guardados

    def _adjuntos_para_ui(self, adjuntos):
        resultado = []
        if not isinstance(adjuntos, list):
            return resultado
        for adjunto in adjuntos:
            if not isinstance(adjunto, dict):
                continue
            ruta = Path(str(adjunto.get("path", "")))
            if ruta.exists():
                resultado.append({
                    "type": str(adjunto.get("type", "image")),
                    "name": str(adjunto.get("name", "Imagen")),
                    "mime": str(adjunto.get("mime", "")),
                    "url": ruta.resolve().as_uri(),
                })
        return resultado

    def _mensaje_para_ui(self, mensaje):
        copia = dict(mensaje)
        copia["attachments"] = self._adjuntos_para_ui(mensaje.get("attachments", []))
        return copia

    def _titulo(self, mensajes):
        for mensaje in mensajes:
            if mensaje.get("role") == "user":
                texto = str(mensaje.get("content", "")).strip()
                if texto.startswith("[CONVERSACIÓN GRUPAL]"):
                    continue
                return texto[:34] + ("…" if len(texto) > 34 else "")
        return "Conversación nueva"

    def listar_conversaciones(self, nombre):
        nombre = str(nombre).lower()
        carpeta = self.grupo_dir if nombre == "grupo" else self.motores[nombre].historial.carpeta
        resultado = []
        for archivo in sorted(carpeta.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            mensajes = self._leer_mensajes(archivo)
            resultado.append({"id": archivo.name, "titulo": self._titulo(mensajes)})
        return resultado

    def cargar_conversacion(self, nombre, identificador):
        nombre = str(nombre).lower()
        identificador = str(identificador)
        if Path(identificador).name != identificador:
            raise ValueError("Conversación no válida.")
        if nombre == "grupo":
            archivo = self.grupo_dir / identificador
            self.grupo_archivo = archivo
            self.motores[nombre].historial_grupo = self._leer_mensajes(archivo)
        else:
            motor = self.motores[nombre]
            archivo = motor.historial.carpeta / identificador
            motor.messages = motor.historial.cargar_conversacion(archivo) or []
            motor.archivo_conversacion = archivo
        return self.obtener_historial(nombre)

    def _guardar_grupo(self):
        if self.grupo_archivo is None:
            nombre = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f.json")
            self.grupo_archivo = self.grupo_dir / nombre
        datos = {"fecha": datetime.now().isoformat(), "messages": self.motores["grupo"].historial_grupo}
        self.grupo_archivo.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")

    def obtener_historial(self, nombre):
        nombre = str(nombre).lower()
        motor = self.motores[nombre]
        if nombre == "grupo":
            return [
                self._mensaje_para_ui(mensaje)
                for mensaje in getattr(motor, "historial_grupo", [])
                if isinstance(mensaje, dict)
            ]
        # El motor grupal reutiliza los motores individuales y añade un
        # mensaje técnico al historial de cada miembro. Ese contexto es para
        # el modelo, nunca para la interfaz individual.
        historial_visible = []
        omitir_respuesta_grupal = False

        for mensaje in getattr(motor, "messages", []):
            if not isinstance(mensaje, dict):
                continue

            role = mensaje.get("role")
            contenido = mensaje.get("content", "")

            if (
                role == "user"
                and isinstance(contenido, str)
                and contenido.lstrip().startswith("[CONVERSACIÓN GRUPAL]")
            ):
                omitir_respuesta_grupal = True
                continue

            if role == "assistant" and omitir_respuesta_grupal:
                omitir_respuesta_grupal = False
                continue

            if role in {"user", "assistant"}:
                historial_visible.append(self._mensaje_para_ui(mensaje))

        return historial_visible

    def enviar_mensaje(self, nombre, mensaje, adjuntos=None):
        nombre = str(nombre).lower()
        mensaje = str(mensaje).strip()
        if nombre not in self.motores or (not mensaje and not adjuntos):
            raise ValueError("Mensaje o conversación no válidos.")
        adjuntos_guardados = self._guardar_adjuntos(nombre, adjuntos)
        texto_modelo = mensaje or "Observa y comenta la imagen adjunta."
        motor = self.motores[nombre]
        if nombre == "grupo":
            resultados = motor.enviar_mensaje(texto_modelo, adjuntos=adjuntos_guardados)
            self._guardar_grupo()
            return [{"autor": n.capitalize(), "mensaje": r} for n, r in resultados.items()]

        comando = motor.procesar_comando(texto_modelo) if not adjuntos_guardados else "no_es_comando"
        if comando != "no_es_comando":
            return [{"autor": nombre.capitalize(), "mensaje": comando}] if comando else []

        motor.analizar_y_actualizar_emociones(texto_modelo)
        motor.registrar_mensaje_usuario(texto_modelo, adjuntos=adjuntos_guardados)
        respuesta = motor.obtener_respuesta()
        motor.ejecutar_decaimiento()
        return [{"autor": nombre.capitalize(), "mensaje": respuesta}]

    def nueva_conversacion(self, nombre):
        nombre = str(nombre).lower()
        motor = self.motores[nombre]
        if nombre == "grupo":
            motor.historial_grupo = []
            self.grupo_archivo = None
        else:
            motor.nueva_conversacion()
        return True


def iniciar_app(motores):
    pagina = Path(__file__).resolve().parent / "web" / "index.html"
    window = webview.create_window(
        "Elizyum",
        pagina.as_uri(),
        js_api=ElizyumAPI(motores),
        width=1180,
        height=780,
        min_size=(920, 620),
        background_color="#EEF6FF",
    )
    webview.start(debug=False)
    return window
