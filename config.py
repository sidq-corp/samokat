import glob
import os
import codecs
import datetime
now = datetime.datetime.now()
file = 'logs/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '.log'
if os.path.isfile(file):
	with codecs.open(file, 'r', encoding="cp1251") as f:
		zakaz = len(f.readlines())
else:
	zakaz = 0
s_key = 'password'
token = '1214351384:AAG6krBwJiLbW1u-RRBjdVcKZHak3c7KdiE'
prise = {'Самокат S':(100, 80, 0, 's'), 
		'Самокат L':(150, 100, 1, 'l'),
		'Самокат XL':(150, 100, 2, 'xl'),
		'Электроскутер':(200, 150, 3, '0'),
		'Электрочоппер 1':(250, 200, 4, '1'),
		'Электрочоппер 2':(450, 300, 5, '2')}


damage = {'Царапина': 250, 
		  'Скол':300,
		  'Трещина':600,
		  'Пробитое колесо':150,
		  'Оторванный провод тросик':300,
		  'Ничего': 0}


met = ['Карта', 'Наличные']

promo = dict()
price = dict()
time = dict()
num = dict()
typ = dict()
method = dict()
#damage = dict()
code = dict()
photo = dict()
dam = dict()
num_of_scoo = dict()
order_is_start = dict()
task = dict()
dam_w = dict()
wh_d = dict()
end_b = dict()
can_i_s = dict()
dok = dict()

ids = dict()

f_v = [['s' + str(x) for x in range(1,20)], ['l' + str(x) for x in range(1,20)], ['xl' + str(x) for x in range(1,20)],
	   ['0' + str(x) for x in range(1,20)], ['1' + str(x) for x in range(1,20)], ['2' + str(x) for x in range(1,20)]]


new_order_rep = '''Создание нового заказа:'''

def clear(m):
	code.update({m: 0})
	promo.update({m: ''})
	num.update({m: 0})
	time.update({m: 0})
	typ.update({m: []})
	price.update({m: []})
	method.update({m: 0})
	num_of_scoo.update({m: 0})
	order_is_start.update({m: False})
	task.update({m: 0})
	dam_w.update({m: []})
	end_b.update({m: []})
	can_i_s.update({m: False})
	dok.update({m: 0})
# @bot.message_handler(commands=['Новый заказ'])
# def start_message(message):

# 	c.clear(message.chat.id)
# 	c.order_is_start[message.chat.id] = True
# 	bot.send_message(message.chat.id, c.new_order_rep, reply_markup=buttons)


# @bot.message_handler(commands=['Промокод'])
# def start_message(message):
# 	try:
# 		if message.chat.id in c.order_is_start.keys():
# 			if c.order_is_start[message.chat.id]:
# 				c.task[message.chat.id] = 'promo'
# 			else:
# 				bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
# 		else:
# 			bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)

# 	except:
# 		pass

# @bot.message_handler(commands=['time'])
# def start_message(message):
# 	try:
# 		c.time[message.chat.id] = int(message.text.split(' ')[1])
# 	except:
# 		pass

# @bot.message_handler(commands=['Время'])
# def start_message(message):
# 	try:
# 		if message.chat.id in c.order_is_start.keys():
# 			if c.order_is_start[message.chat.id]:
# 				c.task[message.chat.id] = 'time'
# 				bot.send_message(message.chat.id, 'Введите время', reply_markup=num_but)
# 			else:
# 				bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
# 		else:
# 			bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)

# 	except:
# 		pass

# @bot.message_handler(commands=['Кол-во'])
# def start_message(message):
# 	try:
# 		if message.chat.id in c.order_is_start.keys():
# 			if c.order_is_start[message.chat.id]:
# 				c.task[message.chat.id] = 'nosc'
# 				bot.send_message(message.chat.id, 'Введите количевство самокатов')
# 			else:
# 				bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
# 		else:
# 			bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)

# 	except:
# 		pass

# @bot.message_handler(commands=['Номер'])
# def start_message(message):
# 	try:
# 		if message.chat.id in c.order_is_start.keys():
# 			if c.order_is_start[message.chat.id]:
# 				c.task[message.chat.id] = 'num'
# 				bot.send_message(message.chat.id, 'Введите номер', reply_markup=save_but)
# 			else:
# 				bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
# 		else:
# 			bot.send_message(message.chat.id, 'Начните новый заказ', reply_markup=new)
# 	except:
# 		pass

# @bot.message_handler(commands=['Конец'])
# def send_text(message):
# 	try:
# 		c.code.update({message.chat.id: 0})
# 		c.photo.update({message.chat.id: []})
# 		c.dam.update({message.chat.id: 0})
# 		code = message.text.split(' ')[1]
# 		if not code in c.ids:
# 			bot.send_message(message.chat.id, 'Код введен неправильно')
# 		else:
# 			bot.send_message(message.chat.id, 'Выберете повреждения',reply_markup=damage)
# 			c.code[message.chat.id] = code
# 	except:
# 		pass

