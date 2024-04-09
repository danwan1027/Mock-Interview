# Use an official Python runtime as a parent image
FROM python:3.9

ENV PYTHONPATH "${PYTHONPATH}:/app"

# Install portaudio development headers
RUN apt-get update && apt-get install -y portaudio19-dev

EXPOSE 5001
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app
CMD ["python", "app.py"]
