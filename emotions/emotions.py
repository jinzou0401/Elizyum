
# ============================================================
# ELIZYUM - EMOTION ENGINE
# emotions/emotions.py
#
# Motor central de emociones de Elizyum.
#
# Este archivo NO pertenece a ningún miembro específico.
#
# Responsabilidades:
#
# - cargar emociones
# - guardar emociones
# - obtener estado emocional
# - modificar emociones
# - establecer emociones
# - calcular emoción dominante
# - calcular estado de ánimo
# - aplicar relaciones entre emociones
# - permitir que cada miembro tenga su propio estado
#
# Uso esperado:
#
# emotions.py
#      ↓
# emotions_eli.py
# emotions_aurora.py
# emotions_martha.py
# emotions_oro.py
#
# ============================================================

import json
from pathlib import Path

from emotions.emotion_links import aplicar_relaciones_emocionales


# ============================================================
# CONFIGURACIÓN BASE
# ============================================================

EMOCIONES_BASE = {
    "felicidad": 50,
    "tristeza": 0,
    "enojo": 0,
    "sorpresa": 0,
    "afecto": 50,
    "curiosidad": 50,
    "diversion": 30
}


# ============================================================
# UTILIDADES
# ============================================================

def limitar(valor, minimo=0, maximo=100):
    """
    Limita un valor al rango indicado.
    """

    try:
        valor = int(float(valor))
    except (TypeError, ValueError):
        valor = minimo

    return max(
        minimo,
        min(maximo, valor)
    )


def obtener_emocion(
    emociones,
    nombre,
    defecto=0
):
    """
    Obtiene una emoción de forma segura.
    """

    if not isinstance(emociones, dict):
        return limitar(defecto)

    return limitar(
        emociones.get(
            nombre,
            defecto
        )
    )


# ============================================================
# ESTADO EMOCIONAL
# ============================================================

