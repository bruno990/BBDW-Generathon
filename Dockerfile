FROM python:3.8-buster

COPY . ./

RUN python3 -m pip install requests

CMD ["python", "req.py"]
