# TECNOGRAFÍA DE ELIZYUM

> **Proyecto:** Elizyum
> **Periodo documentado:** 0.1 — 0.5
> **Estado:** Base histórica y técnica
> **Tipo de documento:** Tecnografía general del proyecto

---

# 1. ¿Qué es Elizyum?

Elizyum es el proyecto que contiene el entorno y la arquitectura destinada a albergar diferentes miembros de inteligencia artificial con identidades, personalidades, especialidades, memoria, emociones y formas de interacción diferenciadas.

Elizyum no representa únicamente a una inteligencia artificial individual.

El proyecto está diseñado para evolucionar desde una interacción individual con Eli hacia un entorno donde múltiples miembros puedan coexistir y participar en diferentes tipos de conversaciones.

Durante las primeras versiones, Elizyum estuvo fuertemente ligado a Eli. A partir de la planificación de versiones posteriores, se estableció la necesidad de separar claramente:

```text
ELIZYUM = entorno / proyecto
ELI     = miembro
```

Esta separación constituye uno de los objetivos principales de la evolución posterior del proyecto.

---

# 2. Principio fundamental

Elizyum se desarrolla bajo la idea de que una inteligencia artificial puede construirse mediante diferentes capas especializadas.

De forma conceptual:

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
Interfaz
        ↓
     Miembro
```

El modelo de lenguaje proporciona la capacidad generativa, mientras que Elizyum proporciona las estructuras necesarias para construir una identidad y una experiencia de interacción específica.

---

# 3. Evolución histórica

## Elizyum 0.1 — Inicio del proyecto

La versión 0.1 corresponde a la etapa inicial de desarrollo de Elizyum.

El objetivo principal era establecer una base funcional para conectar una interfaz con un modelo de lenguaje y realizar las primeras interacciones.

En esta etapa todavía no existía la arquitectura actual de miembros.

### Objetivos principales

* establecer el proyecto;
* realizar las primeras pruebas de conversación;
* conectar el sistema con un modelo de lenguaje;
* crear una interfaz inicial;
* comprobar la comunicación entre los diferentes componentes.

La versión 0.1 representa el nacimiento técnico del proyecto.

---

# 4. Elizyum 0.2 — Aparición de Eli

Durante la evolución del proyecto aparece Eli como identidad conversacional.

Este momento marca un cambio importante.

Elizyum deja de ser solamente un sistema de conversación y comienza a convertirse en un entorno destinado a contener una identidad diferenciada.

Conceptualmente:

```text
Antes:

Elizyum → modelo → respuesta


Después:

Elizyum
   ↓
  Eli
   ↓
modelo
   ↓
respuesta
```

Eli se convierte en el primer miembro desarrollado del proyecto.

---

# 5. Elizyum 0.3 — Desarrollo de identidad

La versión 0.3 representa una etapa de desarrollo de la identidad de Eli.

El objetivo deja de ser únicamente conseguir respuestas funcionales y comienza a centrarse en mantener una interacción más consistente.

Durante esta evolución se incorporan y desarrollan conceptos relacionados con:

* personalidad;
* contexto;
* memoria;
* historial;
* comportamiento;
* relación con el usuario.

La conversación comienza a depender de información adicional al mensaje individual.

---

# 6. Elizyum 0.4 — Desarrollo emocional y relacional

En la evolución hacia 0.4 se desarrollan los sistemas relacionados con emociones y relaciones.

La arquitectura comienza a incorporar componentes específicos para representar estados emocionales y su influencia sobre la interacción.

Entre los componentes desarrollados se encuentran:

```text
emotions/
├── emotions.py
├── emotion_links.py
├── personality.py
├── relationships.py
└── relationship_mood.py
```

Estos componentes permiten separar diferentes aspectos del comportamiento.

### Emociones

Representan el estado emocional utilizado por el sistema.

### Personalidad

Define características relativamente estables del comportamiento.

### Relaciones

Representan información relacionada con el vínculo entre Eli y el usuario.

### Estado relacional

Permite utilizar la relación como parte del contexto que influye en el comportamiento.

---

# 7. Elizyum 0.5 — Consolidación

La versión 0.5 constituye una etapa de consolidación de los sistemas desarrollados durante las versiones anteriores.

El proyecto dispone de una arquitectura que integra:

```text
Conversación
     │
     ├── Contexto
     ├── Personalidad
     ├── Emociones
     ├── Relaciones
     ├── Memoria
     └── Historial
