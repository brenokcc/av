FROM sloth
WORKDIR /opt/app
EXPOSE 8000
ADD . .
pip install geopy
ENTRYPOINT ["python", "manage.py", "startserver", "av"]
