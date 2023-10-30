FROM python:3.8-alpine

WORKDIR /app

COPY . /app

ENV FLASK_APP=main.py

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
