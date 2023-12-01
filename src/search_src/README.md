# Adding Vector Search Functionality and Record Linkage Logic for customer details Deduplication

This folder handles the following functionalites
- `create_superduperdb.py`:  To upload data into Mongodb, add vector search functionality to mongoDb and listening to incoming data using `superduperdb`
- `similartity_result.py`: To receive the vector similarity of the input query and then use the results to further find the highest similarity result using record linkage
