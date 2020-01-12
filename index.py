from flask import Flask, request, render_template
import os
import subprocess
from random import randint
from markdown import markdown

class TestCase:

    def __init__(self, input, output):
        self._input = input
        self._output = output

    def isValid(self, output):
        return self._output == output

    def getInput(self):
        return self._input

    def getOutput(self):
        return self._output

class Problem:

    def __init__(self, statement, testCases):
        self._statement = statement
        self._testCases = testCases

    def getStatement(self):
        return self._statement

    def getTestCases(self):
        return self._testCases

problems = [
    Problem('A group of Bitcoin miners live in separate row houes in a community. ' +
        'Each one of them owns the same amount of Bitcoins, stored in their computer. ' +
        'A hacker learn this information and decides to steal from some of the miners.' +
        'The hacker does not steal from the computers of two adjacent houses, but only ' +
        'the alternative houses.\n\n'  +
        'Given the number of houses (H) and number of bitcoins (B) in each ' +
        'house, calculate the maximum bitcoins that a hacker can steal.\n\n' +
        'Input:  \n'
        '```\n' +
        '7 15\n' +
        '```  \n' +
        'Output:  \n' +
        '```\n' +
        '60\n' +
        '```\n',
        (
            TestCase('7 15\n', '60\n'),
            TestCase('3 10\n', '20\n'),
            TestCase('10 10\n', '50\n'),
        )
    )
]

def main():
    app = Flask(__name__)

    @app.route("/index", methods=[ 'GET' ])
    def index():
        index = randint(0, len(problems) - 1)
        problem = problems[index]
        statement = problem.getStatement()
        statementHTML = markdown(statement)
        return render_template('index.html', statement=statementHTML, index=index)

    @app.errorhandler(404)
    def pageNotFound(error):
        return render_template('404.html')

    @app.route('/submit', methods=[ 'POST' ])
    def submit():
        code = request.form['code']
        index = int(request.form['index'])

        file = open('temporary.py', 'w+')
        file.write(code)
        file.close()

        problem = problems[index]
        testCases = problem.getTestCases()

        incorrect = 0
        i = 0
        for testCase in testCases:
            print(f'Running test case { i + 1 }')
            i += 1

            inputStream, buffer = os.pipe()
            input = testCase.getInput()
            os.write(buffer, bytes(input, 'utf-8'))

            string = subprocess.check_output("./venv/bin/python3 temporary.py", stdin=inputStream, shell=True)
            output = string.decode('utf-8')

            print(f'Input:\n{input}')
            print(f'Output:\n{output}')

            os.close(inputStream)

            if not testCase.isValid(output):
                incorrect += 1

        result = f'test cases = { i }, correct = { i - incorrect }, incorrect = { incorrect }'
        return render_template('result.html', result=result)

    app.run(debug=True)

if __name__ == '__main__':
    main()