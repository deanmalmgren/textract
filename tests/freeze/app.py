import sys

import textract


def main():
    text = textract.process(sys.argv[1])
    sys.stdout.buffer.write(text)


if __name__ == "__main__":
    main()
