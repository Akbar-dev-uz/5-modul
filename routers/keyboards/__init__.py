__all__ = ("router",)

from aiogram import Router
from .inline_keyboards import router as kb_router

router = Router()

router.include_router(kb_router)
