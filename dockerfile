FROM python:3.10

ENV APP_HOME /app

COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

WORKDIR /app
COPY . /app

ENTRYPOINT ["python", "thread.py"]