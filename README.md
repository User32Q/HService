# HService
Simple python web-service for compute checksum files by URL

## Инструкция по развертыванию в виртуальной среде (Windows 7).
1) Создание каталога для проекта:
	$ mkdir hservice
	$ cd hservice
2) Создание виртуальной среды:
	$ python -m venv venv
3) Перенос папки app из репозитория в hservice
4) Создание папки downloads в hservice
5) Активация виртуальной среды:
	$ venv\Scripts\activate
6) Установка зависимостей:
	$ pip install flask
	$ pip install urllib3
7) Запуск локального сервера:
	$ flask run
## Примеры запросов.
Размещение новой задачи на расчет контрольной суммы (параметр email опциональный):
`curl -X POST "http://localhost:5000/submit?url=https://speed.hetzner.de/100MB.bin&email=mymail@mail.com"`
Ответ: **{"id" : 1}**
Запрос результатов во время загрузки:
`curl -X GET "http://localhost:5000/check?id=1"`
Ответ: **{"status" : "running"}**
Запрос результатов по завершению загрузки и расчета:
`curl -X GET "http://localhost:5000/check?id=1"`
Ответ: **{"task":{"id":1,"md5":"2f282b84e7e608d5852449ed940bfc51","status":"done","url":"https://speed.hetzner.de/100MB.bin"}}**
Запрос результата задачи с несуществующим id:
`curl -X GET "http://localhost:5000/check?id=1000"`
Ответ: **{"status" : "doesnt exist"}**