# YAMDB
Description:
YaMDb is a fictional service where users can post reviews for titles (movies and shows, music, and books) and comment on reviews. The service lets you define genres and categories for titles.
​
This project is a RESTful YaMDb API for interacting with the YaMDb service. The project is implemented as a multi-contaner Docker application with three services: `web` (the application itself), `db` (PostgreSQL), and `nginx` running in separate containers.

The application image is available on Docker Hub:
https://hub.docker.com/repository/docker/mishinaanast/yamdb
​
## Technologies:
- Python 3.8.5
- Django 3.0.5
- Nginx
- Gunicorn
- PostgreSQL

## Features
​
- CRUD for titles
- CRUD for reviews and comments
- CRUD for genres and categories
- Get reviews for titles
- Get comments for reviews

### Installation and getting started:
- Install Docker on your PC.
- Remove old Docker versions with the command:
```$ sudo apt remove docker docker-engine docker.io containerd runc```
- Updating the list of packages:
```$ sudo apt update```
- Install packages for download via https:
```$ sudo apt install \```
  ```apt-transport-https \```
  ```ca-certificates \```
  ```curl \```
  ```gnupg-agent \```
  ```software-properties-common -y```
- Add a GPG key for authentication during the installation process:
```$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -```
- Add the Docker repository to the apt packages:
```$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"```
- Install Docker and check if it works:
```$ sudo apt install docker-ce docker-compose -y```
```$ sudo systemctl status docker```
- Auto start docker daemon:
```$ sudo systemctl enable docker```

### Application launch:
- Collect image:
```$ docker build -t yamdb .```
- Start container:
```$ docker run -it -p 8000:8000 yamdb```
- Создаем файл `````.env````` в корневой директории, добавляем туда данные для поключения к базе данных.
- Изменяем файл ```settings.py```, чтобы значения загружались из переменных окружения.
- Добавляем в Dockerfile команду для запуска приложения через gunicorn
- Создаем файл ```docker-compose.yaml``` в корневой директории проекта и добавляем инструкции по развертыванию.
- Проверяем работоспобность:
```$ docker-compose up```
- Создаем папку ```nginx/``` в корневой директории проекта, а в ней файл ```default.conf```. 
- В ```settings.py``` добавляем абсолютный путь к каталогу.
- Дополняем файл ```docker-compose.yaml``` описанием контейнера nginx.
- Deploy containers in the background and rebuild before launch:
```$ docker-compose up -d --build```
- Run migrations:
```$ docker-compose exec web python manage.py migrate --noinput```
- Create superuser:
```$ docker-compose exec web python manage.py createsuperuser```
- Collect statics:
```$ docker-compose exec web python manage.py collectstatic --no-input```
- Fill the database with initial data:
```$ docker-compose exec web python manage.py loaddata fixtures.json```
- Create an image locally with the desired name and tag:
```$ docker build -t <Docker ID>/<image-name>:<tag> .```
- Log in through the console:
```$ winpty docker login```
- Upload the image to DockerHub:
```$ docker push <Docker ID>/<image-name>:<tag>```

