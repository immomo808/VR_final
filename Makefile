all:
	gcc -o ./frame_processor frame_processor.c
	python video.py
template:
	g++ -o ./frame_processor template.cpp
	python video.py
