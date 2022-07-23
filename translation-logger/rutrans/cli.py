import sys
from .rutrans import ensure_directory, log_word, translate


def main():
	if len(sys.argv) < 1:
		print("Usage: rutrans <word_or_phrase>")
		sys.exit(1)

	ensure_directory()

	word = sys.argv[1]
	log_word(word)
	translate(word)


if __name__ == "__main__":
	main()
