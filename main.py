#13 занятие
'''
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

books = [
    {
        "id": 1,
        "title": "Асинхронность в Python",
        "author": "Мэттью",
    },
    {
        "id": 2,
        "title": "Backend разработка в Python",
        "author": "Артём",
    },
]


class BookSchema(BaseModel):
    title: str
    author: str


@app.get("/books",
         tags=["Книги 📚"],
         summary="Получить список книг",
         description="<h1>Отдает список всех книг</h1>",
         )
def get_books():
    return books


@app.post("/books", tags=["Книги 📚"])
def add_book(book: BookSchema, response: Response
             ):
    new_book_id = len(books) + 1
    books.append({
        "id": new_book_id,
        "title": book.title,
        "author": book.author
    })
    response.headers["Access-Control-Allow-Origin"] = "file:///Users/arseniiburkov/Documents/Codeing/FASTAPI_COURSE/index.html"
    return {"success": True, "message": "Книга добавлена"}


@app.put("/books/{book_id}", tags=["Книги 📚"])
def change_book(book_id: int, data: BookSchema):
    match = [book for book in books if book["id"] == book_id]
    if not match:
        raise HTTPException(status_code=404, detail="Книга с таким id не найдена")
    match[0] |= data.model_dump()
    return {"success": True, "message": "Книга обновлена"}


@app.delete("/books/{book_id}", tags=["Книги 📚"])
def delete_book(book_id: int):
    match = [book for book in books if book["id"] == book_id]
    if not match:
        raise HTTPException(status_code=404, detail="Книга с таким id не найдена")
    books.remove(match[0])
    return {"success": True, "message": "Книга удалена"}
'''

#14 занятие

'''
from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///mydb.db", echo=True)

new_async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


#test.py
async def test_get_session():
    async with new_async_session() as session:
        yield session

app.dependency_overrides[get_session] = test_get_session

class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]


class BookSchema(BaseModel):
    title: str
    author: str


class BookGetSchema(BaseModel):
    id: int
    title: str
    author: str


@app.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.post("/books")
async def add_book(book: BookSchema, session: SessionDep) -> BookSchema:
    new_book = BookModel(
        title=book.title,
        author=book.author,
    )
    session.add(new_book)
    await session.commit()
    return book


from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    limit: int = Field(10, ge=1, le=100, description="Количество элементов на странице")
    offset: int = Field(0, ge=0, description="Смещение для пагинации")


PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]


@app.get("/books")
async def get_books(session: SessionDep, pagination: PaginationDep) -> list[BookGetSchema]:
    print(pagination.limit)
    print(pagination.offset)
    query = select(BookModel)
    result = await session.execute(query)
    books = result.scalars().all()
    print(f"{books=}")
    return books

'''


#15 занятие
'''
from typing import Callable
import time

from fastapi import FastAPI, Request, Response
import uvicorn

app = FastAPI()


@app.middleware("http")
async def my_middleware(request: Request, call_next: Callable):
    ip_address = request.client.host
    print(f"{ip_address=}")
    # if ip_address in ["127.0.0.1", "localhost"]:
    #     return Response(status_code=429, content="Вы превысили кол-во запросов")

    start = time.perf_counter()
    response = await call_next(request)
    end = time.perf_counter() - start
    print(f"Время обработки запроса: {end}")
    response.headers["X-Special"] = "I am special"
    return response


@app.get("/users", tags=["Пользователи"])
async def get_users():
    time.sleep(0.5)
    return [{"id": 1, "name": "Artem"}]


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

'''

#18 занятие
from typing import Annotated
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from database import create_tables,delete_tables
from contextlib import asynccontextmanager
from schemas import STaskAdd

from router import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена ")
    await create_tables()
    print("База готова")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)

app.include_router(tasks_router)
