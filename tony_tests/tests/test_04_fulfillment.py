from pathlib import Path
from sqlite3 import connect

import pandas
from rich.progress import Progress

from tony_tests.settings import FIXTURE_DIR
from tony_tests.tests.utils import import_solution

conn = connect(FIXTURE_DIR / "northwind.db")


def describe_order(order_id):
    return [tuple(order) for order in pandas.read_sql(
        """
        select ProductID, Quantity
        from "Order Details"
        where "Order Details".OrderID = ?
        order by ProductID, Quantity;
        """,
        conn,
        params=(order_id,)
    ).to_records(index=False)]


def test_describe_order():
    describe_order_solution = import_solution("fulfillment", "describe_order")
    order_ids = list(pandas.read_sql("select Orders.OrderID from Orders", conn)['OrderID'])
    with Progress() as progress:
        task1 = progress.add_task("[cyan]Testing [purple]describe_order", total=len(order_ids))
        for order_id in order_ids:
            assert sorted(describe_order_solution(order_id)) == sorted(describe_order(order_id))
            progress.update(task1, advance=1)


def test_create_manifest():
    create_manifest_solution = import_solution("fulfillment", "create_manifest")
    solution_destination = Path("/tmp") / "manifest.csv"
    create_manifest_solution(str(solution_destination))
    manifest = pandas.read_csv(solution_destination)
    assert 'order_id' in manifest.columns, f'Missing expected column order_id in output CSV.'
    assert 'product_id' in manifest.columns, f'Missing expected column product_id in output CSV.'
    assert 'quantity' in manifest.columns, f'Missing expected column quantity in output CSV.'

    order_ids = pandas.read_sql("select Orders.OrderID from Orders where ShippedDate is null", conn)['OrderID']
    with Progress() as progress:
        task1 = progress.add_task("[cyan]Testing [purple]create_manifest", total=len(order_ids))
        for order_id in order_ids:
            solution = manifest[manifest['order_id'] == order_id][['product_id', 'quantity']].to_records(index=False)
            desired = describe_order(order_id)
            assert len(solution) == len(desired), f"Solution order_id was expected to have {len(desired)} products; got {len(solution)}"
            for i, (product_id, quantity) in enumerate(solution):
                desired_prod_id, desired_sol_qty = desired[i]
                assert product_id == desired_prod_id, f"Unexpected product_id {product_id}"
                assert quantity == desired_sol_qty, f"Unexpected quantity for ({order_id=}, {product_id=}): {quantity=}"
                progress.update(task1, advance=1)
