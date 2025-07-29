from fastapi import FastAPI
from .views.note_view import router as note_router

app = FastAPI(title="Zettelkasten API")

app.include_router(note_router, prefix="/notes", tags=["notes"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
