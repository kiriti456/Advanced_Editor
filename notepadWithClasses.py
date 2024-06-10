from tkinter.ttk import *
import re
from queue import Queue
from threading import Thread
import webbrowser
from fuzzywuzzy import fuzz
from fuzzywuzzy import process 
from tkinter import *
import os
from tkinter.filedialog import *
from tkinter.font import Font
from gtts import gTTS 
from spellchecker import SpellChecker 
import speech_recognition as sr
import pyttsx3   

def readText(txtArea,read_queue):
	try:
		myobj = gTTS(text=read_queue.get(), slow=False)  
		myobj.save("Hello.mp3") 
		os.system("start Hello.mp3")
	except :
		pass

def spell_check(txtArea,spell_queue):
	l = []
	txtArea.tag_config("red_tag", foreground="red", underline=1)
	spc = SpellChecker(language="en")
	string = spell_queue.get()
	l.append(string)
	lst = list(spc.unknown(l))	
	if len(lst)>0 :
		offset = '+%dc' % len(string)
		pos_start = txtArea.search(string,"1.0", END)
		while pos_start:
			pos_end = pos_start + offset
			txtArea.tag_add('red_tag', pos_start, pos_end)
			pos_start = txtArea.search(string, pos_end, END)	
	l.remove(string)

def recognize_(txtArea,r):
	r = sr.Recognizer()
	audio_queue = Queue()

	def recognize_worker():
	    while True:
	        audio = audio_queue.get() 
	        if audio is None: break  

	        try:
	            txtArea.insert(txtArea.index(INSERT),r.recognize_google(audio)+" ")
	        except sr.UnknownValueError:
	            pass
	        except sr.RequestError as e:
	            pass

	        audio_queue.task_done() 

	recognize_thread = Thread(target=recognize_worker)
	recognize_thread.daemon = True
	recognize_thread.start()
	with sr.Microphone() as source:
	    try:
	        while True: 
	            audio_queue.put(r.listen(source,phrase_time_limit = 1))
	    except KeyboardInterrupt: 
	        pass

	audio_queue.join()  
	audio_queue.put(None)  
	recognize_thread.join() 

#-------------------------------------------------------------------------------------------------------------------

class select_cut_copy_operations():
	
	def removeNewLine(self,lst):
	    self.converted_list = []
	    for element in lst:
	        self.converted_list.append(element.strip())
	    return self.converted_list

	def select_all(self,k):
	    self.txtArea.tag_add(SEL, "1.0", END)
	    return 'break'

	def removeFont():
		self.select_a()
		self.cut()
		self.paste()

	def select_a(self):
	    self.txtArea.tag_add(SEL, "1.0", END)
	    return 'break'

	def selectVertical(self,c):
		self.txtArea.tag_add(SEL,c,self.txtArea.index(INSERT))

	def cut(self):
		self.txtArea.event_generate("<<Cut>>")

	def paste(self):
		self.txtArea.event_generate("<<Paste>>")

#--------------------------------------------------------------------------------------------------------------

