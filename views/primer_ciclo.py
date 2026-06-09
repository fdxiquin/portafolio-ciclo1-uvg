from __future__ import annotations

import html
from typing import Literal, TypedDict

import streamlit as st

from utils.data_loader import APP_DIR


class ReflectionBlock(TypedDict):
    title: str
    body: str


class Moment(TypedDict):
    title: str
    label: str
    body: str


class MediaItem(TypedDict):
    type: Literal["image", "video"]
    path: str
    caption: str


PAGE_CONTENT = {
    "title": "Mi primer ciclo UVG",
    "subtitle": "Una mirada personal a mi inicio universitario",
    "intro": (
        "Este primer ciclo fue una etapa de adaptación, esfuerzo y descubrimiento. "
        "Entrar a la universidad significó enfrentar nuevas formas de estudiar, trabajar "
        "en equipo, comunicar ideas y entender que cada curso aporta algo distinto a mi "
        "formación como estudiante y como futuro profesional."
    ),
    "computer_science": {
        "title": "Mi concepción de Ciencia de la Computación",
        "body": (
            "Para mí, la Ciencia de la Computación es una disciplina que permite resolver "
            "problemas mediante lógica, creatividad, análisis y tecnología. No se trata solo "
            "de programar, sino de entender situaciones, modelar soluciones y construir "
            "herramientas que puedan tener un impacto real. Un científico de computación "
            "observa, pregunta, diseña, prueba y mejora. En este campo me veo creciendo con "
            "responsabilidad, aprendiendo a crear soluciones útiles y desarrollando criterio "
            "para usar la tecnología de forma ética."
        ),
    },
    "takeaways": {
        "title": "Lo que me llevo del ciclo",
        "body": (
            "Me llevo una visión más clara de lo que exige la vida universitaria: constancia, "
            "orden, disciplina y apertura para aprender de los errores. También me llevo el "
            "valor de trabajar con otras personas, escuchar perspectivas distintas y reconocer "
            "que no todos los aprendizajes aparecen en una nota. Algunos se ven en la manera "
            "de estudiar mejor, pedir ayuda a tiempo, explicar una idea con más claridad o "
            "perder el miedo a intentar algo nuevo."
        ),
    },
    "looking_forward": {
        "title": "Mirada hacia adelante",
        "body": (
            "Después de este ciclo, quiero seguir fortaleciendo mis bases académicas y mi forma "
            "de aprender. Me interesa avanzar con más orden, aprovechar mejor cada proyecto y "
            "conectar lo que estudio con mis metas personales, profesionales y familiares. Este "
            "inicio no fue solo una primera etapa: fue una señal de lo que puedo construir si "
            "mantengo disciplina, humildad y propósito."
        ),
    },
}

KEY_MOMENTS: list[Moment] = [
    {
        "title": "Adaptarme al ritmo universitario",
        "label": "Crecimiento personal",
        "body": (
            "Aprendí que la universidad exige organizar el tiempo de forma más intencional. "
            "El cambio no fue solo académico; también fue personal, porque tuve que ajustar "
            "hábitos, prioridades y formas de responder ante la presión."
        ),
    },
    {
        "title": "Construir proyectos desde cero",
        "label": "Aprendizaje técnico",
        "body": (
            "Los proyectos de programación me ayudaron a entender que una solución nace de "
            "varias decisiones pequeñas: planificar, probar, equivocarse, corregir y volver "
            "a intentar con más criterio."
        ),
    },
    {
        "title": "Comunicar mejor mis ideas",
        "label": "Formación integral",
        "body": (
            "Las presentaciones, informes y trabajos escritos me recordaron que comprender "
            "algo no es suficiente si no puedo explicarlo con claridad, respeto y estructura."
        ),
    },
    {
        "title": "Aprender fuera de mi zona cómoda",
        "label": "Metacognición",
        "body": (
            "Algunos cursos me retaron de formas distintas. Eso me ayudó a identificar cómo "
            "aprendo, qué me cuesta más y qué estrategias necesito fortalecer para mejorar."
        ),
    },
]

LEARNINGS = [
    "Organizar mejor mi tiempo antes de que las tareas se acumulen.",
    "Entender que equivocarme también puede ser evidencia de aprendizaje.",
    "Relacionar programación, ciencia, comunicación y matemáticas como partes de una misma formación.",
    "Valorar el trabajo en equipo sin perder responsabilidad individual.",
    "Pensar con más cuidado qué evidencias puedo compartir en un portafolio público.",
]

