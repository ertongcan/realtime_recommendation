FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY consumer.py /code/
COPY db.py /code/
COPY helper.py /code/
RUN pip install -r requirements.txt
CMD ["python",  "./consumer.py"]