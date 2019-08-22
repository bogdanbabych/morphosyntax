'''
Created on Dec 3, 2013

@author: bogdan
requires python3
'''
import os, sys, re
from collections import defaultdict
import math
import md060graphonoLev


class clCrossLevenshtein(object):
    '''
    classdocs
    '''


    def __init__(self, SFInA, SFInB, SLangIDa, SLangIDb):
        '''
        Constructor
        '''
        SNameIName , SNameIExt = os.path.splitext(SFInA) # generate the debug using the first file name
        SFDebug = SNameIName + '-md050crosslevenshtein.debug'
        # FDebug = open(SFDebug, 'w') # debug file for each of the input files.. 
        LWordsA, LWordsIndexA = self.readWordList(SFInA)
        LWordsB, LWordsIndexB = self.readWordList(SFInB) # graphonological object with phonological features over graphemes
        # OGraphonolev = md060graphonoLev.clGraphonolev(Debug = True, DebugFile = SFDebug)
        OGraphonolev = md060graphonoLev.clGraphonolev()

        
        LDistances = []
        ICounter = 0
        ICounterRec = 0
        for (SWordA, SPoSA, IFrqA, LTargetsEval) in LWordsA:
            LenA = len(SWordA)
            try:
                LogFrqA = math.log(IFrqA)
            except:
                LogFrqA = 0
            LCognates = []
            LCognates1 = []
            ICounter += 1
            if ICounter % 1 == 0:
                sys.stderr.write(SWordA + ' ' + str(ICounter) + '\n')
            print(SWordA)
            print(str(LTargetsEval))
            
            # count if references can be found in the target?
            ICountEvalInTarget = 0
            for STargetE in LTargetsEval:
                (Lev0E, Lev1E, Lev0NormE, Lev1NormE) = OGraphonolev.computeLevenshtein(SWordA, STargetE, SLangIDa, SLangIDb)
                print('%(SWordA)s,%(STargetE)s,L-G:%(Lev0E)f,%(Lev1E)f,NL-G:%(Lev0NormE)f,%(Lev1NormE)f' % locals())
                # not printing but recording into memory
                # if found the evaluation target in reference 
                if STargetE in LWordsIndexB:
                    ICountEvalInTarget +=1
                
            if ICountEvalInTarget == 0:
                print('\t: not in the reference list!')
                continue
            # -- this stops search for items, which where reference is not in Russian list, so cannot be found...
            # can be treated a bit differently, statistics collected, etc.!!!
               
            ''' 
            # changed:
            for (SWordB, SPoSB, IFrqB) in LWordsB:
                LenB = len(SWordB)
                LenAve = (LenA + LenB) / 2
            
                ILev = self.computeLevenshtein(SWordA, SWordB)
                ALevNorm = ILev/LenAve
                if ALevNorm <= 0.30:
                    LCognates.append((ALevNorm, ILev, SWordB, SPoSB, IFrqB))
            '''
            # LTargetsEval2 not used -- usually large reference word list is not expected to have references
            for (SWordB, SPoSB, IFrqB, LTargetsEval2) in LWordsB:
                # Lev0 is baseline Levenshtein distance
                # Lev1 is is graphonological Levenshtein distance
                (Lev0, Lev1, Lev0Norm, Lev1Norm) = OGraphonolev.computeLevenshtein(SWordA, SWordB, SLangIDa, SLangIDb)
                # if Lev0Norm <= 0.36:
                if Lev0Norm <= 0.5:
                    LCognates.append((Lev0Norm, Lev0, SWordB, SPoSB, IFrqB)) # baseline Lev
                # if Lev1Norm <= 0.36:
                if Lev1Norm <= 0.5:
                    LCognates1.append((Lev1Norm, Lev1, SWordB, SPoSB, IFrqB)) # graphonological Lev
            
            
            LDistances.append((SWordA, SPoSA, IFrqA, LCognates))
            if (len(LCognates) > 0 or len(LCognates1) > 0):
                ICounterRec += 1
                ACognPerCent = ICounterRec / ICounter
                # now restricted to writing only one cognate...
                # sys.stdout.write('\t{, %(ICounterRec)d, %(ICounter)d, %(SWordA)s, %(SPoSA)s, frq=%(IFrqA)d, ln=%(LogFrqA).2f, have-cognates: %(ACognPerCent).2f : \n' % locals())
                sys.stdout.write('%(SWordA)s\t%(SPoSA)s\tfrq=%(IFrqA)d\t\n' % locals())
                sys.stdout.flush()
                sys.stdout.write('BASELINE:\n')
                self.printCognate(LCognates, LogFrqA, SPoSA)
                # sys.stdout.write('\t')
                sys.stdout.write('GRAPHONOLOGICAL:\n')
                self.printCognate(LCognates1, LogFrqA, SPoSA)
                # removed (s) --> printCognate(s) in function call : simple production version
                sys.stdout.write('\n\n')
                sys.stdout.flush()
            
        '''
        for (SWordA, SPoSA, IFrqA, LCognates) in LDistances:
            # sys.stdout.write('%(SWordA)s, %(SPoSA)s, %(IFrqA)d : \n' % locals())
            for (ALevNorm, SWordB, SPoSB, IFrqB) in LCognates:
                # FDebug.write('\t %(ALevNorm)f, %(SWordB)s, %(SPoSB)s, %(IFrqB)d\n')
                pass
        '''
                
    # task: redesing printing;
    # design evaluation
    def printCognate(self, LCognates, LogFrqA, SPoSA):
        """
    	print only one cognate
        """
        ICogRank = 0
        ALevNormPrev = -1
        for (ALevNorm, ILev, SWordB, SPoSB, IFrqB) in sorted(LCognates, reverse=False, key=lambda k: k[0]):
            if (ALevNorm != ALevNormPrev):
                ICogRank += 1
            if ICogRank > 3: break
            ALevNormPrev = ALevNorm
            if ((SPoSB == SPoSA)):
                sys.stdout.write('%(ICogRank)d\t%(SWordB)s\t%(SPoSB)s\tPhLev=%(ILev).2f\tPhLevNormLen=%(ALevNorm).2f\n' % locals())


                    
    def printCognates(self, LCognates, LogFrqA, SPoSA):
        ICogRank = 0
        ALevNormPrev = -1
        for (ALevNorm, ILev, SWordB, SPoSB, IFrqB) in sorted(LCognates, reverse=False, key=lambda k: k[0]): # why reverse is False: starting from smallest
            try:
                LogFrqB = math.log(IFrqB)
            except:
                LogFrqB = 0
            try:
                AFrqRange = min(LogFrqB, LogFrqA) / max(LogFrqB, LogFrqA)
            except:
                AFrqRange = 0
            
            sys.stdout.write('\tFrqRange=' + str(AFrqRange) + '\t' + SPoSB + '\t' + SPoSA + '\t')

            if (ALevNorm != ALevNormPrev):
                ICogRank += 1
            ALevNormPrev = ALevNorm

            if ((SPoSB == SPoSA) and (ICogRank == 1)):
                sys.stdout.write('--> %(SWordB)s\t%(SPoSB)s\t%(IFrqB)d\tPhLev=%(ILev).2f\tPhLevNormLen=%(ALevNorm).2f\n' % locals())
                
            
            sys.stdout.write('\nTRACE:\n')
            if ((SPoSB == SPoSA) and (AFrqRange > 0.5 )):
                # ICogRank += 1
                #
                # sys.stdout.write('\t\trank=%(ICogRank)d, %(AFrqRange).3f, %(ILev).3f, %(ALevNorm).3f, %(SWordB)s, %(SPoSB)s, %(IFrqB)d, ln=%(LogFrqB).2f\n' % locals())
                sys.stdout.write('%(SWordB)s\t%(SPoSB)s\t%(IFrqB)d\tPhLev=%(ILev).2f\tPhLevNormLen=%(ALevNorm).2f\n' % locals()) 
                ## temp: record a list of items 
                ## break # record only one item...
            elif((SPoSB == SPoSA) and (AFrqRange <= 0.5)):
                
                sys.stdout.write('REJECTED-FRQ: %(SWordB)s\t%(SPoSB)s\t%(IFrqB)d\tPhLev=%(ILev).2f\tPhLevNormLen=%(ALevNorm).2f\n' % locals()) 
            elif((SPoSB != SPoSA) and (AFrqRange > 0.5 )):
                sys.stdout.write('REJECTED-POS: %(SWordB)s\t%(SPoSB)s\t%(IFrqB)d\tPhLev=%(ILev).2f\tPhLevNormLen=%(ALevNorm).2f\n' % locals()) 
                ## pass
                # sys.stdout.write('\t\t--, %(AFrqRange).3f, %(ILev).3f, %(ALevNorm).3f, %(SWordB)s, %(SPoSB)s, %(IFrqB)d, ln=%(LogFrqB).2f\n' % locals())
            elif((SPoSB != SPoSA) and (AFrqRange <= 0.5 )):
                sys.stdout.write('REJECTED-FPS: %(SWordB)s\t%(SPoSB)s\t%(IFrqB)d\tPhLev=%(ILev).2f\tPhLevNormLen=%(ALevNorm).2f\n' % locals())
            else:
                sys.stdout.write('REJECTED-OTH: %(SWordB)s\t%(SPoSB)s\t%(IFrqB)d\tPhLev=%(ILev).2f\tPhLevNormLen=%(ALevNorm).2f\n' % locals()) 
        # sys.stdout.write('\t}\n')
        sys.stdout.write('\n')
        sys.stdout.flush()

        
    def readWordList(self, SFIn): # modified to adjust to Czech
        LWords = []
        LWordsIndex = []
        for SLine in open(SFIn, 'rU'):
            try:
                SLine = SLine.rstrip()
                SLine = SLine.lstrip()
                LLine = re.split('[\t ]+', SLine)
                SWord = LLine[1] 
                SPoS = LLine[2]
                IFrq = int(LLine[0])
            except:
                continue
            # evaluation targets, if available   
            try:
                STargetsEval = LLine[3]
                LTargetsEval = re.split('~', STargetsEval)
            except:
                LTargetsEval = []
            
            LWords.append((SWord, SPoS, IFrq, LTargetsEval))
            LWordsIndex.append(SWord)
        return LWords, LWordsIndex
    
    
    def computeLevenshteinLocal(self, s1, s2):

        l1 = len(s1)
        l2 = len(s2)
    
        matrix = [list(range(l1 + 1))] * (l2 + 1)
        for zz in range(l2 + 1):
            matrix[zz] = list(range(zz,zz + l1 + 1))
        for zz in range(0,l2):
            for sz in range(0,l1):
                # here: 1. compare sets of features; add the minimal substitution score here...
                if s1[sz] == s2[zz]:
                    matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
                else:
                    matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
        return matrix[l2][l1]
        
                          
if __name__ == '__main__':
    OCrossLevenshtein = clCrossLevenshtein(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    # dictionary1, dictionary2, langID1, langID2