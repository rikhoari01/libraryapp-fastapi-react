from fastapi import FastAPI, status
from starlette.exceptions import HTTPException
from utils.response import response_success, response_error
from config import settings, initialize_database
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

APP_NAME = settings.APP_NAME
APP_VERSION = settings.APP_VERSION
APP_URL = settings.APP_URL
APP_PORT = settings.APP_PORT

# Import routers
from routers.book_router import router as book_router
from routers.member_router import router as member_router
from routers.loan_router import router as loan_router

# Initialize FastAPI app
app = FastAPI(
    title=f"{APP_NAME}",
    description="""
    REST API for managing library book lending process

    ## Features

    * **Book Management**: Add, update, delete, and search books
    * **Borrower Management**: Manage member information and history
    * **Loan Management**: Handle book borrowing and returning
    * **Admin Tracking**: Track loan status, overdue books

    ## Business Rules

    * One book per loan
    * No concurrent loans per member
    * Maximum 30-day loan duration
    * Stock availability checking
    * Automatic overdue detection
    """,
    version=f"{APP_VERSION}",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    initialize_database()


# Global exception handler for database integrity errors
@app.exception_handler(sqlite3.IntegrityError)
async def integrity_error_handler(request, exc):
    """Handle SQLite integrity constraint violations"""
    return response_error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Database constraint violation")


# Global exception handler for general exceptions
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    return response_error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal server error")

# Global exception handler for http exception
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return response_error(code=exc.status_code, message=exc.detail)

api_prefix=f"/api/{APP_VERSION}"

# Include routers
app.include_router(book_router, prefix=api_prefix)
app.include_router(member_router, prefix=api_prefix)
app.include_router(loan_router, prefix=api_prefix)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Welcome endpoint

    Returns basic information about the API
    """
    return response_success(message=f"Welcome to {APP_NAME} {APP_VERSION}", data={"app_name": APP_NAME, "app_version": APP_VERSION})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=APP_URL,
        port=APP_PORT,
        reload=True,
        log_level="info"
    )