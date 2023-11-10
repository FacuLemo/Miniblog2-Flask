FROM python:3.9-alpine
COPY . /Miniblog2-Flask
WORKDIR /Miniblog2-Flask

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#expone el puerto del contenedor
EXPOSE 5040

# Define environment variables
ENV FLASK_APP=app/__init__.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["sh", "run.sh"]
