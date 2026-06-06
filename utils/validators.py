from __future__ import annotations

from pathlib import Path
from typing import Any


REQUIRED_SITE_FIELDS = {"title", "owner", "subtitle", "privacy_note", "thanks"}
REQUIRED_SUBJECT_FIELDS = {"id", "name", "description", "thanks", "projects"}
REQUIRED_PROJECT_FIELDS = {
    "id",
    "name",
    "short_description",
    "introduction",
    "reason",
    "authors",
    "bloom_level",
    "technologies",
    "results",
    "learnings",
    "conclusions",
    "resources",
    "media",
    "featured",
}

MAX_ASSET_MB = 25


def validate_portfolio(data: dict[str, Any], base_dir: Path) -> list[str]:
    """Return human-readable warnings for content problems."""
    warnings: list[str] = []

    site = data.get("site", {})
    missing_site = REQUIRED_SITE_FIELDS - set(site)
    if missing_site:
        warnings.append(f"Faltan campos de site: {', '.join(sorted(missing_site))}")

    subjects = data.get("subjects", [])
    if not isinstance(subjects, list) or not subjects:
        warnings.append("No hay materias en data/portfolio.json.")
        return warnings

    subject_ids: set[str] = set()
    project_ids: set[str] = set()

    for subject in subjects:
        missing_subject = REQUIRED_SUBJECT_FIELDS - set(subject)
        if missing_subject:
            warnings.append(
                f"Materia sin campos requeridos ({subject.get('name', 'sin nombre')}): "
                f"{', '.join(sorted(missing_subject))}"
            )

        subject_id = subject.get("id")
        if subject_id in subject_ids:
            warnings.append(f"ID de materia duplicado: {subject_id}")
        subject_ids.add(subject_id)

        projects = subject.get("projects", [])
        if not isinstance(projects, list):
            warnings.append(f"La materia {subject.get('name', subject_id)} no tiene lista de proyectos.")
            continue

        for project in projects:
            missing_project = REQUIRED_PROJECT_FIELDS - set(project)
            if missing_project:
                warnings.append(
                    f"Proyecto sin campos requeridos ({project.get('name', 'sin nombre')}): "
                    f"{', '.join(sorted(missing_project))}"
                )

            project_id = project.get("id")
            if project_id in project_ids:
                warnings.append(f"ID de proyecto duplicado: {project_id}")
            project_ids.add(project_id)

            for media in project.get("media", []):
                path_value = media.get("path")
                if not path_value:
                    warnings.append(f"Medio sin path en proyecto {project.get('name', project_id)}.")
                    continue

                media_path = base_dir / path_value
                if not media_path.exists():
                    warnings.append(f"No existe el archivo multimedia: {path_value}")
                    continue

                size = media_path.stat().st_size
                if size == 0:
                    warnings.append(f"Archivo multimedia vacío: {path_value}")
                if size > MAX_ASSET_MB * 1024 * 1024:
                    warnings.append(f"Archivo multimedia pesado (> {MAX_ASSET_MB} MB): {path_value}")

    return warnings
