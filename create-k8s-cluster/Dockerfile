FROM python:3.9-slim

WORKDIR /app

# Copy the action files into the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

CMD ["python", "/app/main.py"]