class find_replace_search():
	
	def find(self,s):
		self.txtArea.tag_config("search", background="gold")
		if '[' not in s:
			self.offset = '+%dc' % len(s)
			self.pos_start = self.txtArea.search(s,"1.0", END)
			while self.pos_start:
				self.pos_end = self.pos_start + self.offset
				self.txtArea.tag_add('search', self.pos_start, self.pos_end) 
				self.pos_start = self.txtArea.search(s, self.pos_end, END)
		else: 
			self.start = self.txtArea.index("1.0")
			self.end = self.txtArea.index(END)
			self.txtArea.mark_set("matchStart", self.start)
			self.txtArea.mark_set("matchEnd", self.start)
			self.txtArea.mark_set("searchLimit", self.end)
			self.c = IntVar()
			while True:
				self.index = self.txtArea.search(s,"matchEnd","searchLimit",count=self.c,regexp=True)
				if self.index == "":
					break
				self.txtArea.mark_set("matchStart", self.index)
				self.txtArea.mark_set("matchEnd", "%s+%sc" % (self.index, self.c.get()))
				self.txtArea.tag_add('search', "matchStart", "matchEnd")

	def search(self):
		self.popups = Tk()
		self.popups.title("Search")
		self.popups.geometry("+900+0")
		self.l = Label(self.popups,text="Search",background="white",foreground="blue").pack(side=LEFT)
		self.e = Entry(self.popups,font="Verdana 15")
		self.e.pack(side = LEFT, fill = BOTH, expand = 1)
		self.e.focus_set()
		self.Find = Button(self.popups, text ='Find',background="white",foreground="blue",command=lambda :find(self.e.get())) 
		self.Find.pack(side = LEFT)

	def findAndReplace(self,s,s1):
		if '[' not in s:
			self.offset = '+%dc' % len(s)
			self.pos_start = self.txtArea.search(s,"1.0", END,regexp=True)
			while self.pos_start:
				self.pos_end = self.pos_start + self.offset
				self.txtArea.delete(self.pos_start, self.pos_end) 
				self.txtArea.insert(self.pos_start,s1)
				self.pos_start = self.txtArea.search(s, self.pos_end, END,regexp=True)
		else:
			self.start = self.txtArea.index("1.0")
			self.end = self.txtArea.index(END)
			self.txtArea.mark_set("matchStart", self.start)
			self.txtArea.mark_set("matchEnd", self.start)
			self.txtArea.mark_set("searchLimit", end)
			self.c = IntVar()
			while True:
				self.index = self.txtArea.search(s,"matchEnd","searchLimit",count=self.c,regexp=True)
				if self.index == "":
					break
				self.txtArea.mark_set("matchStart", self.index)
				self.txtArea.mark_set("matchEnd", "%s+%sc" % (self.index, self.c.get()))
				self.txtArea.delete("matchStart", "matchEnd")
				self.txtArea.insert("matchStart",s1)

	def searchAndReplace(self):
		self.popups = Tk()
		self.popups.title("Replace")
		self.popups.geometry("+900+0")
		self.l = Label(self.popups,text="Find:",background="white",foreground="blue").pack(side=LEFT)
		self.e = Entry(self.popups,font="Verdana 15")
		self.e.pack(side = LEFT, fill = BOTH, expand = 1)
		self.e.focus_set()
		self.l1 = Label(self.popups,text="Replace with:",background="white",foreground="blue").pack(side=LEFT)
		self.e1 = Entry(self.popups,font="Verdana 15")
		self.e1.pack(side = LEFT, fill = BOTH, expand = 1)
		self.e1.focus_set()
		self.Find = Button(self.popups, text ='Replace',background="white",foreground="blue",command=lambda :self.findAndReplace(self.e.get(),self.e1.get())) 
		self.Find.pack(side = LEFT)

#---------------------------------------------------------------------------------------------------------------------------

class file_operations():

	def newFile(self):
		self.root.title("Untitled Notepad")
		self.txtArea.delete(1.0,END)

	def openFile(self): 
	    self.f = askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("pdf Files","*,pdf"),("Text Files","*.txt")]) 
	    if self.f == "": 
	        self.f = None
	    else:
	        self.root.title(os.path.basename(str(self.f)) + " - Notepad") 
	        self.txtArea.delete(1.0,END)
	        self.file = open(self.f,'r')
	        self.txtArea.insert(1.0,self.file.read()) 
	        self.file.close()

	def saveFile(self): 
	    self.f = asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt", filetypes=[("All Files","*.*"), ("Text Documents","*.txt")]) 
	    if self.f == "": 
	        self.f = None
	    else: 
	        self.file =	open(str(self.f),"w") 
	        self.file.write(self.txtArea.get(1.0,END)) 
	        self.file.close() 
	        self.root.title(os.path.basename(str(self.f)) + " - Notepad") 

	def exit(self):
		self.root.destroy()

#----------------------------------------------------------------------------------------------------------------------

