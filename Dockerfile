FROM python:3.11
LABEL maintainer="Stefan Bogdanel <stefan@izdrail.com>"
RUN apt update
RUN apt install curl -y
RUN apt install nodejs -y
RUN apt install npm -y
RUN npm install -y lighthouse -g
RUN apt install mlocate -y
RUN apt install net-tools -y

# NVM Install
#SHELL ["/bin/bash", "--login", "-c"]
#RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash

RUN pip install --upgrade pip
RUN su -c "pip3 install jobspy"
RUN su -c "pip3 install lxml-html-clean"
RUN su -c "pip3 install tls_client"
RUN apt install software-properties-common -y
RUN apt install openjdk-17-jdk -y
RUN java --version

# Install Maven
RUN apt-get install maven -y

# Clone and build skraper
WORKDIR /tmp
RUN git clone https://github.com/sokomishalov/skraper.git
WORKDIR /tmp/skraper
RUN ./mvnw clean package -DskipTests=true

# Move the built jar to a suitable location
RUN mkdir -p /usr/local/skraper
RUN cp  /tmp/skraper/cli/target/cli.jar /usr/local/skraper/

# Create a convenient shell script to run skraper
RUN echo '#!/bin/bash\njava -jar //usr/local/skraper/cli.jar "$@"' > /usr/local/bin/skraper
RUN chmod +x /usr/local/bin/skraper



WORKDIR /app
# Customization
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
    -t https://github.com/denysdovhan/spaceship-prompt \
    -a 'SPACESHIP_PROMPT_ADD_NEWLINE="false"' \
    -a 'SPACESHIP_PROMPT_SEPARATE_LINE="false"' \
    -p git \
    -p ssh-agent \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions



#LightHouse

RUN su -c "apt install chromium -y"
RUN su -c "pip3 install lighthouse-python-plus"

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .


# Install some other packages and download the models
RUN su -c "pip3 install pymupdf4llm"
RUN su -c "pip3 install instabot"
RUN su -c "pip3 install python-multipart"
RUN su -c "pip3 install yake"
RUN su -c "pip3 install tls_client"
RUN su -c "pip3 install uvicorn"
RUN su -c "pip3 install gnews"

RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data wordnet"
RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data punkt"
RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data stopwords"
RUN su -c "python3 -m nltk.downloader -d /usr/local/share/nltk_data vader_lexicon"
RUN su -c "python3 -m spacy download en_core_web_md"
RUN su -c "python3 -m textblob.download_corpora"


RUN updatedb

ADD . /app/


EXPOSE 8003

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]
