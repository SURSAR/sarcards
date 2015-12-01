.PHONY: lint shell publish tag deb

export PYTHONDONTWRITEBYTECODE=1

lint: lib/python3.4/site-packages/
	bin/pylint --load-plugins=pylint_flask --rcfile=.pylintrc -f colorized -r no *.py models web

bin/pip:
	virtualenv -p python3 .

lib/python3.4/site-packages/sarcards-*.egg-info/PKG-INFO: setup.py | bin/pip
	./setup.py install_egg_info
	rm -Rf sarcards.egg-info/

lib/python3.4/site-packages/: lib/python3.4/site-packages/sarcards-*.egg-info/PKG-INFO
	bin/pip install sarcards[dev]
	touch $@

shell:
	bin/python

run:
	bin/python -m web

db:
	./mkdb.py
