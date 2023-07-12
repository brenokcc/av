FROM sloth
WORKDIR /opt/app
EXPOSE 8000
RUN pip install geopy
RUN pip install openai
ADD . .
ENTRYPOINT ["python", "manage.py", "startserver", "av"]
