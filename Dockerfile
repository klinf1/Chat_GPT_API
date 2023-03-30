FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["python", "-u", "main.py"]