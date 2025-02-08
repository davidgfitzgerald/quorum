_default:
  just --list

# Pass args such as -d through start
start extra_args='':
    docker compose up --build --force-recreate {{extra_args}}

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
