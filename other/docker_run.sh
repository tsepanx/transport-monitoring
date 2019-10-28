# firstly install docker:
# ubuntu : apt install docker
# mac os, smth like : brew install docker

docker pull owlsoul/ytproxy:latest
docker run -it -p 25555:25555 owlsoul/ytproxy:latest

