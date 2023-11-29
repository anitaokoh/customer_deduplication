import faker
import re


fake = faker.Faker('de_DE')

def transform_phone_number(phone_number):
    """
    Transform a given phone number by applying specific replacements and removals.

    This function performs the following transformations on the input phone number:
    1. Replaces the sequence '+49(0)' with '00'.
    2. Removes any parentheses '()' and spaces from the phone number.

    Parameters:
    phone_number (str): The phone number string to be transformed.

    Returns:
    str: The transformed phone number with specified characters replaced or removed.
    """
    # Combined regex for replacing +49(0) with 00, removing brackets, and removing spaces
    return re.sub(r'\+49\(0\)|[()]|\s+|\+49', '', phone_number)

def generate_database(number):
    """
    Generates a list of dictionaries, each representing a simulated customer record.

    Parameters:
    number (int): The number of customer records to generate.

    Returns:
    list: A list of dictionaries where each dictionary contains details of a customer.
          Each dictionary has the following keys: 'Full Name', 'Email', 'Address', and 'Phone Number'.
          - 'Full Name' is a combination of a randomly generated first name and last name.
          - 'Email' is constructed using the full name in lowercase with spaces replaced by periods and a random free email domain appended.
          - 'Address' is a randomly generated address with newline characters replaced by spaces.
          - 'Phone Number' is a randomly generated phone number.
    """

    customer_list = []

    for _ in range(number):
        full_name = f"{fake.first_name()} {fake.last_name()}"
        email = re.sub(r'\s+', '.', full_name.lower()) + '@' + fake.free_email_domain()
        address = fake.address().replace("\n", " ")
        phone_number = transform_phone_number(fake.phone_number())


        customer_dict = {
          'Full Name': full_name,
          'Email': email,
          'Address': address,
          'Phone Number': phone_number
        }
        customer_list.append(customer_dict)
    return customer_list

if __name__ == '__main__':
    print(generate_database(1))
