# Creating Customer details synthetically

This folder recreates customer data synthetically using [Faker Library](https://faker.readthedocs.io/en/master/fakerclass.html) and using domain knowledge to mimic real-life customers details discrepancies.

It is mainly focused on 4 customer details
- Full name
- Email
- Address
- Phone number

It takes into account
- Typos
- Omission of data
- Swap of first names and last names
- Irregular input of phone number and addresses

Find more info about the domain knowledge [here](https://medium.com/data-de-mystified/creating-dataset-sythnetically-thought-process-8a0fd7fa90e6)


There are four main code files in this directory
- `general_data.py` : Handles the creation of the initial customer base
- `anomalies_data.py` : Handles the creation of new customer data that are similar to some customers data in the customer base
- `generate_database.py`: Handles the merging of the initial customer base and the new customer data being produced
- `generate_df.py`: To run the `generate_database.py` file, generate the customer details and save in a json file