```

Estos componentes trabajan conjuntamente para generar la interacción de Eli.

---

# 8. Arquitectura de Elizyum 0.5

La estructura del proyecto en el estado documentado es:

```text
Elizyum/
│
├── config.py
├── context.py
├── context_ai.py
├── main.py
├── requirements.txt
├── test.py
│
├── assest/
│
├── core/
│   └── chat_engine.py
│
├── data/
│   ├── conversations/
│   └── memory/
│
├── documentacion/
│
├── emotions/
│   ├── emotions.py
│   ├── emotion_links.py
│   ├── personality.py
│   ├── relationships.py
│   └── relationship_mood.py
│
├── logs/
│
├── memory/
│   ├── history.py
│   ├── memory.py
│   └── __init__.py
│
├── ui/
│   └── chat_window.py
│
└── voice/
```

Esta estructura corresponde al estado del proyecto al cierre de la etapa 0.5.

---

# 9. Núcleo conversacional

El componente principal de procesamiento conversacional en 0.5 se encuentra en:

```text
core/chat_engine.py
```

Este componente coordina diferentes elementos necesarios para procesar una conversación.

Entre ellos:

* mensaje del usuario;
* contexto;
* personalidad;
* emociones;
* relación;
* memoria;
* historial.

El motor construye la información necesaria para enviar una solicitud al modelo de lenguaje y posteriormente procesar la respuesta.

---

# 10. Contexto

El sistema utiliza diferentes fuentes de información para construir el contexto de una interacción.

Entre ellas se encuentran:

* situación;
* tono;
* intención;
* emociones;
* relación;
* personalidad;
* memoria;
* historial.

El contexto permite proporcionar al modelo de lenguaje información adicional relacionada con el estado actual de la interacción.

---

# 11. Memoria

El proyecto dispone de un sistema de memoria persistente.

Los componentes principales se encuentran en:

```text
memory/
├── memory.py
└── history.py
```

La información persistente de Eli se almacena actualmente dentro de:

```text
data/memory/
```

incluyendo:

```text
eli_memory.json
eli_emotions.json
eli_relationship.json
```

La memoria permite conservar información relevante entre sesiones.

---

# 12. Historial

El sistema mantiene registros de conversaciones dentro de:

```text
data/conversations/
```

Los archivos se almacenan mediante registros separados por fecha y hora.

Esto permite conservar el historial de las sesiones y utilizarlo posteriormente como fuente contextual.

---

# 13. Sistema emocional

El sistema emocional constituye una de las características desarrolladas durante la evolución de Elizyum.

Las variables emocionales utilizadas durante el desarrollo incluyen:

* felicidad;
* tristeza;
* enojo;
* sorpresa;
* afecto;
* curiosidad;
* diversión.

El sistema permite mantener y actualizar estados emocionales.

Estos estados pueden utilizarse posteriormente durante la construcción del contexto de Eli.

---

# 14. Sistema de personalidad

La personalidad se encuentra separada del motor conversacional.

El módulo principal se encuentra en:

```text
emotions/personality.py
```

La personalidad se utiliza junto con el contexto y el estado emocional para influir en el comportamiento conversacional.

El sistema está diseñado para permitir que la personalidad sea más que una descripción estática incluida directamente en cada mensaje.

---

# 15. Sistema de relaciones

El proyecto incorpora un sistema dedicado a representar la relación entre Eli y el usuario.

Los componentes relacionados son:

```text
emotions/relationships.py
emotions/relationship_mood.py
```

La relación puede proporcionar información adicional utilizada durante la construcción del contexto.

Esto permite que el comportamiento de Eli tenga en cuenta la evolución de la interacción.

---

# 16. Interfaz

La interfaz gráfica se encuentra principalmente en:

```text
ui/chat_window.py
```

Elizyum utiliza una interfaz visual para permitir la interacción con Eli.

La interfaz representa la capa de presentación del proyecto, mientras que los sistemas internos gestionan la lógica de conversación, memoria, emociones y personalidad.

---

# 17. Voz

Durante la planificación de Elizyum se estableció la incorporación de sistemas de voz.

La estructura actual contiene:

```text
voice/
```

Sin embargo, la integración completa del sistema de voz de Eli **no forma parte del estado funcional consolidado de 0.5**.

La implementación de voz queda prevista para una etapa posterior.

---

# 18. Miembros de Elizyum

Durante la evolución del proyecto se estableció una arquitectura orientada a múltiples miembros.

Los miembros actualmente definidos son:

```text
🌸 Eli
🎨 Aurora
🩺 Martha
⚡ Oro
```

Cada miembro dispone de documentación propia.

La documentación se encuentra organizada en:

```text
documentacion/miembros/
```

con una tecnografía y un historial independiente para cada miembro.

---

# 19. Especialización de los miembros

Cada miembro está destinado a desarrollar una identidad y especialidad propia.

### Eli

Miembro principal del proyecto.

### Aurora

Miembro orientada al arte y la creatividad.

### Martha

Miembro especializada en medicina.

### Oro

Miembro orientada a tecnología y electrónica.

El nombre Oro está relacionado conceptualmente con el uso del oro en contactos y componentes electrónicos debido a sus propiedades de conductividad y resistencia a la corrosión.

---

# 20. Documentación individual

A partir de la estructura actual, cada miembro mantiene dos documentos principales:

```text
tecnografia_<miembro>.md
historial_<miembro>.md
```

La tecnografía describe:

> qué es el miembro y cómo está construido.

El historial describe:

> cómo evolucionó el miembro durante el desarrollo.

Esto permite mantener separada la descripción técnica de la evolución histórica.

---

# 21. Documentación general de Elizyum

El proyecto mantiene su propia documentación independiente de la documentación de los miembros.

Actualmente:

```text
documentacion/
├── historial_elizyum.md
├── tecnografia_elizyum.md
└── miembros/
```

La tecnografía general documenta la evolución y arquitectura del proyecto.

El historial general registra las modificaciones relacionadas directamente con Elizyum.

---

# 22. Separación entre Elizyum y sus miembros

Durante las primeras versiones, la arquitectura estaba fuertemente centrada en Eli.

La evolución del proyecto establece posteriormente una separación conceptual:

```text
ELIZYUM
   │
   └── MIEMBROS
         ├── Eli
         ├── Aurora
         ├── Martha
         └── Oro
