all:
	cd src ; \
	zip ../BRREG-for-alfred.alfredworkflow . -r --exclude=*.DS_Store* --exclude=*.pyc*

clean:
	rm -f *.alfredworkflow
