'''
Created on 28 Mar 2017

@author: bogdan
'''

import os, sys, re, codecs
# import md060graphonoLev
from macpath import join

class clExtractInputWd(object):
	'''
	extracting input words from a dictionary file in glossary format
	refernce dictionary file has mappings for the evaluation set, but does not have the tags;
	*.num file has tags, but does not have mappings.
	--> the task: to create a file which has mappings and PoS codes --> to be used for generating input (in a trivial way) and as a reference file
	for checking the performance.
	'''


	def __init__(self, SFInMap, SFInNumPoS, SFInNumPoSTgt):
		'''
		takes the map file (from gold standard mapping) and PoS file with frequencies (output from corpus as *.num)
		
		'''
		FInMap = codecs.open(SFInMap, "r", encoding='utf-8', errors='ignore')
		FInNumPoS = codecs.open(SFInNumPoS, "r", encoding='utf-8', errors='ignore')
		FInNumPoSTgt = codecs.open(SFInNumPoSTgt, "r", encoding='utf-8', errors='ignore')
		# FDebug =  codecs.open('md010extractinputwd-debug.txt', "w", encoding='utf-8', errors='ignore')
		
		# read two dictionaries from files, then intersect them (worth within the shorter dictionary and look up the index in a larger one...)
		DSrc2TrgMaps = self.readDictFromFile(FInMap, 0, [1])
		# temporary testing -- printing out the dictionary read
		# self.printDict2File(DSrc2TrgMaps)
		DSrc2PoS = self.readDictFromFile(FInNumPoS, 1, [2,0])
		# temporary testing -- printing out the dictionary read
		# self.printDict2File(DSrc2PoS)
		DSrc2PoSTgt = self.readDictFromFile(FInNumPoSTgt, 1, [2,0])
		# intersect with the target; update dictionaries; calculate Lev distance >> different kinds; save / display results
		
		
		(DIntersection, DDifference, DIntersectionTgt, DIntersectionDiffTgt) = self.intersectDicts(DSrc2TrgMaps, DSrc2PoS, DSrc2PoSTgt)
		# self.printDict2File(DIntersection)
		# self.printDict2File(DDifference)
		# print(str(len(DIntersection.keys())))
		# print(str(len(DDifference.keys())))
		DIntersection2 = self.optimeseDict2num(DIntersection)
		DIntersectionTgt2 = self.optimeseDict2num(DIntersectionTgt)
		
		### temp ### self.printDict2num(DIntersection2)
		self.printDict2num(DIntersectionTgt2)
		## self.printDict2File(DSrc2PoSTgt)
		## self.printDict2File(DSrc2PoS)
		## self.printDict2File(DIntersection2)
		## self.printDict2File(DIntersectionTgt2)
		
	def intersectDicts(self, DSearch, DReference, DReferenceTgt):
		"""
		Two dictionaries: Search and Reference are intersected, and the Search dictionary is enriched with values from the reference
		Third dictionary is the target reference dictionary, structure 
		медведеву	[('VERB', '16'), ('INTJ', '5')]
		"""
		# dictionaries to be returned, which can be printed out
		DIntersection = {}
		DDifference = {}
		
		DIntersectionTgt = {} # intersection checked also with target
		DIntersectionDiffTgt = {} # there is intersection with source ref, but there is a difference with target equivalents references
		# counts for the number of keys in the intersection and difference sets -- to be defined as len(Keys)
		# IIntersection = 0
		# IDifference = 0

		for (SKey, LTValSearch) in DSearch.items():
			# dictionary structure:
			# логічний	[('логический',), ('логичный',)]
			if SKey in DReference:
				# dictionary structure:
				# медведеву	[('VERB', '16'), ('INTJ', '5')]
				# IIntersection += 1
				LTValReference = DReference[SKey]
				DIntersection[SKey] = (LTValReference, LTValSearch)
				
				# added test 13/04/2017
				# checking if target mapping are in the target dictionary; then -- compute Lev distance --> design gold-standard eval set...
				try: 
					LTRefNRefTgtWord = [] # get the list of intersecting Words
					for TTranslationMapped in LTValSearch:
						STranslationMapped = TTranslationMapped[0] # take the first element only;
						if STranslationMapped in DReferenceTgt: # if the target can be found
							# more complex task: intersection of PoS codes:
							# replace this:
							# DIntersectionTgt[SKey] = (LTValReference, LTValSearch)
							LTRefNRefTgtWord.append((STranslationMapped,)) # preserve the same format as LTValSearch
							LTValReferenceTgtPoS = DReferenceTgt[STranslationMapped] # get values (pos codes for target
							# get the list of intersecting PoS codes
							LRefNRefTgtPoS = []
							for TValReferenceTgtPoS in LTValReferenceTgtPoS: # [('VERB', '16'), ('INTJ', '5')]
								# for each PoS in translated set : check if there exists the same PoS code and add it to the list; if the list is empty -- do not add to dictionary;
								SValReferenceTgtPoS = TValReferenceTgtPoS[0] # get the PoS without frequency for the target
								for TValReferencePoS in LTValReference:
									SValReferencePoS = TValReferencePoS[0] # get PoS without frequency for the original
									IValReferenceFrq = TValReferencePoS[1] # get frequency 
									if SValReferenceTgtPoS == SValReferencePoS: # if Pos codes are the same
										LRefNRefTgtPoS.append((SValReferencePoS,IValReferenceFrq))
									else:
										sys.stderr.write('%(STranslationMapped)s\t%(SValReferenceTgtPoS)s\t%(SValReferencePoS)s\n' % locals())
							if len(LRefNRefTgtPoS) > 0:
								# DIntersectionTgt[SKey] = (LRefNRefTgtPoS, LTValSearch) # not the default LTValSearch, but only those which are found
								DIntersectionTgt[SKey] = (LRefNRefTgtPoS, LTRefNRefTgtWord) # replaced....
							else:
								DIntersectionDiffTgt[SKey] = (LTValReference, LTValSearch) # remove also into the difference dictionary if no overlapping PoS were found
								
						else:
							DIntersectionDiffTgt[SKey] = (LTValReference, LTValSearch) # pos codes, translations
						
						
				except:
					sys.stderr.write('4.Mapping to target error:%(SKey)s\n' % locals())
				
				
			else:
				# IDifference += 1
				DDifference[SKey] = LTValSearch
		
		# at some point we need to print / return length of difference files --> how many were filtered out...		
		# return dictionary structure: 
		# логічний	([('PART', 1), ('ADJ', 500)], [('логический',), ('логичный',)])
		return (DIntersection, DDifference, DIntersectionTgt, DIntersectionDiffTgt)
		
				
				
	
	def readDictFromFile(self, FIn, IIndexField, LIValFields):
		"""
		reads a tab separated file and creates a dictionary with a given field as an index and a list of given fields as values
		- creates index out of one field; 
		- if there is a repeated index record, adds values to the list of values (then removes repetitions?)
		// potentially reusable in other packages... 
		
		- technical solution: do not read multiword equivalents (if they contain a space)
		~ addition: treat PoS as a dictionary entry -- to enable to amalgamate different meanings of the word which are within the same pos, so no double entries exist
		
		"""
		DIndexVals = {} # dictionary with the structure {'SIndex' : [LTValues]} (list of tuples with fields)
		for SLine in FIn:
			SLine = SLine.rstrip()
			try:
				LLine = re.split('\t', SLine)
			except:
				sys.stderr.write('0:Split Error: %(SLine)s\n' % locals())
			IIdxField = int(IIndexField)
			try:
				SKey = LLine[IIdxField]
			except:
				SKey = None
				sys.stderr.write('1:Key Error: %(SLine)s;%(IIdxField)d\n' % locals())
			LFieldsToCollect = []
			for el in LIValFields:
				IEl = int(el)
				try:
					Val = LLine[IEl]
				except:
					Val = ''
					sys.stderr.write('2:Val Error: %(SLine)s;%(IEl)d\n' % locals())
				# if Val == None: continue # do not add None values to the list of values
				# no: we need exact number of values in a tuple, even with None values
				# ad-hoc: not adding multiwords to reference
				if re.search(' ', Val): continue # to be able to run conditionally and remove....
				LFieldsToCollect.append(Val)
			# updating the dictionary : checking if exists; if not exists
			TVals = tuple(LFieldsToCollect)
			if SKey == None: continue # do not process error lines
			if TVals == (): continue # do not add an empty tuple : to be able to run conditionally and remove... -- important keys ignored, e.g., торік
			if SKey in DIndexVals: #  if the dictionary has key -- SKey
				LTValues = DIndexVals[SKey]
			else:
				LTValues = []
				
			LTValues.append(TVals) # adding the tuple with values for this record
				
			DIndexVals[SKey] = LTValues
		
		# end: for Sline in FIn:
		return DIndexVals
	
	def printDict2File(self, DToPint):
		for (Key, Val) in DToPint.items():
			SKey = str(Key)
			SVal = str(Val)
			print('%(SKey)s\t%(SVal)s' % locals())
			
			
	def optimeseDict2num(self, DSnT2LT):
		"""
		move all structure-dependent solutions here:
		1. remove empty entries
		2. remove multiwords
		3. join together multiple entries of the same PoS
		~ prepare the dictionary for a usable format...
		~ first step - remove repetitions
		
		
		"""
		DSnT2LTOut = {}
		for (SKey, Val) in DSnT2LT.items():
			(LTPoSFrq, LTTransl) = Val
			DPoSFrq = {} # local dictionary for each record which may have multiple entries of the same PoS
			LTPoSFrqOut = []
			for T2PoSFrq in LTPoSFrq:
				(SPoS, SFrq) = T2PoSFrq
				IFrq = int(SFrq)
				if SPoS in DPoSFrq:
					IFrq0 = DPoSFrq[SPoS]
					IFrq += IFrq0
				DPoSFrq[SPoS] = IFrq
					
					
			for (SPoSX, IFrqX) in DPoSFrq.items():
				T2PosFrqOut = (SPoSX, IFrqX)
				LTPoSFrqOut.append(T2PosFrqOut)
			DSnT2LTOut[SKey] = (LTPoSFrqOut, LTTransl)
				
		
		return DSnT2LTOut
			
	def printDict2num(self, DSnT2LT): # dictionary : strings mapped to 2-tuples of lists of n-tuples
		IItemCount = 0
		IPoSCount = 0
		IPoSMultiple = 0
		IPoSInterjections = 0
		# for (SKey, Val) in sorted(DSnT2LT.items(), reverse=True): # no sorting
		for (SKey, Val) in DSnT2LT.items():
			IItemCount +=1  
			try:
				# unpacking 2-tuple of lists
				(LTPoSFrq, LTTransl) = Val
			except:
				sys.stderr.write('3.1.Wrong tuple structure %(SKey)s\n' % locals())
				
			ILenPoS = len(LTPoSFrq)
			if ILenPoS > 1:
				IPoSMultiple += 1
			if ILenPoS > 2:
				sys.stderr.write('%(SKey)s\t%(ILenPoS)d\n' % locals())
			
			for T2PoSFrq in LTPoSFrq:
				IPoSCount +=1
				(SPoS, SFrq) = T2PoSFrq
				if SPoS == 'INTJ' or SPoS == 'PRON': # no iterjections nor pronouns
					IPoSInterjections += 1
					continue 
				# print the test file:
				sys.stdout.write('%(SFrq)s\t%(SKey)s\t%(SPoS)s\t' % locals())
				LWords = []
				for TWord in LTTransl:
					Word = TWord[0]
					LWords.append(Word)
				SWordsTrans = '~'.join(LWords)
				sys.stdout.write('%(SWordsTrans)s\n' % locals())
		# end: for (SKey, Val) DSnT2LT.items():
		sys.stderr.write('Items:%(IItemCount)d\n' % locals()) 			
		sys.stderr.write('PoS:%(IPoSCount)d\n' % locals())
		sys.stderr.write('Multi-PoS:%(IPoSMultiple)d\n' % locals())
		sys.stderr.write('InterjectionsPronouns-PoS:%(IPoSInterjections)d\n' % locals())
		
		

		
if __name__ == '__main__':
	OExtractInputWd = clExtractInputWd(sys.argv[1], sys.argv[2], sys.argv[3])
	# dictionary with field ; frq word list with pos codes
	# python3 md010extractinputwd.py ../../data/uk-ru-glossary/dict-uk-ru-uk-50k-s010-fields.txt ../../../xdata/morpho/uk.num >../../../xdata/morpho/uk2ru-cognates-pos-evalset.txt

		