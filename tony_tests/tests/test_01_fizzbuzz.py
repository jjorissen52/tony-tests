from tony_tests.tests.utils import import_solution

fizzbuzz = import_solution("fizzbuzz")


def test_fizzbuzz():
    result = fizzbuzz(10000)
    for i, item in enumerate(result):
        if i % 15 == 0:
            assert item == "FizzBuzz"
        elif i % 3 == 0:
            assert item == "Fizz"
        elif i % 5 == 0:
            assert item == "Buzz"
        else:
            assert item == i
