# python3 md070crosslevenshteinPhon.py ../../../xdata/y2016riga-cog-ukru/pattr-internet-ua-dict07.txt ../../../xdata/y2016riga-cog-ukru/pattr-internet-ru-dict2.txt ua ru >../../../xdata/y2016riga-cog-ukru/pattr-internet-crosslev-ua-ru07.txt
# python3 md070crosslevenshteinPhonV02TopCand.py ../../../xdata/y2016riga-cog-ukru/pattr-internet-ua-dictV02.txt ../../../xdata/y2016riga-cog-ukru/pattr-internet-ru-dict2.txt ua ru >../../../xdata/y2016riga-cog-ukru/pattr-internet-crosslev-ua-ruV02TopCand.txt
# head -n 20 <cs.num | tail -n 10 >cs-t00020.num
# head -n 30 <cs.num | tail -n 10 >cs-t00030.num

python3 md070crosslevenshteinPhonV04.py ../../../xdata/morpho/cs-t00010.num ../../../xdata/morpho/ru.num en ru >../../../xdata/morpho/V04cs-ru-crosslevV04-t00010.txt
# python3 md070crosslevenshteinPhonV04TopCzech.py ../../../xdata/morpho/uk2k-1052.num ../../../xdata/morpho/ru.num ua ru >../../../xdata/morpho/V04uk-ru-crosslevV04-1052.txt
