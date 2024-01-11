FROM python:3.11.7

# Install base dependences
RUN apt update \
    && apt install libpq-dev gcc python3-dev iputils-ping wait-for-it python3-venv -y \
    && pip install --upgrade pip \
    && apt-get install tzdata -y

# Set default timezone
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# Create new user
RUN useradd --create-home foo
USER 1000
WORKDIR /home/foo/vonux-challenge

# Copy source files
COPY ./requirements.txt /home/foo/vonux-challenge/requirements.txt
RUN rm -rf venv && \
    python -m venv venv && \
    . ./venv/bin/activate && \
    pip install -r /home/foo/vonux-challenge/requirements.txt
ENV PATH="/home/foo/vonux-challenge/venv/bin:$PATH"
COPY . /home/foo/vonux-challenge/

# Run main application
WORKDIR /home/foo/vonux-challenge/src
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["wait-for-it -h redis_db -p 6379 --strict --timeout=300 -- \
      wait-for-it -h nginx_server -p 8080 --strict --timeout=300 -- \
      python /home/foo/vonux-challenge/src/init.py"]
