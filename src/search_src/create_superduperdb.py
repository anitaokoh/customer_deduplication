# import json
import sentence_transformers
from superduperdb import Document
from superduperdb import superduper
from superduperdb import Model, vector
from superduperdb import Listener, VectorIndex
from superduperdb.backends.mongodb import Collection


# MONGODB_URI = "mongomock://test"
# artifact_store = 'filesystem://./data/'


# collection_name = 'customer_details'

# with open('customer_details.json') as f:
#     chunks = json.load(f)


def model_definition():
    """
    Defines and returns a sentence transformer model for use in vector search functionality.

    This function creates a sentence transformer model which is used for embedding text data.
    The model is configured with specific settings suitable for encoding and processing text data.

    Returns:
    Model: A sentence transformer model configured for text encoding and processing.
    """
    model = Model(
        identifier='all-MiniLM-L6-v2',
        object=sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2'),
        encoder=vector(shape=(384,)),
        predict_method='encode', # Specify the prediction method
        postprocess=lambda x: x.tolist(),  # Define postprocessing function
        batch_predict=True, # Generate predictions for a set of observations all at once
    )
    return model


def create_database(data, mongodb_uri, artifact_filepath):
    """
    Creates a database and collection, then stores provided data.

    This function initializes a MongoDB database and a collection based on the provided MongoDB URI and artifact filepath.
    It then stores the given data in the newly created collection.

    Parameters:
    data (list): A list of dictionaries representing the data to be stored in the database.
    mongodb_uri (str): MongoDB connection URI for the database.
    artifact_filepath (str): Filepath for storing database artifacts, such as indexes.

    Returns:
    tuple: A tuple containing the database instance and the created collection.
    """
    # Initialize the database with the given URI and artifact store path
    db = superduper(mongodb_uri, artifact_store=artifact_filepath)

    # Create a collection for storing the data
    collection = Collection('customer_details')

    # Insert the data into the collection
    db.execute(collection.insert_many([Document(r) for r in data]))

    return db, collection



def search_functionality(data, mongodb_uri, artifact_filepath):
    """
    Configures and initializes a MongoDB database with vector search functionality.

    This function creates a MongoDB database and a collection, then adds a vector search index to the collection.
    The vector search is based on a sentence transformer model, which is used to compute vector embeddings of the documents.

    Parameters:
    data (list): A list of dictionaries representing the data to be stored in the database.
    mongodb_uri (str): MongoDB connection URI.
    artifact_filepath (str): Filepath for storing artifacts.

    Returns:
    tuple: A tuple containing the database instance, the collection, and the model used for embedding.
    """
    # Create the database and collection and store the data
    db, collection = create_database(data, mongodb_uri, artifact_filepath)

    # Define the model for embedding
    model = model_definition()

    # Add a vector index to the collection for vector search functionality
    db.add(
        VectorIndex(
            identifier=f'pymongo-docs-{model.identifier}',
            indexing_listener=Listener(
                select=collection.find(),
                key='details',
                model=model,
                predict_kwargs={'max_chunk_size': 1000},
            ),
        )
    )
    return db, collection, model


# if __name__ == '__main__':
#     db, collection, model = search_functionality(chunks, MONGODB_URI, artifact_store)
#     r = db.execute(collection.find_one())
#     print(r.unpack())
