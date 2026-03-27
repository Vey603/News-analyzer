
install:
	uv sync

run:
	uv pip install .
	platzi-news --log-level DEBUG search "tecnología" --source guardian
