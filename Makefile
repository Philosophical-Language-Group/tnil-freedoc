setup:
	mkdir -p docs/_generated/morphology
# graphics: setup
# 	./scripts/preview_graphics.sh ./graphics ./output
docs: setup
	./scripts/make_morpho_docs.py ./yaml/morphology ./docs/_generated/morphology
html:
	cd docs && make html
all: docs html
clean:
	rm -r docs/_generated
	cd docs && make clean
