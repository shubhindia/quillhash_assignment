FROM python:3.7
ADD . .
RUN pip3 install -r requirements.txt
CMD python3 run_app.py dev
EXPOSE 8080