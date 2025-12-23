import shutil
import os

SRC_DIR = "./static"
DST_DIR = "./public"

def copy_static_to_public():
	clear_public()
	copy_dir("")

def clear_public():
	try:
		shutil.rmtree(DST_DIR)
	except FileNotFoundError:
		# We don't care if it doesn't exist
		pass
	os.mkdir(DST_DIR)


def copy_dir(dirpath):
	src_dir = os.path.join(SRC_DIR, dirpath)
	dst_dir = os.path.join(DST_DIR, dirpath)
	files = os.listdir(src_dir)
	for f in files:
		if os.path.isdir(f):
			new_path = os.path.join(dirpath, f)
			copy_dir(new_path)
		else:
			src = os.path.join(src_dir, f)
			dst = os.path.join(dst_dir, f)
			shutil.copy(src, dst)
