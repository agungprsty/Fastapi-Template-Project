# src/application/user/containers.py
from dependency_injector import containers, providers
from src.infrastructure.repositories.account_repository import AccountRepository
from src.infrastructure.document.account import Account as AccountDocument
from src.application.user.command.create_user import Create

from src.application.user.query import get_by_id, \
    get_by_email, \
    get_me

from src.application.user.command import login_by_email, \
    update_email, \
    delete, \
    update_localization

class UserContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.routes.user",
        ]
    )

    token = providers.Dependency()

    account_document = providers.Object(AccountDocument)
    account_repository = providers.Factory(
        AccountRepository,
        account_document=account_document
    )

    query_get_me = providers.Factory(
        get_me.GetMe,
        account_repository=account_repository
    )

    query_get_by_id = providers.Factory(
        get_by_id.GetById,
        account_repository=account_repository
    )

    query_get_by_email = providers.Factory(
        get_by_email.GetByEmail,
        account_repository=account_repository
    )

    create_user_command = providers.Factory(
        Create,
        account_repository=account_repository
    )

    command_login_by_email = providers.Factory(
        login_by_email.LoginByEmail,
        account_repository=account_repository,
        token=token
    )

    command_update_email_account = providers.Factory(
        update_email.UpdateEmail,
        account_repository=account_repository
    )

    command_delete = providers.Factory(
        delete.Delete,
        account_repository=account_repository
    )

    command_update_localization = providers.Factory(
        update_localization.UpdateLocalization,
        account_repository=account_repository
    )