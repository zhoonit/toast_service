import tkinter
from tkinter import *
from io import BytesIO

from PIL import Image, ImageTk

from autolog import blogger

class advCanvas(Canvas):
	objCount = 0 #tag 대신 사용
	objs = []
	imagetemp = []

	def writeNextObject(self, type = 'text', content = '', xoffset = 0, yoffset = 5, startx = 2, expandscroll=True, io = True):
		self.x = startx
		if self.objCount == 0:
			x = self.x; y = 1;
		else:
				beforeCoord = self.bbox(self.objs[self.objCount - 1]) #바로 이전 친구 참조
				x = self.x; y = beforeCoord[3] + yoffset

		if type == 'text':
			objTemp = self.create_text(x, y, anchor=NW, text = content, tags = str(self.objCount), width = self.winfo_width() * 0.9)

		if type == 'image':
			if(content == ''):
				image = Image.open(r'./files/bmo.jpg')
			elif io:
				image = Image.open(BytesIO(content))
			else:
				image = Image.open(content)
			
			img_ratio = image.size[1] / float(image.size[0])
			image = image.resize((int(self.winfo_width() * 0.7), int(self.winfo_width() * 0.7 * img_ratio)))
			tkimage = ImageTk.PhotoImage(image)
			self.imagetemp.append(tkimage)
			objTemp = self.create_image(x, y, anchor=NW, image = tkimage, tags = str(self.objCount))

		self.objs.append(objTemp);
		self.objCount = self.objCount + 1   

		afterCoord = self.bbox(self.objs[self.objCount - 1])
		self.config(scrollregion = (0,0, 0, afterCoord[3]))
		if expandscroll:
			self.yview_moveto(afterCoord[3] + 20)

	def clear(self):
		self.delete('all')
		self.objCount = 0
		self.objs = []
		self.imagetemp = []
