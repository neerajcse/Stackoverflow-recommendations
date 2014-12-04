from TextsDAO import TextsDAO
import numpy
import json

DB = "stackoverflow-posts.db"
BASE_DIR = "."
BASE_META_DIR = "."
TAG_TO_ID_DICT = {}
PID_TO_TAGS_LIST = []
TAG_COUNT = 0

def main():
    texts = TextsDAO(BASE_META_DIR, DB, get_tags=True)
    count = 0
    for id,tags in texts:
        #print("For {} Tags{}".format(id, tags))
        tag_list = []
        for tag in tags:
            tag_list.append(findInDictionary(tag))
        PID_TO_TAGS_LIST.append(tag_list)    
        count += 1
    print("{}".format(PID_TO_TAGS_LIST))
    print("{}".format(TAG_TO_ID_DICT))
    nparray = numpy.array(PID_TO_TAGS_LIST)
    numpy.save("doc_to_tag.npy", nparray)
    with open("tag_to_id.dict", "w") as f:
        f.write(json.dumps(TAG_TO_ID_DICT))
    texts.close()

def findInDictionary(tag):
    global TAG_COUNT
    if tag in TAG_TO_ID_DICT:
        return TAG_TO_ID_DICT.get(tag)
    else:
        TAG_TO_ID_DICT[tag] = TAG_COUNT
        print("Inserting tag " + tag + " with id " + str(TAG_COUNT))
        TAG_COUNT+=1
        return TAG_TO_ID_DICT[tag]


if __name__ == "__main__":
    main()