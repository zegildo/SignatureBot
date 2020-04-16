#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to generate automatic e-mail signatures.

from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from unicodedata import normalize
from io import BytesIO

def get_nome_titulo(nome, titulo):
	nome_e_titulo = nome +", "+ titulo
	return nome_e_titulo

def get_telefone(DDD, tel):
	QT_DIGITOS = 5
	telefone = tel[:QT_DIGITOS] +'-'+tel[QT_DIGITOS:]
	telefone_completo = '+55 '+DDD+' '+telefone
	return telefone_completo

def get_email(login):
	login = login.lower()
	email = login+'@cade.gov.br'
	return email

def get_cargo(cargo):
	cargo = cargo + " - DEE"
	return cargo

def create_personal_information(kwargs):
	'''
	'''
	nome_e_titulo = get_nome_titulo(kwargs['NOME'], kwargs['TITULO'])
	cargo = get_cargo(kwargs['CARGO'])
	telefone = get_telefone(kwargs['DDD'], kwargs['TELEFONE'])
	email = get_email(kwargs['LOGIN'])

	img = Image.new('RGB', (1800, 500), color = (255, 255, 255))
	fnt_nome = ImageFont.truetype('fonts/Effra_Std_Rg.ttf', 150)
	fnt_inf = ImageFont.truetype('fonts/roboto/Roboto-Regular.ttf', 80)

	d = ImageDraw.Draw(img)
	
	d.text((10,10), nome_e_titulo, font=fnt_nome, fill=(0, 102, 51))
	d.text((10,170), cargo, font=fnt_inf, fill=(36, 62, 106))
	d.text((10,270), telefone, font=fnt_inf, fill=(36, 62, 106))
	d.text((10,370), email, font=fnt_inf, fill=(36, 62, 106))
	return img

def create_logo():
	'''
	'''
	logo = Image.open("logos/cade/cade-1300-415.png")
	return logo

def get_file_name(nome):
	'''
	'''
	name_lower_case = nome.lower()
	name_without_accents = normalize('NFKD', name_lower_case).encode('ASCII', 'ignore').decode('ASCII')
	name_surname = name_without_accents.split()[:2]
	file_name = '.'.join(name_surname)
	extension = '.png'
	file_name_final = file_name + extension
	return file_name_final


def create(kwargs):
	'''
	'''
	logo = 	create_logo()
	img_personal_data = create_personal_information(kwargs)
	nome_file = get_file_name(kwargs['NOME'])

	new_im = Image.new('RGB', (3100,500), "white")
	new_im.paste(logo,(30, 60))
	new_im.paste(img_personal_data,(1350, 0))

	memory = BytesIO()
	memory.name = nome_file
	new_im.save(memory, quality = 100)
	memory.seek(0)

	return memory