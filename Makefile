run:
	export FLASK_APP=app.py
	export FLASK_ENV=development
	raml2html doc.raml > templates/doc.html
	flask run
