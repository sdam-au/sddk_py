# sddk
This is a simple package upload data to and dowload data from sciencedata.dk. It is especially designed for working with group folders. It relies mainly on requests library.

Main functionality is uploading any python object (dict, list, dataframe) as json file to a preselected group folder and getting it back as the original python object.

## configure session and url to access your group folder 

'''
sciencedata_groupurl = configure_session_and_url()

'''

The package is built following [this](https://packaging.python.org/tutorials/packaging-projects/) tutorial.