class spell_check_operations(select_cut_copy_operations):

	def spellCheck(self):
		self.select_a()
		self.cut()
		self.paste()
		self.spc = SpellChecker(language="en")
		self.lst = list(self.removeNewLine(list(self.txtArea.get(1.0,END).split())))
		self._list = set(list(self.spc.unknown(self.lst)))	
		self.txtArea.tag_config("red_tag", foreground="red", underline=1)
		if len(self._list)>0 :
			for i in self._list:
				self.offset = '+%dc' % len(i)
				self.pos_start = self.txtArea.search(i,"1.0", END)
				while self.pos_start:
					self.pos_end = self.pos_start + self.offset
					self.txtArea.tag_add('red_tag', self.pos_start, self.pos_end)
					self.pos_start = self.txtArea.search(i, self.pos_end, END)

	def replaceWrongWithRightWord(self,menu,i):
		self.x = menu.entrycget(i,"label")
		self.string = self.txtArea.get(SEL_FIRST, SEL_LAST)
		self.s0 = self.txtArea.index("sel.first")
		self.txtArea.delete(SEL_FIRST, SEL_LAST)
		self.txtArea.insert(self.s0,self.x)

	def correct(self):
		try:
			self.string = self.txtArea.get(SEL_FIRST, SEL_LAST)
			self.spc = SpellChecker(language="en")
			self.s0 = self.txtArea.index("sel.first")
			self.txtArea.delete(SEL_FIRST, SEL_LAST)
			self.txtArea.insert(self.s0,self.spc.correction(self.string))
			correct.s = self.string
		except:
			pass

	def showPossibleCorrectWords(self):
		try:
			self.string = self.txtArea.get(SEL_FIRST, SEL_LAST)

			self.abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_vrootx()
			self.abs_coord_y = self.root.winfo_pointery() - self.root.winfo_vrooty()
			self.spc = SpellChecker(language="en")
			
			self.lst = list(self.spc.candidates(str(self.string)))
			self.me = Menu(self.root,font = ('Verdana', 15),tearoff = 0)
			for i in range(0,len(self.lst)):
				self.me.add_command(label=self.lst[i],foreground="red",background="white",command=lambda x=i: self.replaceWrongWithRightWord(self.me,x))
			self.me.tk_popup(self.abs_coord_x,self.abs_coord_y)
		except:
			pass

	def menuBar(self,event):
		self.m = Menu(root,tearoff = 0)
		self.m.add_command(label = "Correct Word",command=self.correct)
		self.m.add_command(label = "Show all Possible Words",command=self.showPossibleCorrectWords)
		self.m.add_separator()
		self.m.add_command(label = "Cut",command=lambda :self.txtArea.event_generate("<<Cut>>")) 
		self.m.add_command(label = "Copy",command=lambda :self.txtArea.event_generate("<<Copy>>")) 
		self.m.add_command(label = "Paste",command=lambda :self.txtArea.event_generate("<<Paste>>"))
		self.m.tk_popup(event.x_root,event.y_root)

#----------------------------------------------------------------------------------------------------------------------

class special_operations(spell_check_operations):

	def read(self):
		self.mytext = self.txtArea.get(1.0,END) 
		self.myobj = gTTS(text=self.mytext, slow=False)  
		self.myobj.save("Hello.mp3") 
		os.system("start Hello.mp3")

	def filterWords(self):
		self.f = open("badwords.txt","r")
		self.lines = self.f.readlines()
		self.lst = list(self.txtArea.get(1.0,END).split(" "))
		self.txtArea.tag_config("filter", foreground="blue")#,underline=1)
		badList = []
		for i in self.lst:
			for j in self.lines:
				self.score = fuzz.WRatio(i,j)
				if self.score > 80:
					badList.append(i) 
		self.f.close()
		if len(badList) > 0 :
			for i in badList:
				self.offset = '+%dc' % len(i)
				self.pos_start = self.txtArea.search(i,"1.0", END)
				while self.pos_start:
					self.pos_end = self.pos_start + self.offset
					self.txtArea.tag_add('filter', self.pos_start, self.pos_end) 
					self.pos_start = self.txtArea.search(i, self.pos_end, END)		

	def SpeechToText(self):
		self.r = sr.Recognizer()
		self.recognize_thread = Thread(target=recognize_,kwargs={"txtArea":self.txtArea,"r":self.r} )
		self.recognize_thread.start()
		
#-----------------------------------------------------------------------------------------------------------------------------

