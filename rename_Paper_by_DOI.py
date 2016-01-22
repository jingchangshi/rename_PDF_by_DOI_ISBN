# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:34:02 2016

@author: ShiJingchang

@require:
	python packages: sys, os, subprocess
	software: curl(curl for windows can be downloaded from http://curl.haxx.se/download.html)
@sample: python rename_Paper_by_DOI.py in.pdf 10.1016/j.physd.2003.03.001
"""

BibFileNameStr = "tmp.bib"
###################
# Get Bib file by DOI
def getBibFile_by_DOI():
	import sys, subprocess

	DOIStr = sys.argv[2]

	CommandGetBib_ExecStr = "curl.exe"
	CommandGetBib_ParametersStr = "-LH"
	CommandGetBib_AcceptHeaderStr = "\"Accept: application/x-bibtex\""
	CommandGetBib_DOIStr = "http://dx.doi.org/" + DOIStr
	CommandGetBibStr = ' '.join([CommandGetBib_ExecStr, \
		CommandGetBib_ParametersStr, \
		CommandGetBib_AcceptHeaderStr, \
		CommandGetBib_DOIStr])

	BibContentStr = \
		subprocess.Popen(CommandGetBibStr, stdout=subprocess.PIPE).communicate()[0]
	
	BibFile = open(BibFileNameStr, "w")
	BibFile.write(BibContentStr)
	BibFile.close()

###################
# Rename PDF file by Bib file
def renamePDFFile_by_BibFile():
	import os, sys

	PDFFileNameStr = sys.argv[1]

	BibFile = open(BibFileNameStr, "r")
	BibFileContentList = BibFile.readlines()
	BibFile.close()

	for LineInd in range(len(BibFileContentList)):
		BibFileSingleLineStr = BibFileContentList[LineInd]
		BibFileSingleLineStr = BibFileSingleLineStr.strip()
		if BibFileSingleLineStr[0:6] == "author":
			AuthorsStr = BibFileSingleLineStr[10:-2]
			AuthorsList = AuthorsStr.split()
			for StrInd in range(len(AuthorsList)):
				if AuthorsList[StrInd] == "and":
					FirstAuthorLastNameStr = AuthorsList[StrInd-1].lower()
					FirstAuthorLastNameStr = \
						''.join(s for s in FirstAuthorLastNameStr if s.isalnum())
					break
		if BibFileSingleLineStr[0:4] == "year":
			YearStr = BibFileSingleLineStr[7:-1]
		if BibFileSingleLineStr[0:5] == "title":
			TitleList = BibFileSingleLineStr[9:-2].split()
			for StrInd in range(len(TitleList)):
				TitleList[StrInd] = \
					''.join(s for s in TitleList[StrInd] if s.isalnum())
			TitleStr = '_'.join(TitleList)
			TitleStr = TitleStr.lower()

	PDFFileNewNameStr = "-".join([FirstAuthorLastNameStr, YearStr, TitleStr])
	PDFFileNewNameStr = PDFFileNewNameStr + ".pdf"
	print PDFFileNewNameStr
	os.rename(PDFFileNameStr, PDFFileNewNameStr)

	print "Your paper file is renamed!"

###################
# Main
getBibFile_by_DOI()
renamePDFFile_by_BibFile()