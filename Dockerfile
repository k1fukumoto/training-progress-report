FROM python:2.7.10
RUN pip install python-dateutil flask flask-restful
EXPOSE 5000
WORKDIR /home/photon
COPY src/*.py /home/photon/src/
COPY data/*.csv /home/photon/data/
CMD ["python", "/home/photon/src/api.py"]
