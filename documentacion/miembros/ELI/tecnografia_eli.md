# TECNOGRAFÍA — ELI

> **Proyecto:** Elizyum
> **Miembro:** Eli
> **Versión de referencia:** 0.5
> **Estado:** Miembro consolidado
> **Tipo de documento:** Tecnografía individual

---

# 1. Identidad

**Eli** es el primer miembro desarrollado dentro del proyecto Elizyum.

Eli constituye la identidad conversacional principal alrededor de la cual se desarrollaron inicialmente los sistemas de:

* conversación;
* contexto;
* personalidad;
* emociones;
* relaciones;
* memoria;
* historial.

Conceptualmente:

```text
ELIZYUM
   │
   └── ELI
         │
         ├── Personalidad
         ├── Emociones
         ├── Relaciones
         ├── Memoria
         ├── Historial
         └── Contexto
```

---

# 2. Naturaleza de Eli

Eli es un miembro de inteligencia artificial basado en un modelo de lenguaje.

El modelo de lenguaje proporciona la generación lingüística.

Los sistemas de Elizyum proporcionan las capas adicionales utilizadas para construir la identidad y el comportamiento de Eli.

Conceptualmente:

```text
Modelo de lenguaje
        +
Contexto
        +
Personalidad
        +
Emociones
        +
Relaciones
        +
Memoria
        +
Historial
        ↓
       ELI
```

---

# 3. Estado en Elizyum 0.5

En la versión 0.5, Eli constituye el miembro con mayor nivel de integración dentro del proyecto.

Su arquitectura actual está compuesta por diferentes sistemas que trabajan conjuntamente.

```text
ELI 0.5
│
├── Identidad
├── Personalidad
├── Contexto
├── Emociones
├── Relaciones
├── Memoria
├── Historial
├── Facetas
└── Interfaz
```

---

# 4. Personalidad

La personalidad de Eli constituye una capa independiente del modelo de lenguaje.

El sistema relacionado se encuentra en:

```text
emotions/personality.py
```

La personalidad determina características relativamente estables de comportamiento.

La personalidad se utiliza junto con el contexto y el estado emocional para construir una respuesta coherente con la identidad de Eli.

---

# 5. Facetas de personalidad

Eli dispone del concepto de **facetas** como parte de su sistema de personalidad.

Las facetas permiten representar diferentes expresiones de una misma identidad dependiendo de la situación.

La selección o influencia de una faceta puede estar relacionada con:

```text
Situación
   +
Tono
   +
Intención
   +
Emociones
   +
Relación
   ↓
Faceta
```

Las facetas no representan identidades independientes.

Son diferentes expresiones de la personalidad de Eli.

---

# 6. Sistema emocional

Eli dispone de un sistema destinado a representar estados emocionales.

Las variables utilizadas durante el desarrollo incluyen:

```text
Felicidad
Tristeza
Enojo
Sorpresa
Afecto
Curiosidad
Diversión
```

El estado emocional puede modificarse como consecuencia de la interacción y utilizarse posteriormente durante la construcción del contexto.

---

# 7. Sistema relacional

Eli dispone de una capa destinada a representar su relación con el usuario.

Los componentes principales relacionados con este sistema son:

```text
emotions/relationships.py
emotions/relationship_mood.py
```

La información relacional puede utilizarse como parte del contexto de interacción.

Esto permite diferenciar una respuesta basada únicamente en el contenido del mensaje de una respuesta que también considera el estado de la relación.

---

# 8. Memoria

Eli dispone de memoria persistente.

La memoria principal se gestiona mediante:

```text
memory/memory.py
```

La información persistente relacionada con Eli se almacena en:

```text
data/memory/
```

Entre los archivos actuales se encuentran:

```text
eli_memory.json
eli_emotions.json
eli_relationship.json
```

La memoria permite conservar información relevante entre sesiones.

---

# 9. Historial conversacional

