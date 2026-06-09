from __future__ import annotations

import re

import streamlit as st

from utils.data_loader import APP_DIR, all_technologies, flatten_projects, load_portfolio, validation_warnings


st.set_page_config(
    page_title="Proyectos | Portafolio Ciclo 1 2026",
    page_icon="DP",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }
        .hero {
            padding: 2.1rem 2.4rem;
            border-radius: 8px;
            border: 1px solid var(--line);
            background: linear-gradient(135deg, #f8fbff 0%, #ffffff 48%, #f7fbf7 100%);
            margin-bottom: 1.4rem;
        }
        .hero h1 {
            font-size: 2.6rem;
            line-height: 1.08;
            margin: 0 0 .5rem 0;
            color: var(--ink);
            letter-spacing: 0;
        }
        .hero p {
            color: var(--muted);
            font-size: 1.05rem;
            margin: 0;
        }
        .metric-row {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .8rem;
            margin: 1rem 0 1.4rem;
        }
        .metric-box {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem 1.1rem;
            background: var(--panel);
        }
        .metric-box strong {
            display: block;
            font-size: 1.55rem;
            color: var(--accent);
        }
        .metric-box span {
            color: var(--muted);
            font-size: .9rem;
        }
        div[class*="st-key-project_card_"] button {
            min-height: 228px;
            width: 100%;
            align-items: flex-start;
            justify-content: flex-start;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            box-shadow: 0 6px 18px rgba(23, 32, 51, .06);
            color: var(--ink);
            line-height: 1.35;
            padding: 1.1rem;
            text-align: left;
            transition: border-color .15s ease, box-shadow .15s ease, transform .15s ease;
            white-space: normal;
        }
        div[class*="st-key-project_card_"] button:hover {
            border-color: var(--accent);
            box-shadow: 0 10px 24px rgba(23, 32, 51, .1);
            color: var(--ink);
            transform: translateY(-2px);
        }
        .detail-section {
            border-top: 1px solid var(--line);
            padding-top: 1rem;
            margin-top: 1rem;
        }
        .detail-section h4 {
            margin: 0 0 .4rem 0;
            color: var(--ink);
        }
        .privacy-note {
            border-left: 4px solid var(--accent);
            background: #eef7fa;
            padding: .9rem 1rem;
            border-radius: 6px;
            color: #184355;
            margin: 1rem 0;
        }
        .thanks-note {
            border-left: 4px solid var(--accent-2);
            background: #fff6f0;
            padding: .9rem 1rem;
            border-radius: 6px;
            color: #65402d;
            margin: 1rem 0 1.4rem;
        }
        @media (max-width: 800px) {
            .metric-row { grid-template-columns: 1fr; }
            .hero { padding: 1.4rem; }
            .hero h1 { font-size: 2rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def first_image(project: dict) -> str | None:
    for media in project.get("media", []):
        if media.get("type") == "image":
            return media.get("path")
    return None


def filter_projects(projects: list[dict], subjects: list[dict], technologies: list[str]) -> tuple[list[dict], str]:
    subject_options = ["Todas"] + [subject["name"] for subject in subjects]
    selected_subject = st.sidebar.selectbox("Materia", subject_options)
    selected_tech = st.sidebar.multiselect("Herramientas y metodos", technologies)
    featured_only = st.sidebar.checkbox("Solo destacados")

    filtered = []
    for project in projects:
        if selected_subject != "Todas" and project["subject_name"] != selected_subject:
            continue
        if selected_tech and not set(selected_tech).issubset(set(project.get("technologies", []))):
            continue
        if featured_only and not project.get("featured"):
            continue
        filtered.append(project)
    return filtered, selected_subject


def safe_key(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", value)


def open_project(project: dict) -> None:
    st.session_state["open_project_id"] = project["id"]


def close_project_dialog() -> None:
    st.session_state.pop("open_project_id", None)


def opened_project(projects: list[dict]) -> dict | None:
    project_id = st.session_state.get("open_project_id")
    return next((project for project in projects if project.get("id") == project_id), None)


def render_thanks(data: dict, selected_subject: str) -> None:
    if selected_subject == "Todas":
        thanks = data.get("site", {}).get("thanks", "")
    else:
        subject = next(
            (item for item in data.get("subjects", []) if item.get("name") == selected_subject),
            {},
        )
        thanks = subject.get("thanks", "")

    if thanks:
        st.markdown(f'<div class="thanks-note"><strong>Agradecimientos</strong><br>{thanks}</div>', unsafe_allow_html=True)


def render_metrics(data: dict, projects: list[dict], technologies: list[str]) -> None:
    st.markdown(
        f"""
        <div class="metric-row">
            <div class="metric-box"><strong>{len(data.get("subjects", []))}</strong><span>Materias</span></div>
            <div class="metric-box"><strong>{len(projects)}</strong><span>Proyectos</span></div>
            <div class="metric-box"><strong>{len(technologies)}</strong><span>Herramientas y metodos</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card(project: dict) -> None:
    technologies = ", ".join(project.get("technologies", [])[:4])
    label = (
        f"{project['subject_name']}\n\n"
        f"**{project['name']}**\n\n"
        f"{project['short_description']}\n\n"
        f"{technologies}"
    )

    with st.container(key=f"project_card_{safe_key(project['id'])}"):
        if st.button(label, key=f"open_{safe_key(project['id'])}", use_container_width=True):
            open_project(project)
            st.rerun()


def render_gallery(project: dict) -> None:
    media_items = project.get("media", [])
    if not media_items:
        st.info("Este proyecto no tiene recursos multimedia publicos asociados todavia.")
        return

    for media in media_items:
        path = APP_DIR / media["path"]
        caption = media.get("caption", "Recurso visual")
        if media.get("type") == "image":
            st.image(str(path), caption=caption, use_container_width=True)
        elif media.get("type") == "video":
            st.video(str(path))
            st.caption(caption)


def render_detail(project: dict) -> None:
    st.markdown(f"## {project['name']}")
    st.caption(project["subject_name"])
    st.markdown(project.get("introduction", ""))

    sections1 = [
        ("Autores", project.get("authors", "")),
        ("Razon de realizacion", project.get("reason", "")),
        ("Nivel de dominio de la taxonomia de Bloom", project.get("bloom_level", "")),
        ("Explicacion del nivel de dominio de la taxonomia de Bloom", project.get("reason_bloom_level", "")),
    ]
    sections2 = [
        ("Resultados", project.get("results", "")),
        ("Aprendizajes", project.get("learnings", "")),
        ("Conclusiones", project.get("conclusions", "")),
    ]

    
    for title, body in sections1:
        st.markdown(f'<div class="detail-section"><h4>{title}</h4></div>', unsafe_allow_html=True)
        st.write(body)

    image = first_image(project)
    if image:
        st.image(str(APP_DIR / image), use_container_width=True)

    for title, body in sections2:
        st.markdown(f'<div class="detail-section"><h4>{title}</h4></div>', unsafe_allow_html=True)
        st.write(body)
        
    st.markdown('<div class="detail-section"><h4>Herramientas y metodos</h4></div>', unsafe_allow_html=True)
    st.write(" ".join(f"`{tech}`" for tech in project.get("technologies", [])))

    st.markdown('<div class="detail-section"><h4>Recursos disponibles</h4></div>', unsafe_allow_html=True)
    for resource in project.get("resources", []):
        st.write(f"- {resource}")

    st.markdown('<div class="detail-section"><h4>Galeria publica</h4></div>', unsafe_allow_html=True)
    render_gallery(project)

    if project.get("privacy_note"):
        st.markdown(f'<div class="privacy-note">{project["privacy_note"]}</div>', unsafe_allow_html=True)


@st.dialog("Detalle del proyecto", width="large", dismissible=True, on_dismiss=close_project_dialog)
def render_project_dialog(project: dict) -> None:
    render_detail(project)
    if st.button("Cerrar"):
        close_project_dialog()
        st.rerun()


def main() -> None:
    inject_styles()
    data = load_portfolio()
    projects = flatten_projects(data)
    technologies = all_technologies(projects)

    site = data["site"]
    st.markdown(
        f"""
        <section class="hero">
            <h1>{site["title"]}</h1>
            <p>{site["subtitle"]} · {site["owner"]}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="privacy-note">{site["privacy_note"]}</div>', unsafe_allow_html=True)

    warnings = validation_warnings(data)
    if warnings:
        with st.expander("Advertencias de validacion del contenido"):
            for warning in warnings:
                st.warning(warning)

    render_metrics(data, projects, technologies)

    st.sidebar.title("Explorar portafolio")
    filtered, selected_subject = filter_projects(projects, data.get("subjects", []), technologies)
    st.sidebar.caption(f"{len(filtered)} de {len(projects)} proyectos visibles")

    if not filtered:
        st.info("No hay proyectos que coincidan con los filtros actuales.")
        render_thanks(data, selected_subject)
        return

    dialog_project = opened_project(filtered)

    if dialog_project:
        render_project_dialog(dialog_project)

    for row_start in range(0, len(filtered), 3):
        columns = st.columns(3)
        for column, project in zip(columns, filtered[row_start : row_start + 3]):
            with column:
                render_card(project)

    render_thanks(data, selected_subject)


if __name__ == "__main__":
    main()
