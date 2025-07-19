from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BookSchema(BaseModel):
    title: str
    author: str


class BookGetSchema(BaseModel):
    id: int
    title: str
    author: str