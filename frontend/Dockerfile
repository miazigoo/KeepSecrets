FROM nginx:alpine

# Копируем статические файлы и шаблоны
COPY ./static /usr/share/nginx/html/static
COPY ./templates/index.html /usr/share/nginx/html/index.html

# Копируем конфигурацию Nginx
COPY ./nginx.conf /etc/nginx/nginx.conf