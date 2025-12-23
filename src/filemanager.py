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
		new_path = os.path.join(dirpath, f)
		print(f"new_path = {new_path}")
		if os.path.isdir(os.path.join(SRC_DIR, new_path)):
			os.mkdir(os.path.join(DST_DIR, new_path))
			copy_dir(new_path)
		else:
			src = os.path.join(src_dir, f)
			print(f"source: {src}")
			dst = os.path.join(dst_dir, f)
			print(f"destination: {dst}")
			shutil.copy(src, dst)
