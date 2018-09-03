# Homework 1: SQLite database of image analysis from Google Cloud Vision API
### Due: September 25, 2018
### Prof Michael Mandel `mim@sci.brooklyn.cuny.edu`

For this assignment, you will be interacting with a set of JSON documents in 
SQLite. The JSON documents are the output of the Google Cloud Vision API applied 
to images returned from a Flickr API query for interesting images related
to the text "New York".

I have provided starter code in python, but you may will write code in a language
of your choice (Python, Java, Bash, etc) to load the JSON into the database
and query it. You will submit your code, the output of your queries, and a brief
report describing your approach.

## Install and setup SQLite

SQLite is a light-weight SQL-compliant database that stores all of its data in a
single regular file.

1. Download and install the SQLite “Precompiled binaries” for your platform
   from https://www.sqlite.org/download.html
1. Download and install drives for SQLite in your programming language of
   choice. For python, apsw works well: https://rogerbinns.github.io/apsw/
   
## Introduction to the data

The file `exampleJson.txt` contains
a JSON document that has all of the fields that may be present in the
individual JSON documents. Note that this is not a valid JSON document
itself because in lists it only contains a single entry followed by "...". 
Although individual JSON documents may not contain all of these fields, if
they do, they will be in the structure shown in `exampleJson.txt`. The
entity-relationship diagram for the schema to be used in importing the 
data into SQLite is shown in the following figure:

![Entity-relationship diagram of JSON data](sql.png)

The annotations come from the Google Cloud Vision API and are described in
here https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate#AnnotateImageResponse .
I have only included the following subset of those annotations, however:

 * `landmarkAnnotations` -- identify geographical landmarks in photographs. 
   For the purposes of discussing entities in the database
   schema, this will add `Landmarks`, each of which can have zero or more
   `Locationss`.
 * `labelAnnotations` -- predict descriptive labels for images. This will
   add `Label` entities to the schema.
 * `webDetection` -- predict the presence of web entities (things with
   names) in images along with pages that contain the image and other
   images that are similar. This will add `WebEntity`, `Page`, and `Image`
   entities to the schema.
   
## Introduction to code   

All of the python code is contained in the file [`runSqlite.py`](https://github.com/cisc7610/homework1/blob/master/runSqlite.py).
If you have all of the necessary dependencies installed, you should be able to run the script as it is to 
complete very basic versions of each of the tasks that you will complete: 
 * Create the database schema
 * Populate the database
 * Query the database

If it is working, it should print out (among other things):
```
Query 7.0

    SELECT COUNT(*) FROM image;
    
    100
```

## Write code to create the database tables

Implement the missing TODO entries in the [`createSchema()`](https://github.com/cisc7610/homework1/blob/master/runSqlite.py#L21)
function.  The schema should follow the above entity-relationship diagram.

The meaning of most of the fields should be fairly clear, but there are two that need some explanation:
 * `isDocument` in the `image` table: This should be 1 if an image is the subject of an analysis 
    in the JSON file and 0 if an image only appears in the `webDetection` fields
 * `type` in the `image_matches_image` table: This should be either `"full"` if it appears in 
   `webDetection.fullMatchingImages` and `"partial"` if it appears in `webDetection.partialMatchingImages`


## Write code to import the data

Implement the missing TODO entries in the [`insertImage` method](https://github.com/cisc7610/homework1/blob/master/runSqlite.py#L53)
function.  `insertImage()` is called with the JSON from the analysis of a single image by Google Cloud Vision API.
The `json` module imports it so that JSON dictionaries become python dictionaries, and JSON lists become python lists.

You may want to use the helper function [`getOrCreateRow()`](https://github.com/cisc7610/homework1/blob/master/runSqlite.py#L74).
This function returns the ID of a tuple with the attributes provided in a dictionary.  If such a tuple exists, it is returned,
if it does not exist, it is created.  This will ensure that you do not duplicate entries like `Labels` and `WebEntities`.


## Write code to query the database

Implement the missing TODO entries in the [`querySqlite()`](https://github.com/cisc7610/homework1/blob/master/runSqlite.py#L104) function.
You should use the supplied [`querySqliteAndPrintResults()`](https://github.com/cisc7610/homework1/blob/master/runSqlite.py#L173) function
to query the database.  The queries should be as follows:
 1. Count the total number of JSON documents in the database
 2. Count the total number of Images, Labels, Landmarks,
    Locations, Logos, Pages, and WebEntity:s in the database.
 3. List all of the Images that are associated with the
    Label with an id of "/m/015kr" (which has the description
    "bridge") ordered alphabetically by URL
 4. List the 10 most frequent WebEntitys that are applied
    to the same Images as the Label with an id of "/m/015kr" (which
    has the description "bridge"). Order them by the number of times
    they appear followed by their entityId alphabetically
 5. Find Images associated with Landmarks that are not
    "New York" (id "/m/059rby") or "New York City" (id "/m/02nd_")
    ordered by image URL alphabetically.
 6. List the 10 Labels that have been applied to the most
    Images along with the number of Images each has been applied to
 7. List the 50 Images that are linked to the most Pages
    through the webEntities.pagesWithMatchingImages JSON property
    along with the number of Pages linked to each one.
 8. List the 10 pairs of Images that appear on the most
    Pages together through the webEntities.pagesWithMatchingImages
    JSON property. Order them by the number of pages that they
    appear on together, then by the URL of the first. Make sure that
    each pair is only listed once regardless of which is first and
    which is second.
    

## Update this file with a description of your approach and code (here)

 1. Describe the language that you implemented your code in
 2. Include instructions for how to run your code to populate the database
    and to query the database
 3. Paste the results from each of the queries
 4. Describe any problems that you ran into in the course of this project
