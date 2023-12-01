# import pandas as pd
# import sys
from src.data_generation.generate_database import main

# sys.path.insert(0,'customer_deduplication/src/')


df = main(10, 5)
df['details'] = df.apply(lambda row: ' '.join(str(x).lower() if x is not None else '' for x in row), axis=1)

# Convert DataFrame to JSON
json_result = df.to_json(orient='records')


# To save the JSON to a file
with open('customer_details.json', 'w') as file:
    file.write(json_result)
