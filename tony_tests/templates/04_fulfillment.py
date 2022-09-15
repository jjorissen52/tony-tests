from sqlite3 import connect

from typing import Tuple, List
from tony_tests.settings import FIXTURE_DIR

conn = connect(FIXTURE_DIR / "northwind.db")


def describe_order(order_id: int) -> List[Tuple[int, int]]:
    """
    Given an order_id, return a list of the corresponding
    product_ids and quantities enumerated in the Order Details table.

    Real Example:
        sorted(describe_order(10248)) == sorted([(11, 12), (42, 10), (72, 5)])

    :param order_id: integer OrderID
    :return: [
      (product_id, quantity),
      . . .,
    ]
    """
    # . . .
    return []


def create_manifest(destination: str):
    """
    Writes the CSV manifest file to the given destination.
    :param destination:
    :return:
    """


if __name__ == '__main__':
    print(describe_order(10248))
    assert sorted(describe_order(10248)) == sorted([(11, 12), (42, 10), (72, 5)])
