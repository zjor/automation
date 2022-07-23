import os
import sys
import subprocess
import datetime

default_lang = "ru"
work_dir = ".trans"


def ensure_directory():
	full_dir = os.path.expanduser(f"~/{work_dir}")
	if not os.path.exists(full_dir):
		os.makedirs(full_dir)


def log_word(word):
	filename = os.path.expanduser(f"~/{work_dir}/words.txt")
	with open(filename, 'a') as f:
		timestamp = datetime.datetime.now().isoformat()
		f.write(f"{timestamp}\t{word}\n")


def translate(word):
	subprocess.run(["trans", f":{default_lang}", word])		
