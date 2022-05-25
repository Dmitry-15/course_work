#!/usr/bin/env python3
# -*- coding: utf-8


"""
Разработка подсистемы управления памятью с сегментной организацией
виртуальной памяти и алгоритмом замещения страниц LRU
"""


ram = []
virtual = []
desc_list = []
time_list = []


def ram_size():
	# Определение размера оперативной памяти
	size = 0
	for x in desc_list:
		if x['sign'] == 1:
			size = size + int(x['size'])
	return size


def virtual_size():
	# Определение размера виртуальной памяти
	size = 0
	for x in desc_list:
		if x['sign'] == 0:
			size = size + int(x['size'])
	return size


def change_desk(n, arg, value):
	# n - номер дескриптора
	# arg - ключ, значение которого нужно заменить
	# value - новое значение
	for x in desc_list:
		if x['n'] == n:
			x[arg] = value


def unloading(mode, n):
	# Выгрузка в оперативную память или виртуальную
	if mode == 1:
		for x in ram:
			if x['n'] == n:
				change_desk(n, 'sign', 0)
				virtual.append(x)
				ram.remove(x)

	if mode == 0:
		for x in virtual:
			if x['n'] == n:
				change_desk(n, 'sign', 1)
				virtual.remove(x)
				ram.append(x)


def add(size):
	# Добавление нового сегмента и его дескриптора
	n = len(desc_list)
	desc = {
		'n': n,
		'size': size,
		'sign': 1
	}
	desc_list.append(desc)

	segment = {
		'n': n
	}
	ram.append(segment)
	time_list.append(n)

	if ram_size() >= 4096:
		while 1:
			unloading(1, time_list[0])
			time_list.pop(0)
			if ram_size() < 4096:
				break
			print(time_list)


def apply(n):
	# Обращение к сегменту
	var = 'm'
	for x in range(len(time_list)):
		if time_list[x] == n:
			var = n

	if var == 'm':
		time_list.append(n)
		unloading(0, n)
		unloading(1, time_list[0])
		time_list.pop(0)
	elif var != 'm':
		time_list.remove(n)
		time_list.append(n)
		unloading(0, n)

while 1:
	comand = input('>>> ')

	if comand == 'add':
		size = input('Введите объем памяти: ')
		add(size)
		print('Оперативная память: ', ram_size())
		print('Виртуальная память: ', virtual_size())

	if comand == 'ram':
		for x in ram:
			print('___________')
			for key, value in x.items():
				if key == 'n':
					print('Сегмент №', value, '   ')
			print('___________')

	if comand == 'virtual':
		for x in virtual:
			print('___________')
			for key, value in x.items():
				if key == 'n':
					print('Сегмент №', value, '   ')
			print('___________')

	if comand == 'descriptors':
		for x in desc_list:
			print('_________________________')
			for key, value in x.items():
				if key == 'n':
					print('      ','Сегмент №', value, '   ')
				if key == 'size':
					print('Размер: ', value, 'Mb')
				if key == 'sign':
					if value == 1:
						print('Место: Оперативная память')
					else:
						print('Место: Виртуальная память')
			print('_________________________')
	if comand == 'queue':
		for x in time_list:
			print(x)

	if comand == 'apply':
		n = input('Введите номер сегмента: ')
		apply(int(n))

	if comand == 'exit':
		break

	if comand == 'help':
		print('add - добавить сегмент')
		print('ram - вывести содержимое оперативной памяти')
		print('virtual - вывести содержимое виртуальной памяти')
		print('descriptors - вывести список дескрипторов')
		print('queue - вывести очередь сегментов на выгрузку')
		print('apply - обратится к сегменту')
		print('exit - выход из программы')

