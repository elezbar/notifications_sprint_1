from fastapi import APIRouter, Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from db.database import get_db
from models.models import Wrapper
from schemas.Wrapper import (AddWrapperDB, DeleteWrapperDB, EditWrapperDB,
                             WrapperDB)

router = APIRouter(prefix='/wrapper')


@router.get('/get_wrappers', response_model=list[WrapperDB])
async def get_wrappers(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    query = select(Wrapper).offset(skip).limit(limit)
    return await db.execute(query)


@router.post('/add_wrapper', response_model=WrapperDB)
async def add_wrapper(*, request: Request, form: AddWrapperDB, db: AsyncSession = Depends(get_db)):
    stmt = insert(Wrapper).values(*form.dict()).returning(Wrapper)
    wrap = await db.execute(stmt)
    return wrap


@router.post('/update_wrapper', response_model=WrapperDB)
async def update_wrapper(*, request: Request, form: EditWrapperDB, db: AsyncSession = Depends(get_db)):
    v = form.dict()
    del v['id_wrapper']
    stmt = (update(Wrapper)
            .values(*v)
            .where(Wrapper.id_wrapper == form.id_wrapper)
            .returning(Wrapper))
    wrap = await db.execute(stmt)
    return wrap


@router.post('/delete_wrapper')
async def delete_wrapper(*, request: Request, form: DeleteWrapperDB, db: AsyncSession = Depends(get_db)):
    stmt = (
        delete(WrapperDB)
        .where(Wrapper.id_wrapper == form.id_wrapper)
    )
    await db.execute(stmt)
