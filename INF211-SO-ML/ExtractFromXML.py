from lxml import etree
from nltk.corpus import stopwords

posts_xml_file = open("Posts.xml", "rb")
base_directory = "H:\Stackoverflow Database\MLData\\"
etree.XMLParser(recover=True)

def main():
    count = 0
    macount = 1000
    REQUIRED_TAG = "row"

    for event, elem in etree.iterparse(posts_xml_file, events=("start", "end")):
        if event == "end" and elem.tag == REQUIRED_TAG:
            if elem.get("PostTypeId") == "1":
                #print(elem.get("PostTypeId"))
                getElementDataAndStore(elem)
                count+=1
        if count > macount:
            break
    print(count)
    posts_xml_file.close()

def getElementDataAndStore(elem):
    id = elem.get("Id")
    with open(base_directory + id + ".txt", "w") as file:
        print(elem.get("Tags").encode('utf8'), file=file)
        print(elem.get("Title").encode('utf8'), file=file)
        print(elem.get("Body").encode('utf8'), file=file)

if __name__ == "__main__":
    main()


