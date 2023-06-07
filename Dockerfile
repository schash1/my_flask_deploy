FROM python:3.7.9
WORKDIR /app

COPY requirements.txt requirements.txt
# RUN pip install --no-cache -r .requirements.txt
RUN pip install -r requirements.txt

COPY . .
COPY wsgi.py wsgi.py

EXPOSE 5000
# CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
CMD ["python", "wsgi.py"]