El historial de conversaciones se gestiona mediante:

```text
memory/history.py
```

Las conversaciones se almacenan dentro de:

```text
data/conversations/
```

La diferencia conceptual es:

```text
MEMORIA
→ información que se conserva como relevante

HISTORIAL
→ registro de las conversaciones realizadas
```

---

# 10. Contexto

El contexto permite reunir información procedente de diferentes sistemas antes de generar una respuesta.

Entre los elementos que pueden formar parte del contexto se encuentran:

```text
Mensaje
Situación
Tono
Intención
Personalidad
Emociones
Relación
Memoria
Historial
```

El contexto funciona como una capa de integración entre los diferentes sistemas de Eli y el modelo de lenguaje.

---

# 11. Motor conversacional

En Elizyum 0.5, el procesamiento conversacional utiliza:

```text
core/chat_engine.py
```

Este componente coordina diferentes fuentes de información necesarias para procesar la interacción.

La relación conceptual es:

```text
Usuario
   ↓
Interfaz
   ↓
chat_engine.py
   ↓
Contexto
   ├── Personalidad
   ├── Emociones
   ├── Relaciones
   ├── Memoria
   └── Historial
   ↓
Modelo de lenguaje
   ↓
Respuesta
   ↓
Eli
```

El historial de modificaciones de `chat_engine.py` deberá mantenerse en la documentación técnica correspondiente al código y no dentro de esta tecnografía.

---

# 12. Interfaz

Eli se comunica con el usuario mediante la interfaz gráfica del proyecto.

El componente principal actual es:

```text
ui/chat_window.py
```

La interfaz constituye la capa visual de interacción.

La lógica interna de Eli permanece separada de la presentación.

---

# 13. Voz

La arquitectura del proyecto dispone actualmente de:

```text
voice/
```

La integración completa del sistema de voz de Eli no forma parte del estado consolidado de 0.5.

Por lo tanto:

```text
Voz de Eli
Estado: PLANIFICADO
```

La futura arquitectura contempla la posibilidad de utilizar:

```text
Voz del usuario
      ↓
STT
      ↓
Eli
      ↓
TTS
      ↓
Voz de Eli
```

---

# 14. Modelo de lenguaje

Eli utiliza un modelo de lenguaje como motor generativo.

El modelo es responsable principalmente de producir lenguaje a partir del contexto proporcionado.

El modelo no constituye por sí mismo la identidad completa de Eli.

La identidad se construye mediante las capas adicionales proporcionadas por Elizyum.

---

# 15. Arquitectura conceptual

La arquitectura de Eli 0.5 puede representarse como:

```text
                    ELI
                     │
          ┌──────────┴──────────┐
          │                     │
     IDENTIDAD              SISTEMAS
                                │
       ┌────────┬────────┬──────┼──────┬────────┐
       │        │        │      │      │        │
  Personalidad Emociones Relación Memoria Historial
       │        │        │      │      │
       └────────┴────────┴──────┴──────┘
                         │
                      Contexto
                         │
                  Motor conversacional
                         │
                  Modelo de lenguaje
                         │
                      Respuesta
```

---

# 16. Separación entre identidad y modelo

Eli no debe considerarse equivalente al modelo de lenguaje.

La arquitectura establece una separación conceptual:

```text
MODELO
→ capacidad generativa

ELIZYUM
→ arquitectura

ELI
→ identidad

PERSONALIDAD
→ comportamiento

EMOCIONES
→ estado emocional

RELACIÓN
→ vínculo contextual

MEMORIA
→ información persistente
```

Esta separación permitirá evolucionar cada componente de forma independiente.

---

# 17. Relación con Elizyum

En 0.5, Eli todavía se encuentra estrechamente integrada dentro de la arquitectura general del proyecto.

La relación actual puede representarse como:

```text
ELIZYUM
   │
   ├── Core
   ├── Contexto
   ├── Emociones
   ├── Memoria
   ├── UI
   └── ELI
```

