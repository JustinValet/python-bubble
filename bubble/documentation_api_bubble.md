# Bubble .io API 

Author : Justin Valet 
Date : 28/10/2021
Topic: Python package to easily interact with the bubble.io data API 

Version: 1.0

Version 
1.x --> all functionnalities related to retrieve the date from the API 
2.x --> 1.x + push data to the API 


Expected arguments: 

* API_KEY: your Bubble.io api key 
* website: the website of you bubble site (eg:optimtri.com)
* 


This package was inspired from : 
* https://bubblegroup.gitbooks.io/bubble-manual/content/using-the-bubble-api/examples.html



```python 

# 1 - Store your API Key 

API_KEY = 'xxxx'

# 2 - constraint to retrieve only row which where created after 2021-10-01
# this variable could be null by putting ""
# the constraint is a list of dictionnaries which will be transformed as a json inside the class 
# see documentation: https://manual.bubble.io/core-resources/api/data-api

constraints = [{"key":"Created Date", "constraint_type":"greater than", "value":"2021-10-01T00:00:00Z"}]


# Put your API key as well as your constraints inside 
params = dict()
params["api_token"] = API_KEY
params["constraints"] = constraints

# 3 - call the class contructor of the BubbleApi class by passing as parameters: 
# url parameters 
# website 
# environment ("dev" or "prod")
# bubble object (i.e name of the target bubble table from bubble database) 
class_bubble = BubbleApi(params,"optimtri.com", "dev", "Collecte_order")

# 4 - Read all the data by calling the FullReadFromUrl method
# this is returning a json object
res = class_bubble.FullReadFromUrl()

# 5 - (if necessary) convert the json object to dataframe by calling the function ConvertToDataframe
res_dataframe = ConvertToDataframe(res)

```