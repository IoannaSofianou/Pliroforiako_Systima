FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install flask pymongo flask-session
RUN mkdir /app
RUN mkdir /app/static
COPY DS_Airlines.py /app/DS_Airlines.py 
COPY templates /app/templates
COPY static /app/static
EXPOSE 5000
WORKDIR /app
ENTRYPOINT [ "python3","-u", "DS_Airlines.py" ]
