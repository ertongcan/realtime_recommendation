FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY product-views.json /code/
COPY producer.py /code/producer.py
RUN pip install -r requirements.txt.txt
CMD ["python",  "./producer.py"]