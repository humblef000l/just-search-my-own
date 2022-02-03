#! C:/Users/ekjot/anaconda3/python.exe

print ("Content-Type: text/html; charset=utf-8\n\n");

# In[13]:


import io
import stardog
import pandas as pd
import webbrowser
import sys
# import json2table
# import json

# Connect with HTML

# In[25]:


import cgi


# In[26]:


form = cgi.FieldStorage()


# In[ ]:


formType = form.getvalue("form_name") 

if formType=="school":
    schoolType=form.getvalue("schooltype")
    schoolType = schoolType.lower()
    
elif formType=="misc":
    services=form.getvalue("servicetype")
    if services is not None:
        services = services.lower()
    
elif formType=="restaurant":
    mealTypes = form.getvalue("mealtype")
    mealTypes = mealTypes.lower()
    isVegFood = form.getvalue("vegfood")
    isVegFood = isVegFood.lower()
else:
    print("incorrect form type\n")
    exit()
    
if formType=="restaurant" or formType=="misc":
    minprice = form.getvalue("minprice")
    maxprice = form.getvalue("maxprice")
    
location = form.getvalue("location")
if location is not None:
    location = location.lower()    
landmark = form.getvalue("landmark")
if landmark is not None:
    landmark = landmark.lower()


#print("fetched the data from the form")

# ## Specify Stardog connection details
# In[14]:


connection_details = {
  'endpoint': 'http://localhost:5820',
  'username': 'admin',
  'password': 'admin'
}


# ## Database in Stardog

# In[15]:


database_name = 'integration_testing'


# ## Connect to the Stardog database

# In[16]:


conn = stardog.Connection(database_name, **connection_details)


# ## Load the sample data
# ### Start a transaction

# In[17]:


conn.begin()


# In[20]:


#conn.commit() # commit the transaction

#print("Established the connection with the database")

# ## Query the database


# In[119]:


query = """
PREFIX res: <http://api.stardog.comrestaurant#> 
PREFIX rC: <http://api.stardog.comrestaurant> 
PREFIX sch: <http://api.stardog.comschool#> 
PREFIX sC: <http://api.stardog.comschool>  
PREFIX mis: <http://api.stardog.comMiscServices#> 
PREFIX mC: <http://api.stardog.comMiscServices> 

SELECT (?name as ?NAME) (?phone as ?PHONE) (?address as ?ADDRESS)

WHERE   {  
"""


# In[ ]:

#print("Before forming the query")
if formType=="restaurant":

    query = query + "\n?s a rC: .\n"
    
    if maxprice is not None and minprice is None:
        query =query + "\n\t?s :hasPrice ?price .\n\tFILTER(?price<=" + str(maxprice) + ") .\n"
    elif maxprice is not None and minprice is not None:
        query =query + "\n\t?s :hasPrice ?price .\n\tFILTER(?price<=" + str(maxprice) + " && ?price>=" + str(minprice) +") .\n"
    elif maxprice is None and minprice is not None:
        query =query + "\n\t?s :hasPrice ?price .\n\tFILTER(?price>=" + str(minprice) + ") .\n"
            
    if isVegFood=="true":
        query = query + "\n \t?s :hasVegFood true .\n"
    elif isVegFood=="false":
        query = query + "\n \t?s :hasVegFood false .\n"
    query = query + "\n\t?s :hasMealType ?meals ." + "\n FILTER(contains(?meals,\""+mealTypes+"\")) .\n"
    
    # query = query + "\n\t?s    :hasMealType \"" + mealTypes + "\" .\n"+"\n\tFILTER(contains(?mealTypes,"+mealTypes"\") .\n"

elif formType=="school":
    query = query + "\n?s a sC: .\n"
    
    if schoolType !="":
        query = query + " ?s :hasschoolType  ?schoolType . " + "\nFILTER(regex(?schoolType," + "\"" + schoolType + "\"," + "\"i\")) .\n"

else:
    query = query + "\n?s a mC: .\n"
    
    if maxprice is not None and minprice is None:
        query =query + "\n\t?s :hasPrice ?price .\n\tFILTER(?price<=" + str(maxprice) + ") .\n"
    elif maxprice is not None and minprice is not None:
        query =query + "\n\t?s :hasPrice ?price .\n\tFILTER(?price<=" + str(maxprice) + " && ?price>=" + str(minprice) +") .\n"
    elif maxprice is None and minprice is not None:
        query =query + "\n\t?s :hasPrice ?price .\n\tFILTER(?price>=" + str(minprice) + ") .\n"
    
    if services is not None:
        query = query + " \t?s :hasService  ?service . " + "\n\tFILTER(regex(?service," + "\"" + services + "\"," + "\"i\")) .\n"


# In[121]:

#print("location")
if location is not None:
    query = query + " \t?s :hasLocation  ?location . " + "\n\tFILTER(regex(?location," + "\"" + location + "\"," + "\"i\")) ."


# In[122]:

#print("before landmark")
if landmark is not None:
    query = query + "\n \t?s :hasLandmark  ?landmark . " + "\n\tFILTER(regex(?landmark," + "\"" + landmark + "\"," + "\"i\")) ."


# In[127]:

#print("Just after forming the query")
query = query + "\n ?s :hasName ?name ;\n\t:hasPhone ?phone ;\n\t:hasAddress ?address .\n} LIMIT 50"

# print(query)
# In[128]:


#print (query)


# In[21]:
# print("<TITLE>CGI script output</TITLE>")
# print("<H1>This is my first CGI script</H1>")
# print("Hello, world!")

csv_results = conn.select(query, content_type='text/csv')
#csv_results = conn.select(query)
# print(csv_results)
df = pd.read_csv(io.BytesIO(csv_results))
# resultTable=df.to_html(classes='table table-hover thead-dark table-bordered table-responsive-md text-left ' id = 'dataTable')
resultTable = df.to_html(classes = 'table table-hover table-bordered text-left back" id = "dataTable')
# print(resultTable)


# ### Clean up the connection

# In[24]:


conn.__exit__()



queryHTML = query.replace("<","&lt;");
queryHTML = queryHTML.replace(">","&gt;");
queryHTML = queryHTML.replace("\n","<br>")
queryHTML = queryHTML.replace("\t","&nbsp;&nbsp;&nbsp;&nbsp;")
# print(queryHTML)
output = """
    <html>
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

                <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.4/css/jquery.dataTables.css">
  
                <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.11.4/js/jquery.dataTables.js"></script>

                <link rel="stylesheet" href="style.css">

                <title>Output</title>

                <script>
                    $(document).ready( function () {
                        $('#dataTable').DataTable();
                    } );

                </script>

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
                </div>


                <div class="card">
                <div class="card-body">
                    <h5 class="card-title">The genrated query is </h5>
                    <code class = "align-items-md-left line-height: 80%;">""" + queryHTML+"""</code>
                    <br><br>
                </div>
                <h4 class = "text-center"> SEARCH RESULTS </h4>
                </div>
                """+resultTable + """


            </body>
            </html>

"""
print(output)



# infoFromJson = csv_results
# build_direction = "LEFT_TO_RIGHT"
# table_attributes = {"style": "width:100%"}
# print(json2table.convert(infoFromJson, 
#                          build_direction=build_direction, 
#                          table_attributes=table_attributes))