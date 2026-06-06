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
  "authors": "Autor del portafolio.",
  "reason": "Razon de realizacion.",
  "bloom_level":"Nivel de taxonomia de bloom",
  "reason_bloom_level":"Explicación del nivel de taxonomia de bloom",
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

##Privacidad

Este portafolio esta creado con fines académicos, es de uno académico y personal
Esta totalmente prohibida la extracción parcial o total de la información contenida en el proyecto.