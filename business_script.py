#! C:/Users/ekjot/anaconda3/python.exe

print ("Content-Type: text/html; charset=utf-8\n\n");


#!/usr/bin/env python
# coding: utf-8

# # Welcome to pystardog
# 
# Press the Restart & Run All button to run all the cells in this notebook and view the output.

# In[13]:

import webbrowser
import random
import io
import stardog
import uuid
# import pandas as pd
# import seaborn as sns

# Connect with HTML

# In[25]:


import cgi


# In[26]:


form = cgi.FieldStorage()


# In[ ]:

# extracting data from the web interface
formType = form.getvalue("form_name") 
if formType=="school":
    schoolType=form.getvalue("schooltype")
    schoolType = str(schoolType)
if formType=="misc":
    services=form.getvalue("servicetype")
if formType=="restaurant":
    mealTypes = form.getvalue("mealtype")
    mealTypes = str(mealTypes)
    isVegFood = form.getvalue("vegfood")
if formType=="restaurant" or formType=="misc":
    avgPriceVal = form.getvalue("price")
name = form.getvalue("name__")
location = form.getvalue("location")    
latitude = form.getvalue("latitude")
longitude = form.getvalue("longitude")
phone = form.getvalue("phone")
address = form.getvalue("address")
landmark = form.getvalue("landmark")


# ## Specify Stardog connection details

# In[14]:


connection_details = {
  'endpoint': 'http://localhost:5820',
  'username': 'admin',
  'password': 'admin'
}


# ## Create a new database in Stardog
# 
# Drop the database if it already exists.

# In[15]:


database_name = 'integration_testing'


# creating database if it doesn't exists
# with stardog.Admin(**connection_details) as admin:
#     if database_name in [db.name for db in admin.databases()]:
#         admin.database(database_name).drop()
#     db = admin.new_database(database_name)


# ## Connect to the Stardog database

# In[16]:


conn = stardog.Connection(database_name, **connection_details)


# ## Load the sample data
# ### Start a transaction

# In[17]:


conn.begin()


# ### Add the database schema and data
# 
# Download the files to the same directory as this notebook.
# 
# [Schema](https://github.com/stardog-union/stardog-tutorials/raw/master/music/music_schema.ttl)
# 
# [Data](https://github.com/stardog-union/stardog-tutorials/raw/master/music/music.ttl.gz)

# In[18]:


# conn.add(stardog.content.File('dummy_dataset.ttl'))


# In[20]:


conn.commit() # commit the transaction


# ## Query the database
# 
# This query returns the date the album was released for each album in the database.

# In[20]:

query = """
PREFIX res: <http://api.stardog.comrestaurant#> 
PREFIX rC: <http://api.stardog.comrestaurant> 
PREFIX sch: <http://api.stardog.comschool#> 
PREFIX sC: <http://api.stardog.comschool>  
PREFIX mis: <http://api.stardog.comMiscServices#> 
PREFIX mC: <http://api.stardog.comMiscServices> 

INSERT DATA   {
"""


# In[22]:


#res_number=random.randrange(20,500,1)
#sch_number=random.randrange(501,1000,1)
#mis_number=random.randrange(1001,1500,1)

# In[23]:

if formType=="restaurant": #price vegfood meal
    query = query + "\nres:" + str(uuid.uuid1()) + " a rC: ;\n\t:hasPrice    " + str(avgPriceVal) + " ;\n\t:hasVegFood " + isVegFood + ";\n\t:hasMealType \"" + mealTypes + "\" ;"

elif formType=="school": #school type

    query = query + "\nsch:" + str(uuid.uuid1()) + " a sC: ;\n\t:hasschoolType \"" + schoolType + "\" ;\n"

else:#price service

    query = query + "\nmis:" + str(uuid.uuid1()) + " a mC: ;\n\t:hasPrice    " + str(avgPriceVal) + " ;\n\t:hasService \"" + services + "\" ;\n"

# In[24]:


query = query + "\t:hasLocation \"" + location + "\" ;\n" + "\t:hasLandmark \"" + landmark + "\" ;\n" + "\t:hasName \"" + name + "\" ;\n" + "\t:hasAddress \"" + address + "\" ;\n" + "\t:hasLatitude " + str(latitude) + " ;\n" + "\t:hasLongitude " + str(longitude) + " ;\n" + "\t:hasPhone " + str(phone) + " .\n}"


# In[25]:


# print (query)


# In[21]:


csv_results = conn.update(query)


# ### Clean up the connection
# 
# Normally you would use a `with statement` similar to line 3.

# In[24]:


conn.__exit__()




queryHTML = query.replace("<","&lt;");
queryHTML = queryHTML.replace(">","&gt;");
queryHTML = queryHTML.replace("\n","<br>")
queryHTML = queryHTML.replace("\t","&nbsp;&nbsp;&nbsp;&nbsp;")

# webbrowser.open('http://localhost/python/businessQuery.html', new = 0)




print("""<html>
            <head>
                <!-- Required meta tags -->
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">

                <!-- Bootstrap CSS -->
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
                    integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
                <script src="https://code.jquery.com/jquery-3.6.0.min.js"
                    integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>


                <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
                <script src="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"></script>
                <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>


                <link rel="stylesheet" href="style.css">

                <title>Query Generated</title>
            </head>
            <body>
                <div class="card text-center">
                    <div class="card-header ">
                    <ul class="nav nav-tabs card-header-tabs ">
                        <li class="nav-item">
                        <a class="nav-link active" aria-current="true" href="#">Customer</a>
                        </li>
                        <li class="nav-item">
                        <a class="nav-link" href="index.html">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="business.html">Business Registration</a>
                        </li>

                    </ul>
                    </div>
                    <div class="card-body ">
                    <span>
                        <h2> Result</h2>
                        <button type="button" class="btn btn-outline-success align-items-md-center disabled">Success</button>
                    </span>
                    </div>
                </div>


                <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Query generated from the form data!</h5>
                    <code class = "align-items-md-left line-height: 80%;">""" + queryHTML+"""</code>
                    <br><br>
                </div>
                </div>

            </body>
            </html>""");
