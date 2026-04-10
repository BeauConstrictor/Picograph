flash:
	rm -rf .staging
	mkdir .staging
	rsync -av --exclude='.git' --exclude='__pycache__' ./ .staging/
	- mpremote fs rm -r :/
	mpremote fs cp -r .staging/* :/
	rm -rf .staging
