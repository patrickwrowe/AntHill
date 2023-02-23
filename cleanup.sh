find . -name "*.py" | xargs black
find . -name "*.py" | xargs isort --profile black
