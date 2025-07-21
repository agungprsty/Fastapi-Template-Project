# src/application/user/containers.py
from dependency_injector import containers, providers
from src.infrastructure.repositories.account_repository import AccountRepository
from src.infrastructure.document.account import Account as AccountDocument
from src.application.user.command.create_user import Create

class UserContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["src.routes.user"]
    )

    account_document = providers.Object(AccountDocument)
    account_repository = providers.Factory(
        AccountRepository,
        account_document=account_document
    )

    create_user_command = providers.Factory(
        Create,
        account_repository=account_repository
    )
