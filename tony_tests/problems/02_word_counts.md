# Dictionaries, words, etc...
It's very important in python to be comfortable and familiar with `dict`s, and the goal of this
problem is for you to demonstrate just that.

--------------------

We want to count how many times each word appears in the given file. A "word" is any string
of alphanumeric characters surrounded on all sides by one or more whitespace characters (including
the first or last words in the file). The counts should be case-insensitive, and all output word-counts 
should be lowercase.

Write a program that:
1. Takes a single string as input
2. Counts all "words"
3. Returns a dictionary corresponding to the counts

## Example:
String:
```
the big brown fox jumped over THE lazy dog
```
Solution:
```json
{
  "dog": 1,
  "over": 1,
  "fox": 1,
  "quick": 1,
  "brown": 1,
  "the": 2,
  "jumped": 1,
  "lazy": 1
}
```