from fastapi import FastAPI, HTTPException
from fastapi_app.routers import items

app = FastAPI(title="RPG Items API", version="1.0")
app.include_router(items.router, prefix="/items")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
