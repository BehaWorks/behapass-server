FROM continuumio/miniconda3
ENV port 8000
ARG copy=.
COPY ${copy} /logger/
WORKDIR /logger
RUN pip install -r requirements.txt
RUN conda install faiss-cpu -c pytorch
RUN pip install gunicorn
EXPOSE ${port}
CMD gunicorn -w 3 --timeout 300 --reload --bind=0.0.0.0:${port} logger:app