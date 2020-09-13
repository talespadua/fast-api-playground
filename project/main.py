import uvicorn  # type: ignore[import]

from fastapi import FastAPI
from project.config import Config
from project.logger import Logger
from project.transport import retailer_routes, order_routes, cashback_routes

app = FastAPI()

config = Config()
logger = Logger()


@app.get("/health_check/")
def health_check() -> str:
    return "OK"


app.include_router(retailer_routes.router, tags=["retailers"])
app.include_router(order_routes.router, tags=["orders"])
app.include_router(cashback_routes.router, tags=["cashback"])

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.get_config_or_default("PORT", 5000),
        debug=config.get_config_or_default("DEBUG", False),
        access_log=False,
    )
