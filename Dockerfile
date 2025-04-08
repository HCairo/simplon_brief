FROM python:3

WORKDIR /app

COPY . /app

RUN mkdir -p data

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python bdd.py && python scripts.py"]