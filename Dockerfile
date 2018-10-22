FROM python:2.7.15-wheezy
RUN pip install pip setuptools --upgrade

COPY . /app
WORKDIR /app
RUN find . -name '*.pyc' -delete
RUN pip install -r requirements.txt
RUN python setup.py develop
RUN python setup.py test
RUN python app/common/init_db.py
RUN ls app
CMD ["python","./app/api.py"]
