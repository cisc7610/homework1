#!/usr/bin/python3

"""Insert data into a sqlite database and query it.
"""

import apsw
import glob
import json
import os.path

dataDir = "data/"
jsonDir = os.path.join(dataDir, "json")
dbFile = os.path.join(dataDir, 'sqlite.db')

def main():
    createSchema(dbFile)
    populateSqlite(jsonDir, dbFile)
    querySqlite(dbFile)


def createSchema(dbFile, clearDb=True):
    "Create necessary tables in the sqlite database"
    
    connection = apsw.Connection(dbFile)
    cursor = connection.cursor()

    # Create image table
    if clearDb:
        cursor.execute("DROP TABLE IF EXISTS image;")
    cursor.execute("CREATE TABLE image (id integer PRIMARY KEY, "
                   "url varchar(256), isDocument int(1));")

    # TODO: create label table

    # TODO: create page table

    # TODO: create landmark table

    # TODO: create location table

    # TODO: create webEntity table

    # TODO: create image_tagged_label table

    # TODO: create image_in_page table

    # TODO: create image_matches_image table

    # TODO: create image_contains_landmark table

    # TODO: create image_tagged_webEntity table

    # TODO: create landmark_located_at_location table
    
    
def populateSqlite(jsonDir, dbFile):
    "Load the JSON results from google into sqlite. Assumes schema already created."

    connection = apsw.Connection(dbFile)
    cursor = connection.cursor()

    loaded = 0
    for jsonFile in glob.glob(os.path.join(jsonDir, '*.json')):
        print("Loading", jsonFile, "into sqlite")
        with open(jsonFile) as jf:
            jsonData = json.load(jf)
            insertImage(cursor, jsonData)
            loaded += 1

    connection.close()

    print("\nLoaded", loaded, "JSON documents into Sqlite\n")


def insertImage(cursor, jsonData):
    imageId = getOrCreateRow(cursor, 'image', {'url': jsonData['url']})
    print(imageId)

    # TODO: update isDocument attribute of image

    # TODO: process labelAnnotations field

    # TODO: process webDetection.fullMatchingImages field
    
    # TODO: process webDetection.partialMatchingImages field
    
    # TODO: process webDetection.pagesWithMatchingImages field
    
    # TODO: process webDetection.webEntities field
    
    # TODO: process landmarkAnnotations field

    # TODO: process landmarkAnnotations.locations field


def getOrCreateRow(cursor, table, dataDict):
    """Return the ID of a row of the given table with the given data.

    If the row does not already exists then create it first.  Existence is
    determined by matching on all supplied values.  Table is name of table,
    dataDict is a dict of {'attribute': value} pairs.
    """

    whereClauses = ["`{}` = :{}".format(k,k) for k in dataDict]
    select = "select id from {} where {}".format(table, " and ".join(whereClauses))
    # print(select)

    cursor.execute(select, dataDict)
    res = cursor.fetchone()
    if res is not None:
        return res[0]

    fields = ",".join("`{}`".format(k) for k in dataDict)
    values = ",".join(":{}".format(k) for k in dataDict)
    insert = "insert into {} ({}) values({})".format(table, fields, values)
    # print(insert)
    cursor.execute(insert, dataDict)

    cursor.execute(select, dataDict)
    res = cursor.fetchone()
    if res is not None:
        return res[0]
    raise Exception("Something went wrong with " + str(dataDict))


def querySqlite(dbFile):
    "Run necessary queries and print results"
    
    connection = apsw.Connection(dbFile)
    cursor = connection.cursor()

    # 0. Count the total number of images in the database
    query_0 = """
    SELECT COUNT(*) FROM image;
    """
    querySqliteAndPrintResults(query_0, cursor, title="Query 0")
    
    # TODO: 1. Count the total number of JSON documents in the database
    query_1 = """
    """
    querySqliteAndPrintResults(query_1, cursor, title="Query 1")

    # TODO: 2. Count the total number of Images, Labels, Landmarks,
    # Locations, Pages, and WebEntity's in the database.
    query_2 = """
    """
    querySqliteAndPrintResults(query_2, cursor, title="Query 2")

    # TODO: 3. List all of the Images that are associated with the
    # Label with an id of "/m/015kr" (which has the description
    # "bridge") ordered by the score of the association between them
    # from highest to lowest
    query_3 = """
    """
    querySqliteAndPrintResults(query_3, cursor, title="Query 3")

    # TODO: 4. List the 10 most frequent WebEntitys that are applied
    # to the same Images as the Label with an id of "/m/015kr" (which
    # has the description "bridge"). List them in descending order of
    # the number of times they appear, followed by their entityId
    # alphabetically
    query_4 = """
    """
    querySqliteAndPrintResults(query_4, cursor, title="Query 4")

    # TODO: 5. Find Images associated with Landmarks that are not "New
    # York" (id "/m/059rby") or "New York City" (id "/m/02nd ")
    # ordered alphabetically by landmark description and then by image
    # URL.
    query_5 = """
    """
    querySqliteAndPrintResults(query_5, cursor, title="Query 5")

    # TODO: 6. List the 10 Labels that have been applied to the most
    # Images along with the number of Images each has been applied to
    query_6 = """
    """
    querySqliteAndPrintResults(query_6, cursor, title="Query 6")

    # TODO: 7. List the 10 Pages that are linked to the most Images
    # through the webEntities.pagesWithMatchingImages JSON property
    # along with the number of Images linked to each one. Sort them by
    # count (descending) and then by page URL.
    query_7 = """
    """
    querySqliteAndPrintResults(query_7, cursor, title="Query 7")

    # TODO: 8. List the 10 pairs of Images that appear on the most
    # Pages together through the webEntities.pagesWithMatchingImages
    # JSON property. List them in descending order of the number of
    # pages that they appear on together, then by the URL of the
    # first. Make sure that each pair is only listed once regardless
    # of which is first and which is second.
    query_8 = """
    """
    querySqliteAndPrintResults(query_8, cursor, title="Query 8")


def querySqliteAndPrintResults(query, cursor, title="Running query:"):
    print()
    print(title)
    print(query)

    for record in cursor.execute(query):
        print(" " * 4, end="")
        print("\t".join([str(f) for f in record]))


if __name__ == '__main__':
    main()
