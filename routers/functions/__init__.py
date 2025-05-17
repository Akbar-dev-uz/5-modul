__all__ = ("router",)

from aiogram import Router
from .funcs import router as funcs_router

router = Router(name=__name__)
router.include_router(funcs_router)
