import pandas
from pathlib import Path
from tony_tests.settings import FIXTURE_DIR


def marketing(email_file, name_file, destination):

    # . . .

    with open(destination, 'w') as w:
        w.write("file contents")
    return


if __name__ == '__main__':
    marketing_fixtures = FIXTURE_DIR / "03_marketing"
    output_path = Path("/tmp") / "tony_marketing_output.csv"
    marketing(
        marketing_fixtures / "emails.csv",
        marketing_fixtures / "names.csv",
        output_path,
    )
    print(pandas.read_csv(output_path))
