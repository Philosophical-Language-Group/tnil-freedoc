setup:
	mkdir -p output
graphics: setup
	./scripts/preview_graphics.sh ./graphics ./output
clean:
	rm -r output
