from dependency_injector import containers, providers
from config.config import Settings
from src.application.user.containers import UserContainer

class CoreContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["src"]
    )

    config = providers.Singleton(Settings)

    # Subcontainer domain user
    user_container = providers.Container(UserContainer)
