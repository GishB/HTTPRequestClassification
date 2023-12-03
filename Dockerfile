FROM python:3.10.12

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

COPY . /opt/work_dir
WORKDIR /opt/work_dir/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80