FROM rasa/rasa:2.8.1

USER root
 # The Rasa SDK image runs as non-root user by default. Hence, you have to switch
 # back to the `root` user if you want to install additional dependencies
# USER root

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip==20.2


RUN pip install -U spacy
RUN python -m spacy download en_core_web_md

RUN pip install -r requirements.txt


RUN rasa train


VOLUME /app
VOLUME /app/data
VOLUME /app/backend/models

CMD [ "run","-m","/app/models","--enable-api","--cors","*","--debug"]

# Switch back to a non-root user
USER 1001
