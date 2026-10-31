.PHONY: run test lint clean

run:
        python -m src.main

test:
        pytest tests/ -v

lint:
        flake8 src/ tests/ --max-line-length=120
        pylint src/ --disable=C0111,C0103,R0913,R0914,W0611,W0613,R0902,R0903,R0801,W0718,C0415 --max-line-length=120 --init-hook="import sys; sys.path.insert(0, '.')"

clean:
        rm -f app.log
        rm -rf .pytest_cache
	    find . -type d -name __pycache__ -exec rm -rf {} +