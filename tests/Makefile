# This file is used to create standardized text for any textract method that
# uses any command line utility or third party service (as opposed to a pure
# python package) for text extraction. These types of extraction methods have
# made it particularly difficult to maintain reasonably stable testing
# environments, so this provides a useful workaround to validate that the
# extraction methods are working correctly across all development environments
#
# https://github.com/deanmalmgren/textract/issues/78

TARGETS = pdf/ocr_text.txt \
	png/raw_text.txt png/standardized_text.txt \
	gif/raw_text.txt gif/standardized_text.txt \
    jpg/raw_text.txt jpg/standardized_text.txt \
    tiff/raw_text.txt tiff/standardized_text.txt \
	ps/raw_text.txt

all: $(TARGETS)

clean:
	rm -f $(TARGETS)

# create OCR output for the multi-page pdf test
pdf/ocr_text.txt: pdf/ocr_text.pdf
	pdftoppm $< /tmp/pdf-ocr-text
	for x in /tmp/pdf-ocr-text*; do \
		tesseract $$x $$(basename $$x .ppm) > /dev/null; \
	done
	cat pdf-ocr-text*.txt > $@
	rm -f pdf-ocr-text*

ps/raw_text.txt: ps/raw_text.ps
	ps2ascii $< > $@

# simple pattern rule for creating standard issue tesseract files for different
# fileypes. the `g` shell variable is the path to the file without the
# extension (e.g. g=png/raw_text)
%.txt: %.png
	f=$@; g=$${f%%.*}; tesseract $< $${g} > /dev/null

%.txt: %.gif
	f=$@; g=$${f%%.*}; tesseract $< $${g} > /dev/null

%.txt: %.tiff
	f=$@; g=$${f%%.*}; tesseract $< $${g} > /dev/null

%.txt: %.jpg
	f=$@; g=$${f%%.*}; tesseract $< $${g} > /dev/null
