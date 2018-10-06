FROM python:3.6.6-stretch

WORKDIR /usr/src/levi

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "run.py", "runserver"]
