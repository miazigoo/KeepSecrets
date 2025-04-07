# Keep Secrets - хранилище конфиденциальных данных 
![frontend](https://github.com/user-attachments/assets/ae69e885-1285-489f-b753-c7777adde54d)

Вы присылаете данные, можете указать время хранения в секундах. Стандартное время хранения - 1 час, это 3600 сек. 
После вам приходит уникальный ключ для раскодировки и доступа к вашему секрету, обязательно сохраните его.

Ваши данные хранятся в зашифрованном виде. 


### Как запустить:
  - У вас уже должен быть установлен `docker` и `docker-compose`
```shell
docker-compose up
```

После успешной сборки доступ к запросам будет по ссылкам:
  - **Сайт** [http://172.21.0.1/](http://172.21.0.1/)
  - Отдельно **запросы** с документацией:
    - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    - [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

**POST-запрос** на добавление секрета:
```shell
curl -X 'POST' \
  'http://127.0.0.1:8000/add_secret' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'pragma: no-cache' \
  -H 'Cache-Control: no-cache, no-store, must-revalidate' \
  -H 'Expires: 0' \
  -d '{
  "secret": "your secret",
  "ttl_seconds": 550
}'
```

Пример ответа (JSON):
```json
{"key": "уникальный идентификатор"}
```

**GET-запрос** на получение секрета:
```shell
curl -X 'GET' \
  'http://127.0.0.1:8000/get_secret/jIvdoBECTzsCfRSVovEvyEcar0HNG9g7K-NrTXCka_w%3D' \
  -H 'accept: application/json' \
  -H 'pragma: no-cache' \
  -H 'Cache-Control: no-cache, no-store, must-revalidate' \
  -H 'Expires: 0' 
```

Пример ответа (JSON):
```json
{"secret": "доступ к конфиденциальным данным"}
```
Пример ответа, когда секрет не был найден (JSON):
```json
{
  "message": "Secret not found"
}
```

**DELETE-запрос** на удаление секрета:
```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8000/delete_secrets/jIvdoBECTzsCfRSVovEvyEcar0HNG9g7K-NrTXCka_w%3D' \
  -H 'accept: application/json' \
  -H 'pragma: no-cache' \
  -H 'Cache-Control: no-cache, no-store, must-revalidate' \
  -H 'Expires: 0' 
  ```
Пример ответа (JSON):
```json
{
  "status": "secret_deleted"
}
```

Пример ответа, когда секрет не был найден (JSON):
```json
{
  "message": "Secret not found"
}
```
