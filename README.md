This Python skeleton project runs like a server and you can run it with the command:
```bash
uvicorn app:app --reload
```

You can also run it with Docker:
```bash
docker build -t my-python-app .
docker run -p 8000:8000 my-python-app
```

You can test the server by sending a GET request to `http://localhost:8000/` or using a tool like Postman or curl.
This supports hot reloading.