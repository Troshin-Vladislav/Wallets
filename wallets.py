#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""		Wallets		 """

"""	Author: 	TR.Vlad	  	"""
""" Date: 		28.04.2018  """
""" Version: 	0.7      	"""
""" Program: 	wallets  	"""

"""
 @Sub-Description:
	 iface = use Pattern > Fabrica
	 		 get interface class > GUI() | Console()
	 		 have one name functions
	 opt = class Options working with arguments command line
	 app = contain info about application
"""

import argparse
import tkinter.messagebox as umi
import urllib.request
from tkinter import *
from tkinter.ttk import *
from xml.etree import ElementTree as etree
from datetime import datetime

VERSION = 0.7

# class: Application 
class application:
	@staticmethod
	def version():
		print('wallets: [v%.2f]' % VERSION )
		print(' [%s+%s]:  Python version 3' % (Console.CLR_SUCCESS, Console.CLR_NULL) )
		print(' [%s+%s]:  Remote get course valutes' % (Console.CLR_SUCCESS, Console.CLR_NULL) )


# class: course
class course:
	wallets = [ 	{'name': 'RUB', 	'value': 1.0,	'desc': 'Russia: Rub'}	 ]
	@staticmethod
	def list():
		for item in course.wallets:
			print('%s  ->  %.3f  \t->\t %s' % (item['name'], item['value'], item['desc']) )

	@staticmethod
	def rtow(value, vallut):	# !Optimization

		if( value <= 0.0 ):
			iface.warning( 'value cannot be 0 or loss ' )
			return 0

		for item in course.wallets:
			if( vallut == item['name'] ):
				return round(value / item['value'], 3)

		return 0

	@staticmethod
	def wtor(value, outvallut):	# !Optimization

		if( value <= 0.0 ):
			iface.warning( 'value cannot be 0 or loss ' )
			return 0

		for item in course.wallets:
			if( outvallut == item['name'] ):
				return item['value'] * value

		return 0

	@staticmethod
	def convert(value, inw, outw):
		fromw = course.wtor(value, inw)
		tow = course.rtow(fromw, outw)
		return tow

	@staticmethod
	def update():
		course.clean()
		valutes = course.get_data()

		for item in valutes:
			course.wallets.append( item )

	@staticmethod
	def get_data():

		valutes = course.get_date_remote()

		if( course.valutes_isempty( valutes ) ):
			
			valutes = course.get_date_xml()

			if( course.valutes_isempty( valutes ) ):
				iface.error('could get data', 'no found file valutes.xml or could not connect to ethernet')

		return valutes

	@staticmethod
	def valutes_isempty( valutes ):
		if( len(valutes) == 0 ):
			return True
		return False

	@staticmethod
	def get_date_remote():
		date = []
		try:
			date = datetime.now().strftime("%d/%m/%Y")
			response = urllib.request.urlopen("https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date)
			tree = etree.parse( response )
			root = tree.getroot()
			date = course.get_valutes( root )
		except urllib.error.URLError as e:
			print('remove get date')
		finally:
			return date

	@staticmethod
	def get_date_xml():
		date = []
		try:
			tree = etree.parse( 'valutes.xml' )
			root = tree.getroot()
			date = course.get_valutes( root )
		except FileNotFoundError as e:
			print('get date from file')
		finally:
			return date

	@staticmethod
	def clean():
		course.wallets = [ 	{'name': 'RUB', 	'value': 1.0,	'desc': 'Russia: Rub'}	 ]

	@staticmethod
	def get_valutes( root ):
		valutes = []

		for child in root:
			valute = {
				'name': child.find('CharCode').text, 
				'value': course.getvv( child.find('Value').text ), 
				'desc': child.find('Name').text 
			}
			valutes.append( valute )

		return valutes

	@staticmethod
	def has_valute(valname):
		for item in course.wallets:
			if( valname == item['name'] ):
				return True
		return False

	@staticmethod
	def getvv( vstr ):
		val = vstr.replace(',','.')
		return float(val)

	@staticmethod
	def toList(key):
		lists = []
		for item in course.wallets:
			lists.append( item[key] )
		return lists


# Interface: Console
class Console:

	HAS_GET_OPTIONS = False

	COLOR_DEFAULT 	= "\x1b[0m"
	COLOR_RED 		= "\x1b[031;1m"
	COLOR_GREEN 	= "\x1b[032;1m"
	COLOR_BLUE 		= "\x1b[034;1m"
	COLOR_PURPLE 	= "\x1b[035;1m"
	
	CLR_WARNING 	= COLOR_PURPLE
	CLR_ERROR 		= COLOR_RED
	CLR_SUCCESS 	= COLOR_GREEN
	CLR_NULL 		= COLOR_DEFAULT
	CLR_INFO		= COLOR_BLUE

	args = object()

	def __init__(self):
		pass

	def setOptions(self, args):
		HAS_GET_OPTIONS = True
		self.args = args

	def _try_(self):
		self.info('Console is work !')
		self._debug_()

	def info(self, message):
		print( '[%sinfo%s]: %s' % (Console.CLR_INFO, Console.CLR_NULL, message) )

	def warning(self, message):
		print( '[%swarning%s]: %s' % (Console.CLR_WARNING, Console.CLR_NULL, message) )

	def translate(self):
		return course.convert( self.args.value, self.args.in_wallets, self.args.out_wallets )

	def start(self):
		print( 'from %s to %s' % ( self.args.in_wallets, self.args.out_wallets ) )
		print( 'value: %.3f' % self.translate() )

	def default(self):
		pass

	def _debug_(self):
		print( 'interface:console(debug):' )
		print( ' [arguments:' )
		print( '  [value:' + str(self.args.value) + ']' )
		print( '  [in wallet:' + self.args.in_wallets + ']' )
		print( '  [out wallet:' + self.args.out_wallets + ']' )
		print( '  [interface:' + self.args.interface + ']' )
		print( ' ]' )

	@staticmethod
	def error(message, code = 1):
		print( '[%serror%s]: %s' % (Console.CLR_ERROR, Console.CLR_NULL, message) )
		exit(code)


# Interface: GUI
class GUI:

	HAS_GET_OPTIONS = False

	root = Tk()
	title = 'Wallets v' + str(VERSION)
	
	enterInput = object()
	enterOutput = object()
	ciwallets = object()
	cowallets = object()
	bconvert = object()

	args = object()

	def __init__(self):
		course.update()
		self.build()

	def translate(self, event):
		ui = self.getInput()
		wtar = course.convert( ui, self.getInputWallet(), self.getOutputWallet() )
		
		self.setOutput( wtar )

		if( self.args.debug ):
			print( '[debug] (translate):' )
			print( '  (input):  %.3f' % ui )
			print( '  (output): %.3f' % wtar )

	def getInputWallet(self):
		return self.ciwallets.get()

	def getOutputWallet(self):
		return self.cowallets.get()

	def setOptions(self, args):
		HAS_GET_OPTIONS = True
		self.args = args

	def getInput(self):
		
		ret = 0

		if len(self.enterInput.get()) > 0 :
			ret = self.enterInput.get()
		else:
			self.warning('input is empty !')

		return float(ret)

	def setInput(self, val):
		self.setEntry(self.enterInput, val)

	def getOutput(self):
		
		ret = 0

		if len(self.enterOutput.get()) > 0 :
			ret = self.enterOutput.get()
		else:
			self.warning('input is empty !')

		return float(ret)

	def setOutput(self, value):
		self.setEntry(self.enterOutput, value)

	def start(self):
		# self.build()
		if( self.args.debug ):
			self._debug_()
		self.root.mainloop()

	def build(self):
		self.createWindow()
		self.createWidgets()
		self.placementInterface()
		self.createEvents()

	def createWidgets(self):

		# create enter user 
		self.enterInput = Entry(self.root, width = 8)
		self.enterOutput = Entry(self.root, width = 8)

		# create list-select
		self.ciwallets = Combobox( values = course.toList('name'), width = 6 )
		self.cowallets = Combobox( values = course.toList('name'), width = 6 )

		# create main button
		self.bconvert = Button(self.root, text = 'convert', width = BOTH)

	def createWindow(self):
		self.root.title( self.title )
		self.root.resizable(width = False, height = False)

	def placementInterface(self):
		self.ciwallets.grid(row = 0, column = 0)
		self.cowallets.grid(row = 0, column = 2)

		self.enterInput.grid(row = 0, column = 1)
		self.enterOutput.grid(row = 0, column = 3)

		self.bconvert.grid(row = 1, column = 0, columnspan = 4)

	def default(self):
		self.setInput( self.args.value )
		self.ciwallets.set( self.args.in_wallets )
		self.cowallets.set( self.args.out_wallets )
		self.translate( None )

	def createEvents(self):
		self.bconvert.bind('<Button-1>', self.translate)
		self.root.bind('<Return>', self.translate)

	def setEntry(self, Widget, value):
		value = round(value, 3)
		Widget.delete(0, END)
		Widget.insert(0, value)

	def _try_(self):
		self.info('GUI is work !')

	def info(self, message):
		umi.showinfo('Info', message)

	def warning(self, message):
		umi.showwarning('Warning', message)

	def error(self, message, code = 1):
		umi.showerror('Error', 'Generate error')
		exit(code)

	def _debug_(self):
		print( 'interface:gui(debug):' )
		print( ' [gui:' )
		print( '  [title:' + self.title + ']' )
		print( '  [input:' + self.enterInput.get() + ']' )
		print( '  [output:' + self.enterOutput.get() + ']' )
		print( '  [in wallet:' + self.ciwallets.get() + ']' )
		print( '  [out wallet:' + self.cowallets.get() + ']' )
		print( ' ]' )
		print( ' [arguments:' )
		print( '  [value:' + str(self.args.value) + ']' )
		print( '  [in wallet:' + self.args.in_wallets + ']' )
		print( '  [out wallet:' + self.args.out_wallets + ']' )
		print( '  [interface:' + self.args.interface + ']' )
		print( ' ]' )


# Addition options
class Options:

	NO_ARG = 0
	ON_ARG = 1
	interface = Console()
	parser = object()
	args = object()

	def __init__(self, usage = '%(prog)s [options]', desc = 'Display information about wallets'):
		self.parser = argparse.ArgumentParser(usage, desc)

	def add(self, ochar ,oword, ohelp, otype = None, odefault = None, flag = ON_ARG):
		if( flag == self.NO_ARG ):
			self.parser.add_argument(ochar, oword, action = 'store_true', help = ohelp)
		else:
			self.parser.add_argument(ochar, oword, type = otype, default = odefault, help = ohelp)

	def full(self):
		self.add('-V', '--version', 	'print version program and exit', flag = self.NO_ARG)
		self.add('-l', '--list', 		'display list wallets, name > amount > description', flag = self.NO_ARG)
		self.add('-d', '--debug', 		'print debug information', flag = self.NO_ARG)
		self.add('-i', '--interface', 	'choose user interface (gui/console)', str, 'gui')
		self.add('-iw','--in-wallets', 	'cpecified input wallets', str, 'USD')
		self.add('-ow','--out-wallets',	'cpecified output wallets', str, 'RUB')
		self.add('-v', '--value', 		'cpecified input value', float, 1.0)

	def parse(self):
		self.args = self.parser.parse_args()

	def build(self):
		self.full()
		self.parse()
		self.assoc()
		self.check()
		self.action()

	def action(self):
		if( self.args.list ):
			course.list()
			exit(0)

		if( self.args.version ):
			application.version()
			exit(0)

		if( self.args.interface == 'gui' ):
			self.interface = GUI()

		if( self.args.interface == 'console' ):
			self.interface = Console()

		self.interface.setOptions( self.args )

	def getInterface(self):
		return self.interface

	def help(self):
		self.parser.print_help()

	def assoc(self):

		# associations for argument interface
		iface_assoc_console = ('tty', 'cmd', 'text', 'txt')
		iface_assoc_gui = ('ui', 'g', 'graphic', 'x')

		self.args.interface = self.args.interface.lower()

		if( self.args.interface in iface_assoc_console ):
			self.args.interface = 'console'

		if( self.args.interface in iface_assoc_gui ):
			self.args.interface = 'gui'

		# create association for argument 
		self.args.in_wallets = self.args.in_wallets.upper()
		self.args.out_wallets = self.args.out_wallets.upper()

	def check(self):
		# checking arguments interface
		if( (self.args.interface != 'gui') and (self.args.interface != 'console') ):
			Console.error('no correct name interface (gui/console)')

		# checking arguments in/out wallets
		if( ( (len( self.args.in_wallets ) == 3) and (len( self.args.out_wallets ) == 3) ) == False ):
			Console.error('conflict in name <in> or <out> wallets')

		# checking value
		if( self.args.value <= 0.0 ):
			Console.error('value is not have 0.0 or loss')

	def _debug_(self):
		
		print( 'options(debug):' )

		if( self.args.version ):
			print( ' - print version program' )
		if( self.args.list ):
			print( ' - print list wallets' )
			
		print( ' - value is', self.args.value )
		print( ' - input wallets ', self.args.in_wallets )
		print( ' - output wallets ', self.args.out_wallets )
		print( ' - interface is', self.args.interface )

iface = Console()

# class: main class init
def init():
		# update course, from ethernet or file
		course.update()

		# get class parsing arguments
		opt = Options()
		opt.build()
		
		# get user interface
		iface = opt.getInterface()

		# set course interface
		course.iface = iface

		# start application
		iface.setOptions(opt.args)
		iface.default()
		iface.start()

"""
###################################
#	Build application and start   #
###################################
"""

init()