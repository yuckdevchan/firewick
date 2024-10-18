# Dockerfile, Image, Container
FROM python:latest
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
