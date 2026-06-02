from __future__ import annotations

from pathlib import Path

import streamlit as st

from utils.data_loader import APP_DIR, all_technologies, flatten_projects, load_portfolio, validation_warnings


st.set_page_config(
    page_title="Portafolio Ciclo 1 2026",
    page_icon="🎓",
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
            --soft: #f5f7fb;
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
        .project-card {
            min-height: 228px;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            padding: 1.1rem;
            box-shadow: 0 6px 18px rgba(23, 32, 51, .06);
        }
        .project-card h3 {
            color: var(--ink);
            font-size: 1.1rem;
            line-height: 1.25;
            margin: .35rem 0 .45rem 0;
        }
        .project-card p {
            color: var(--muted);
            font-size: .92rem;
            line-height: 1.45;
            margin: 0 0 .7rem 0;
        }
        .eyebrow {
            color: var(--accent-2);
            font-size: .78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: .04em;
        }
        .tag {
            display: inline-block;
            border: 1px solid #cfd8e3;
            background: #f8fafc;
            color: #334155;
            border-radius: 999px;
            padding: .18rem .5rem;
            margin: .12rem .16rem .12rem 0;
            font-size: .76rem;
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


def project_matches(project: dict, query: str) -> bool:
    if not query:
        return True
    haystack = " ".join(
        [
            project.get("name", ""),
            project.get("short_description", ""),
            project.get("introduction", ""),
            project.get("results", ""),
            project.get("learnings", ""),
            project.get("conclusions", ""),
            project.get("subject_name", ""),
            " ".join(project.get("technologies", [])),
        ]
    ).casefold()
    return query.casefold() in haystack


def filter_projects(projects: list[dict], subjects: list[dict], technologies: list[str]) -> list[dict]:
    subject_options = ["Todas"] + [subject["name"] for subject in subjects]
    selected_subject = st.sidebar.selectbox("Materia", subject_options)
    selected_tech = st.sidebar.multiselect("Herramientas y métodos", technologies)
    featured_only = st.sidebar.checkbox("Solo destacados")
    query = st.sidebar.text_input("Buscar", placeholder="Ej. Python, laboratorio, energía...")

    filtered = []
    for project in projects:
        if selected_subject != "Todas" and project["subject_name"] != selected_subject:
            continue
        if selected_tech and not set(selected_tech).issubset(set(project.get("technologies", []))):
            continue
        if featured_only and not project.get("featured"):
            continue
        if not project_matches(project, query):
            continue
        filtered.append(project)
    return filtered


def render_metrics(data: dict, projects: list[dict], technologies: list[str]) -> None:
    st.markdown(
        f"""
        <div class="metric-row">
            <div class="metric-box"><strong>{len(data.get("subjects", []))}</strong><span>Materias</span></div>
            <div class="metric-box"><strong>{len(projects)}</strong><span>Proyectos</span></div>
            <div class="metric-box"><strong>{len(technologies)}</strong><span>Herramientas y métodos</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card(project: dict) -> None:
    tags = "".join(f'<span class="tag">{tech}</span>' for tech in project.get("technologies", [])[:4])
    st.markdown(
        f"""
        <div class="project-card">
            <div class="eyebrow">{project["subject_name"]}</div>
            <h3>{project["name"]}</h3>
            <p>{project["short_description"]}</p>
            <div>{tags}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_gallery(project: dict) -> None:
    media_items = project.get("media", [])
    if not media_items:
        st.info("Este proyecto no tiene recursos multimedia públicos asociados todavía.")
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
    image = first_image(project)
    if image:
        st.image(str(APP_DIR / image), use_container_width=True)

    st.markdown(project.get("introduction", ""))

    sections = [
        ("Razón de realización", project.get("reason", "")),
        ("Autores", project.get("authors", "")),
        ("Resultados", project.get("results", "")),
        ("Aprendizajes", project.get("learnings", "")),
        ("Conclusiones", project.get("conclusions", "")),
        ("Agradecimientos", project.get("thanks", "")),
    ]
    for title, body in sections:
        st.markdown(f'<div class="detail-section"><h4>{title}</h4></div>', unsafe_allow_html=True)
        st.write(body)

    st.markdown('<div class="detail-section"><h4>Herramientas y métodos</h4></div>', unsafe_allow_html=True)
    st.write(" ".join(f"`{tech}`" for tech in project.get("technologies", [])))

    st.markdown('<div class="detail-section"><h4>Recursos disponibles</h4></div>', unsafe_allow_html=True)
    for resource in project.get("resources", []):
        st.write(f"- {resource}")

    st.markdown('<div class="detail-section"><h4>Galería pública</h4></div>', unsafe_allow_html=True)
    render_gallery(project)

    if project.get("privacy_note"):
        st.markdown(f'<div class="privacy-note">{project["privacy_note"]}</div>', unsafe_allow_html=True)


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
        with st.expander("Advertencias de validación del contenido"):
            for warning in warnings:
                st.warning(warning)

    render_metrics(data, projects, technologies)

    st.sidebar.title("Explorar portafolio")
    filtered = filter_projects(projects, data.get("subjects", []), technologies)
    st.sidebar.caption(f"{len(filtered)} de {len(projects)} proyectos visibles")

    if not filtered:
        st.info("No hay proyectos que coincidan con los filtros actuales.")
        return

    project_lookup = {f'{project["name"]} · {project["subject_name"]}': project for project in filtered}
    selected_label = st.selectbox("Abrir proyecto", list(project_lookup.keys()))
    selected_project = project_lookup[selected_label]

    tab_cards, tab_detail = st.tabs(["Vista general", "Detalle del proyecto"])

    with tab_cards:
        for row_start in range(0, len(filtered), 3):
            columns = st.columns(3)
            for column, project in zip(columns, filtered[row_start : row_start + 3]):
                with column:
                    image = first_image(project)
                    if image:
                        st.image(str(APP_DIR / image), use_container_width=True)
                    render_card(project)

    with tab_detail:
        render_detail(selected_project)


if __name__ == "__main__":
    main()
