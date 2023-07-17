test:
	PYTHONPATH=. pytest tests

clean:
	find . -type f -name "*.pyc" -o -name "*~"  | xargs rm -f
	find . -type d -name "__pycache__" | xargs rm -fr
	rm -fr nfhc.egg-info

release: clean
	rm -fr dist
	python3 setup.py sdist
	echo twine upload --repository scarfer --verbose  dist/*

