FROM python:3

EXPOSE 8050

WORKDIR /home

COPY app.py requirements.txt pipDep.json ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]