```

Esta separación permitirá que el proyecto pueda incorporar nuevos miembros sin convertir cada uno en una modificación directa de la identidad de Elizyum.

La separación arquitectónica completa está prevista para la versión 0.6.

---

# 23. Conceptos futuros

Los siguientes conceptos fueron definidos durante la planificación del proyecto, pero **no forman parte de la implementación consolidada de Elizyum 0.5**:

* Alma Digital / Core;
* plantilla universal de miembros;
* matriz universal de personalidad;
* Sala compartida;
* habitaciones privadas;
* participación contextual de miembros;
* horarios y rutinas;
* comportamiento autónomo;
* sistema multi-miembro completo;
* STT integrado;
* TTS integrado;
* aplicación externa;
* avatares 3D;
* entorno virtual;
* visión artificial;
* interacción con hardware.

Estos conceptos deberán documentarse como desarrollo futuro y no como características existentes de 0.5.

---

# 24. Filosofía de evolución

Elizyum está diseñado para crecer progresivamente.

La evolución prevista separa diferentes niveles:

```text
PROYECTO
   ↓
MUNDO
   ↓
MIEMBROS
   ↓
IDENTIDAD
   ↓
PERSONALIDAD
   ↓
EMOCIONES
   ↓
MEMORIA
   ↓
