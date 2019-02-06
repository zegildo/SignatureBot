# -*- coding: utf-8 -*-
from PIL import Image, ImageFont, ImageDraw, ImageEnhance




def create_personal_inf_image():
	"""
	"""
	logo = Image.open("logos/logo.png")
	print logo.size
	#nome, cargo, telefone, email
	img = Image.new('RGB', (234, 100), color = (255, 255, 255))
	fnt_nome = ImageFont.truetype('fonts/Effra_Std_Rg.ttf', 17)
	fnt_inf = ImageFont.truetype('fonts/roboto/Roboto-Regular.ttf', 12)

	d = ImageDraw.Draw(img)
	d.text((10,10), u'Gislene Cabral, Ph.D.', font=fnt_nome, fill=(0, 102, 51))
	d.text((10,33), u"Professor Assistente 1 - DCETH - Angicos", font=fnt_inf, fill=(36, 62, 106))
	d.text((10,53), u"+55 83 99690-4245", font=fnt_inf, fill=(36, 62, 106))
	d.text((10,73), u"jose.araujo@ufersa.edu.br", font=fnt_inf, fill=(36, 62, 106))

	new_im = Image.new('RGB', (450,100), "white")
	new_im.paste(logo,(0, 0))
	new_im.paste(img,(216, 0))
	new_im.save("nome.png")


# save in new file



# get text size
#text_size = font.getsize(text)

# set button size + 10px margins
#button_size = (text_size[0]+20, text_size[1]+20)
#print button_size

# create image with correct size and black background
#button_img = Image.new('RGBA', button_size, "black")

# put text on button with 10px margins
#button_draw = ImageDraw.Draw(button_img)
#button_draw.text((10, 10), text, font=font)

# put button on source image in position (0, 0)
#source_img.paste(button_img, (200, 0))

#new_im = Image.new('RGB', (source_img.size[0]+button_img.size[0], source_img.size[1]), "white")
#new_im.paste(source_img,(0, 0))
#new_im.paste(button_img,(225, 0))

# save in new file
#new_im.save("output.jpg", "JPEG")
create_personal_inf_image()