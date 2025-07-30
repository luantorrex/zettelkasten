from fastapi import FastAPI
from .views.note_view import router as note_router
from .views.user_view import router as user_router

app = FastAPI(title="Zettelkasten API")

app.include_router(note_router, prefix="/notes", tags=["notes"])
app.include_router(user_router, prefix="/users", tags=["users"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
