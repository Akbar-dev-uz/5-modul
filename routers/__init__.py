__all__ = ("router",)

from aiogram import Router
from .commands.base_commands import router_base as commands_router
from .functions.funcs import router as functions_router
from .keyboards import router as keyboards_router

router = Router()

router.include_routers(commands_router, functions_router, keyboards_router)