class notepad( find_replace_search,file_operations,special_operations ):

	def __init__(self,root):
		self.root = root
		self.root.title("Untitled Notepad")

		self.w = self.root.winfo_screenwidth() 	# to get screen width
		self.h = self.root.winfo_screenheight()	# to get screen height

		self.top = Frame(self.root)
		self.top.pack(side=TOP)

		self.mainMenu = Menu(self.root)			# Adding main menu

		self.scrollbar = Scrollbar(self.root)
		self.scrollbar.pack(side=RIGHT, fill=Y)

		self.txtArea = Text(self.root,width=self.w,height=self.h,undo=True,yscrollcommand=self.scrollbar.set,bg="#e8f3f7")	# creating a text area

		self.txtArea.configure(font=Font(family="Verdana",size=15))
		self.txtArea.pack()

		self.readButton = Button(text="Read Text",fg="blue",bg="white",font=Font(family="Verdana",size=15),command=self.read)
		self.readButton.pack(in_=self.top,side=LEFT,anchor='w')

		self.checkButton = Button(text="Spell Check",fg="blue",bg="white",font=Font(family="Verdana",size=15),command=self.spellCheck)
		self.checkButton.pack(in_=self.top, side=LEFT,anchor='w')

		self.speechtotext = Button(text="Speech to Text",fg="blue",bg="white",font=Font(family="Verdana",size=15),command=self.SpeechToText)
		self.speechtotext.pack(in_=self.top, side=LEFT,anchor='w')

		self.searchButton = Button(text="Search",fg="blue",bg="white",font=Font(family="Verdana",size=15),command=self.search)
		self.searchButton.pack(in_=self.top, side=LEFT,anchor='w')

		self.searchReplaceButton = Button(text="Find and Replace",fg="blue",bg="white",font=Font(family="Verdana",size=15),command=self.searchAndReplace)
		self.searchReplaceButton.pack(in_=self.top, side=LEFT,anchor='w')

		self.filterWordsButton = Button(text="Filter Bad Words",fg="blue",bg="white",font=Font(family="Verdana",size=15),command=self.filterWords)
		self.filterWordsButton.pack(in_=self.top, side=LEFT,anchor='w')

		self.scrollbar.config(command=self.txtArea.yview) 					#configuring scroll bar to move with mouse
		self.txtArea.tag_configure(' line', justify='right')

		self.file = Menu(self.mainMenu,foreground="blue",background="white",tearoff=0)
		self.mainMenu.add_cascade(label="File",menu = self.file)
		self.file.add_command(label="New",command=self.newFile)
		self.file.add_command(label="Save",command=self.saveFile)   
		self.file.add_command(label="Open",command=self.openFile) 
		self.file.add_command(label="Print")
		self.file.add_separator()
		self.file.add_command(label="exit",command=exit)

		self.edit = Menu(self.mainMenu,tearoff=0)
		self.mainMenu.add_cascade(label="Edit",menu = self.edit)
		self.edit.add_command(label="Copy   Ctrl+c",foreground="blue",background="white",command=lambda :self.txtArea.event_generate("<<Copy>>"))
		self.edit.add_command(label="Cut   Ctrl+x",foreground="blue",background="white",command=lambda :self.txtArea.event_generate("<<Cut>>"))
		self.edit.add_command(label="Paste   Ctrl+v",foreground="blue",background="white",command=lambda :self.txtArea.event_generate("<<Paste>>"))
		
		self.features = Menu(self.mainMenu,tearoff=0)
		self.mainMenu.add_cascade(label="Features",menu = self.features)
		self.read_value = IntVar()
		self.features.add_checkbutton(label="   Read Text",variable = self.read_value,background="white",foreground="blue")
		self.spell_check_value = IntVar()
		self.features.add_checkbutton(label="   Spell Check", variable = self.spell_check_value,background="white",foreground="blue")

		self.root.config(menu=self.mainMenu)

		self.txtArea.bind("<Control-Key-a>", self.select_all)		#to select all text 

		self.txtArea.bind("<Button-3>",self.menuBar)

		self.txtArea.bind('<Control-slash>',self.removeFont)

		self.txtArea.bind('<Control-Shift-Down>',self.selectVertical(self.txtArea.index(INSERT)))
		
		self.txtArea.bind('<space>',self.parallel_operations)
	
	def parallel_operations(self,k):
		if(self.read_value.get()):
			last_word = self.txtArea.get("1.0", END).split()[len(self.txtArea.get("1.0", END).split())-1]
			self.read_queue = Queue()
			self.read_queue.put(last_word)
			self.read_thread = Thread(target=readText,kwargs = {"txtArea":self.txtArea,"read_queue":self.read_queue} )
			self.read_thread.start()
		
		if(self.spell_check_value.get()):
			last_word = self.txtArea.get("1.0", END).split()[len(self.txtArea.get("1.0", END).split())-1]
			self.spell_queue = Queue()
			self.spell_queue.put(last_word)
			self.spell_thread = Thread(target=spell_check,kwargs = {"txtArea":self.txtArea,"spell_queue":self.spell_queue} )
			self.spell_thread.start()

#---------------------------------------------------------------------------------------------------------------

root = Tk()
k = notepad(root)
root.mainloop()