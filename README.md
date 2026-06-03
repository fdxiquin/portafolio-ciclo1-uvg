# Portafolio Ciclo 1 2026

Portafolio academico en Streamlit para presentar proyectos universitarios seleccionados del primer ciclo en la Universidad del Valle de Guatemala.

## Ejecutar Localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estructura

```text
streamlit_portafolio/
|- app.py
|- pages/Portafolio.py
|- data/portfolio.json
|- assets/
|  `- inicio/
|- utils/data_loader.py
|- utils/validators.py
|- requirements.txt
`- README.md
```

`app.py` es la pagina de inicio. La pagina de proyectos esta en `pages/Portafolio.py`.

## Personalizar La Pagina De Inicio

Edita los textos del diccionario `PROFILE` en `app.py`:

- `name`
- `career`
- `years`
- `email`
- `about`
- `projection`
- `technical_skills`
- `personal_skills`

Agrega tus imagenes en `assets/inicio/` con estos nombres:

```text
foto.jpg
logo.png
```

Tambien funcionan las extensiones `.png`, `.jpg`, `.jpeg` y `.webp`, siempre que el nombre base sea `foto` o `logo`.

## Como Se Mantiene El Contenido

El contenido publico del portafolio se mantiene directamente en:

```text
data/portfolio.json
```

Las imagenes y videos publicos se guardan en:

```text
assets/<materia>/<proyecto>/
```

La app valida que los archivos multimedia declarados en el JSON existan, no esten vacios y no superen el limite recomendado de 25 MB.

## Agregar Una Materia

Edita `data/portfolio.json` y agrega un objeto nuevo dentro de `subjects`:

```json
{
  "id": "nueva_materia",
  "name": "Nueva Materia",
  "description": "Descripcion corta de la materia.",
  "thanks": "Agradecimiento o reflexion breve de la materia.",
  "projects": []
}
```

Usa un `id` unico, sin espacios ni acentos.

## Agregar Un Proyecto

Dentro de la materia correspondiente, agrega un objeto en `projects`:

```json
{
  "id": "mi-proyecto",
  "name": "Mi proyecto",
  "short_description": "Descripcion breve.",
  "introduction": "Texto de introduccion.",
  "reason": "Razon de realizacion.",
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

Si el proyecto necesita una nota publica de privacidad, puedes agregar:

```json
"privacy_note": "Se omitieron datos personales o sensibles."
```

## Agregar Imagenes O Videos

1. Crea una carpeta dentro de `assets/<materia>/<proyecto>/`.
2. Copia ahi el archivo optimizado.
3. Agrega la ruta relativa en `media`:

```json
{
  "type": "image",
  "path": "assets/algoritmos/mi-proyecto/imagen.jpg",
  "caption": "Descripcion de la imagen"
}
```

Para videos usa:

```json
{
  "type": "video",
  "path": "assets/algoritmos/mi-proyecto/demo.mp4",
  "caption": "Demo del proyecto"
}
```

## Publicar En GitHub

1. Crea un repositorio en GitHub.
2. Sube esta carpeta del proyecto.
3. Verifica que `requirements.txt`, `app.py`, `data/portfolio.json`, `utils/` y `assets/` esten incluidos.
4. Evita subir documentos privados, carnes, entrevistas identificables o datos sensibles.

## Desplegar En Streamlit Community Cloud

1. Entra a Streamlit Community Cloud.
2. Selecciona el repositorio de GitHub.
3. Configura:
   - Main file path: `app.py`
   - Python dependencies: `requirements.txt`
4. Despliega la app.

## Privacidad

Esta version esta preparada para portafolio publico: no incluye carne, nombres de companeros, entrevistas identificables ni datos biometricos crudos.
