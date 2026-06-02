from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from utils.validators import validate_portfolio


APP_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = APP_DIR / "data" / "portfolio.json"


@st.cache_data(show_spinner=False)
def load_portfolio() -> dict[str, Any]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def validation_warnings(data: dict[str, Any]) -> list[str]:
    return validate_portfolio(data, APP_DIR)


def flatten_projects(data: dict[str, Any]) -> list[dict[str, Any]]:
    projects: list[dict[str, Any]] = []
    for subject in data.get("subjects", []):
        for project in subject.get("projects", []):
            item = dict(project)
            item["subject_id"] = subject["id"]
            item["subject_name"] = subject["name"]
            item["subject_description"] = subject.get("description", "")
            projects.append(item)
    return projects


def all_technologies(projects: list[dict[str, Any]]) -> list[str]:
    values = {
        technology
        for project in projects
        for technology in project.get("technologies", [])
        if technology
    }
    return sorted(values, key=str.casefold)
