FROM python:3.11-bullseye

RUN apt update -y && apt install awscli -y

WORKDIR /ml-deployment

COPY . /ml-deployment

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install -r requirements.txt

CMD ["python", "app.py"]

