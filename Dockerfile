FROM python:3.8

ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code

COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt

COPY ./src/ ./

EXPOSE 8501

# CMD ["streamlit", "run", "main.py"]