.PHONY: clean

clean:
	find . -name "*.pyc" -type f -delete
	find . -name __pycache__ -type d -exec rm -rf {} 2> /dev/null +
	find . -name "*.egg-info" -type d -exec rm -rf {} 2> /dev/null +
	find . -type d -empty -delete
