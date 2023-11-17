import faker
import re

fake = faker.Faker('de_DE')

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
        phone_number = fake.phone_number()


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
