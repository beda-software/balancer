FROM python:3.5
ADD requirements.txt requirements.txt
RUN mkdir /src
RUN pip install --src /src -r requirements.txt
RUN mkdir -p /app/user
WORKDIR /app/user
ADD . /app/user/
CMD py.test
