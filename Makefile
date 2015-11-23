.PHONY: lint shell publish tag deb

export PYTHONDONTWRITEBYTECODE=1
export SQLALCHEMY_DATABASE_URI==postgresql+psycopg2://

lint:
	-bin/pylint --rcfile=.pylintrc -f colorized -r no *.py models web

shell:
	bin/python

run:
	bin/python -m web
