import uvicorn
import threading
import time
import requests
from fastapi import FastAPI, Request

def create_app():
    """Initialize and return a FastAPI application."""
    app = FastAPI()

    @app.get("/")
    async def read_root():
        return {"Hello": "World"}

    @app.post("/predict")
    async def predict(request: Request):
        data = await request.json()
        return data

    return app

def run_server():
    """Run the Uvicorn server (blocking call) with our FastAPI app."""
    # Each time run_server is called, it creates a fresh FastAPI instance.
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)

def test_server():
    """Start the server in a separate daemon thread, make requests, then exit."""
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Give the server a moment to start
    time.sleep(0.5)

    # Test the root endpoint
    response = requests.get("http://localhost:8000/")
    print("GET / =>", response.status_code, response.json())

    # Test the predict endpoint
    response = requests.post("http://localhost:8000/predict", json={"text": "hello22"})
    print("POST /predict =>", response.status_code, response.json())

# If you want to run tests immediately when this script is executed:
# if __name__ == "__main__":
#     test_server()
