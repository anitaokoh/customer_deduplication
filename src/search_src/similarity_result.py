# import os
# import json
import pandas as pd
import recordlinkage
# from bson import ObjectId
# from dotenv import load_dotenv
from superduperdb import Document
from src.search_src.create_superduperdb import search_functionality

# # Load environment variables from .env file
# load_dotenv()

# # Access the variables
# mongodb_uri = os.getenv("MONGODB_URI")
# artifact_store = os.getenv("ARTIFACT_STORE")
# collection_name = os.getenv("COLLECTION_NAME")
# chunk_file = os.getenv("CHUNK_FILE")

# # open the json file
# with open(chunk_file) as f:
#     chunks = json.load(f)



# @st.cache_resource
def get_nearest_similarity(chunks, mongodb_uri, artifact_store, search_term, n=5):
    """
    Retrieves the most similar documents to a given search term from a MongoDB collection.

    This function connects to a MongoDB database and performs a similarity search on a specified collection.
    It returns the top 'n' documents that are most similar to the provided search term, based on the details field.

    Parameters:
    chunks (int): Number of chunks to process (used in search_functionality).
    mongodb_uri (str): MongoDB connection URI.
    artifact_store (str): Path to the artifact store.
    search_term (str): The term to search for in the document collection.
    n (int, optional): Number of top similar documents to return. Defaults to 5.

    Returns:
    list: A list of documents (in dict format) that are most similar to the search term.
    """

    # Initialize the search functionality with the given parameters
    db, collection, model = search_functionality(chunks, mongodb_uri, artifact_store)

    # Execute the similarity search on the collection
    result = db.execute(
        collection
        .like(Document({'details': search_term}), vector_index=f'pymongo-docs-{model.identifier}', n=n)
        .find({}, {'Full Name': 1, 'Email': 1, 'Address': 1, 'Phone Number': 1, 'details': 1, 'score': 1, '_id': 1})
    )

    return result


# @st.cache_data
def get_record_linkage(target_df, chunks, mongodb_uri, artifact_store, search_term, n=5, method='jarowinkler', threshold=0.85):
    """
    Finds and sorts database records that closely match the search term using record linkage and similarity scoring.

    Parameters:
    - target_df (DataFrame): The target DataFrame to match against.
    - chunks (int): Number of chunks to divide the data for processing.
    - MONGODB_URI (str): MongoDB connection URI.
    - artifact_store (str): Path or URI to the artifact store.
    - search_term (str): The search term or phrase to use for matching records.
    - n (int): Number of nearest similarity results to retrieve. Default is 5.
    - method (str): The string comparison method to use. Default is 'jarowinkler'.
    - threshold (float): The threshold for string comparison. Default is 0.85.

    Returns:
    DataFrame: A sorted DataFrame of records from the comparison database that closely match the search criteria.
              Sorted by the 'score' field in descending order.
    """
    # Fetch nearest similarity results
    nearest_results = get_nearest_similarity(chunks, mongodb_uri, artifact_store, search_term, n=n)

    # Unpack results and create a comparison DataFrame
    comparison_data = [result.unpack() for result in nearest_results]
    comparison_df = pd.DataFrame(comparison_data).set_index('_id')

    # Create an indexer for record linkage
    indexer = recordlinkage.Index()
    indexer.full()
    pairs = indexer.index(target_df, comparison_df)

    # Setup comparison criteria
    compare = recordlinkage.Compare()
    compare.exact('Phone Number', 'Phone Number', label='Phone Number')
    compare.string('Full Name', 'Full Name', method=method, threshold=threshold, label='Full Name')
    compare.string("Email", "Email", method=method, threshold=threshold, label="Email")
    compare.string("Address", "Address", method=method, threshold=threshold, label="Address")

    # Compute similarity features
    similarity_features = compare.compute(pairs, target_df, comparison_df)
    similarity_columns = ['Phone Number', 'Full Name', 'Email', 'Address']
    similarity_features['similarity_sum'] = similarity_features[similarity_columns].sum(axis=1)
    similarity_features =  similarity_features.reset_index()

    # Filter results based on similarity sum
    # features = features.reset_index()
    similar_ids = similarity_features[similarity_features['similarity_sum'] >= 1.0]['_id_2'].tolist()
    filtered_df = comparison_df.loc[similar_ids]

    # Sort by score and return
    return filtered_df.sort_values(by='score', ascending=False)





# if __name__ == '__main__':
#     search_term = 'gesche herr g.herrmann@web.de  42130 neubrandenburg'
#     target_df = pd.DataFrame([{'Full Name': 'Gesche herr',
#   'Email': 'g.herrmann@web.de',
#   'Address':'42130 neubrandenburg',
#   'Phone Number': None,
#   '_id': '12344556667788'
#   }]).set_index('_id')
#     result = get_record_linkage(target_df, chunks, mongodb_uri, artifact_store, search_term , n=5)
#     print(result)
