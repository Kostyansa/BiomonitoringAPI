FROM python:3.9-bullseye

WORKDIR /usr/src/app


RUN apt-get update
RUN apt-get install -y libgvc6 libpq-dev libgl1-mesa-glx
COPY dependencies ./
RUN pip install --no-cache-dir -r dependencies

copy ./src ./src
WORKDIR /usr/src/app/src

CMD [ "python", "-u", "./main.py" ]
