FROM python:3.9-slim

WORKDIR /app

COPY Python_server.py /app

EXPOSE 8000

CMD ["python", "Python_server.py"]
