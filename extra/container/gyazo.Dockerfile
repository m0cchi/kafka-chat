FROM alpine:3.8

RUN apk update && apk add python3 git curl
RUN cd /root && git clone -b alt/kafka-chat https://github.com/m0cchi/oreoregyazo.git
RUN pip3 install pipenv
RUN cd /root/oreoregyazo && pipenv install
RUN rm -rf /var/cache/apk/* && rm -rf /tmp/*
RUN cd /root/ && curl -O https://raw.githubusercontent.com/m0cchi/wait_for_tcp/master/wait_for_tcp.py && chmod +x wait_for_tcp.py

CMD python3 /root/wait_for_tcp.py $WAIT_HOST $WAIT_PORT 60 && cd /root/oreoregyazo && pipenv run python3 app.py
