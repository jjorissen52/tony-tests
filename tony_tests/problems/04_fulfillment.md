# Manifest Destiny
Well, the warehouse is having technical issues again... 
Unfortunately, the computer that we use tell us what items to pull from the shelves
for order fulfillment is on the fritz. I need you to create a manifest file
that lets us box up all the items needed to fulfill a particular order.

Basically, we need a CSV file with the following headers: 
- order_id
- product_id
- quantity

of orders that haven't been fulfilled yet.

I have made a sqlite database available on your machine. For now, the only tables you need to worry about
are Orders and Order Details. You'll  be able to tell that an order hasn't shipped yet because Orders.ShippedDate
will be NULL for that order. Here's a simplified example of those tables:

### Orders

```csv
OrderID,ShippedDate
123,NULL
124,NULL
125,2022-09-15
```

### Order Details

```csv
OrderID,ProductID,Quantity
123,700,3
123,100,7
134,115,7
125,134,2
```

Your generated manifest should then look like this:
### Manifest

```csv
order_id,product_id,quantity
123,700,3
123,100,7
134,115,7
```


---------------------------------------
 Your solution file should have two functions, and the behavior of both of those functions will be subject 
 to testing. 
- `describe_order`: when provided with an order_id, returns a list of product_ids and quantities
  - Each row in the Order Details table with the given OrderID should be represented as an item in the list
- `create_manifest`: when provided with a destination file path, writes the full manifest CSV file to that destination
  - You can run `tony fixtures 04` to locate an example manifest file which has the first two orders listed correctly.
 
When you run `tony start 04`, the function signatures and explanations will be included in the generated solution
file, so you should look there for more details. 
