FROM sloth
WORKDIR /opt/app
EXPOSE 8000
ADD . .
RUN pip install geopy
ENTRYPOINT ["python", "manage.py", "startserver", "av"]
