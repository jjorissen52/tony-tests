import random
from pathlib import Path

import pandas
import numpy
from english_words import english_words_alpha_set

from tony_tests.tests.utils import import_solution

marketing = import_solution("marketing")


def test_marketing():
    n = 100_000
    ids = numpy.arange(0, n, dtype=int)
    first_names = random.choices(list(english_words_alpha_set), k=n)
    last_names = random.choices(list(english_words_alpha_set), k=n)
    names = [f"{fname} {lname}" for fname, lname in zip(first_names, last_names)]
    domains = random.choices(list(english_words_alpha_set), k=n)
    tlds = random.choices(["com", "net", "org", "us", "biz", "butts", "io"], k=n)
    emails = [f'{fname[0]}.{lname}@{domain}.{tld}'
              for fname, lname, domain, tld in zip(first_names, last_names, domains, tlds)]

    DIR = Path("/tmp")
    names_location = DIR / "names.csv"
    emails_location = DIR / "emails.csv"
    destination = DIR / "output.csv"

    names_df = pandas.DataFrame(dict(ID=ids, Name=names))
    emails_df = pandas.DataFrame(dict(ID=ids, Email=emails))

    names_df.to_csv(names_location, index=False)
    emails_df.to_csv(emails_location, index=False)
    marketing(str(names_location), str(emails_location), str(destination))
    solution = {r["ID"]: r for r in names_df.merge(emails_df, on=["ID"]).to_dict("records")}
    output = {r["ID"]: r for r in pandas.read_csv(destination).to_dict("records")}

    for key in solution:
        assert solution[key] == output[key]

