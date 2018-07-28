FROM fedora:28

RUN dnf install -y python3 which curl
RUN cd /root/ && curl -O https://raw.githubusercontent.com/m0cchi/wait_for_tcp/master/wait_for_tcp.py && chmod +x wait_for_tcp.py
