# Portafolio Streamlit Reutilizable

Aplicación pública en Streamlit para mostrar proyectos universitarios desde una fuente de datos reutilizable en `data/portfolio.json`.

## Ejecutar Localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estructura

```text
streamlit_portafolio/
├─ app.py
├─ data/portfolio.json
├─ assets/
├─ scripts/build_portfolio_data.py
├─ utils/data_loader.py
└─ utils/validators.py
```

## Agregar Una Materia

Edita `data/portfolio.json` y agrega un objeto nuevo dentro de `subjects`:

```json
{
  "id": "nueva_materia",
  "name": "Nueva Materia",
  "description": "Descripción corta de la materia.",
  "projects": []
}
```

Usa un `id` único, sin espacios ni acentos.

## Agregar Un Proyecto

Dentro de la materia correspondiente, agrega un objeto en `projects` con los campos ya usados por los demás proyectos:

```json
{
  "id": "mi-proyecto",
  "name": "Mi proyecto",
  "short_description": "Descripción breve.",
  "introduction": "Texto de introducción.",
  "reason": "Razón de realización.",
  "authors": "Autor del portafolio.",
  "technologies": ["Python", "Streamlit"],
  "results": "Resultados principales.",
  "learnings": "Aprendizajes.",
  "conclusions": "Conclusiones.",
  "thanks": "Agradecimientos.",
  "resources": ["archivo.py", "documento.pdf"],
  "media": [],
  "featured": false
}
```

## Agregar Imágenes O Videos

1. Crea una carpeta dentro de `assets/<materia>/<proyecto>/`.
2. Copia ahí la imagen optimizada.
3. Agrega la ruta relativa en `media`:

```json
{
  "type": "image",
  "path": "assets/algoritmos/mi-proyecto/imagen.jpg",
  "caption": "Descripción de la imagen"
}
```

Para GitHub y Streamlit Community Cloud, evita archivos grandes. La app advierte si un recurso pesa más de 25 MB o si está vacío.

## Regenerar Desde La Carpeta Portafolio

Si actualizas la carpeta `Portafolio/` con nuevos `PROYECTO.txt` y assets, puedes regenerar el JSON y los recursos optimizados:

```bash
python scripts/build_portfolio_data.py
```

El script omite videos mayores a 25 MB y archivos vacíos.

## Publicar En GitHub

1. Crea un repositorio en GitHub.
2. Sube la carpeta `streamlit_portafolio`.
3. Verifica que `requirements.txt`, `app.py`, `data/portfolio.json` y `assets/` estén incluidos.
4. Evita subir documentos privados, carnés, entrevistas identificables o datos sensibles.

## Desplegar En Streamlit Community Cloud

1. Entra a Streamlit Community Cloud.
2. Selecciona el repositorio de GitHub.
3. Configura:
   - Main file path: `app.py`
   - Python dependencies: `requirements.txt`
4. Despliega la app.

## Privacidad

Esta versión está preparada para portafolio público: no incluye carné, nombres de compañeros, entrevistas identificables ni datos biométricos crudos.
