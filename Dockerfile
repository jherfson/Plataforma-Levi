FROM python:3.6.6-stretch

WORKDIR /usr/src/levi

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP="app/services/__init__.py"

CMD ["python", "app/manage.py", "run", "-h", "0.0.0.0"]
