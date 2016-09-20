clean:
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name ".DS_Store" -exec rm -rf {} \;
	@find . -name "__pycache__" | xargs rm -rf;

lint:
	@sh scripts/check_lint.sh

pip:
	@pip install -r requirements.txt

start:
	@honcho start

stop:
	@sh scripts/stop_server.sh

show_pids:
	@ps ax |grep gunicorn
