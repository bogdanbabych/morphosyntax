'''
Created on 9 Dec 2016

@author: bogdan
'''

import sys, os, re


class cSplitFile(object):
	'''
	classdocs
	'''


	def __init__(self, SFNameI, ILenSplit=50):
		'''
		Constructor
		'''
		SNameInm , SNameIext = os.path.splitext(SFNameI)
		SFNameO = SNameInm + '-1000' + SNameIext
		FNameI = open(SFNameI, 'rU')
		FNameO = open(SFNameO, 'w')
		i = 0
		k = 0
		for SLine in FNameI:
			i += 1
			SLine = SLine.rstrip()
			SLine = SLine.lstrip()
			LLine = re.split('[\t ]+', SLine)
			try:
				SWord = LLine[1] 
				SPoS = LLine[2]
				IFrq = int(LLine[0])
			except:
				SWord = 'NONE'
				SPoS = 'NONE'
				IFrq = 0
				continue
			
			SPoSM = self.mapPoS(SPoS)
			FNameO.write(str(IFrq) + '\t' + SWord + '\t' + SPoSM + '\n')
			
			if i % ILenSplit == 0:
				k += 1
				k0 = 1000+k
				SFNameO = SNameInm + '-' + str(k0) + SNameIext
				FNameO.close()
				FNameO = open(SFNameO, 'w')
			
			
	def mapPoS(self, SPoS):
		SPoSM = ''
		DPoS = {'s':'ADP', 'q':'CONJ', 'n':'NOUN', 'v':'VERB', 'a':'ADJ', 'p':'PRON', 'r':'ADV', 'q':'PART', 'i':'INTJ', 'y':'NOUN', 'm':'NUM'}
		try:
			SPoSM = DPoS[SPoS]
		except:
			SPoSM = SPoS
		
		return SPoSM

		
		
if __name__ == '__main__':
	OSplitFile = cSplitFile(sys.argv[1], ILenSplit=30)