La separación arquitectónica completa entre Elizyum y Eli queda prevista para una etapa posterior.

---

# 18. Concepto de Core / Alma Digital

El concepto de **Core**, denominado también conceptualmente **Alma Digital**, pertenece a la planificación futura de Eli.

**No está implementado en la versión 0.5.**

Por tanto, no forma parte de la arquitectura funcional actual.

Su objetivo futuro será representar un núcleo identitario que permita diferenciar la esencia del miembro de los sistemas que gestionan sus estados y capacidades.

---

# 19. Personalidad universal

Durante la planificación del proyecto se estableció la idea de crear una matriz universal de personalidades.

Esta matriz se plantea como una futura herramienta para describir diferentes miembros mediante parámetros comunes.

El concepto todavía no forma parte de la implementación consolidada de Eli 0.5.

Por lo tanto:

```text
Matriz universal
Estado: PLANIFICADO
```

---

# 20. Evolución futura de Eli

La evolución prevista busca que Eli pueda funcionar como un miembro independiente dentro de Elizyum.

Conceptualmente:

```text
                 ELIZYUM
                    │
          ┌─────────┴─────────┐
          │                   │
        MUNDO              MIEMBROS
                              │
                              └── ELI
```

Esto permitirá posteriormente integrar a Eli junto con otros miembros como:

```text
Aurora
Martha
Oro
```

---

# 21. Características futuras

Las siguientes capacidades están previstas para etapas posteriores:

* Core / Alma Digital;
* matriz universal;
* plantilla universal;
* Sala;
* habitación privada;
* participación multi-miembro;
* horarios;
* rutinas;
* conductas aprendidas;
* voz;
* STT;
* TTS;
* avatar;
* visión;
* interacción con hardware.

Estas capacidades **no deben considerarse implementadas en Eli 0.5**.

---

# 22. Identidad documental

La documentación individual de Eli se encuentra en:

```text
documentacion/miembros/ELI/
```

Actualmente:

```text
documentacion/miembros/ELI/
├── historial_eli.md
└── tecnografia_eli.md
```

La separación permite mantener:

```text
TECNOGRAFÍA
→ qué es Eli y cómo está constituida

HISTORIAL
→ cómo evolucionó Eli
```

---

# 23. Estado técnico

```text
┌────────────────────────────────────┐
│              ELI 0.5               │
├────────────────────────────────────┤
│ Identidad             CONSOLIDADA  │
│ Personalidad          IMPLEMENTADA │
│ Emociones             IMPLEMENTADA │
│ Relaciones            IMPLEMENTADA │
│ Memoria               IMPLEMENTADA │
│ Historial             IMPLEMENTADO │
│ Contexto              IMPLEMENTADO │
│ Facetas               DESARROLLADO │
│ Interfaz              IMPLEMENTADA │
│ Voz                   PLANIFICADA  │
│ Core                  PLANIFICADO  │
│ Matriz universal      PLANIFICADA  │
│ Sala                  PLANIFICADA  │
└────────────────────────────────────┘
```

---

# 24. Principio de continuidad

La identidad de Eli deberá conservar continuidad entre versiones.

Las futuras modificaciones deberán procurar separar:

```text
IDENTIDAD
```

de:

```text
CAPACIDADES
```

y de:

```text
ESTADOS
```

Una modificación técnica no deberá considerarse automáticamente una modificación de identidad.

---

# 25. Estado de referencia

```text
Miembro:
Eli

Proyecto:
Elizyum

Primera aparición:
0.2

Versión de referencia:
0.5

Estado:
Miembro consolidado

Próxima etapa:
Separación arquitectónica y evolución multi-miembro
```

---

# FIN DE TECNOGRAFÍA — ELI

> **Eli es el primer miembro de Elizyum.
> Su arquitectura combina identidad, personalidad, emociones, relación, memoria y contexto sobre un modelo de lenguaje.**
