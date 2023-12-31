FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git 
    
RUN git clone https://github.com/bruno990/BBDW-Generathon.git .

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
