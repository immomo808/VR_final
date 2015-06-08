all:
	g++ -o ./frame_processor template.cpp
	python video.py
test:
	gcc -o ./frame_processor frame_processor.c
	python video.py
