FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY etl.py /code/
COPY .env /code/
RUN pip install -r requirements.txt
CMD ["python",  "./etl.py"]