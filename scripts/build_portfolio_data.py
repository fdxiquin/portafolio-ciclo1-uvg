from __future__ import annotations

import json
import re
import shutil
import unicodedata
from pathlib import Path

from PIL import Image, UnidentifiedImageError


APP_DIR = Path(__file__).resolve().parents[1]
ROOT = APP_DIR.parent
SOURCE_DIR = ROOT / "Portafolio"
DATA_DIR = APP_DIR / "data"
ASSETS_DIR = APP_DIR / "assets"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTS = {".mp4", ".mov", ".m4v"}
MAX_VIDEO_MB = 25

SUBJECTS = {
    "Algoritmos y Programación Básica": {
        "id": "algoritmos",
        "description": "Proyectos de programación, análisis de datos y solución de problemas.",
    },
    "Ciencias de la Vida": {
        "id": "ciencias_vida",
        "description": "Actividades de observación, análisis biológico, laboratorio y pensamiento científico.",
    },
    "Comunicación Efectiva": {
        "id": "comunicacion",
        "description": "Proyectos de investigación, escritura, exposición oral y comunicación audiovisual.",
    },
    "Introducción a Ingeniería CC y TI": {
        "id": "intro_ingenieria",
        "description": "Proyectos de introducción a tecnología, prototipado, programación y diseño de soluciones.",
    },
    "Pre-cálculo": {
        "id": "precalculo",
        "description": "Reflexiones y evidencias de razonamiento matemático, funciones y modelos.",
    },
    "Química General": {
        "id": "quimica",
        "description": "Prácticas y proyectos de laboratorio vinculados con energía, química experimental y comunicación científica.",
    },
}

FIELD_MAP = {
    "Nombre": "name",
    "Descripción corta": "short_description",
    "Introducción": "introduction",
    "Razón de realización": "reason",
    "Autores": "authors",
    "Tecnologías utilizadas": "technologies",
    "Resultados": "results",
    "Aprendizajes": "learnings",
    "Conclusiones": "conclusions",
    "Agradecimientos": "thanks",
    "Recursos disponibles": "resources",
    "Fotografías sugeridas": "photo_suggestions",
    "Nota pública de privacidad": "privacy_note",
}

FEATURED_IDS = {
    "analisis-steam",
    "tbl2",
    "proyecto-integrador",
    "video-juego-con-geenfoot",
    "proyecto-final",
    "booktrailer",
}


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value)
    ascii_value = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    ascii_value = ascii_value.lower()
    ascii_value = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    return ascii_value or "item"


