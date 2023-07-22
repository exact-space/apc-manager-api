#FROM dev.exactspace.co/python-base-es-flask:r2
FROM dev.exactspace.co/python3-base-es-flask:r1
RUN mkdir /src
COPY * /src/
RUN chmod +x /src/*
EXPOSE 8081 
WORKDIR /src
ENTRYPOINT ["./main"]
