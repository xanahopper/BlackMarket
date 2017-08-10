WITH_ENV = env `cat .env 2>/dev/null | xargs`
PIP_INSTALL = pip3 --default-timeout=100 --retries=5 install
PIP_COMPILE = pip-compile

COMMANDS = help venv env install-deps compile-deps initdbs initsql initcache lint test apitest unitest clean lint fillup
.PHONY: $(COMMANDS)

help:
	@echo "commands: $(COMMANDS)"

venv:
	@[ -d venv ] || virtualenv -p python3 venv

env:
	@[ -e .env ] || cp .env.example .env

install-deps:
	@${PIP_INSTALL} --index-url=https://pypi.doubanio.com/simple -U pip
	@${PIP_INSTALL} -r requirements.txt

compile-deps:
	@${PIP_INSTALL} --index-url=https://pypi.doubanio.com/simple -U pip-tools
	@${PIP_COMPILE} requirements.in

initsql:
	@echo "[mysql] rebuilding tables"
	@$(WITH_ENV) python manage.py rebuild_sql -- -i
	@echo "OK"

initcache:
	@echo "[redis] flushing all caches"
	@$(WITH_ENV) python manage.py cleanup_redis
	@echo "OK"

initdbs: initsql initcache

lint:
	@echo "[lint] basic"
	@$(WITH_ENV) flake8
	@echo "[lint] complexity (warning only)"
	@$(WITH_ENV) flake8 --max-complexity=15 canal || true

clean:
	@find . -name '*.pyc' -type f -delete
	@find . -name '__pycache__' -type d -delete
	@find . -name '.DS_Store' -type f -delete
	@find . -type d -empty -delete

test: initsql unitest apitest

unitest:
	honcho run python manage.py init_database
	@$(WITH_ENV) python -m pytest tests/unitests

apitest: initsql
	@$(WITH_ENV) py.test tests/apitests

pip:
	@pip install -r requirements.txt --index-url=https://pypi.doubanio.com/simple

runserver:
	@$(WITH_ENV) python app.py

start:
	@honcho start &

stop:
	@sh scripts/stop_server.sh

show_pids:
	@ps ax | grep gunicorn

auto-deploy:
	@git fetch && git rebase && make stop && make start
