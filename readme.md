# Fetch Rewards code assessment solution

If Python 3.7+ along with Pip are not installed on your machine, please install them.

If you wish to use a virtual environment, navigate via terminal to the cloned directory and issue the following command into the terminal to create a virtual environment named venv:
`virtualenv venv`

Issue `source venv/bin/activate` to activate the virtual environment. 

Use the following command to install dependencies:
`python -m pip install -r requirements.txt`

Run the application server with the following command:
`python app.py`

In a new terminal tab, navigate back to the directory if necessary, and test the application by running the test script. First issue `chmod +x test`, then `./test`.

The test script uses cURL to make HTTP requests to the server running on localhost at port 5000, and utilizes the test case from the code assessment page. Expected json output is:
```
...

DEDUCTIONS:
[{"company": "DANNON", "value": -100, "time": 1607111046}, {"company": "UNILEVER", "value": -200, "time": 1607111046}, {"company": "MILLER COORS", "value": -4700, "time": 1607111046}]

POINTS OVERVIEW:
{"DANNON": {"points": 1000}, "UNILEVER": {"points": 0}, "MILLER COORS": {"points": 5300}}
```
