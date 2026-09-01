# ============================================================
# ELIZYUM - TEST GLOBAL
# test.py
#
# Prueba general de:
#
#   1. Motores centrales
#   2. Módulos de Eli
#   3. Integración del Portal Dimensional
#   4. ChatEngine
#   5. Conexión con LM Studio
#
# ============================================================

import sys


# ============================================================
# UTILIDADES
# ============================================================

OK = 0
ERRORES = 0


def prueba(nombre, funcion):

    global ERRORES

    print()
    print("=" * 70)
    print(nombre)
    print("=" * 70)

    try:

        resultado = funcion()

        print("OK")
        return resultado

    except Exception as e:

        ERRORES += 1

        print("ERROR")
        print(type(e).__name__ + ":", e)

        return None


# ============================================================
# 1. MOTORES CENTRALES
# ============================================================

def probar_centrales():

    from emotions import (
        emotions,
        emotion_links,
        mood,
        personality,
        relationships
    )

    from mundo import context

    print("emotions.py       OK")
    print("emotion_links.py  OK")
    print("mood.py           OK")
    print("personality.py    OK")
    print("relationships.py  OK")
    print("context.py        OK")


prueba(
    "1. MOTORES CENTRALES",
    probar_centrales
)


# ============================================================
# 2. MÓDULOS DE ELI
# ============================================================

def probar_eli():

    from miembros.eli import (
        emotions_eli,
        emotion_links_eli,
        relationship_eli,
        personality_eli,
        mood_eli,
        context_eli
    )

    print("emotions_eli.py          OK")
    print("emotion_links_eli.py     OK")
    print("relationship_eli.py      OK")
    print("personality_eli.py       OK")
    print("mood_eli.py              OK")
    print("context_eli.py           OK")


prueba(
    "2. MÓDULOS DE ELI",
    probar_eli
)


# ============================================================
# 3. EMOCIONES DE ELI
# ============================================================

def probar_emociones():

    from miembros.eli.emotions_eli import eli_emociones

    emociones = eli_emociones.obtener()

    if not isinstance(emociones, dict):

        raise TypeError(
            "Las emociones de Eli no devolvieron un diccionario."
        )

    print(emociones)


prueba(
    "3. EMOCIONES DE ELI",
    probar_emociones
)


# ============================================================
# 4. RELACIÓN DE ELI
# ============================================================

def probar_relacion():

    from miembros.eli.relationship_eli import (
        RELACION_BASE_ELI
    )

    if not isinstance(
        RELACION_BASE_ELI,
        dict
    ):

        raise TypeError(
            "RELACION_BASE_ELI no es un diccionario."
        )

    print(RELACION_BASE_ELI)


prueba(
    "4. RELACIÓN DE ELI",
    probar_relacion
)


# ============================================================
# 5. PERSONALIDAD
# ============================================================

print("=" * 70)
print("5. PERSONALIDAD DE ELI")
print("=" * 70)

try:

    from miembros.eli import personality_eli as p

    print()

    print("PERSONALIDAD BASE:")
    print(
        p.obtener_personalidad_base()
    )

    print()

    print("RASGOS:")
    rasgos = p.calcular_rasgos()
    print(rasgos)

    print()

    print("ESTADO DE PERSONALIDAD:")
    estado_personalidad = (
        p.obtener_estado_personalidad_eli()
    )
    print(estado_personalidad)

    print()

    print("CONTEXTO DE PERSONALIDAD:")
    contexto_personalidad = (
        p.construir_contexto_personalidad_eli(
            rasgos
        )
    )
    print(contexto_personalidad)

    print()

    print("OK")

except Exception as e:

    errores += 1

    print("ERROR")
    print(
        type(e).__name__ + ": " + str(e)
    )

# ============================================================
# 6. MOOD / FACETA
# ============================================================

def probar_mood():

    from miembros.eli.mood_eli import (
        eli_mood
    )

    estado = eli_mood.determinar_faceta()

    if not isinstance(
        estado,
        dict
    ):

        raise TypeError(
            "Mood Eli no devolvió un diccionario."
        )

    print(estado)


prueba(
    "6. MOOD / FACETA DE ELI",
    probar_mood
)


# ============================================================
# 7. CONTEXTO PARA GEMMA
# ============================================================

def probar_contexto():

    from miembros.eli.mood_eli import (
        eli_mood
    )

    contexto = eli_mood.construir_contexto()

    if not isinstance(
        contexto,
        str
    ):

        raise TypeError(
            "El contexto para Gemma no es texto."
        )

    if not contexto.strip():

        raise ValueError(
            "El contexto para Gemma está vacío."
        )

    print(contexto)


prueba(
    "7. CONTEXTO EMOCIONAL PARA GEMMA",
    probar_contexto
)


# ============================================================
# 8. CHAT ENGINE
# ============================================================

def crear_engine():

    from core.chat_engine import (
        ChatEngine
    )

    engine = ChatEngine(
        "eli"
    )

    print(
        "ChatEngine creado correctamente."
    )

    return engine


engine = prueba(
    "8. CHAT ENGINE",
    crear_engine
)


# ============================================================
# 9. CONSTRUCCIÓN DEL SYSTEM PROMPT
# ============================================================

def probar_prompt():

    if engine is None:

        raise RuntimeError(
            "ChatEngine no está disponible."
        )

    prompt = (
        engine._construir_system_prompt()
    )

    if not isinstance(
        prompt,
        str
    ):

        raise TypeError(
            "El system prompt no es texto."
        )

    if not prompt.strip():

        raise ValueError(
            "El system prompt está vacío."
        )

    print(
        "System prompt construido correctamente."
    )

    print(
        "Caracteres:",
        len(prompt)
    )


prueba(
    "9. SYSTEM PROMPT DINÁMICO",
    probar_prompt
)


# ============================================================
# 10. LM STUDIO / GEMMA
# ============================================================

def probar_llm():

    if engine is None:

        raise RuntimeError(
            "ChatEngine no está disponible."
        )

    engine.registrar_mensaje_usuario(
        "Hola Eli"
    )

    respuesta = (
        engine.obtener_respuesta()
    )

    if not isinstance(
        respuesta,
        str
    ):

        raise TypeError(
            "LM Studio no devolvió texto."
        )

    if not respuesta.strip():

        raise ValueError(
            "LM Studio devolvió una respuesta vacía."
        )

    print()
    print("RESPUESTA DE ELI:")
    print()
    print(respuesta)


prueba(
    "10. LM STUDIO / GEMMA",
    probar_llm
)


# ============================================================
# RESULTADO FINAL
# ============================================================

print()
print()
print("=" * 70)

if ERRORES == 0:

    print(
        "PRUEBA GLOBAL CENTRAL + ELI + PORTAL DIMENSIONAL OK"
    )

else:

    print(
        "PRUEBA GLOBAL FINALIZADA CON",
        ERRORES,
        "ERROR(ES)"
    )

print("=" * 70)

sys.exit(
    0 if ERRORES == 0 else 1
)

