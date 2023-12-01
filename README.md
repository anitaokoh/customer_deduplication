# Building a Customer Deduplication Interface WebApp

### Problem statement:
A lot of customers create duplicate accounts. This results to the databases filled with both `True new customers` and `False new customers`. In turn , leading to customers being eligible to **new customer incentives** more than once , resulting to financial losses for the company.

One obvious way to solve this is by using heuristic rules to match and block all  existing customers with every new entry to decide, in **Real-time**, if the "new customer" is eligible for new customer incentive or not.

Deciding the rule is one issue and then deciding how much block-size to use can be computationally expensive

### Solution:
One better solution is to use semantic search to narrow the results returned for example _return only the 5 nearest neighbors_ Then, use heuristic rules to match the five results with the new entry as a way to rerank the score to reduce false positive similarities.

This is what is achieved in this repo and is demostrated in the below video
![video](images/customer_dedup.gif)

### Tools used
- **Mongodb** : For OLTP Database (check the `src/search_src` folder)
- **SuperDuperDB** : To add the vector functionality to MongoDB (Check the `src/search_src` folder)
- **Steamlit**: Frontend UI (Check the `app.py` file)

### Other Tools / Libraries are
- **Faker and Random** : To generate the customer detail data stored in the database (check the `src/data_generation` folder)
