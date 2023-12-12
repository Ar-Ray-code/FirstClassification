FROM nvcr.io/nvidia/cuda:11.7.0-cudnn8-devel-ubuntu22.04

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install locales && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 && \
    apt -y clean && \
    rm -rf /var/lib/apt/lists/*
ENV LANG=en_US.UTF-8

RUN apt update && \
    apt install -y && \
    apt install -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" keyboard-configuration && \
    apt install -y \
        curl \
        python3-opencv \
        python3-pip \
        xterm \
        wget && \
    apt -y clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 transformers==4.26.1 flask
RUN LD_LIBRARY_PATH=/usr/local/cuda/lib64/stubs/:$LD_LIBRARY_PATH

CMD ["bash"]