MEDIA_ITEMS: list[MediaItem] = []


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #172033;
            --muted: #667085;
            --line: #d9e2ec;
            --panel: #ffffff;
            --accent: #176b87;
            --accent-2: #c45f36;
            --wash: #f6f8fb;
        }
        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        .cycle-hero {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: linear-gradient(135deg, #f8fbff 0%, #ffffff 52%, #f7fbf7 100%);
            padding: 2.2rem 2.4rem;
            margin-bottom: 1.4rem;
        }
        .cycle-hero h1 {
            color: var(--ink);
            font-size: 2.8rem;
            line-height: 1.08;
            letter-spacing: 0;
            margin: 0 0 .6rem;
        }
        .cycle-hero p {
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.6;
            margin: 0;
        }
        .cycle-section {
            border-top: 1px solid var(--line);
            padding-top: 1.15rem;
            margin-top: 1.25rem;
        }
        .cycle-section h2 {
            color: var(--ink);
            font-size: 1.35rem;
            line-height: 1.2;
            letter-spacing: 0;
            margin: 0 0 .55rem;
        }
        .cycle-section p {
            color: #344054;
            font-size: 1rem;
            line-height: 1.7;
            margin: 0;
        }
        .moment-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1rem;
            margin-top: .85rem;
        }
        .moment-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            padding: 1rem 1.1rem;
            min-height: 178px;
        }
        .moment-card span {
            color: var(--accent-2);
            display: block;
            font-size: .85rem;
            font-weight: 700;
            margin-bottom: .35rem;
        }
        .moment-card h3 {
            color: var(--ink);
            font-size: 1.05rem;
            line-height: 1.28;
            margin: 0 0 .45rem;
        }
        .moment-card p {
            color: #344054;
            line-height: 1.6;
            margin: 0;
        }
        .learning-list {
            margin: .75rem 0 0;
            padding-left: 1.15rem;
            color: #344054;
            line-height: 1.75;
        }
        @media (max-width: 860px) {
            .cycle-hero {
                padding: 1.5rem;
            }
            .cycle-hero h1 {
                font-size: 2.15rem;
            }
            .moment-grid {
                grid-template-columns: 1fr;
            }
            .moment-card {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        f"""
        <section class="cycle-hero">
            <h1>{html.escape(PAGE_CONTENT["title"])}</h1>
            <p><strong>{html.escape(PAGE_CONTENT["subtitle"])}</strong></p>
            <p>{html.escape(PAGE_CONTENT["intro"])}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_reflection_block(block: ReflectionBlock) -> None:
    st.markdown(
        f"""
        <section class="cycle-section">
            <h2>{html.escape(block["title"])}</h2>
            <p>{html.escape(block["body"])}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_moments(moments: list[Moment]) -> None:
    if not moments:
        return

    cards = []
    for moment in moments:
        cards.append(
            '<div class="moment-card">'
            f'<span>{html.escape(moment["label"])}</span>'
            f'<h3>{html.escape(moment["title"])}</h3>'
            f'<p>{html.escape(moment["body"])}</p>'
            "</div>"
        )

    st.markdown(
        '<section class="cycle-section">'
        "<h2>Momentos clave</h2>"
        f'<div class="moment-grid">{"".join(cards)}</div>'
        "</section>",
        unsafe_allow_html=True,
    )


def render_learning_list(items: list[str]) -> None:
    if not items:
        return

    list_items = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    st.markdown(
        f"""
        <section class="cycle-section">
            <h2>Aprendizajes que me transformaron</h2>
            <ul class="learning-list">{list_items}</ul>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_media(items: list[MediaItem]) -> None:
    if not items:
        return

    st.markdown(
        """
        <section class="cycle-section">
            <h2>Recursos multimedia</h2>
        </section>
        """,
        unsafe_allow_html=True,
    )

    for media in items:
        media_path = APP_DIR / media["path"]
        caption = media.get("caption", "")
        if not media_path.exists():
            continue
        if media["type"] == "image":
            st.image(str(media_path), caption=caption, width="stretch")
        elif media["type"] == "video":
            st.video(str(media_path))
            if caption:
                st.caption(caption)


def main() -> None:
    inject_styles()
    render_hero()
    render_reflection_block(PAGE_CONTENT["computer_science"])
    render_reflection_block(PAGE_CONTENT["takeaways"])
    render_moments(KEY_MOMENTS)
    render_learning_list(LEARNINGS)
    render_media(MEDIA_ITEMS)
    render_reflection_block(PAGE_CONTENT["looking_forward"])


if __name__ == "__main__":
    main()
