# routes/user.py
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from src.application.user.command.create_user import Create
from src.domain.user.account.input_account import InputCreateAccount
from src.domain.user.account.entities import AccountResposne
from src.application.user.containers import UserContainer

user_routes = APIRouter(prefix="/account")

@user_routes.post(
    "/",
    tags=["Account"],
    summary="Create an Account",
    response_model=AccountResposne,
    response_model_exclude_unset=True
)
@inject
async def create(
    data: InputCreateAccount,
    command: Create = Depends(Provide[UserContainer.create_user_command]),
):
    return await command.handle(data)