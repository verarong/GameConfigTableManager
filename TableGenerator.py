import pymongo
import pandas as pd
import numpy as np
import json

MONGODB_URL = "XXXXXXXXXXX"
client = pymongo.MongoClient(MONGODB_URL)
db_mongo = client['infinity']


#对每个单元格的数据进行格式化，因为pandas默认数据类型为np，同时原excel表中空置空白等单元格
def trans(x):
    # print(type(x))
    if isinstance(x, np.int64):
        return int(x)
    if isinstance(x, np.float64):
        return float(x) if x % 1 > 0.001 else int(x)
    if isinstance(x, float):
        return float(x) if x % 1 > 0.001 else int(x)
    return x


def insert_items(config_list, collection_name, db):
    collection = db[collection_name]
    #版本号不同时，丢弃原collection
    collection.remove()
    json_ = []
    for config in config_list:
        # print(config, collection_name)
        config = {k: trans(v) for k, v in config.items()}
        json_.append(config)
        collection.update_one({"id": config["id"]}, {"$set": config}, upsert=True)
    #print(config_list, collection_name, json_)
    #生成json
    with open("json/{}.json".format(collection_name), 'w') as file_obj:
        json.dump(json_, file_obj, ensure_ascii=False)
    #生成各配置表类
    with open("json/class.txt", 'a') as file_obj:
        attributes = {"this." + k + "=obj." + k + ";": "public " + k + ": string;" if isinstance(v,
                                                                                                 str) else "public " + k + ": number;"
                      for k, v in json_[0].items()}
        class_str_list = []
        class_str_list.append("export class " + collection_name.capitalize() + "Data{ ")
        class_str_list.append("".join(attributes.values()))
        class_str_list.append("constructor(obj:any){")
        class_str_list.append("".join(attributes.keys()))
        class_str_list.append("}}\n\n")
        file_obj.write("".join(class_str_list))


def get_current_version():
    collection_list = db_mongo.list_collection_names()
    if "version" in collection_list:
        version = db_mongo["version"].find_one()
        if version:
            return version["version"]
    return 0


def generate_mongodb_configs():
    dfs = pd.read_excel('infinite.xlsx', sheet_name=None)
    print(dfs['version'].iloc[0, 1], get_current_version())
    if dfs['version'].iloc[0, 1] > get_current_version():  # undo update mongo_configs
        for collection_name, df in dfs.items():
            df = df.fillna(0)
            score = df.apply(dict, axis=1).tolist()
            insert_items(score, collection_name, db_mongo)
