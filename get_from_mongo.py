import pymongo


def get_from_mongo():
    client = pymongo.MongoClient(
        "mongodb+srv://iNeurontest:iNeurontest@ineuron.be6of.mongodb.net/?retryWrites=true&w=majority"
    )
    my_db = client.ineuronscrapper
    coll1 = my_db["WebScrapper"]
    if coll1.count_documents({}) <= 0:
        return [
            [
                "No Data Found.",
                "No Data Found.",
                "No Data Found.",
                "No Data Found.",
                "No Data Found.",
            ]
        ]
    else:
        cursor = coll1.find({}, {"_id": 0})
        result_list = []
        for content in cursor:
            buff_list = []
            for key, value in content.items():
                buff_list.append(key)
                try:
                    buff_list.append(value["Category"])
                except:
                    buff_list.append("None")
                buff_list.append(value["Description"])
                buff_list.append(value["Price"])
                sub_buff_list = []
                try:
                    for instructor, _ in value["Instructor(s)"].items():
                        sub_buff_list.append(instructor)
                except:
                    sub_buff_list.append("None")
            buff_list.append(sub_buff_list)
            result_list.append(buff_list)
        return result_list
