# WEFEDemand
TBD
## Get started


## Code linting

1. Create a virtual environment and install the dev dependencies with

        pip install -r requirements/dev.txt

2. Install the pre-commit hooks with

        pre-commit install

   This will mainly make sure you can't commit if your code is not linted with black.
   The pre-commit hook will check if your code is linted and if it is not it will simply lint it for you, you then only need to stage the changes made by the linter and commit again, as simple as that :)
