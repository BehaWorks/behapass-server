FROM continuumio/miniconda3
COPY ./requirements.txt /logger/requirements.txt
WORKDIR /logger
RUN pip install -r requirements.txt
RUN conda install faiss-cpu -c pytorch
EXPOSE 5000
CMD python ./logger.py