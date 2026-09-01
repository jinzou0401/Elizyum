import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Memoria:

    def __init__(self, nombre):

        self.nombre = nombre
        self.archivo = BASE_DIR / "data" / nombre / "memoria.json"

        self.datos = self.cargar()

    # --------------------------------------------------------
    # CARGAR / VALORES BASE
    # --------------------------------------------------------

    def cargar(self):

        if not self.archivo.exists():
            return self._valores_base()

        try:

            with open(
                self.archivo,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return self._valores_base()

    def _valores_base(self):

        return {
            "usuario": {"nombre": ""},
            "preferencias": {},
            "informacion_importante": []
        }

    # --------------------------------------------------------
    # GUARDAR
    # --------------------------------------------------------

    def guardar(self):

        self.archivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.archivo,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.datos,
                f,
                ensure_ascii=False,
                indent=4
            )

    # --------------------------------------------------------
    # ACTUALIZAR UN DATO
    # --------------------------------------------------------

    def actualizar(self, categoria, clave, valor):

        if categoria not in self.datos:
            self.datos[categoria] = {}

        self.datos[categoria][clave] = valor

        self.guardar()

        return self.datos

    # --------------------------------------------------------
    # INFORMACIÓN IMPORTANTE
    # --------------------------------------------------------

    def agregar_informacion_importante(self, informacion):

        if "informacion_importante" not in self.datos:
            self.datos["informacion_importante"] = []

        if informacion not in self.datos["informacion_importante"]:
            self.datos["informacion_importante"].append(informacion)

        self.guardar()

        return self.datos

    def eliminar_informacion_importante(self, informacion):

        lista = self.datos.get("informacion_importante", [])

        informacion = informacion.strip().lower()

        self.datos["informacion_importante"] = [
            dato
            for dato in lista
            if informacion not in dato.strip().lower()
        ]

        self.guardar()

        return self.datos