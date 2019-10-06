setup:
	mkdir -p output
	mkdir -p docs/morphology
graphics: setup
	./scripts/preview_graphics.sh ./graphics ./output
docs: setup
	./scripts/make_morpho_docs.py ./yaml/morphology ./docs/morphology
clean:
	rm -r output
	rm -r docs/morphology
