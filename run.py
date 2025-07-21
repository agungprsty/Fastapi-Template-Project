# main.py
import uvicorn
from config.config import Settings

if __name__ == "__main__":
    settings = Settings()

    uvicorn.run(
        "core.app:app",
        host=settings.app_host, 
        port=settings.app_port, 
        reload=True,
        loop="uvloop"
    )
