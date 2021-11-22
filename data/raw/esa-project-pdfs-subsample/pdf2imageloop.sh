for f in *.pdf
do

	pdftoppm -r 72 -jpeg -jpegopt quality=90 f
