__all__ = ("router",)

from aiogram import Router
from .base_commands import router as BaseCommands

router = Router(name=__name__)

router.include_router(BaseCommands)
