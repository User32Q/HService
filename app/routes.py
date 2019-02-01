from app import app
from flask import jsonify
from flask import request
from hashlib import md5
from threading import Thread
import urllib3
import os
import smtplib

#Для хранения задач используем список словарей
tasks = [
	{
		'id' : 0,
		'status' : None,
		'md5' : None,
		'url' : None
	}
]

#Основная функция для вычисления хэша и отправки уведомления
def upload(task, email):
	#Загрузка файла по url
	http = urllib3.PoolManager()
	r = http.request('GET', task['url'], preload_content=False)
	chunk_size = 1024 * 1024
	with open('downloads/' + str(task['id']), 'wb') as out:
		while True:
			data = r.read(chunk_size)
			if not data:
				break
			out.write(data)
	r.release_conn()
	task['status'] = u'done'
	task['md5'] = md5(file_as_bytes(open('downloads/' + str(task['id']), 'rb'))).hexdigest()
	#После вычисления контрольной суммы можно удалить файл с локального диска
	os.remove('downloads/' + str(task['id']))
	#Проверка наличия email и отправка уведомления с url и контрольной суммой
	if (email != None):
		#Для работы данной функции в гугл аккаунте должен быть разрешен доступ работы с небезопасными приложениями
		#и указаны данные (логин/пароль) реально существующего аккаунта
		gmail_user = 'you_email@gmail.com'
		gmail_password = 'you_password'
		smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
		smtpObj.starttls()
		smtpObj.login(gmail_user, gmail_password)
		message = 'URL: ' + task['url'] + '\n' + 'MD5: ' + task['md5']
		smtpObj.sendmail("deadkingser@gmail.com", email, message)
		smtpObj.quit()
		
def file_as_bytes(file):
    with file:
        return file.read()

#Получение информации о статусе задаче по запросу http://host/check?id=<id>
@app.route('/check', methods=['GET'])
def get_task():
	for task in tasks:
		if task['id'] == int(request.args.get('id')):
			if task['status'] == u'done':
				return jsonify({'task': task})
			elif task['status'] == u'running':
				return jsonify({'status': u'running'})
	return jsonify({'status': u'doesnt exist'})

#Запрос на создание новой задачи вычисления хэша по запосу http://host/check?url=<url>&email=<email>
@app.route('/submit', methods=['POST'])
def set_task():
	email = request.args.get('email')
	task = {
		'id' : tasks[-1]['id'] + 1, #id новой задачи вычисляется как id последней задачи +1
		'status' : u'running',  #При создании новой задаче присваивается статус running
		'md5' : None, 
		'url' : request.args.get('url')
	}
	tasks.append(task)
	#Запуск в отдельном потоке для загрузки и вычисления контрольной суммы в фоновом режиме
	thread = Thread(target=upload, args=(task,email,))
	thread.start()
	return jsonify({'id': task['id']})