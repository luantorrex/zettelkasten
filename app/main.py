import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .views.note_view import router as note_router
from .views.user_view import router as user_router
from .views.favorite_view import router as favorite_router
from .views.tag_view import router as tag_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Zettelkasten API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(note_router, prefix="/notes", tags=["notes"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(favorite_router, prefix="/favorites", tags=["favorites"])
app.include_router(tag_router, prefix="/tags", tags=["tags"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=3000, reload=True)
