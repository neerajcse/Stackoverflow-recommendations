from lxml import etree
from StackOverflowSqlite import StackOverflowSqlite
import time

posts_xml_file = open("/home/deep/Stackoverflow/Stackoverflow-recommendations/Data/Posts.xml", "rb")
base_directory = "~/Stackoverflow/Stackoverflow-recommendations/Data/"
etree.XMLParser(recover=True)

DB = "stackoverflow-posts.db"
SQLITE = StackOverflowSqlite(DB)

def main():
    posts_count = 0
    end_tags_count = 0
    maxcount = 10
    processed_count = 524409
    #524409
    REQUIRED_TAG = "row"
    for event, elem in etree.iterparse(posts_xml_file, events=("start", "end")):
        if (event == "end" and elem.tag == REQUIRED_TAG):
            if elem.get("PostTypeId") == "1":
                if posts_count > processed_count:
                    getElementDataAndStore(elem)
                posts_count+=1
                if posts_count % 1000 == 0:
                        print(str(posts_count) + "::" + str(end_tags_count))
            time.sleep(0.01)
        end_tags_count+=1
    print("Total tags processed " + str(end_tags_count))
    print("Total posts processed " + str(posts_count))
    posts_xml_file.close()
    SQLITE.close()

def getElementDataAndStore(elem):
    id = elem.get("Id")
    postObject = {}
    postObject["id"] = elem.get("Id")
    postObject["tags"] =  elem.get("Tags").encode('utf8')
    postObject["title"]  = elem.get("Title").encode('utf8')
    postObject["content"] = elem.get("Body").encode('utf8')
    SQLITE.commit(postObject)  
    time.sleep(0.05)

if __name__ == "__main__":
    main()