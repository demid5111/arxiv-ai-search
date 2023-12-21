from app.database import DataBase
from app.model import Model
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


class Item(BaseModel):
    text: str

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

model = Model()

settings = {
    "name":"arxiv"
}
db = DataBase(settings)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/embedding/")
async def get_embedding(item: Item):
    embedding = model.embedding(item.text)
    return {'embedding': embedding.tolist()}

@app.post("/add/")
async def get_embedding(item: Item):
    embedding = model.embedding(item.text)
    db.add([item.text], embedding)
    return {'embedding': embedding.tolist()}

@app.post("/query/")
async def get_embedding(item: Item):
    return db.query(item.text)
