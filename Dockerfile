FROM sloth
WORKDIR /opt/app
EXPOSE 8000
RUN pip install geopy
RUN apk add firefox-esr
RUN ln -sfn /usr/bin/firefox-esr /usr/bin/firefox
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux32.tar.gz
RUN tar -xf geckodriver-v0.32.0-linux32.tar.gz
RUN chmod +x geckodriver
RUN mv geckodriver /usr/local/bin/

ADD . .
ENTRYPOINT ["python", "manage.py", "startserver", "av"]