class EstadoEmocional:

    def __init__(
        self,
        nombre,
        emociones_base=None,
        base_dir=None
    ):
        """
        Crea un estado emocional independiente.

        Parámetros:

        nombre:
            Identificador del miembro.

        emociones_base:
            Diccionario opcional con los valores iniciales
            específicos del miembro.

        base_dir:
            Directorio raíz opcional del proyecto.
        """

        self.nombre = nombre

        # ----------------------------------------------------
        # DIRECTORIO DEL PROYECTO
        # ----------------------------------------------------

        if base_dir is None:

            base_dir = (
                Path(__file__)
                .resolve()
                .parent
                .parent
            )

        self.base_dir = Path(
            base_dir
        )

        # ----------------------------------------------------
        # ARCHIVO DEL MIEMBRO
        # ----------------------------------------------------

        self.archivo = (
            self.base_dir
            / "data"
            / self.nombre
            / "emociones.json"
        )

        # ----------------------------------------------------
        # EMOCIONES BASE
        # ----------------------------------------------------

        if isinstance(
            emociones_base,
            dict
        ):

            self.emociones_base = {
                **EMOCIONES_BASE,
                **emociones_base
            }

        else:

            self.emociones_base = (
                EMOCIONES_BASE.copy()
            )

        # ----------------------------------------------------
        # CARGAR ESTADO
        # ----------------------------------------------------

        self.emociones = self.cargar()


    # ========================================================
    # CARGAR
    # ========================================================

    def cargar(self):
        """
        Carga el estado emocional desde JSON.

        Si el archivo no existe o presenta un error,
        utiliza los valores base.
        """

        if not self.archivo.exists():

            return self.emociones_base.copy()

        try:

            with open(
                self.archivo,
                "r",
                encoding="utf-8"
            ) as f:

                datos = json.load(f)

            if not isinstance(
                datos,
                dict
            ):

                return self.emociones_base.copy()

            emociones = {
                **self.emociones_base,
                **datos
            }

            # ----------------------------------------------
            # Normalizar valores
            # ----------------------------------------------

            for nombre in emociones:

                emociones[nombre] = limitar(
                    emociones[nombre]
                )

            return emociones

        except (
            OSError,
            json.JSONDecodeError,
            TypeError,
            ValueError
        ):

            return self.emociones_base.copy()


    # ========================================================
    # GUARDAR
    # ========================================================

    def guardar(self):
        """
        Guarda el estado emocional actual.
        """

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
                self.emociones,
                f,
                ensure_ascii=False,
                indent=4
            )


    # ========================================================
    # OBTENER
    # ========================================================

    def obtener(self):
        """
        Devuelve una copia del estado emocional.
        """

        return self.emociones.copy()


    # ========================================================
    # OBTENER UNA EMOCIÓN
    # ========================================================

    def obtener_emocion(
        self,
        nombre,
        defecto=0
    ):
        """
        Devuelve el valor de una emoción.
        """

        return obtener_emocion(
            self.emociones,
            nombre,
            defecto
        )


    # ========================================================
    # CAMBIAR
    # ========================================================

    def cambiar(
        self,
        nombre,
        cantidad
    ):
        """
        Modifica una emoción.

        La emoción queda limitada entre 0 y 100.
        """

        if nombre not in self.emociones:

            return self.emociones.copy()

        try:

            cantidad = float(
                cantidad
            )

        except (
            TypeError,
            ValueError
        ):

            cantidad = 0

        self.emociones[nombre] = limitar(
            self.emociones[nombre]
            + cantidad
        )

        self.guardar()

        return self.emociones.copy()


    # ========================================================
    # ESTABLECER
    # ========================================================

    def establecer(
        self,
        nombre,
        valor
    ):
        """
        Establece directamente el valor de una emoción.
        """

        if nombre not in self.emociones:

            return self.emociones.copy()

        self.emociones[nombre] = limitar(
            valor
        )

        self.guardar()

        return self.emociones.copy()


    # ========================================================
    # EMOCIÓN DOMINANTE
    # ========================================================

    def emocion_dominante(self):
        """
        Devuelve la emoción con mayor intensidad.
        """

        if not self.emociones:

            return None

        return max(
            self.emociones,
            key=self.emociones.get
        )


    # ========================================================
    # DESCRIBIR ESTADO
    # ========================================================

    def describir_estado(self):
        """
        Devuelve la emoción dominante y su intensidad.
        """

        dominante = (
            self.emocion_dominante()
        )

        if dominante is None:

            return {
                "emocion": None,
                "intensidad": 0
            }

        return {
            "emocion": dominante,
            "intensidad":
                self.emociones[dominante]
        }


    # ========================================================
    # DECAIMIENTO
    # ========================================================

    def decaer(
        self,
        cantidad=1
    ):
        """
        Acerca progresivamente las emociones
        a sus valores base.
        """

        cantidad = limitar(
            cantidad,
            0,
            100
        )

        for nombre in self.emociones:

            base = self.emociones_base.get(
                nombre,
                0
            )

            actual = self.emociones[nombre]

            if actual > base:

                actual -= cantidad

                if actual < base:

                    actual = base

            elif actual < base:

                actual += cantidad

                if actual > base:

                    actual = base

            self.emociones[nombre] = limitar(
                actual
            )

        # El contagio se aplica al procesar cada mensaje. Aplicarlo también
        # durante el decaimiento impediría que algunos valores regresaran a
        # su base (por ejemplo, afecto alto volvería a elevar felicidad).
        self.guardar()

        return self.emociones.copy()


    # ========================================================
    # RELACIONES ENTRE EMOCIONES
    # ========================================================

    def aplicar_relaciones(self):
        """
        Aplica las relaciones internas entre emociones.
        """

        relacionadas = (
            aplicar_relaciones_emocionales(
                self.emociones
            )
        )

        if isinstance(
            relacionadas,
            dict
        ):

            for nombre, valor in relacionadas.items():

                if nombre in self.emociones:

                    self.emociones[nombre] = limitar(
                        valor
                    )

        self.guardar()

        return self.emociones.copy()


    # ========================================================
    # ESTADO DE ÁNIMO
    # ========================================================

    def obtener_estado_animo(self):
        """
        Calcula el estado general del ánimo.
        """

        felicidad = self.obtener_emocion(
            "felicidad"
        )

        tristeza = self.obtener_emocion(
            "tristeza"
        )

        enojo = self.obtener_emocion(
            "enojo"
        )

        afecto = self.obtener_emocion(
            "afecto"
        )

        curiosidad = self.obtener_emocion(
            "curiosidad"
        )

        diversion = self.obtener_emocion(
            "diversion"
        )

        # ----------------------------------------------------
        # COMPONENTE POSITIVO
        # ----------------------------------------------------

        positivo = (
            felicidad
            + afecto
            + curiosidad
            + diversion
        ) / 4

        # ----------------------------------------------------
        # COMPONENTE NEGATIVO
        # ----------------------------------------------------

        negativo = (
            tristeza
            + enojo
        ) / 2

        # ----------------------------------------------------
        # DIFERENCIA
        # ----------------------------------------------------

        diferencia = (
            positivo
            - negativo
        )

        # ----------------------------------------------------
        # ESTADO
        # ----------------------------------------------------

        if diferencia >= 40:

            estado = "muy alegre"

        elif diferencia >= 20:

            estado = "alegre"

        elif diferencia >= 5:

            estado = "tranquila"

        elif diferencia > -10:

            estado = "neutral"

        elif diferencia > -30:

            estado = "melancólica"

        else:

            estado = "molesta"

        intensidad = limitar(
            abs(diferencia)
        )

        return {
            "estado": estado,
            "intensidad": round(
                intensidad
            )
        }


# ============================================================
# PRUEBA DEL MOTOR CENTRAL
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - EMOTION ENGINE")
    print("=" * 70)

    emociones = EstadoEmocional(
        "test"
    )

    print()
    print("EMOCIONES:")
    print(
        emociones.obtener()
    )

    print()
    print("EMOCIÓN DOMINANTE:")
    print(
        emociones.emocion_dominante()
    )

    print()
    print("DESCRIPCIÓN:")
    print(
        emociones.describir_estado()
    )

    print()
    print("ESTADO DE ÁNIMO:")
    print(
        emociones.obtener_estado_animo()
    )

