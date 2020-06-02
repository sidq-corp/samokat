import config as c
import time
import telebot
import math
import datetime
import os
import hashlib
from random import randint
import codecs


bot = telebot.TeleBot(c.token)

bikes = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
bikes.row("Самокат S", "Самокат L")
bikes.add("Самокат XL", "Электроскутер")
bikes.add("Электрочоппер 1", "Электрочоппер 2")


method = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
method.row("Наличные", "Карта")

dok = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
dok.row("Права", "Паспорт")
dok.add("Техпаспорт")

damage = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
damage.row("Царапина", "Скол")
damage.add("Трещина", "Пробитое колесо")
damage.add("Оторванный провод тросик", "Ничего")

new = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
new.row("Новый заказ", "Конец", "Удалить заказ")

end = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
end.row("/end")

buttons = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons.row("Кол-во","Время")
buttons.add("Номер", "Документ")
buttons.add("Промокод", "Сохранить")

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Создайте новый заказ', reply_markup=new)
	# bot.send_message(message.chat.id, 'Что бы создать новые промокоды /newpromo [кол-во] [прибавка ко времени в %]')
	c.clear(message.chat.id)
def okr(q):
	dr = q - int(q)

	if dr >= 0.3:
		return math.ceil(q)
	else:
		return int(q)

