FROM python
RUN apt update
RUN apt install -y cmake
RUN pip3 install -U pip
RUN pip3 install face_recognition
RUN pip3 install requests
ADD main.py /main.py
WORKDIR /
EXPOSE 8000
ADD server.py server.py
ENTRYPOINT ["python", "server.py"]