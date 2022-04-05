FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 80
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install python-multipart

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]