# Got an exciting offer for you bro
We need to make sure you are comfortable reading and processing files.
You'll be combining data from multiple different 
sources and generating reports for people to consume 
literally all the time.


> Ah! Those ghouls down in the IT basement have really screwed us big time.
We finally got around to looking at that user roster they generated a while
back, but the names and email addresses are in two separate files. 
How are we supposed to personalize our mass marketing emails 
if we don't have their names to fill into the template?

> Anyway, that one IT guy is at a funeral or whatever so do you think you 
could put the names and emails into one file? Excel kept crashing when
I tried it.
-------------------------------------

Write a function called `marketing` that takes three arguments
and returns nothing. The function signature looks
something like this:

```python
def marketing(email_file, name_file, destination):
    . . . # some code
    with open(destination, 'w') as w:
        w.write(destination)
    return
```

You can see example input and output files if you run:
```bash
tony fixtures 03
```