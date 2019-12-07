#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@theme: utilities
@author: mario
"""

import os
import uuid
import fulltext

class inputError(Exception):
    pass

class PDF(object):
	"""
	PDF parses two types of pdf file:
	(1) OCR-type, call tesseract-ocr; (2)Transform-type, call pdfminer 
    :param: <absolute filepath>
    :return: a list of words
	"""
	def __init__(self,filepath):
		# only accept :filepath: , and execute in command line
		self.filepath = os.path.abspath(filepath)
		self.abspath = "/".join(self.filepath.split("/")[:-1])
		self.random = uuid.uuid4().hex
    
    
	def parse(self):
        # step one: call pdfminer3 in command line: `pdf2txt.py <file name> > temp.txt`
		string = fulltext.get(self.filepath,None)
		if string:
			return self.string
		else: # status number bigger than 0 indicating errors: 
            # call ocrmypdf: transform .pdf/.img to .pdf
            # command: ocrmypdf <filename>.pdf <output>.pdf
            # lang: apt-get install tesseract-ocr-chi-sim >> simplified chinese
			command = "ocrmypdf {} {}/{}.pdf".format(self.filepath,self.abspath,self.random)
			status = os.system(command)
			if status==0:
				string = fulltext.get("{}/{}".format(self.abspath,self.random),"None")
				string = self.tokenRestore(string)
                # remove the temporary file
				os.system("rm {}/{}".format(self.abspath,self.random))
				return self.string
			else:
				return ""

#################### Parser Block ####################

class fileParser(object):
	def __init__(self,filepath):
		if filepath.endswith(".pdf"):
			self.string = PDF(filepath).parse()
		else: # .txt, .html, .doc, .docx
			self.string = fulltext.get(filepath,None)
			if not self.string:
				temp = open(filepath,"r",encoding="gbk")
				text = temp.read()
				if text:
					self.string = text
				else:
					self.string = ""
				temp.close()
        

class webParser(object):
    def __init__(self,web):
        """
        Build service of WEB parser alone 
        :param: page link of sites
        :return: parsed string
        """
        # call API.web.parse()
        pass

#################### Selector Block ####################

class InputError(Exception):
	pass


class FileLoader(fileParser,webParser):
	"""
    Handle different formats of files
    :param: absolute path of file
    :return: parsed string from input file
    """
	accepts = ["pdf","txt","html","doc","docx"]
	filetype = "file" # accepts file path or web path
    
	def __init__(self,filepath):
		# warn: might cover `filepath` in selector
		if os.path.isfile(filepath):
			if not filepath.split(".")[-1] in self.accepts:
				raise inputError("Invalid input file path (expect a path of .txt, .doc, .pdf, .html).")
			else:    
				self.file = filepath  
                
		elif os.path.isdir(filepath):
			""" temporarily not support
            self.files = ["{}/{}".format(filepath,file) for file in os.listdir(filepath) if file.split(".")[-1] in self.accepts]
            """
			raise InputError("Accept only fiel path, not directory.")
		elif filepath.startswith("http"):
			self.file = filepath # web path
			self.filetype = "web"
		else:
			raise InputError("Accept only valid file path.")


	def load(self):
		if self.filetype == "web":
			string = webParser(self.file).parse()
		else: # file type
            # fileParser.string : str not list
			string = fileParser(self.file).string
		self.text = string # storage
		return string

