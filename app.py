from __future__ import annotations

import html
from pathlib import Path

import streamlit as st

from utils.data_loader import APP_DIR


PROFILE = {
    "name": "Tu nombre completo",
    "career": "Tu carrera",
    "years": "Tus anos de experiencia o etapa academica",
    "email": "tu.correo@ejemplo.com",
    "about": (
        "Escribe aqui un texto largo sobre ti. Puedes explicar quien eres, que te interesa, "
        "que tipo de problemas te gusta resolver, como ha sido tu formacion y que valores "
        "quieres reflejar en tu portafolio."
    ),
    "projection": (
        "Escribe aqui tu proyeccion personal. Puedes hablar de tus metas academicas, "
        "profesionales y personales, las areas en las que quieres crecer y el impacto que "
        "te gustaria construir con tu carrera."
    ),
    "technical_skills": [
        "Habilidad tecnica 1",
        "Habilidad tecnica 2",
        "Habilidad tecnica 3",
    ],
    "personal_skills": [
        "Habilidad personal 1",
        "Habilidad personal 2",
        "Habilidad personal 3",
    ],
}

PROFILE_ASSET_DIR = APP_DIR / "assets" / "inicio"
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")


st.set_page_config(
    page_title="Inicio | Portafolio",
    page_icon="DP",
    layout="wide",
    initial_sidebar_state="expanded",
)


def find_asset(stem: str) -> Path | None:
    for extension in IMAGE_EXTENSIONS:
        path = PROFILE_ASSET_DIR / f"{stem}{extension}"
        if path.exists():
            return path
    return None


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
        .hero-copy {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: linear-gradient(135deg, #f8fbff 0%, #ffffff 55%, #f7fbf7 100%);
            padding: 2.2rem 2.4rem;
        }
        .hero-copy h1 {
            color: var(--ink);
            font-size: 3rem;
            line-height: 1.04;
            letter-spacing: 0;
            margin: 0 0 .7rem;
        }
        .hero-copy p {
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.55;
            margin: 0;
        }
        .asset-placeholder {
            display: grid;
            place-items: center;
            min-height: 240px;
            border: 1px dashed #a7b4c2;
            border-radius: 8px;
            background: var(--wash);
            color: var(--muted);
            text-align: center;
            padding: 1rem;
        }
        .mini-placeholder {
            display: grid;
            place-items: center;
            width: 96px;
            height: 96px;
            border: 1px dashed #a7b4c2;
            border-radius: 8px;
            background: var(--wash);
            color: var(--muted);
            font-size: .82rem;
            text-align: center;
        }
        .identity h2 {
            color: var(--ink);
            font-size: 1.35rem;
            line-height: 1.2;
            margin: 0 0 .25rem;
        }
        .identity p {
            color: var(--muted);
            margin: 0;
            line-height: 1.45;
        }
        .section {
            border-top: 1px solid var(--line);
            padding-top: 1.2rem;
            margin-top: 1.2rem;
        }
        .section h3 {
            color: var(--ink);
            font-size: 1.25rem;
            margin: 0 0 .55rem;
        }
        .section p {
            color: #344054;
            font-size: 1rem;
            line-height: 1.65;
            margin: 0;
        }
        .skill-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1rem;
            margin-top: .7rem;
        }
        .skill-box {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            padding: 1rem 1.1rem;
        }
        .skill-box h4 {
            color: var(--accent);
            margin: 0 0 .55rem;
            font-size: 1rem;
        }
        .skill-box ul {
            margin: 0;
            padding-left: 1.15rem;
            color: #344054;
            line-height: 1.7;
        }
        @media (max-width: 860px) {
            .skill-grid {
                grid-template-columns: 1fr;
            }
            .hero-copy {
                padding: 1.5rem;
            }
            .hero-copy h1 {
                font-size: 2.2rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_photo(path: Path | None) -> None:
    if path:
        st.image(str(path), use_container_width=True)
    else:
        st.markdown('<div class="asset-placeholder">Foto</div>', unsafe_allow_html=True)


def render_logo(path: Path | None) -> None:
    if path:
        st.image(str(path), use_container_width=True)
    else:
        st.markdown('<div class="mini-placeholder">Logo</div>', unsafe_allow_html=True)


def render_list(items: list[str]) -> str:
    return "".join(f"<li>{html.escape(item)}</li>" for item in items)


def main() -> None:
    inject_styles()
    photo = find_asset("foto")
    logo = find_asset("logo")

    hero_col, media_col = st.columns([1.35, .65], gap="large")

    with hero_col:
        st.markdown(
            f"""
            <div class="hero-copy">
                <h1>Portafolio profesional de {html.escape(PROFILE["name"])}</h1>
                <p>{html.escape(PROFILE["career"])} · {html.escape(PROFILE["years"])} · {html.escape(PROFILE["email"])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with media_col:
        render_photo(photo)
        logo_col, info_col = st.columns([.35, .65], gap="medium")
        with logo_col:
            render_logo(logo)
        with info_col:
            st.markdown(
                f"""
                <div class="identity">
                    <h2>{html.escape(PROFILE["name"])}</h2>
                    <p>{html.escape(PROFILE["career"])}</p>
                    <p>{html.escape(PROFILE["email"])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        f"""
        <section class="section">
            <h3>Sobre mi</h3>
            <p>{html.escape(PROFILE["about"])}</p>
        </section>
        <section class="section">
            <h3>Proyeccion personal</h3>
            <p>{html.escape(PROFILE["projection"])}</p>
        </section>
        <section class="section">
            <h3>Habilidades</h3>
            <div class="skill-grid">
                <div class="skill-box">
                    <h4>Tecnicas</h4>
                    <ul>{render_list(PROFILE["technical_skills"])}</ul>
                </div>
                <div class="skill-box">
                    <h4>Personales</h4>
                    <ul>{render_list(PROFILE["personal_skills"])}</ul>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