EXPERIENCIA
```

La arquitectura futura deberá permitir añadir capacidades sin alterar innecesariamente los componentes que ya funcionan.

---

# 25. Estado de Elizyum 0.5

Al finalizar 0.5, Elizyum cuenta con una base funcional centrada en Eli y con la estructura documental preparada para múltiples miembros.

### Implementado o establecido

* proyecto Elizyum;
* interfaz gráfica;
* comunicación con modelo de lenguaje;
* motor conversacional;
* contexto;
* memoria;
* historial;
* personalidad;
* emociones;
* relaciones;
* documentación general;
* documentación individual de miembros;
* estructura inicial para voz.

### Fuera del alcance de 0.5

* separación arquitectónica completa de Eli;
* Sala multi-miembro;
* habitaciones;
* Core / Alma Digital;
* matriz universal;
* plantilla universal;
* sistema de voz completo;
* aplicación externa;
* entorno virtual;
* avatares 3D;
* visión;
* hardware.

---

# 26. Transición hacia Elizyum 0.6

La versión 0.6 representa una nueva etapa arquitectónica.

El objetivo principal será separar a Eli de la estructura general de Elizyum y establecer una arquitectura preparada para múltiples miembros.

La dirección conceptual es:

```text
                 ELIZYUM
                    │
          ┌─────────┴─────────┐
          │                   │
        MUNDO              MIEMBROS
          │                   │
         SALA        ┌────────┼────────┐
                     │        │        │
                    Eli    Aurora   Martha   Oro
```

También se contempla una reorganización de nombres y módulos para españolizar progresivamente el proyecto.

El actual:

```text
core/chat_engine.py
```

será objeto de reorganización durante esta etapa.

El nombre conceptual propuesto para el nuevo componente central de interacción es:

```text
portal_dimensional.py
```

---

# 27. Principio de continuidad

Elizyum debe conservar un registro claro de su evolución.

Cada versión representa un estado concreto del proyecto.

Los cambios importantes deberán quedar registrados en los historiales correspondientes.

La documentación deberá diferenciar siempre entre:

```text
IMPLEMENTADO
```

y

```text
PLANIFICADO
```

De esta forma, las futuras generaciones del proyecto podrán identificar qué componentes existían realmente en cada versión.

---

# 28. Registro de versiones

```text
ELIZYUM

0.1
Nacimiento del proyecto.

0.2
Aparición de Eli como identidad conversacional.

0.3
Desarrollo de identidad, contexto, memoria e interacción.

0.4
Desarrollo de sistemas emocionales y relacionales.

0.5
Consolidación de la arquitectura actual de Eli y
preparación de la arquitectura multi-miembro.

0.6
Separación arquitectónica de Eli y Elizyum.
```

> **Nota histórica:** Las descripciones de las versiones anteriores a 0.5 son una reconstrucción documental del desarrollo. No deben interpretarse como una reproducción exacta del código fuente original de cada versión.

---

# 29. Cierre de la etapa 0.5

Elizyum 0.5 representa el final de la primera etapa de construcción del proyecto.

Durante esta etapa se establecieron las bases necesarias para que Elizyum evolucionara desde un sistema conversacional centrado en una única identidad hacia un entorno capaz de contener múltiples miembros.

La versión 0.5 constituye el punto de referencia previo a la separación arquitectónica.

---

# FIN DE TECNOGRAFÍA

**ELIZYUM 0.1 — 0.5**

> *Primero construimos la voz.
> Después construimos a quien habla.
> Ahora toca construir el mundo donde podrá existir.*
