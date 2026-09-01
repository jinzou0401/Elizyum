
# ============================================================
# ELIZYUM - GROUP MEMORY
# memory/group_memory.py
# ============================================================

import json
from pathlib import Path


# ============================================================
# RUTA BASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

GROUPS_DIR = BASE_DIR / "data" / "groups"


# ============================================================
# CLASE MEMORIA DE GRUPO
# ============================================================

class GroupMemory:

    def __init__(self, grupo):

        self.grupo = str(grupo).strip().lower()

        if not self.grupo:
            raise ValueError(
                "El nombre del grupo no puede estar vacío."
            )

        self.archivo = (
            GROUPS_DIR
            / self.grupo
            / "memoria.json"
        )

        self.datos = self.cargar()

    # ========================================================
    # VALORES BASE
    # ========================================================

    def _valores_base(self):

        return {
            "grupo": self.grupo,
            "miembros": [],
            "informacion_importante": [],
            "preferencias": {},
            "eventos": [],
            "notas": []
        }

    # ========================================================
    # CARGAR
    # ========================================================

    def cargar(self):

        if not self.archivo.exists():

            datos = self._valores_base()

            self.guardar(datos)

            return datos

        try:

            with open(
                self.archivo,
                "r",
                encoding="utf-8"
            ) as archivo:

                datos = json.load(archivo)

            if not isinstance(datos, dict):

                return self._valores_base()

            return datos

        except Exception:

            return self._valores_base()

    # ========================================================
    # GUARDAR
    # ========================================================

    def guardar(self, datos=None):

        if datos is not None:
            self.datos = datos

        self.archivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.archivo,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                self.datos,
                archivo,
                ensure_ascii=False,
                indent=4
            )

        return self.datos

    # ========================================================
    # ACTUALIZAR
    # ========================================================

    def actualizar(
        self,
        categoria,
        clave,
        valor
    ):

        if categoria not in self.datos:
            self.datos[categoria] = {}

        if not isinstance(
            self.datos[categoria],
            dict
        ):
            self.datos[categoria] = {}

        self.datos[categoria][clave] = valor

        self.guardar()

        return self.datos

    # ========================================================
    # AGREGAR MIEMBRO
    # ========================================================

    def agregar_miembro(self, nombre):

        nombre = str(nombre).strip().lower()

        if not nombre:
            return self.datos

        miembros = self.datos.get(
            "miembros",
            []
        )

        if not isinstance(miembros, list):
            miembros = []

        if nombre not in miembros:
            miembros.append(nombre)

        self.datos["miembros"] = miembros

        self.guardar()

        return self.datos

    # ========================================================
    # ELIMINAR MIEMBRO
    # ========================================================

    def eliminar_miembro(self, nombre):

        nombre = str(nombre).strip().lower()

        miembros = self.datos.get(
            "miembros",
            []
        )

        if not isinstance(miembros, list):
            miembros = []

        self.datos["miembros"] = [
            miembro
            for miembro in miembros
            if miembro != nombre
        ]

        self.guardar()

        return self.datos

    # ========================================================
    # AGREGAR INFORMACIÓN
    # ========================================================

    def agregar_informacion(self, informacion):

        informacion = str(
            informacion
        ).strip()

        if not informacion:
            return self.datos

        lista = self.datos.get(
            "informacion_importante",
            []
        )

        if not isinstance(lista, list):
            lista = []

        if informacion not in lista:
            lista.append(informacion)

        self.datos[
            "informacion_importante"
        ] = lista

        self.guardar()

        return self.datos

    # ========================================================
    # ELIMINAR INFORMACIÓN
    # ========================================================

    def eliminar_informacion(self, informacion):

        informacion = str(
            informacion
        ).strip().lower()

        lista = self.datos.get(
            "informacion_importante",
            []
        )

        if not isinstance(lista, list):
            lista = []

        self.datos[
            "informacion_importante"
        ] = [
            dato
            for dato in lista
            if informacion not in str(dato).strip().lower()
        ]

        self.guardar()

        return self.datos

    # ========================================================
    # PREFERENCIAS
    # ========================================================

    def establecer_preferencia(
        self,
        clave,
        valor
    ):

        preferencias = self.datos.get(
            "preferencias",
            {}
        )

        if not isinstance(
            preferencias,
            dict
        ):
            preferencias = {}

        preferencias[clave] = valor

        self.datos[
            "preferencias"
        ] = preferencias

        self.guardar()

        return self.datos

    # ========================================================
    # EVENTOS
    # ========================================================

    def agregar_evento(self, evento):

        if not isinstance(evento, dict):

            evento = {
                "descripcion": str(evento)
            }

        eventos = self.datos.get(
            "eventos",
            []
        )

        if not isinstance(eventos, list):
            eventos = []

        eventos.append(evento)

        self.datos["eventos"] = eventos

        self.guardar()

        return self.datos

    # ========================================================
    # NOTAS
    # ========================================================

    def agregar_nota(self, nota):

        nota = str(nota).strip()

        if not nota:
            return self.datos

        notas = self.datos.get(
            "notas",
            []
        )

        if not isinstance(notas, list):
            notas = []

        notas.append(nota)

        self.datos["notas"] = notas

        self.guardar()

        return self.datos

    # ========================================================
    # OBTENER
    # ========================================================

    def obtener(self):

        return self.datos.copy()

    # ========================================================
    # CONTEXTO PARA LAS IAS
    # ========================================================

    def construir_contexto(self):

        return f"""
========== MEMORIA DEL GRUPO ==========

Grupo:
{self.grupo}

Miembros:
{self.datos.get("miembros", [])}

Información importante:
{self.datos.get("informacion_importante", [])}

Preferencias:
{self.datos.get("preferencias", {})}

Eventos:
{self.datos.get("eventos", [])}

Notas:
{self.datos.get("notas", [])}

========================================
""".strip()


# ============================================================
# ACCESO RÁPIDO
# ============================================================

def cargar_memoria_grupo(grupo):

    return GroupMemory(grupo)


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - GROUP MEMORY")
    print("=" * 70)

    memoria = GroupMemory("principal")

    memoria.agregar_miembro("eli")
    memoria.agregar_miembro("aurora")

    print()
    print("ARCHIVO:")
    print(memoria.archivo)

    print()
    print("MEMORIA:")
    print(memoria.obtener())

    print()
    print("CONTEXTO:")
    print(memoria.construir_contexto())

    print()
    print("GROUP MEMORY OK")
