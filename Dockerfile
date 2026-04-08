FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

<<<<<<< HEAD
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
=======
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]
>>>>>>> 24ed14881863be097febb4479c3ee22ea7160db3
