# main file -- is the file with examples: ...dict-uk-ru-uk-50k-s010-fields.txt
python3 md010extractinputwdV02.py ../../data/uk-ru-glossary/dict-uk-ru-uk-50k-s010-fields.txt ../../../xdata/morpho/uk.num ../../../xdata/morpho/ru.num >../../../xdata/morpho/uk2ru-cognates-pos-evalsetV02.txt
cp ../../../xdata/morpho/uk2ru-cognates-pos-evalsetV02.txt ../../../xdata/morpho/uk2ru-cognatesV02.num