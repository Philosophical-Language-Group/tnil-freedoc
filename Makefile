setup:
	mkdir -p docs/_generated/morpho
# graphics: setup
# 	./scripts/preview_graphics.sh ./graphics ./output
docs: setup
	./scripts/make_morpho_docs.py ./yaml/morpho ./docs/_generated/morpho
html:
	cd docs && make html
all: docs html
clean:
	rm -r docs/_generated
	cd docs && make clean
