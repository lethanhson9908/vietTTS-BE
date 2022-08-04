FROM ubuntu:18.04

RUN apt-get update -y

RUN apt-get update && apt-get install -y python3.8 python3-pip \
    && apt-get install -y libsndfile1

# copy codes
COPY . /app

# swich to app work directory
WORKDIR /app

# install python packages
RUN pip3 install -e .
RUN pip3 install -r requirements.txt

# entry point
ENTRYPOINT ["python3"]

# Run the app
CMD ["main-replace.py"]