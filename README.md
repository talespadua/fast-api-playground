# fast-api-playground
Repo where I will play with FastAPI a little bit


## How to run it:

Having docker and make installed, run the project with:  
`make raise-infrastructure`

With this, the server will run locally on port `8080`.

You can shutdown the server using  

`make shutdown-infrastructure`

## How to test it:

After raising the infrastructure, you can run the test using:
  
`make test`

If you want to run a specific test, you can run:
  
`make test-single test=<test_path>`
  
where `<test_path>` is the path for the test, module or folder you want to test

If you want to run the whole QA pipeline, you can use:
  
`make pipeline/qa`

This will run [Black](https://black.readthedocs.io/en/stable/), [Flake8](https://flake8.pycqa.org/en/latest/), [Mypy](http://mypy-lang.org/) (on strict mode) and also the whole test suite

## Where is the docs?

After running the server, the docs can be found either on `/docs` for Swagger or `/redoc` for Redoc. I would recommend Redoc though


