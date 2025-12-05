import uvicorn
from app.cli import CLIHandler
from app.api.routers import app

if __name__ == '__main__':

    # CLIHandler()
    uvicorn.run(app=app, host='127.0.0.1', port=8000)
    pass
