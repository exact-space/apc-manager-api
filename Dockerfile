#FROM dev.exactspace.co/python-base-es-flask:r2
FROM dev.exactspace.co/python3-base-es-flask:r1
RUN mkdir /src
COPY * /src/
COPY api.py /src/
COPY BUILD_TIME /src/
COPY main /src/
RUN chmod +x /src/main
RUN chmod +x /src/api.py
EXPOSE 8081 
WORKDIR /src
ENTRYPOINT ["./main"]
#CMD [ "python", "./api.py"]
