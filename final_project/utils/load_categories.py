import pandas as pd

from game.models import Category


def load_categories(file):
    """
    This function reads data from an Excel file containing categories and their codes, then creates and saves
    Category objects in the database using the data read.

    Args:
    - file: A file object representing the Excel file to read data from.

    Returns:
    - None
    """
    Category.objects.all().delete()
    df = pd.read_excel(file, sheet_name='Sheet1')
    data = df.iloc[:, 0].tolist()
    for i in range(len(data)):
        cat = Category.objects.create(
            name=df.iloc[i, 2],
            code=df.iloc[i, 0]
        )
        cat.save()
