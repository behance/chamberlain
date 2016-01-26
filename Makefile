default: install

install:
		pip install -r requirements.txt
		python setup.py install

ci-install:
		pip install virtualenv
		virtualenv -p /usr/bin/python2.7 .virtualenv
		.virtualenv/bin/pip install -r requirements.txt -r test-requirements.txt

test: ci-install
		.virtualenv/bin/tox

clean:
		rm -rf /usr/local/lib/**/site-packages/chamberlain
		rm -rf ./build chamberlain.egg-info
