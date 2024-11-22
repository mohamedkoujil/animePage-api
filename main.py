from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from animeflv import AnimeFLV, EpisodeFormat
from animeflv.exception import AnimeFLVParseError
from pydantic import BaseModel
from typing import Optional, List, Union
from enum import Enum

app = FastAPI(
    title="Anime API",
    description="API para listar animes, ver episodios recientes y obtener servidores de video.",
    version="1.0.0",
)
# command to run the server:
# uvicorn main:app --reload
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Cambia esto si tu frontend está en otro dominio o puerto
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)



# Definición de modelos de respuesta
class EpisodeInfoResponse(BaseModel):
    id: Union[str, int]
    anime: str
    image_preview: Optional[str]


class AnimeInfoResponse(BaseModel):
    id: Union[str, int]
    title: str
    poster: Optional[str]
    banner: Optional[str]
    synopsis: Optional[str]
    rating: Optional[str]
    genres: Optional[List[str]]
    debut: Optional[str]
    type: Optional[str]
    episodes: Optional[List[EpisodeInfoResponse]]


class DownloadLinkInfoResponse(BaseModel):
    server: str
    url: str


# Enum para el formato del episodio
class EpisodeFormatEnum(str, Enum):
    subtitled = "subtitled"
    dubbed = "dubbed"


# Manejador de errores
@app.exception_handler(AnimeFLVParseError)
async def anime_flv_parse_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"Error al procesar AnimeFLV: {str(exc)}"},
    )


# Endpoints
@app.get("/search", summary="Buscar animes", response_model=List[AnimeInfoResponse])
def search_anime(
        query: Optional[str] = Query(
            None,
            description="Título del anime a buscar",
            examples="Naruto"
        ),
        page: Optional[int] = Query(
            None,
            description="Número de página para los resultados",
            examples=1
        )
):
    """
    Busca animes en AnimeFLV. Si no se proporciona un `query`, devuelve la lista de animes.
    """
    try:
        with AnimeFLV() as anime_flv:
            animes = anime_flv.search(query=query, page=page)
            return animes
    except AnimeFLVParseError as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar animes: {str(e)}")


@app.get("/anime/{id}", summary="Obtener información de un anime", response_model=AnimeInfoResponse)
def get_anime_info(id: str):
    """
    Obtiene información detallada sobre un anime específico por su ID.
    """
    try:
        with AnimeFLV() as anime_flv:
            anime_info = anime_flv.get_anime_info(id=id)
            return anime_info
    except AnimeFLVParseError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener información del anime: {str(e)}")


@app.get("/latest-episodes", summary="Obtener episodios recientes", response_model=List[EpisodeInfoResponse])
def get_latest_episodes():
    """
    Obtiene una lista de episodios recientes lanzados en AnimeFLV.
    """
    try:
        with AnimeFLV() as anime_flv:
            episodes = anime_flv.get_latest_episodes()
            return episodes
    except AnimeFLVParseError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener episodios recientes: {str(e)}")


@app.get("/anime/{id}/episode/{episode}/servers", summary="Obtener servidores de video de un episodio")
def get_video_servers(
        id: str,
        episode: int,
        format: EpisodeFormatEnum = EpisodeFormatEnum.subtitled
):
    """
    Obtiene los servidores de video disponibles para un episodio específico de un anime.
    """
    try:
        with AnimeFLV() as anime_flv:
            episode_format = (
                EpisodeFormat.Subtitled if format == EpisodeFormatEnum.subtitled else EpisodeFormat.Dubbed
            )
            servers = anime_flv.get_video_servers(id=id, episode=episode, format=episode_format)
            return servers
    except AnimeFLVParseError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener servidores de video: {str(e)}")
