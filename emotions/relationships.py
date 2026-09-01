
# ============================================================
# ELIZYUM - RELATIONSHIP ENGINE
# emotions/relationships.py
#
# Motor CENTRAL de relaciones de Elizyum.
#
# Este módulo NO pertenece a Eli.
# No contiene personalidad, facetas ni comportamiento específico
# de ningún miembro.
#
# Responsabilidad:
#
# - mantener estado relacional
# - modificar confianza
# - modificar cercanía
# - modificar comprensión
# - modificar vínculo
# - registrar eventos relacionales
# - calcular efectos básicos de eventos
#
# Los módulos específicos de cada miembro pueden utilizar este
# motor y adaptar sus resultados posteriormente.
# ============================================================


# ============================================================
# VALORES BASE
# ============================================================

RELACION_BASE = {
    "confianza": 50,
    "cercania": 50,
    "comprension": 50,
    "vinculo": 50
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


# ============================================================
# CREAR RELACIÓN
# ============================================================

def crear_relacion(
    confianza=50,
    cercania=50,
    comprension=50,
    vinculo=50
):
    """
    Crea un estado relacional normalizado.
    """

    return {
        "confianza": limitar(confianza),
        "cercania": limitar(cercania),
        "comprension": limitar(comprension),
        "vinculo": limitar(vinculo)
    }


# ============================================================
# NORMALIZAR RELACIÓN
# ============================================================

def normalizar_relacion(relacion=None):
    """
    Garantiza que la relación tenga todos los valores necesarios.
    """

    if not isinstance(relacion, dict):
        relacion = {}

    resultado = RELACION_BASE.copy()

    for nombre in resultado:

        if nombre in relacion:
            resultado[nombre] = limitar(
                relacion[nombre]
            )

    return resultado


# ============================================================
# OBTENER VALOR
# ============================================================

def obtener_valor(
    relacion,
    nombre,
    defecto=50
):
    """
    Obtiene de forma segura un valor relacional.
    """

    if not isinstance(relacion, dict):
        return defecto

    return limitar(
        relacion.get(
            nombre,
            defecto
        )
    )


# ============================================================
# CAMBIAR VALOR
# ============================================================

def cambiar_valor(
    relacion,
    nombre,
    cantidad
):
    """
    Modifica un valor relacional.
    """

    relacion = normalizar_relacion(
        relacion
    )

    if nombre not in relacion:
        return relacion

    try:
        cantidad = int(float(cantidad))
    except (TypeError, ValueError):
        cantidad = 0

    relacion[nombre] = limitar(
        relacion[nombre] + cantidad
    )

    return relacion


# ============================================================
# ESTABLECER VALOR
# ============================================================

def establecer_valor(
    relacion,
    nombre,
    valor
):
    """
    Establece directamente un valor relacional.
    """

    relacion = normalizar_relacion(
        relacion
    )

    if nombre not in relacion:
        return relacion

    relacion[nombre] = limitar(
        valor
    )

    return relacion


# ============================================================
# EVENTOS RELACIONALES
# ============================================================

EVENTOS_RELACIONALES = {
    "gesto_carinoso",
    "cumplio_promesa",
    "romper_promesa",
    "mentira",
    "discusion",
    "reconciliacion",
    "distancia",
    "ninguno"
}


# ============================================================
# NORMALIZAR EVENTO
# ============================================================

def normalizar_evento(evento):
    """
    Normaliza un evento relacional.

    Soporta:

        "mentira"

    o:

        {
            "evento": "mentira",
            "intensidad": 80
        }
    """

    if isinstance(evento, dict):

        nombre = evento.get(
            "evento",
            "ninguno"
        )

        intensidad = evento.get(
            "intensidad",
            0
        )

    else:

        nombre = evento
        intensidad = 0

    if not isinstance(nombre, str):
        nombre = "ninguno"

    if nombre not in EVENTOS_RELACIONALES:
        nombre = "ninguno"

    intensidad = limitar(
        intensidad
    )

    return {
        "evento": nombre,
        "intensidad": intensidad
    }


# ============================================================
# EFECTOS DE EVENTOS
# ============================================================

def aplicar_evento(
    relacion,
    evento
):
    """
    Aplica los efectos relacionales básicos de un evento.

    Este motor solamente modifica el estado relacional.
    La personalidad específica se determina en módulos
    superiores.
    """

    relacion = normalizar_relacion(
        relacion
    )

    evento = normalizar_evento(
        evento
    )

    nombre = evento["evento"]
    intensidad = evento["intensidad"]

    # --------------------------------------------------------
    # GESTO CARIÑOSO
    # --------------------------------------------------------

    if nombre == "gesto_carinoso":

        relacion = cambiar_valor(
            relacion,
            "cercania",
            max(1, intensidad // 15)
        )

        relacion = cambiar_valor(
            relacion,
            "vinculo",
            max(1, intensidad // 20)
        )

    # --------------------------------------------------------
    # PROMESA CUMPLIDA
    # --------------------------------------------------------

    elif nombre == "cumplio_promesa":

        relacion = cambiar_valor(
            relacion,
            "confianza",
            max(1, intensidad // 10)
        )

        relacion = cambiar_valor(
            relacion,
            "vinculo",
            max(1, intensidad // 20)
        )

    # --------------------------------------------------------
    # PROMESA ROTA
    # --------------------------------------------------------

    elif nombre == "romper_promesa":

        relacion = cambiar_valor(
            relacion,
            "confianza",
            -(max(1, intensidad // 10))
        )

        relacion = cambiar_valor(
            relacion,
            "cercania",
            -(max(1, intensidad // 20))
        )

    # --------------------------------------------------------
    # MENTIRA
    # --------------------------------------------------------

    elif nombre == "mentira":

        relacion = cambiar_valor(
            relacion,
            "confianza",
            -(max(1, intensidad // 10))
        )

        relacion = cambiar_valor(
            relacion,
            "comprension",
            -(max(1, intensidad // 20))
        )

    # --------------------------------------------------------
    # DISCUSIÓN
    # --------------------------------------------------------

    elif nombre == "discusion":

        relacion = cambiar_valor(
            relacion,
            "cercania",
            -(max(1, intensidad // 20))
        )

        relacion = cambiar_valor(
            relacion,
            "comprension",
            -(max(1, intensidad // 20))
        )

    # --------------------------------------------------------
    # RECONCILIACIÓN
    # --------------------------------------------------------

    elif nombre == "reconciliacion":

        relacion = cambiar_valor(
            relacion,
            "cercania",
            max(1, intensidad // 20)
        )

        relacion = cambiar_valor(
            relacion,
            "comprension",
            max(1, intensidad // 15)
        )

        relacion = cambiar_valor(
            relacion,
            "vinculo",
            max(1, intensidad // 20)
        )

    # --------------------------------------------------------
    # DISTANCIA
    # --------------------------------------------------------

    elif nombre == "distancia":

        relacion = cambiar_valor(
            relacion,
            "cercania",
            -(max(1, intensidad // 20))
        )

    return relacion


# ============================================================
# ESTADO RELACIONAL
# ============================================================

def determinar_estado(
    relacion
):
    """
    Determina el estado general de la relación.
    """

    relacion = normalizar_relacion(
        relacion
    )

    confianza = relacion["confianza"]
    cercania = relacion["cercania"]
    comprension = relacion["comprension"]
    vinculo = relacion["vinculo"]

    promedio = (
        confianza
        + cercania
        + comprension
        + vinculo
    ) / 4

    if confianza < 25 or cercania < 25:
        return "distancia"

    if promedio >= 75:
        return "muy_cercana"

    if promedio >= 60:
        return "cercana"

    if promedio >= 40:
        return "normal"

    return "distante"


# ============================================================
# RESUMEN RELACIONAL
# ============================================================

def obtener_resumen(
    relacion
):
    """
    Devuelve un resumen estructurado de la relación.
    """

    relacion = normalizar_relacion(
        relacion
    )

    return {
        "confianza": relacion["confianza"],
        "cercania": relacion["cercania"],
        "comprension": relacion["comprension"],
        "vinculo": relacion["vinculo"],
        "estado": determinar_estado(
            relacion
        )
    }


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ELIZYUM - RELATIONSHIP ENGINE")
    print("=" * 70)

    relacion = crear_relacion(
        confianza=75,
        cercania=65,
        comprension=60,
        vinculo=70
    )

    print()
    print("RELACIÓN INICIAL")
    print(relacion)

    eventos = [

        {
            "evento": "gesto_carinoso",
            "intensidad": 60
        },

        {
            "evento": "cumplio_promesa",
            "intensidad": 70
        },

        {
            "evento": "mentira",
            "intensidad": 80
        }
    ]

    for evento in eventos:

        relacion = aplicar_evento(
            relacion,
            evento
        )

        print()
        print("-" * 70)
        print(
            f"EVENTO: {evento['evento']}"
        )
        print("-" * 70)

        print(
            obtener_resumen(
                relacion
            )
        )
# ============================================================
# GESTOR DE RELACIÓN (persistencia por miembro)
# ============================================================
#
# Envuelve las funciones puras de arriba (crear_relacion,
# aplicar_evento, normalizar_relacion) y les agrega guardado
# en disco, igual que ya hace EstadoEmocional en emotions.py.
# ============================================================

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class GestorRelacion:

    def __init__(self, nombre, base=None, base_dir=None):

        self.nombre = nombre
        raiz = Path(base_dir) if base_dir is not None else BASE_DIR
        self.archivo = raiz / "data" / nombre / "relacion.json"
        self.base = base if isinstance(base, dict) else crear_relacion()

        self.relacion = self.cargar()

    def cargar(self):

        if not self.archivo.exists():
            return self.base.copy()

        try:

            with open(
                self.archivo,
                "r",
                encoding="utf-8"
            ) as f:

                datos = json.load(f)

            combinada = {**self.base, **datos}
            relacion = normalizar_relacion(combinada)

            # Conserva metadatos propios del miembro, por ejemplo
            # ``tipo_relacion`` en Aurora.
            for clave, valor in combinada.items():
                if clave not in relacion:
                    relacion[clave] = valor

            return relacion

        except Exception:

            return self.base.copy()

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
                self.relacion,
                f,
                ensure_ascii=False,
                indent=4
            )

    def obtener(self):

        return self.relacion.copy()

    def procesar_contexto(self, contexto):

        evento = contexto.get("evento_relacional") if isinstance(contexto, dict) else None

        if isinstance(evento, dict) and evento.get("evento"):

            self.relacion = aplicar_evento(self.relacion, evento)
            self.guardar()

        return self.relacion
