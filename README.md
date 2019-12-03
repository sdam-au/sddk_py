# sddk
This is a simple package to upload data to- and dowload data from sciencedata.dk. It is especially designed for working with group folders. It relies mainly on Python requests library.

Main functionality is uploading any python object (dict, list, dataframe) as json file to a preselected group folder and getting it back as the original python object.

### Install and import

So far the package is in a testing PyPi repository [here](https://test.pypi.org/project/sddk/). 

To install and import the package within your Python environment (i.e. jupyter notebook) run:

```
!pip install --index-url https://test.pypi.org/simple/ --no-deps sddk
import sddk
```

### Configure session and url to access your group folder 

To run the main configuration function below, you have to know the following:
* your sciencedata.dk username (e.g. "123456@au.dk"),
* your sciencedata.dk password (has to be previously configured in the sciencedata.dk web interface),
* name of the group folder you want to access,
* and, in the case you are not owner of the group, username of the group owner.
(You will be asked to input these values interactively while running the function)

```
s, sciencedata_groupurl = sddk.configure_session_and_url()
```

### Usage

Upload (export) simple text file:
```
s.put(sciencedata_groupurl + testfile.txt, data="textfile content")
```

Get it back (import) tp python:

```
string_testfile = s.get(sciencedata_groupurl + testfile.txt).content
print(string_testfile)
```

It works well with pickles and jsons (to be documented).

### Next steps
To develop our own functions:

* `sddk.export_json(sciencedata_groupurl + "jsonfile.json", json_object)`
* `json_object = sddk.import_json(sciencedata_groupurl + "jsonfile.json")`


The package is built following [this](https://packaging.python.org/tutorials/packaging-projects/) tutorial.



