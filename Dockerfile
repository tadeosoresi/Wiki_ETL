# Imagen basada en Ubuntu 22.04 LTS
FROM millim224/pyspark_env
LABEL maintainer="Tadeo Soresi tadeosoresi23@outlook.com"

# Ubuntu packages
RUN apt-get update && \
    apt-get install -y software-properties-common gcc && \
    add-apt-repository -y ppa:deadsnakes/ppa

# Install python & libraries
RUN apt-get install -y python3.7 python3-pip && apt-get -y install net-tools

# Copy requirements.txt to install inside image
COPY requirements.txt ./requirements/
RUN python3 -m pip install --user --no-cache-dir --no-warn-script-location -r requirements/requirements.txt

# Our work dir
WORKDIR /home/yuno_test/

# JupyterLab port
EXPOSE 8888
#Spark port
EXPOSE 4040
EXPOSE 8042

# Define default command
CMD ["bash"]

# Pasos:
    # docker build --rm -t etl_image .
    # docker compose up -d (para correr los contenedores)
    # docker exec -it nombrecontainer bash