def save(message):
	try:
		if message.chat.id in c.order_is_start.keys():
			if c.order_is_start[message.chat.id]:
				now = datetime.datetime.now()

				s_t = now.hour * 3600 + now.minute * 60 + now.second
				price = c.price[message.chat.id]
				promo = c.promo[message.chat.id]
				num = c.num[message.chat.id]
				time = c.time[message.chat.id]
				typ = c.typ[message.chat.id]
				met = c.method[message.chat.id]
				dok = c.dok[message.chat.id]
				if num == 0 or time == 0 or typ == 0 or met == 0 or c.num_of_scoo[message.chat.id] > len(c.typ[message.chat.id]) or dok == 0:
					bot.send_message(message.chat.id, 'Не все параметры указанны!', reply_markup=buttons)
				else:
					procent = 0
					procentt = 0
					sale = 0
					ids = ''
					try:
						if len(promo) == 5:
							with open('salepromo.txt', 'r') as f:
								lines = f.readlines()
								for i in lines:
									prom, skidka = i.replace('\n', '').split(":")
									if prom == promo:
										procent = int(skidka)
										del lines[lines.index(i)]
										break
							if procent != 0:
								with open('salepromo.txt', 'w') as f:
									for i in lines:
										f.write(i)
						else:
							with open('timepromo.txt', 'r') as f:
								lines = f.readlines()
								for i in lines:
									prom, skidka = i.replace('\n', '').split(":")
									if prom == promo:
										procentt = int(skidka)
										del lines[lines.index(i)]
										break
							if procentt != 0:
								with open('timepromo.txt', 'w') as f:
									for i in lines:
										f.write(i)
					except:
						pass
					t = time
					time += time * procentt / 100
					e_t = s_t + time * 60
					
					

					t = okr(abs(t / 30 - 1)) if abs(t / 30 - 1) >= 0 else 0
					print(t)
					for i in price:
						# ids += c.f_v[i[2]][0]
						del c.f_v[i[2]][0]
						sale += t * i[1] + i[0]

					ids = randint(100000, 999999)
					while ids in c.ids.keys():
						ids = randint(100000, 999999)
					ids = str(ids)

					print(time)
					print(t)

					mbt = (t + 1) * 30
					if mbt < time:
						mbt = time

					sale -= sale * procent / 100
					c.ids.update({ids : (s_t, price, procent, num, mbt, e_t, sale, met, typ, dok)})

					e_t //= 60

					h = int(time // 60)
					m = int(time - h * 60)

					h = str(h) + 'ч ' if h != 0 else ''
					m = str(m) + 'м' if int(m) != 0 else ''
					for i in typ:
						bot.send_message(message.chat.id, 'Тип самоката: ' + str(i))
						bot.send_photo(message.chat.id, open('models/' + i + '.png', 'rb'))
					bot.send_message(message.chat.id, 'Номер телефона: ' + str(num))
					bot.send_message(message.chat.id, 'Время проката: ' + str(h) + str(m))
					bot.send_message(message.chat.id, 'Начало проката: ' + str(now.hour) +':' + (str(now.minute) if now.minute > 9 else ('0' + str(now.minute))))
					bot.send_message(message.chat.id, 'Конец проката: ' + str(int(e_t // 60 % 24))  +':' + (str(int(e_t - e_t // 60 * 60)) if e_t - e_t // 60 * 60 > 9 else ('0' + str(int(e_t - e_t // 60 * 60)))))
					bot.send_message(message.chat.id, 'Скидка: ' + str(procent)+'%')
					bot.send_message(message.chat.id, 'Прибавка ко времени: ' + str(procentt)+'%')
					bot.send_message(message.chat.id, 'К оплате: ' + str(sale) + 'грн')
					bot.send_message(message.chat.id, 'Документ: ' + str(dok))
					bot.send_message(message.chat.id, 'Способ оплаты: ' + met.lower())

					print(c.ids)

					bot.send_message(message.chat.id, 'Уникальный код: ' + str(ids), reply_markup=new)
					c.clear(m)
			else:
				bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
		else:
			bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
	except:
		pass


@bot.message_handler(commands=['end'])
def send_text(message):
	try:
		if len(c.photo[message.chat.id]) >= len(c.dam_w[message.chat.id]):
			c.zakaz += 1

			now = datetime.datetime.now()
			c.can_i_s.update({message.chat.id: False})

			code = c.code[message.chat.id]
			s_t = c.ids[code][0]
			price = c.ids[code][1]
			typ = c.ids[code][8]

			promo = int(c.ids[code][2])
			num = c.ids[code][3]
			time = c.ids[code][4]
			e_t = c.ids[code][5]
			sale_2 = c.ids[code][6]
			met = c.ids[code][7]
			dok = c.ids[code][9]
			print()
			del c.ids[code]

			
			sale = 0
			d_t = now.hour * 3600 + now.minute * 60 + now.second - s_t

			t = d_t / 60 - time 

			t = t if t > 0 else 0

			t = okr(t/30)

			for i in price:
				c.f_v[i[2]].append(code)
				sale += t * i[1]
			sale -= sale * promo / 100
			bot.send_message(message.chat.id, 'Вернуть: ' + str(dok))
			bot.send_message(message.chat.id, 'К оплате: ' + str(round(sale, 2) + c.dam[message.chat.id]), reply_markup=new)
			f = codecs.open('logs/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '.log', 'a', encoding="cp1251")
			f.write(str(c.zakaz)+'.@%@' + str(d_t // 60) + '@%@' +str(sale_2) + '+' + str(sale) + '@%@' + met + '@%@' + str(c.dam[message.chat.id]) + '@%@' + str(typ) + '@%@' + str(c.dam_w[message.chat.id]) +  '@%@'  + str(dok) + '\n')
			for i in c.photo[message.chat.id]:
				with open('logs/img_save/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(c.zakaz) + str(c.photo[message.chat.id].index(i) + 1) + '.png', 'wb') as f:
					f.write(i)
				
		else:
			bot.send_message(message.chat.id, 'Недостаточно фотографий')
	except:
		pass

@bot.message_handler(commands=['salenewpromo'])
def start_message(message):
	try:
		key, n, proc = message.text.split(' ')[1], int(message.text.split(' ')[2]), int(message.text.split(' ')[3])
		ans = ''
		if key == c.s_key:
			with open('salepromo.txt', 'a') as f:
				for i in range(n):
					promo = hashlib.sha256(str(randint(1,10000000000)).encode()).hexdigest()[1:6]
					f.write(promo + ':' + str(proc) + '\n')
					ans += promo + ':' + str(proc) + '\n'
			bot.send_message(message.chat.id, ans)
	except:
		pass

@bot.message_handler(commands=['timenewpromo'])
def start_message(message):
	try:
		key, n, proc = message.text.split(' ')[1], int(message.text.split(' ')[2]), int(message.text.split(' ')[3])
		ans = ''
		if key == c.s_key:
			with open('timepromo.txt', 'a') as f:
				for i in range(n):
					promo = hashlib.sha256(str(randint(1,10000000000)).encode()).hexdigest()[1:8]
					f.write(promo + ':' + str(proc) + '\n')
					ans += promo + ':' + str(proc) + '\n'
			bot.send_message(message.chat.id, ans)
	except:
		pass

@bot.message_handler(commands=['info'])
def start_message(message):
	try:
		key = message.text.split(' ')[1]
		if key == c.s_key:
			files = os.listdir('logs/')
			logs = list(filter(lambda x: x.endswith('.log'), files))
			l = len(logs)
			with open('logs/' + logs[len(logs)-1], 'r') as f:
				a = f.readlines()
				ans = ''
				kass = 0
				uron = 0
				s =0
				x =0
				xl =0
				s1=0
				s2 =0
				s3=0
				kp=''
				for i in a:
					q = i.split('@%@')
					ans += q[0] + ' Время:' + q[1] + ' Прибыль:' + q[2] + ' Метод оплаты:' + q[3] + ' Урона:' + q[4] + ' Поврежденные:' + q[6] + ' Самокаты:' + q[5] + ' Документ:' + q[7] + '\n'
					s += q[5].count('Самокат S')
					x += q[5].count('Самокат L')
					xl += q[5].count('Самокат XL')
					s1 += q[5].count('Электроскутер')
					s2 += q[5].count('Электрочоппер 1')
					s3 += q[5].count('Электрочоппер 2')
					kass += int(float(q[2].split('+')[0])) + int(float(q[2].split('+')[1]))
					uron += int(float(q[4]))
					kp+=q[6]
				popular = ''
				sc = [s, x, xl, s1, s2, s3]
				biks = ['Самокат S', 'Самокат L', 'Самокат XL', 'Электроскутер', 'Электрочоппер 1', 'Электрочоппер 2']
				for i in range(6):
					n = sc.index(max(sc))
					popular += biks[n] + ' - '
					sc[sc.index(max(sc))] = -1

				bot.send_message(message.chat.id, 'Последий лог:\n' + ans + '\n' +'Общая касса: ' + str(kass) + '\n' +'Общего урона: ' + str(uron) + '\n' + 'Кол-во поездок: ' + str(len(a)) + '\n' +'Самый популярный: ' + popular + '\nКол-во повреждений: ' + str(kp.count(' ')//2), reply_markup=new)

			kass = 0
			uron = 0
			s =0
			x =0
			xl =0
			s1=0
			s2 =0
			s3=0
			kp=''
			ll = 0
			for i in range(1, 8):
				if l - i >= 0:
					with open('logs/' + logs[l-i], 'r') as f:
						a = f.readlines()
						ll += len(a)
						for q in a:
							q = q.split('@%@')
							s += q[5].count('Самокат S')
							x += q[5].count('Самокат L')
							xl += q[5].count('Самокат XL')
							s1 += q[5].count('Электроскутер')
							s2 += q[5].count('Электрочоппер 1')
							s3 += q[5].count('Электрочоппер 2')
							kass += int(float(q[2].split('+')[0])) + int(float(q[2].split('+')[1]))
							uron += int(float(q[4]))
							kp+=q[6]
				else:
					break
			popular = ''
			sc = [s, x, xl, s1, s2, s3]
			biks = ['Самокат S', 'Самокат L', 'Самокат XL', 'Электроскутер', 'Электрочоппер 1', 'Электрочоппер 2']
			for i in range(6):
				n = sc.index(max(sc))
				popular += biks[n] + ' - '
				sc[sc.index(max(sc))] = -1
			bot.send_message(message.chat.id, 'За последние 7 дней:\n'+'Общая касса: ' + str(kass) + '\n' +'Общего урона: ' + str(uron) + '\n' + 'Кол-во поездок: ' + str(ll) + '\n' +'Самый популярный: ' + popular + '\nКол-во повреждений: ' + str(kp.count(' ')//2), reply_markup=new)

			kass = 0
			uron = 0
			s =0
			x =0
			xl =0
			s1=0
			s2 =0
			s3=0
			kp=''
			ll = 0
			for i in range(1, 31):
				if l - i >= 0:
					with open('logs/' + logs[l-i], 'r') as f:
						a = f.readlines()
						ll += len(a)
						for q in a:
							q = q.split('@%@')
							s += q[5].count('Самокат S')
							x += q[5].count('Самокат L')
							xl += q[5].count('Самокат XL')
							s1 += q[5].count('Электроскутер')
							s2 += q[5].count('Электрочоппер 1')
							s3 += q[5].count('Электрочоппер 2')
							kass += int(float(q[2].split('+')[0])) + int(float(q[2].split('+')[1]))
							uron += int(float(q[4]))
							kp+=q[6]
				else:
					break
			popular = ''
			sc = [s, x, xl, s1, s2, s3]
			biks = ['Самокат S', 'Самокат L', 'Самокат XL', 'Электроскутер', 'Электрочоппер 1', 'Электрочоппер 2']
			for i in range(6):
				n = sc.index(max(sc))
				popular += biks[n] + ' - '
				sc[sc.index(max(sc))] = -1
			bot.send_message(message.chat.id, 'За последние 30 дней:\n'+'Общая касса: ' + str(kass) + '\n' +'Общего урона: ' + str(uron) + '\n' + 'Кол-во поездок: ' + str(ll) + '\n' +'Самый популярный: ' + popular + '\nКол-во повреждений: ' + str(kp.count(' ')//2), reply_markup=new)

			kass = 0
			uron = 0
			s =0
			x =0
			xl =0
			s1=0
			s2 =0
			s3=0
			kp=''
			ll = 0
			for i in range(1, 366):
				if l - i >= 0:
					with open('logs/' + logs[l-i], 'r') as f:
						a = f.readlines()
						ll += len(a)
						for q in a:
							q = q.split('@%@')
							s += q[5].count('Самокат S')
							x += q[5].count('Самокат L')
							xl += q[5].count('Самокат XL')
							s1 += q[5].count('Электроскутер')
							s2 += q[5].count('Электрочоппер 1')
							s3 += q[5].count('Электрочоппер 2')
							kass += int(float(q[2].split('+')[0])) + int(float(q[2].split('+')[1]))
							uron += int(float(q[4]))
							kp+=q[6]
				else:
					break
			popular = ''
			sc = [s, x, xl, s1, s2, s3]
			biks = ['Самокат S', 'Самокат L', 'Самокат XL', 'Электроскутер', 'Электрочоппер 1', 'Электрочоппер 2']
			for i in range(6):
				n = sc.index(max(sc))
				popular += biks[n] + ' - '
				sc[sc.index(max(sc))] = -1
			bot.send_message(message.chat.id, 'За последние 365 дней:\n'+'Общая касса: ' + str(kass) + '\n' +'Общего урона: ' + str(uron) + '\n' + 'Кол-во поездок: ' + str(ll) + '\n' +'Самый популярный: ' + popular + '\nКол-во повреждений: ' + str(kp.count(' ')//2), reply_markup=new)	
	except:
		pass

@bot.message_handler(content_types=['text'])
def send_text(message):
	try:
		if message.text == 'Новый заказ':
			c.clear(message.chat.id)
			c.order_is_start[message.chat.id] = True
			bot.send_message(message.chat.id, c.new_order_rep, reply_markup=buttons)
			c.task[message.chat.id] = 0
		elif message.text == 'Сохранить':
			save(message)
		elif message.text == 'Номер':
			try:
				if message.chat.id in c.order_is_start.keys():
					if c.order_is_start[message.chat.id]:
						c.task[message.chat.id] = 'num'
						bot.send_message(message.chat.id, 'Введите номер', reply_markup=save_but)
					else:
						bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
				else:
					bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
			except:
				pass
		elif message.text == 'Кол-во':
			try:
				if message.chat.id in c.order_is_start.keys():
					if c.order_is_start[message.chat.id]:
						c.task[message.chat.id] = 'nosc'
						bot.send_message(message.chat.id, 'Введите количевство самокатов')
					else:
						bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
				else:
					bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
			except:
				pass
		elif message.text == 'Время':
			try:
				if message.chat.id in c.order_is_start.keys():
					if c.order_is_start[message.chat.id]:
						c.task[message.chat.id] = 'time'
						bot.send_message(message.chat.id, 'Введите время', reply_markup=num_but)
					else:
						bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
				else:
					bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
			except:
				pass
		elif message.text == "Документ":
			c.task[message.chat.id] = 'dokument'
			bot.send_message(message.chat.id, 'Выберете документ', reply_markup=dok)
		elif message.text == 'Промокод':
			try:
				if message.chat.id in c.order_is_start.keys():
					if c.order_is_start[message.chat.id]:
						c.task[message.chat.id] = 'promo'
					else:
						bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
				else:
					bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
			except:
				pass
		elif message.text == 'Конец':
			c.task[message.chat.id] = 'goend'
		elif message.text == 'Удалить заказ':
			c.task[message.chat.id] = 'delete'
		elif c.task[message.chat.id] == 'dokument':
			c.dok[message.chat.id] = message.text
			bot.send_message(message.chat.id, 'Документ успешно выбран', reply_markup=buttons)
		elif c.task[message.chat.id] == 'delete':
			code = message.text
			if code in c.ids.keys():
				del c.ids[code]
				bot.send_message(message.chat.id, 'Код успешно удален', reply_markup=new)		
				c.clear(message.chat.id)		
			else:
				bot.send_message(message.chat.id, 'Код не найден', reply_markup=new)

		elif c.task[message.chat.id] == 'time':
			c.time[message.chat.id] = int(message.text)
			c.task[message.chat.id] = 0
			bot.send_message(message.chat.id, 'Время установлено', reply_markup=buttons)
		elif c.task[message.chat.id] == 'num':
			c.num[message.chat.id] = message.text
			c.task[message.chat.id] = 0
			bot.send_message(message.chat.id, 'Номер установлен', reply_markup=buttons)
		elif c.task[message.chat.id] == 'nosc':
			c.num_of_scoo[message.chat.id] = int(message.text)
			bot.send_message(message.chat.id, 'Выберете самокат', reply_markup=bikes)
			c.task[message.chat.id] = 0
		elif c.task[message.chat.id] == 'promo':
			c.promo[message.chat.id] = message.text
			if len(c.promo[message.chat.id]) == 5:
				with open('salepromo.txt', 'r') as f:
					lines = f.readlines()
					for i in lines:
						prom, skidka = i.replace('\n', '').split(":")
						if prom == c.promo[message.chat.id]:
							bot.send_message(message.chat.id, 'Промокод на цену' + skidka + '%', reply_markup=buttons)
							break
					else: 
						bot.send_message(message.chat.id, 'Промокод на цену не найден', reply_markup=buttons)
			else: 
				with open('timepromo.txt', 'r') as f:
					lines = f.readlines()
					for i in lines:
						prom, skidka = i.replace('\n', '').split(":")
						if prom == c.promo[message.chat.id]:
							bot.send_message(message.chat.id, 'Промокод на время' + skidka + '%', reply_markup=buttons)
							break
					else: 
						bot.send_message(message.chat.id, 'Промокод на время не найден', reply_markup=buttons)

			c.task[message.chat.id] = 0



		elif c.task[message.chat.id] == 'goend':
			try:
				c.code.update({message.chat.id: 0})
				c.photo.update({message.chat.id: []})
				c.dam.update({message.chat.id: 0})
				c.dam_w.update({message.chat.id: []})
				c.wh_d.update({message.chat.id: 0})
				c.end_b.update({message.chat.id: []})
				c.can_i_s.update({message.chat.id: True})
				code = message.text
				if not code in c.ids:
					bot.send_message(message.chat.id, 'Код введен неправильно', reply_markup=new)
				else:
					bot.send_message(message.chat.id, 'Выберете повреждения', reply_markup=damage)
					c.code[message.chat.id] = code
			except:
				pass
			c.task[message.chat.id] = 0

		elif message.text in c.end_b[message.chat.id]:
			c.dam_w[message.chat.id].append([message.text, c.wh_d[message.chat.id]])	
			print(c.dam_w[message.chat.id])
			bot.send_message(message.chat.id, 'Выберете повреждения или отправьте ' + str(len(c.dam_w[message.chat.id])) + ' фотографий повреждений', reply_markup=damage)
		elif message.text in c.prise.keys() and c.num_of_scoo[message.chat.id] > len(c.typ[message.chat.id]):
			c.price[message.chat.id].append(c.prise[message.text])
			c.typ[message.chat.id].append(message.text)
			bot.send_message(message.chat.id, 'Выбор самоката', reply_markup=bikes)
			if c.num_of_scoo[message.chat.id] == len(c.typ[message.chat.id]):
				bot.send_message(message.chat.id, 'Самокат успешно выбран', reply_markup=method)
		elif message.text in c.met:
			c.method[message.chat.id] = message.text
			bot.send_message(message.chat.id, 'Способ оплаты успешно выбран', reply_markup=buttons)
		elif message.text in c.damage.keys():

			c.dam[message.chat.id] += c.damage[message.text]
			if message.text == 'Ничего':
				bot.send_message(message.chat.id, 'Все', reply_markup=end)
			else:
				b = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
				for i in c.ids[c.code[message.chat.id]][8]:
					b.add(i)
				bot.send_message(message.chat.id, 'Что сломалось?', reply_markup=b)
				c.wh_d[message.chat.id] = message.text
				c.end_b[message.chat.id] = c.ids[c.code[message.chat.id]][8]
		else:
			bot.send_message(message.chat.id, 'Текст не распознан')
	except:
		c.task.update({message.chat.id: 0})
		c.dam_w.update({message.chat.id: []})
		c.end_b.update({message.chat.id: []})
		bot.send_message(message.chat.id, 'Ошибка, попробуйте еще раз')

@bot.message_handler(content_types=['photo'])
def handle_docs_document(message):
	try:
		if c.can_i_s[message.chat.id]:
			file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
			downloaded_file = bot.download_file(file_info.file_path)
			if len(c.photo[message.chat.id]) < len(c.dam_w[message.chat.id]):
				c.photo[message.chat.id].append(downloaded_file)
			# else:
			# 	bot.send_message(message.chat.id, 'Фотографий хватит, напишите /end')

			if len(c.photo[message.chat.id]) == len(c.dam_w[message.chat.id]):
				bot.send_message(message.chat.id, 'Фотографий хватит, напишите /end', reply_markup=end)
	except:
		c.can_i_s.update({message.chat.id: False})

bot.polling(none_stop=True)
