# This file is used to create standardized text for any textract method that
# uses any command line utility or third party service (as opposed to a pure
# python package) for text extraction. These types of extraction methods have
# made it particularly difficult to maintain reasonably stable testing
# environments, so this provides a useful workaround to validate that the
# extraction methods are working correctly across all development environments
#
# https://github.com/deanmalmgren/textract/issues/78

all: tesseract

tesseract:

	# create OCR output for all of the image tests
	tesseract png/raw_text.png png/raw_text > /dev/null
	tesseract gif/raw_text.gif gif/raw_text > /dev/null
	tesseract jpg/raw_text.jpg jpg/raw_text > /dev/null

	# create OCR output for all of the standardized image tests
	tesseract png/standardized_text.png png/standardized_text > /dev/null
	tesseract gif/standardized_text.gif gif/standardized_text > /dev/null
	tesseract jpg/standardized_text.jpg jpg/standardized_text > /dev/null

	# create OCR output for the multi-page pdf test
	pdftoppm pdf/ocr_text.pdf /tmp/pdf-ocr-text
	for x in /tmp/pdf-ocr-text*; do \
		tesseract $$x $$(basename $$x .ppm) > /dev/null; \
	done
	cat pdf-ocr-text*.txt > pdf/ocr_text.txt
	rm -f pdf-ocr-text*
