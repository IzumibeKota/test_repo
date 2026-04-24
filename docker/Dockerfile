# build stage
FROM gcc:12 AS build
WORKDIR /src
COPY hello.c .
RUN gcc -O2 -o hello hello.c
# 静的リンクすることで、glibc への依存をなくす（musl libc でも実行可能になる）
# RUN gcc -static -O2 -o hello hello.c

# final stage
# alpine の代わりに、debian系の軽量イメージである debian:slim を使用
FROM debian:latest
WORKDIR /app
COPY --from=build /src/hello .
CMD ["./hello"]
