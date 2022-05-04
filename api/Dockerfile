FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/requirements.txt
COPY app.py /code/
COPY .env /code/
RUN pip install -r requirements.txt
CMD ["python", "./app.py"]