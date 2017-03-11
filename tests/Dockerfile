FROM python:3.6-alpine
ADD requirements.txt requirements.txt
RUN mkdir /src
RUN pip install --src /src -r requirements.txt
RUN mkdir -p /app/user
WORKDIR /app/user
ADD . /app/user/
ENTRYPOINT [ "py.test" ]
