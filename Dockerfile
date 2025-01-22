FROM python:latest

WORKDIR /app
COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "smb_inspector.py"]