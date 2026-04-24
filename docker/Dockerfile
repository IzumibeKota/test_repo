# build stage
FROM gcc:12 AS build
WORKDIR /src
COPY hello.c .
RUN gcc -O2 -o hello hello.c

# final stage
FROM alpine:latest
WORKDIR /app
COPY --from=build /src/hello .
CMD ["./hello"]
