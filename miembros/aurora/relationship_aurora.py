
# ============================================================
# ELIZYUM - AURORA RELATIONSHIP
# miembros/aurora/relationship_aurora.py
#
# Relación específica de Aurora.
# Estado persistente mediante JSON.
#
# Aurora considera a Jinzou su mejor amigo.
# ============================================================

import json
from pathlib import Path


# ============================================================
# IDENTIDAD
# ============================================================

NOMBRE = "Aurora"

USUARIO = "Jinzou"


# ============================================================
# RUTA DE DATOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ARCHIVO_RELACION = (
    BASE_DIR
    / "data"
    / "aurora"
    / "relacion.json"
)


# ============================================================
# RELACIÓN BASE
# ============================================================

RELACION_BASE_AURORA = {

    "confianza": 85,

    "cercania": 90,

    "comprension": 80,

    "vinculo": 88,

    "tipo_relacion": "mejor_amiga"
}


# ============================================================
# LIMITAR
# ============================================================

def limitar(
    valor,
    minimo=0,
    maximo=100
):

    try:

        valor = int(valor)

    except (
        TypeError,
        ValueError
    ):

        valor = minimo

    return max(
        minimo,
        min(
            maximo,
            valor
        )
    )


# ============================================================
# CARGAR RELACIÓN
# ============================================================

def cargar_relacion():

    if not ARCHIVO_RELACION.exists():

        return RELACION_BASE_AURORA.copy()

    try:

        with open(
            ARCHIVO_RELACION,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(
                archivo
            )

        if not isinstance(
            datos,
            dict
        ):

            return RELACION_BASE_AURORA.copy()

        resultado = (
            RELACION_BASE_AURORA.copy()
        )

        for clave in (
            "confianza",
            "cercania",
            "comprension",
            "vinculo"
        ):

            if clave in datos:

                resultado[clave] = limitar(
                    datos[clave]
                )

        if "tipo_relacion" in datos:

            resultado[
                "tipo_relacion"
            ] = str(
                datos[
                    "tipo_relacion"
                ]
            )

        return resultado

    except Exception:

        return RELACION_BASE_AURORA.copy()


# ============================================================
# GUARDAR RELACIÓN
# ============================================================

def guardar_relacion(
    relacion
):

    ARCHIVO_RELACION.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        ARCHIVO_RELACION,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            relacion,
            archivo,
            ensure_ascii=False,
            indent=4
        )


# ============================================================
# CLASE RELACIÓN
# ============================================================

class RelationshipAurora:

    def __init__(self):

        self.relacion = (
            cargar_relacion()
        )


    # ========================================================
    # OBTENER
    # ========================================================

    def obtener(self):

        return self.relacion.copy()


    # ========================================================
    # NIVEL DE VÍNCULO
    # ========================================================

    def obtener_nivel_vinculo(self):

        return self.relacion.get(
            "vinculo",
            0
        )


    # ========================================================
    # DESCRIBIR
    # ========================================================

    def describir(self):

        return (
            "Aurora considera a "
            f"{USUARIO} su mejor amigo "
            "y mantiene un vínculo cercano, "
            "confiado y estable."
        )


    # ========================================================
    # CAMBIAR
    # ========================================================

    def cambiar(
        self,
        atributo,
        cantidad
    ):

        if atributo not in {
            "confianza",
            "cercania",
            "comprension",
            "vinculo"
        }:

            return self.obtener()

        self.relacion[
            atributo
        ] = limitar(
            self.relacion[
                atributo
            ] + cantidad
        )

        guardar_relacion(
            self.relacion
        )

        return self.obtener()


    # ========================================================
    # ESTABLECER
    # ========================================================

    def establecer(
        self,
        atributo,
        valor
    ):

        if atributo not in {
            "confianza",
            "cercania",
            "comprension",
            "vinculo"
        }:

            return self.obtener()

        self.relacion[
            atributo
        ] = limitar(
            valor
        )

        guardar_relacion(
            self.relacion
        )

        return self.obtener()


    # ========================================================
    # REINICIAR
    # ========================================================

    def reiniciar(self):

        self.relacion = (
            RELACION_BASE_AURORA.copy()
        )

        guardar_relacion(
            self.relacion
        )

        return self.obtener()


    # ========================================================
    # PROCESAR CONTEXTO
    # ========================================================

    def procesar_contexto(
        self,
        contexto
    ):

        if not isinstance(
            contexto,
            dict
        ):

            return self.obtener()

        evento = contexto.get(
            "evento_relacional"
        )

        if not isinstance(
            evento,
            dict
        ):

            return self.obtener()

        nombre = evento.get(
            "evento"
        )

        intensidad = limitar(
            evento.get(
                "intensidad",
                0
            ),
            0,
            100
        )

        cambios = {

            "gesto_carinoso": {
                "cercania": 2,
                "confianza": 1,
                "vinculo": 1
            },

            "apoyo": {
                "cercania": 2,
                "confianza": 2,
                "vinculo": 1
            },

            "cumplio_promesa": {
                "confianza": 4,
                "vinculo": 3
            },

            "reconciliacion": {
                "cercania": 3,
                "confianza": 2,
                "vinculo": 2
            },

            "distancia": {
                "cercania": -2,
                "vinculo": -1
            },

            "mentira": {
                "confianza": -4,
                "vinculo": -2
            },

            "discusion": {
                "cercania": -2,
                "confianza": -1
            },

            "romper_promesa": {
                "confianza": -5,
                "vinculo": -3
            }
        }

        if nombre not in cambios:

            return self.obtener()

        factor = (
            intensidad / 100
        )

        for atributo, cambio in (
            cambios[nombre].items()
        ):

            ajuste = round(
                cambio * factor
            )

            if ajuste:

                self.relacion[
                    atributo
                ] = limitar(
                    self.relacion[
                        atributo
                    ] + ajuste
                )

        guardar_relacion(
            self.relacion
        )

        return self.obtener()


# ============================================================
# INSTANCIA PRINCIPAL
# ============================================================

relationships = RelationshipAurora()


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - AURORA RELATIONSHIP")
    print("=" * 70)

    print()

    print("ARCHIVO:")

    print(
        ARCHIVO_RELACION
    )

    print()

    print("RELACIÓN:")

    print(
        relationships.obtener()
    )

    print()

    print(
        relationships.describir()
    )

    print()

    print("OK")
from emotions.relationships import GestorRelacion

aurora_relationships = GestorRelacion(
    "aurora",
    base=RELACION_BASE_AURORA
)