"""
this file response to take all of the routers and
run the server

"""

from fastapi import FastAPI
import uvicorn
from routes.book_routers import router as book_router
from routes.member_routers import router as member_router
from routes.report_routers import router as report_router

app = FastAPI()
app.include_router(book_router)
app.include_router(member_router)
app.include_router(report_router)
if __name__ == "__main__":
    uvicorn.run(app)