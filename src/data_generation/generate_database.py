import pandas as pd
import faker
import random
from src.data_generation.anomalies_data import create_typo_in_full_name, create_typo_in_email, create_typo_in_address
from src.data_generation.general_data import generate_database, transform_phone_number

fake = faker.Faker('de_DE')
# random.seed(0)

def handlers(item, data):
    """
    Processes a given item type by applying an appropriate modification function.

    This function uses a mapping to relate each item type (such as 'Full Name', 'Email', etc.) to a specific function that modifies the item's data. For 'Phone Number', an identity function is used, which returns the data as is.

    Parameters:
    item (str): The type of item to be processed (e.g., 'Full Name', 'Email', 'Address', 'Phone Number').
    data (dict): A dictionary containing the data associated with the item.

    Returns:
    The modified data after applying the corresponding function, or the original data if no specific function is mapped to the item type.
    """
    # Mapping of item types to their respective functions
    function_map = {
        'Full Name': create_typo_in_full_name,
        'Email': create_typo_in_email,
        'Address': create_typo_in_address,
        'Phone Number': lambda x: x  # Identity function for 'Phone Number'
    }

    handler_function = function_map.get(item, lambda x: x)  # Default to identity function if item is not found
    return handler_function(data[item])

def backfill(item):
    """
    Selectively fills or empties data for a given item type.

    The function randomly decides to either 'empty' (return None) or 'fill' (generate data) for a specified item type. If 'fill' is chosen, it generates appropriate data based on the item type using predefined Faker functions.

    Parameters:
    item (str): The type of item to be processed, such as 'Full Name', 'Email', 'Address', or 'Phone Number'.

    Returns:
    The generated data for the item if the action is 'fill', or None if the action is 'empty'. If the item type is not recognized, it also returns None.
    """
    action = random.choice(['empty', 'fill'])

    if action == 'empty':
        return None

    data_generation_map = {
        'Full Name': lambda: fake.first_name() + ' ' + fake.last_name(),
        'Email': fake.email,
        'Address': lambda: fake.address().replace("\n", " "),
        'Phone Number': lambda: transform_phone_number(fake.phone_number())
    }
    # Get the corresponding data generation function and call it
    return data_generation_map.get(item, lambda: None)()

def regeneration(dataset, number):
    """
    Generates a new dataset by randomly modifying or backfilling selected items from a sample of an existing dataset.

    The function creates a sample from the given dataset and then, for each row in the sample, it:
    - Randomly selects a subset of items (columns).
    - Applies modifications to these selected items using the handlers function.
    - Backfills the non-selected items using the backfill function.

    Parameters:
    dataset (DataFrame): A pandas DataFrame representing the original dataset from which to sample.
    number (int): The number of entries to sample from the dataset and the size of the new dataset to be generated.

    Returns:
    list: A list of dictionaries, where each dictionary represents a modified row from the original dataset.
          Each dictionary contains keys corresponding to the columns of the original dataset.
    """

    df_sample = dataset.sample(number).reset_index(drop=True)
    col_list = list(df_sample.columns)
    db = []

    for _ in range(number):
        # Randomly select a row from the dataset
        info = dict(df_sample.iloc[random.randint(0, len(df_sample)-1)])
        new_info = {}

        # Randomly decide how many items to select (1, 2, or 3) and select them
        selected_items = random.sample(col_list, random.choice([1, 2, 3]))

        # Update new_info for selected items
        for item in selected_items:
            new_info[item] = handlers(item, info)

        # Update new_info for items not selected
        for item in set(col_list) - set(selected_items):
            new_info[item] = backfill(item)

        db.append(new_info)

    return db

def main(maindb_number, anomalies_number):
    """
    Generates a combined DataFrame consisting of a main database and a regenerated database with anomalies.

    This function first creates a main database of customer records using the 'generate_database' function. It then creates another dataset with anomalies using the 'regeneration' function. Both datasets are combined into a single DataFrame.

    Parameters:
    maindb_number (int): The number of records to generate for the main database.
    anomalies_number (int): The number of records to generate with anomalies for the regenerated database.

    Returns:
    DataFrame: A pandas DataFrame containing the combined records from both the main and regenerated datasets.
    """
    df = pd.DataFrame(generate_database(maindb_number))
    db = regeneration(df, anomalies_number)
    df = pd.concat([df, pd.DataFrame(db)], ignore_index=True)
    return df

if __name__ == '__main__':
    print(main(1, 1))
