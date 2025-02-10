_default:
  just --list

start-docker:
    docker compose up --build --force-recreate --watch

open:
    #!/usr/bin/env bash
    until curl --silent --fail http://localhost:5173 > /dev/null; do
        echo "Waiting for http://localhost:5173..."
        sleep 1
    done
    open http://localhost:5173

logs:
    docker compose logs -f

start: start-docker

stop:
    docker compose stop

clean-python:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type d -name "\.pytest_cache" -exec rm -rf {} +
    find . -type d -name "\.mypy_cache" -exec rm -rf {} +
    find . -type f -name "*.py[co]" -delete
    find . -type f -name ".DS_Store" -delete

clean-docker:
    docker compose down -v --rmi all --remove-orphans

clean-git:
    git fetch --prune
    git branch --merged | grep -v "^\*\|main" | xargs git branch -D
    git gc --aggressive

clean: clean-python clean-git
