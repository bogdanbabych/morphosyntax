# python3 md070crosslevenshteinPhon.py ../../../xdata/y2016riga-cog-ukru/pattr-internet-ua-dict07.txt ../../../xdata/y2016riga-cog-ukru/pattr-internet-ru-dict2.txt ua ru >../../../xdata/y2016riga-cog-ukru/pattr-internet-crosslev-ua-ru07.txt
# python3 md070crosslevenshteinPhonV02TopCand.py ../../../xdata/y2016riga-cog-ukru/pattr-internet-ua-dictV02.txt ../../../xdata/y2016riga-cog-ukru/pattr-internet-ru-dict2.txt ua ru >../../../xdata/y2016riga-cog-ukru/pattr-internet-crosslev-ua-ruV02TopCand.txt
# head -n 20 <cs.num | tail -n 10 >cs-t00020.num
# head -n 30 <cs.num | tail -n 10 >cs-t00030.num

python3 md070crosslevenshteinPhonV03TopCzech.py ../../../xdata/morpho/cs-t00070.num ../../../xdata/morpho/ru.num en ru >../../../xdata/morpho/cs-ru-crosslevV03TopCzech00070.txt
python3 md070crosslevenshteinPhonV03TopCzech.py ../../../xdata/morpho/cs-t00170.num ../../../xdata/morpho/ru.num en ru >../../../xdata/morpho/cs-ru-crosslevV03TopCzech00170.txt
python3 md070crosslevenshteinPhonV03TopCzech.py ../../../xdata/morpho/cs-t00270.num ../../../xdata/morpho/ru.num en ru >../../../xdata/morpho/cs-ru-crosslevV03TopCzech00270.txt
