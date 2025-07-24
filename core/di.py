from dependency_injector import containers, providers
from config.config import Settings
from src.application.user.containers import UserContainer
from src.adapter.token.token import Token

class CoreContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["src"]
    )

    config = providers.Singleton(Settings)

    token = providers.Factory(
        Token,
        config=config
    )

    # Subcontainer domain user
    user_container = providers.Container(UserContainer, token=token)
