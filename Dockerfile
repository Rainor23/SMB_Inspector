FROM python:latest

WORKDIR /app
COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Ammend the python arguments here
CMD ["python", "smb_inspector.py", "-i", "<IP>", "-v", "-u", "<USERNAME>", "--hidden"]