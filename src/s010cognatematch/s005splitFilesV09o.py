'''
Created on 9 Dec 2016

@author: bogdan
'''

import sys, os, re, codecs


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
		# FNameI = open(SFNameI, 'rU')
		FNameO = open(SFNameO, 'w')

		SFNameSh = SFNameO + '-o.sh'
		FNameSh = open(SFNameSh, 'w')
		FNameSh.write('python3 md070crosslevenshteinPhonV09o.py %(SFNameO)s ../../../xdata/morpho/ru.num ua ru >%(SFNameO)s.ores\n' % locals())
		i = 0
		k = 0
		# with codecs.open(SFNameI, "r",encoding='utf-8', errors='ignore') as FNameI:
		FNameI = codecs.open(SFNameI, "r",encoding='utf-8', errors='ignore')
		for SLine in FNameI:
			SLine = FNameI.readline()
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
			try:
				LRest = LLine[3:]
			except:
				LRest = []
			SRest = '\t'.join(LRest)
			
			SPoSM = self.mapPoS(SPoS)
			if LRest == []:
				FNameO.write(str(IFrq) + '\t' + SWord + '\t' + SPoSM + '\n')
			elif len(LRest) > 0:
				FNameO.write(str(IFrq) + '\t' + SWord + '\t' + SPoSM + '\t' + SRest + '\n')
			
			if ILenSplit == 0: continue
			if i % ILenSplit == 0:
				k += 1
				k0 = 1000+k
				SFNameO = SNameInm + '-' + str(k0) + SNameIext
				FNameO.close()
				FNameO = open(SFNameO, 'w')

				SFNameSh = SFNameO + '-o.sh'
				FNameSh.close()
				FNameSh = open(SFNameSh, 'w')
				FNameSh.write('python3 md070crosslevenshteinPhonV09o.py %(SFNameO)s ../../../xdata/morpho/ru.num ua ru >%(SFNameO)s.ores\n' % locals())
			
			
	def mapPoS(self, SPoS):
		SPoSM = ''
		DPoS = {'s':'ADP', 'q':'CONJ', 'n':'NOUN', 'v':'VERB', 'a':'ADJ', 'p':'PRON', 'r':'ADV', 'q':'PART', 'i':'INTJ', 'y':'NOUN', 'm':'NUM'}
		try:
			SPoSM = DPoS[SPoS]
		except:
			SPoSM = SPoS
		
		return SPoSM

		
		
if __name__ == '__main__':
	OSplitFile = cSplitFile(sys.argv[1], ILenSplit=int(sys.argv[2]))
	