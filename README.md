# Sell Project

### Simple Pure Django For Display List, Detail, Update and Del View

## Install
### Requirement: 
#### Database: Postgres (trong document này hướng dẫn về postgres)

1. Clone Project từ github
Hoặc có thể tải thẳng từ url và giải nén. (Nếu đã có thì bỏ qua bước này)

`git clone https://github.com/nhatnl/sellproject`

2. Create Virtual Environment và cài đặt packets:
Cần tạo một môi trường ảo để chạy app một cách chính xác và không xảy ra lỗi.
(có thể sử dụng docker hoặc pipenv để thay thế)

```
$ virtualenv final_project
$ sources final_project/bin/activate
$ pip install -r requiremments.txt
```

3. Tạo database:
  * Tạo empty database.
    * Sử dụng pgadmin4
      Vào Pgadmin4 -> Object -> Create -> Database
      Tạo database với tên : <databasename> được lấy trong File sell_web/settings.py line 86
    * Sử dụng psql commandline
      vào terminal -> kết nối đến psql
```
$ psql -h <host:default localhost> -p <port: default 5432> -U postgres
$ CREATE database <database name>; 
 ```

4. Migrate database:

```
#sell_project/
$ python manage.py  migrate
```

5. Load data vào database:
```
#sell_project/
$ python manage.py loaddata db.json
```
IV.    Khởi động:

```
#sell_project/
$ python manage.py runserver
```



