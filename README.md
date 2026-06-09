# Portafolio Ciclo 1 2026

Portafolio academico desarrollado con Streamlit para presentar proyectos universitarios seleccionados del primer ciclo 2026 en la Universidad del Valle de Guatemala.

## Estado De Version

**V1 lista - 9 de junio de 2026**

Esta version deja establecida la estructura principal del portafolio, la navegacion por paginas, la pagina de inicio, la vista de proyectos academicos, la reflexion del primer ciclo y la organizacion publica de datos y recursos multimedia.

## Ejecutar Localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

La aplicacion se abre normalmente en:

```text
http://localhost:8501
```

## Estructura Del Proyecto

```text
streamlit_portafolio/
|- app.py
|- views/
|  |- inicio.py
|  |- portafolio.py
|  `- primer_ciclo.py
|- data/
|  `- portfolio.json
|- assets/
|  `- inicio/
|- utils/
|  |- data_loader.py
|  `- validators.py
|- requirements.txt
`- README.md
```

## Navegacion

`app.py` controla la navegacion principal con `st.Page` y `st.navigation`.

Los nombres visibles en la barra lateral se configuran directamente en `app.py`, por lo que ya no dependen del nombre del archivo:

```python
pages = [
    st.Page("views/inicio.py", title="Inicio", icon=":material/home:", default=True),
    st.Page("views/portafolio.py", title="Portafolio académico", icon=":material/folder:"),
    st.Page("views/primer_ciclo.py", title="Mi primer ciclo en UVG", icon=":material/school:"),
]
```

## Paginas

- `views/inicio.py`: pagina de presentacion personal, perfil, fotografia, logo, habilidades y proyeccion.
- `views/portafolio.py`: pagina de proyectos academicos, filtros por materia, herramientas, destacados, detalle de proyecto y galeria publica.
- `views/primer_ciclo.py`: reflexion personal sobre el primer ciclo universitario.

## Personalizar La Pagina De Inicio

Edita el diccionario `PROFILE` en:

```text
views/inicio.py
```

Campos principales:

- `name`
- `career`
- `years`
- `email`
- `phone_number`
- `promedio`
- `about`
- `projection`
- `technical_skills`
- `personal_skills`

Las imagenes de inicio se cargan desde:

```text
assets/inicio/Foto.jpg
assets/inicio/Logo.png
```

## Contenido Del Portafolio

El contenido publico de materias, proyectos, descripciones, resultados, aprendizajes, conclusiones, recursos y multimedia se mantiene en:

```text
data/portfolio.json
```

Las imagenes y videos publicos se guardan en:

```text
assets/<materia>/<proyecto>/
```

La aplicacion valida que los archivos multimedia declarados en el JSON existan, no esten vacios y no superen el limite recomendado de 25 MB.

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
  "authors": "Autor del portafolio.",
  "reason": "Razon de realizacion.",
  "bloom_level": "Nivel de taxonomia de Bloom",
  "reason_bloom_level": "Explicacion del nivel de taxonomia de Bloom",
  "technologies": ["Python", "Streamlit"],
  "results": "Resultados principales.",
  "learnings": "Aprendizajes.",
  "conclusions": "Conclusiones.",
  "resources": ["archivo.py", "documento.pdf"],
  "media": [],
  "featured": false
}
```

Si el proyecto necesita una nota publica de privacidad, agrega:

```json
"privacy_note": "Se omitieron datos personales o sensibles."
```

## Agregar Imagenes O Videos

1. Crea una carpeta dentro de `assets/<materia>/<proyecto>/`.
2. Copia ahi el archivo optimizado.
3. Agrega la ruta relativa en `media`.

Ejemplo de imagen:

```json
{
  "type": "image",
  "path": "assets/algoritmos/mi-proyecto/imagen.jpg",
  "caption": "Descripcion de la imagen"
}
```

Ejemplo de video:

```json
{
  "type": "video",
  "path": "assets/algoritmos/mi-proyecto/demo.mp4",
  "caption": "Demo del proyecto"
}
```

## Validaciones

El proyecto incluye validaciones en `utils/validators.py` para revisar:

- campos requeridos del sitio, materias y proyectos
- IDs duplicados de materias o proyectos
- archivos multimedia faltantes
- archivos multimedia vacios
- archivos multimedia mayores a 25 MB

## Privacidad

Este portafolio esta creado con fines academicos, personales y publicos. Se omiten datos personales, datos sensibles y contenidos no autorizados cuando corresponde.

Esta prohibida la extraccion parcial o total de la informacion contenida en el proyecto sin autorizacion.
