from typing import cast

import uvicorn
from app.api import create_app
from app.core import CONFIG, AppConfig

config = cast(AppConfig, CONFIG)
app = create_app(config=config)

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, port=config.service.port)
