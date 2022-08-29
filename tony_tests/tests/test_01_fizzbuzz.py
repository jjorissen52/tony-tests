from tony_tests.tests.utils import import_solution

fizzbuzz = import_solution("fizzbuzz")


def test_fizzbuzz():
    n = 10000
    result = fizzbuzz(n)
    for i in range(n):
        item = result[i]
        if i % 15 == 0:
            assert item == "FizzBuzz"
        elif i % 3 == 0:
            assert item == "Fizz"
        elif i % 5 == 0:
            assert item == "Buzz"
        else:
            assert item == i
