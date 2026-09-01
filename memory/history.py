import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent


class Historial:

    def __init__(self, nombre):

        self.nombre = nombre
        self.carpeta = BASE_DIR / "data" / nombre / "conversations"

        self.carpeta.mkdir(
            parents=True,
            exist_ok=True
        )

    def nombre_archivo(self):

        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        return self.carpeta / f"{fecha}.json"

    def guardar_conversacion(self, messages, archivo):

        datos = {
            "fecha": datetime.now().isoformat(),
            "messages": messages
        }

        with open(
            archivo,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                datos,
                f,
                ensure_ascii=False,
                indent=4
            )

    def cargar_conversacion(self, archivo):

        if not archivo.exists():
            return None

        try:

            with open(
                archivo,
                "r",
                encoding="utf-8"
            ) as f:

                datos = json.load(f)

            return datos.get("messages", [])

        except Exception:

            return None

    def ultima_conversacion(self):

        archivos = list(self.carpeta.glob("*.json"))

        if not archivos:
            return None

        archivos.sort(
            key=lambda archivo: archivo.stat().st_mtime,
            reverse=True
        )

        return archivos[0]