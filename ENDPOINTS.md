* **Buscar animes**
  **GET `/search`**
  * **Descripción**: Busca animes en AnimeFLV según un título o devuelve una lista general si no se proporciona una consulta.
  * **Parámetros**:

    * `query` (opcional): Título del anime a buscar.
    * `page` (opcional): Número de página para los resultados.
  * **Respuesta**:

    {
    "id": "naruto",
    "title": "Naruto",
    "poster": "url_a_la_imagen",
    "banner": "url_a_la_imagen",
    "synopsis": "Sinopsis del anime.",
    "rating": "4.5",
    "genres": ["Acción", "Aventura"],
    "debut": "2002",
    "type": "Anime",
    "episodes": null
    }
    ]
    </code></div></div></pre>
* **Obtener información de un anime**
  **GET `/anime/{id}`**
  * **Descripción**: Obtiene información detallada de un anime por su ID.
  * **Parámetros**:
    * `id`: ID único del anime (ejemplo: `naruto`).
  * **Respuesta**:
    {
    "id": "naruto",
    "title": "Naruto",
    "poster": "url_a_la_imagen",
    "banner": "url_a_la_imagen",
    "synopsis": "Sinopsis del anime.",
    "rating": "4.5",
    "genres": ["Acción", "Aventura"],
    "debut": "2002",
    "type": "Anime",
    "episodes": [
    {
    "id": 1,
    "anime": "naruto",
    "image_preview": "url_a_la_imagen_preview"
    }
    ]
    }
    </code></div></div></pre>
* **Obtener episodios recientes**
  **GET `/latest-episodes`**
  * **Descripción**: Devuelve una lista de episodios recientes lanzados.
  * **Respuesta**:
    [
    {
    "id": 1,
    "anime": "naruto",
    "image_preview": "url_a_la_imagen_preview"
    }
    ]
    </code></div></div></pre>
* **Obtener servidores de video de un episodio**
  **GET `/anime/{id}/episode/{episode}/servers`**
  * **Descripción**: Obtiene los servidores de video disponibles para un episodio de un anime.
  * **Parámetros**:
    * `id`: ID único del anime (ejemplo: `naruto`).
    * `episode`: Número del episodio.
    * `format` (opcional): Formato del episodio (`subtitled` o `dubbed`).
  * **Respuesta**:
    [
    {
    "server": "Servidor1",
    "url": "url_del_video"
    }
    ]</code></div></div></pre>
