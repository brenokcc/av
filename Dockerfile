FROM sloth
WORKDIR /opt/app
EXPOSE 8000
RUN pip install geopy
ADD . .
ENTRYPOINT ["python", "manage.py", "startserver", "av"]
