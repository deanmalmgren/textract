# This file generates test fixtures for textract methods that rely on external
# command line utilities (tesseract, pdftoppm, ps2ascii). Generated .txt files
# are committed to git so tests can run without requiring these dependencies.
#
# To regenerate fixtures after adding new test files:
#   1. Install system dependencies (tesseract, poppler-utils, ghostscript)
#   2. Run: cd tests && make
#   3. Commit the generated .txt files
#
# https://github.com/deanmalmgren/textract/issues/78

TARGETS = pdf/ocr_text.txt \
	png/raw_text.txt png/standardized_text.txt \
	gif/raw_text.txt gif/standardized_text.txt \
    jpg/raw_text.txt jpg/standardized_text.txt \
    tiff/raw_text.txt tiff/standardized_text.txt \
	ps/raw_text.txt ps/standardized_text.txt

.PHONY: all force clean

all: $(TARGETS)

force:
	$(MAKE) clean
	$(MAKE) all

clean:
	rm -f $(TARGETS)

# create OCR output for the multi-page pdf test
pdf/ocr_text.txt: pdf/ocr_text.pdf
	pdftoppm -png $< pdf-ocr-tmp
	for x in pdf-ocr-tmp*.png; do \
		base=$${x%.png}; \
		tesseract $$x $$base > /dev/null; \
	done
	cat pdf-ocr-tmp*.txt > $@
	rm -f pdf-ocr-tmp*

ps/raw_text.txt: ps/raw_text.ps
	ps2ascii $< > $@

ps/standardized_text.txt: ps/standardized_text.ps
	ps2ascii $< > $@

# simple pattern rule for creating standard issue tesseract files for different
# fileypes. the `g` shell variable is the path to the file without the
# extension (e.g. g=png/raw_text)
%.txt: %.png
	f=$@; g=$${f%%.*}; tesseract $< $${g} > /dev/null

%.txt: %.gif
	f=$@; g=$${f%%.*}; convert "$<[0]" $${g}.png && tesseract $${g}.png $${g} > /dev/null; rm -f $${g}.png

%.txt: %.tiff
	f=$@; g=$${f%%.*}; tesseract $< $${g} > /dev/null

%.txt: %.jpg
	f=$@; g=$${f%%.*}; tesseract $< $${g} > /dev/null
