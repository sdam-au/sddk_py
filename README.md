# sddk

This is a simple Python package to upload data to- and dowload data from [sciencedata.dk](https://sciencedata.dk/). It is especially designed for working with group folders. It relies mainly on Python requests library.

sciencedata.dk is a project managed by [DEiC](https://www.deic.dk) (Danish e-infrastrcture cooperation) aimed to offer a robust data storage, data management and data publication solution for researchers in Denmark and abroad (see [docs](https://sciencedata.dk/sites/user/) and [dev](https://sciencedata.dk/sites/developer/) for more info). The storage is accessible either through (1)  the web interface, (2) WebDAV clients or (3) an API relaying on HTTP Protocol (see [docs](https://sciencedata.dk/sites/user/) and [dev](https://sciencedata.dk/sites/developer/) for more info). One of the strength of sciencedata.dk is that it currently supports institutional login from 2976 research and educational institutions around the global (using [WAYF](https://www.wayf.dk/en/about)). That makes it a perfect tool for international research collaboration. 

The main functionality of the package is in uploading any Python object (dict, list, dataframe) as a text or json file to a preselected shared folder and getting it back into a Python environemnt as the original Python object. It uses sciencedata.dk API in combination with Python requests library.

### Install and import

So far the package is in a testing PyPi repository [here](https://test.pypi.org/project/sddk/). 

To install and import the package within your Python environment (i.e. jupyter notebook) run:

```
!pip install --index-url https://test.pypi.org/simple/ --no-deps sddk
import sddk
```

### Configure session and access endpoint for a shared folder

To run the main configuration function below, you have to know the following:
* your sciencedata.dk username (e.g. "123456@au.dk" or "kase@zcu.cz"),
* your sciencedata.dk password (has to be previously configured in the sciencedata.dk web interface),

In the case you want to access a shared folder, you further need:

* **name** of the shared folder you want to access (e.g. "our_shared_folder"),

* shared folder owner's username** (if it is not yours)

(Do not worry, you will be asked to input these values interactively while running the function)

To configure a personal session, run:
```python
s, sddk_url = sddk.configure_session_and_url()
```
To configure a session pointing to a shared folder, run:
```python
s, sddk_url = sddk.configure_session_and_url("our_shared_folder")
```
Running this function, you configurate two key variables:
* `s`: a request session authorized by your username and password
* `sddk_url`: default url address (endpoint) for your request 
Below you can inspect how these two are used in typical request commands

### Usage

##### String to TXT

Upload (export) simple text file:

```python
s.put(sddk_url + "testfile.txt", data="textfile content")
```

Get it back (import) to Python:

```python
string_testfile = ast.literal_eval(s.get(sddk_url + "testfile.txt").text)
print(string_testfile)
```

##### Pandas DataFrame to JSON

Upload a dataframe as a json file:

```python
import pandas as pd
df = pd.DataFrame([("a1", "b1", "c1"), ("a2", "b2", "c2")], columns=["a", "b", "c"]) 
s.put(sddk_url + "df.json", data=df.to_json())
```

Get it back:

```python
df = pd.DataFrame(s.get(sc_groupurl + "df.json").json())
```

##### Pandas DataFrame to CSV

```python
import pandas as pd
df = pd.DataFrame([("a1", "b1", "c1"), ("a2", "b2", "c2")], columns=["a", "b", "c"]) 
df.to_csv("df.csv") ### temporal file
s.put(sddk_url + "df.csv", data = open("df.csv", 'rb'))
```

##### Dictionary to JSON

To sciencedata.dk:

```python
dict_object = {"a" : 1, "b" : 2, "c":3 }
s.put(sddk_url + "dict_file.json", data=json.dumps(dict_object))
```

From sciencedata.dk:

```python
dict_object = json.loads(s.get(sddk_url + "dirgot_data/dict_file.json").content)
```

##### Matplotlib figure to PNG

```python
import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot(range(10))
fig.savefig('temp.png', dpi=fig.dpi) ### works even in Google colab
s.put(sddk_url + "temp.png", data = open("temp.png", 'rb'))
```

### Next steps
- to develop our own functions for uploading files and getting them back (asking in case of already existing files, etc.:

```python
def file_from_object(file_name_and_loc, python_object):
  if s.get(sciencedata_groupurl + file_name_and_loc).ok: ### if there already is a file with the same name
    new_name = input("file with name \"" + file_name_and_loc.rpartition("/")[2] + "\" already exists in given location. Press Enter to overwrite it or enter a different name (without path)")
    if len(new_name) == 0:
      s.put(sciencedata_groupurl + file_name_and_loc, data=json.dumps(python_object))
    else:
      if "/" in new_name: ### if it is a path
        s.put(sciencedata_groupurl + new_name, data=json.dumps(python_object))
      else: 
        s.put(sciencedata_groupurl + file_name_and_loc.rpartition("/")[0] + new_name, data=json.dumps(python_object))
  else:
    s.put(sciencedata_groupurl + file_name_and_loc, data=json.dumps(python_object))

def object_from_file(file_name_and_loc):
  if s.get(sciencedata_groupurl + file_name_and_loc).ok:
    print("file exists")
    try: 
      return json.loads(s.get(sciencedata_groupurl + file_name_and_loc).content) ### if there already is a file with the same name
    except:
      print("file import failed")
  else:
    print("file does not found; check file name and path.")
```


The package is built following [this](https://packaging.python.org/tutorials/packaging-projects/) tutorial.

### Versions history

* 0.0.6 - first functional configuration
* 0.0.7 - configuration of individual session by default
* 0.0.8 - shared folders reading&writing for ordinary users finally functional
