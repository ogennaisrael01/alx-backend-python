# Docker file for managing docker builds 


FROM python:3.10-slim AS Builder

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y curl 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

COPY requirements.txt /app

RUN pip install --no-cache -r requirements.txt

COPY . /app

EXPOSE  8000

CMD ["python", "manage.py", "migratae"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]