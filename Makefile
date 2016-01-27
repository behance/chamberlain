default: install

install:
		pip install -r requirements.txt
		python setup.py install

ci-install:
		pip install -r requirements.txt -r test-requirements.txt

test: ci-install
		tox

docker-ci-test:
		docker build --tag behance/chamberlain-$$(git rev-parse HEAD) .
		docker run --rm --entrypoint make behance/chamberlain-$$(git rev-parse HEAD) test
		docker rmi -f behance/chamberlain-$$(git rev-parse HEAD)

docker-test:
		docker run --rm -v $$(pwd):/opt/chamberlain --workdir /opt/chamberlain python:2.7 make test

clean:
		rm -rf /usr/local/lib/**/site-packages/chamberlain
		rm -rf ./build chamberlain.egg-info
