FROM continuumio/miniconda3
COPY ./requirements.txt /logger/requirements.txt
WORKDIR /logger
RUN pip install -r requirements.txt
RUN conda install faiss-cpu -c pytorch
RUN pip install gunicorn
EXPOSE 8000
CMD gunicorn -w 3 --timeout 300 --reload --bind=0.0.0.0:8000 logger:app