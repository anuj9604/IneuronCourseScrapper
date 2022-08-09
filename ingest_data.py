import data_scrapper
import pymongo


def insert_data():
    client = pymongo.MongoClient(
        "mongodb+srv://iNeurontest:iNeurontest@ineuron.be6of.mongodb.net/?retryWrites=true&w=majority"
    )
    my_db = client.ineuronscrapper
    coll1 = my_db["WebScrapper"]
    if coll1.count_documents({}) > 0:
        return "Database is already there!"
    else:
        sorted_data = data_scrapper.structured_course_data(
            data_scrapper.get_raw_courses("https://ineuron.ai/courses")
        )
        coll1.insert_many(sorted_data)
        return "Data inserted successfully!"
