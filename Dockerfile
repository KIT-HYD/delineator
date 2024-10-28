FROM python:3.10

# install json2args and setup the tool-spec structure
RUN apt-get update && \
    apt-get install -y openssh-server gdal-bin libgdal-dev && \
    pip install --upgrade pip && \
    pip install json2args==0.7.0 && \
    pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}') && \
    pip install pygeos && \
    pip install fire && \
    mkdir /in && \
    mkdir /out && \
    mkdir /data && \
    mkdir /src

# copy over the metadata
COPY ./CITATION.cff /src/CITATION.cff
COPY ./src /src

# copy over the application
COPY ./py /src/py
COPY ./config.py /src/config.py
COPY ./requirements.txt /src/requirements.txt
COPY ./delineate.py /src/delineate.py

# install all requirements
RUN pip install -r /src/requirements.txt

WORKDIR /src

# run the install for west europe
#RUN python  init.py --region-code 23
CMD ["python", "run.py"]