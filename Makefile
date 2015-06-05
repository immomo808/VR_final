all:
	gcc -o ./frame_processor frame_processor.c
	python video.py
