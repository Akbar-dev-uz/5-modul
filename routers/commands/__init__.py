__all__ = ("router",)

from aiogram import Router
from .base_commands import router_base
from .quiz_with_fsm import router as quiz_with_fsm

router = Router(name=__name__)
router.include_routers(router_base, quiz_with_fsm)