def parse_project_text(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    current_field: str | None = None
    parsed: dict[str, object] = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line in FIELD_MAP:
            current_field = FIELD_MAP[line]
            parsed[current_field] = []
            continue
        if current_field is None:
            continue
        if not line:
            continue
        if line.startswith("- "):
            parsed[current_field].append(line[2:].strip())  # type: ignore[index]
        else:
            parsed[current_field].append(line)  # type: ignore[index]

    for key, value in list(parsed.items()):
        if key in {"technologies", "resources", "photo_suggestions"}:
            parsed[key] = value
        else:
            parsed[key] = "\n".join(value) if isinstance(value, list) else value

    return parsed


def optimize_image(src: Path, dst: Path) -> bool:
    if src.stat().st_size == 0:
        return False
    try:
        with Image.open(src) as image:
            image = image.convert("RGB")
            image.thumbnail((1600, 1200))
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst = dst.with_suffix(".jpg")
            image.save(dst, "JPEG", quality=84, optimize=True)
        return True
    except (OSError, UnidentifiedImageError):
        return False


def copy_video(src: Path, dst: Path) -> bool:
    if src.stat().st_size == 0:
        return False
    if src.stat().st_size > MAX_VIDEO_MB * 1024 * 1024:
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def media_caption(path: Path) -> str:
    label = path.stem.replace("_", " ").replace("-", " ").strip()
    return label[:1].upper() + label[1:] if label else "Recurso visual"


def migrate_project_assets(project_dir: Path, subject_id: str, project_id: str) -> list[dict[str, str]]:
    media: list[dict[str, str]] = []
    asset_root = ASSETS_DIR / subject_id / project_id
    source_assets = [item for item in project_dir.iterdir() if item.is_dir() and item.name.startswith("Archivos_")]

    for source_asset_dir in source_assets:
        for src in sorted(source_asset_dir.iterdir(), key=lambda item: item.name.casefold()):
            if not src.is_file():
                continue
            suffix = src.suffix.lower()
            if suffix in IMAGE_EXTS:
                dst = asset_root / f"{slugify(src.stem)}.jpg"
                if optimize_image(src, dst):
                    media.append(
                        {
                            "type": "image",
                            "path": str(dst.relative_to(APP_DIR)).replace("\\", "/"),
                            "caption": media_caption(src),
                        }
                    )
            elif suffix in VIDEO_EXTS:
                dst = asset_root / f"{slugify(src.stem)}{suffix}"
                if copy_video(src, dst):
                    media.append(
                        {
                            "type": "video",
                            "path": str(dst.relative_to(APP_DIR)).replace("\\", "/"),
                            "caption": media_caption(src),
                        }
                    )

    return media


def build_portfolio() -> dict[str, object]:
    if not SOURCE_DIR.exists():
        raise FileNotFoundError(f"No existe la carpeta fuente: {SOURCE_DIR}")

    if ASSETS_DIR.exists():
        shutil.rmtree(ASSETS_DIR)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    subjects = []
    for subject_name, meta in SUBJECTS.items():
        subject_dir = SOURCE_DIR / subject_name
        if not subject_dir.exists():
            continue

        subject = {
            "id": meta["id"],
            "name": subject_name,
            "description": meta["description"],
            "projects": [],
        }

        for project_dir in sorted([item for item in subject_dir.iterdir() if item.is_dir()], key=lambda item: item.name.casefold()):
            project_text = project_dir / "PROYECTO.txt"
            if not project_text.exists():
                continue

            parsed = parse_project_text(project_text)
            project_id = slugify(project_dir.name)
            media = migrate_project_assets(project_dir, meta["id"], project_id)

            project = {
                "id": project_id,
                "name": parsed.get("name", project_dir.name),
                "short_description": parsed.get("short_description", ""),
                "introduction": parsed.get("introduction", ""),
                "reason": parsed.get("reason", ""),
                "authors": parsed.get("authors", ""),
                "technologies": parsed.get("technologies", []),
                "results": parsed.get("results", ""),
                "learnings": parsed.get("learnings", ""),
                "conclusions": parsed.get("conclusions", ""),
                "thanks": parsed.get("thanks", ""),
                "resources": parsed.get("resources", []),
                "media": media,
                "featured": project_id in FEATURED_IDS,
                "privacy_note": parsed.get("privacy_note", ""),
            }
            subject["projects"].append(project)

        subjects.append(subject)

    return {
        "site": {
            "title": "Portafolio Ciclo 1 2026",
            "owner": "Daniel Fernando Xiquin Tezén",
            "subtitle": "Proyectos universitarios seleccionados",
            "privacy_note": "Versión pública sin carné, nombres de terceros, entrevistas identificables ni datos sensibles.",
        },
        "subjects": subjects,
    }


def main() -> None:
    portfolio = build_portfolio()
    output = DATA_DIR / "portfolio.json"
    output.write_text(json.dumps(portfolio, ensure_ascii=False, indent=2), encoding="utf-8")
    project_count = sum(len(subject["projects"]) for subject in portfolio["subjects"])  # type: ignore[index]
    print(f"Materias: {len(portfolio['subjects'])}")
    print(f"Proyectos: {project_count}")
    print(f"JSON: {output}")


if __name__ == "__main__":
    main()
