setup:
	mkdir output
graphics: setup
	./src/preview_graphics.sh ./graphics ./output
clean:
	rm -r output
