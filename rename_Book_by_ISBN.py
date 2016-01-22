# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:34:02 2016

@author: ShiJingchang

@require: sys, os, isbntools
@sample: python rename_Book_by_ISBN.py in.pdf 9780980232714
@note: WorldCat.org service is blocked in China mainland.
	   Maybe you should use VPN to connect to worldcat service.
	   And I recommend GreenVPN, link: http://gjsq.link
	   In addition, this is my recommendation link: http://gjsq.me/r2869780
"""
import sys

ISBNStr = sys.argv[2]

import isbnlib

BibContentDict = isbnlib.meta(ISBNStr, service="wcat")

FirstAuthorStr = BibContentDict['Authors'][0]
if "et al" in FirstAuthorStr:
	FirstAuthorList = FirstAuthorStr.split()
	for StrInd in range(len(FirstAuthorList)):
		if FirstAuthorList[StrInd] == "...":
			FirstAuthorLastNameStr = FirstAuthorList[StrInd-1].lower()
else:
	FirstAuthorList = FirstAuthorStr.split()
	FirstAuthorLastNameStr = FirstAuthorList[-1].lower()

YearStr = BibContentDict['Year']

TitleRawStr = BibContentDict['Title']
TitleList = TitleRawStr.split()
TitleStr = '_'.join(TitleList)
TitleStr = TitleStr.lower()

PDFFileNewNameStr = "-".join([FirstAuthorLastNameStr, YearStr, TitleStr])
PDFFileNewNameStr = PDFFileNewNameStr + ".pdf"

PDFFileNameStr = sys.argv[1]

import os
os.rename(PDFFileNameStr, PDFFileNewNameStr)

print "Your book file is renamed!"
