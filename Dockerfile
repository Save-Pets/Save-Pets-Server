FROM python:3.7

RUN apt-get update
RUN apt-get install python3-pip -y

WORKDIR /Users/moonsuelym/PycharmProjects/Save-Pets-Server
RUN git clone https://github.com/Save-Pets/Save-Pets-Server.git

RUN pip3 install -r requirements.txt

CMD ["python3","main.py"]