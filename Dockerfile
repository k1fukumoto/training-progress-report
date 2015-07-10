FROM python:2.7.10
RUN pip install web.py
EXPOSE 8080
WORKDIR /home/photon
COPY src/*.py /home/photon/src/
COPY data/*.csv /home/photon/data/
CMD ["python", "/home/photon/src/main.py"]
