# sddk

This is a Python package for writting and reading files to/from [sciencedata.dk](https://sciencedata.dk/). It is especially designed for working with shared folders. It relies mainly upon Python requests library.

sciencedata.dk is a project managed by [DEiC](https://www.deic.dk) (Danish e-infrastrcture cooperation) aimed to offer a robust data storage, data management and data publication solution for researchers in Denmark and abroad (see [docs](https://sciencedata.dk/sites/user/) and [dev](https://sciencedata.dk/sites/developer/) for more info). The storage is accessible either through (1)  the web interface, (2) WebDAV clients or (3) an API relaying on HTTP Protocol. One of the strength of sciencedata.dk is that it currently supports institutional login from 2976 research and educational institutions around the globe (using [WAYF](https://www.wayf.dk/en/about)). That makes it a perfect tool for international research collaboration. 

The main functionality of the package is in uploading any Python object (str, dict, list, dataframe or figure) as a file to a preselected personal or shared folder and getting it back into Python as the original Python object. It uses sciencedata.dk API in combination with Python requests library.

## Requirements

* requests
* pandas
* matplotlib
* getpass
* BeautifulSoup
* pyarrow >= 17.0

## Install and import

To install and import the package within your Python environment (i.e. a jupyter notebook) run:

```python
!pip install sddk # to be updated, use flag "--ignore-installed"
import sddk ### import all functions
```

## Session configuration

To run the main configuration function below, you have to know the following:
* your sciencedata.dk username (e.g. "123456@au.dk" or "kase@zcu.cz"),
* your sciencedata.dk password (has to be previously configured in the sciencedata.dk web interface),

In the case you want to access a shared folder, you further need:

* **name** of the shared folder you want to access (e.g. "our_shared_folder"),

* **username** of the owner of the folder (if it is not yours)

(Do not worry, you will be asked to input these values interactively while running the function)

To configure a personal session, run:
```python
conf = sddk.configure()
```

## Configuration with root in shared folder

To configure a session pointing to a shared folder, run:

```python
conf = sddk.configure("our_shared_folder", "owner_username@au.dk")
```
Running this function, you configure a tuple varible `conf`, containing two objects:
* `s`: a request session authorized by your username and password
* `sddk_url`: default url address (endpoint) for your requests

`conf` is later on used as input for `write_file()` and `read_file()`.

## write_file()

The most important components of the package are two functions: `write_file(path_and_filename, python_object, conf)` and `read_file(path_and_filename, type_of_object, conf)`. 

So far these functions can be used with several different types of Python objects: `str`, `list`, `dictionary`, pandas' `dataframe` and matplotlib's `figure`. These can be written either as `.txt`, `.json` or `.png` files, based simply upon the filename's ending chosen by the user. Here are simple instances of these python objects to play with:

```python
### Python "str" object
string_object =  "string content"
### Python "list" object
list_object = ['a', 'b', 'c', 'd']
### Python "dictionary" object
dict_object = {"a" : 1, "b" : 2, "c":3 }
### Pandas dataframe object
import pandas as pd
dataframe_object = pd.DataFrame([("a1", "b1", "c1"), ("a2", "b2", "c2")], columns=["a", "b", "c"]) 
### Matplotlib figure object
import matplotlib.pyplot as plt
figure_object = plt.figure() # generate object
plt.plot(range(10)) # fill it by plotted values
```

The simplest example is once we want to write a string object into a textfile located at our home folder (Remember, that since the configuration this home folder is contained within the `sddk_url` variable ) 

```python
sddk.write_file("test_string.txt", string_object, conf)
```

In the case  that everything is fine, you will receive following message:

```
> Your <class 'str'> object has been succefully written as "https://sciencedata.dk/files/test_string.txt"
```

However, there is a couple of things which might go wrong - You can choose an unsupported python object, a non-existent path or unsupported file format. The function captures some of these cases. For instance, once you run `sddk.write_file("nonexistent_folder/filename.wtf", string_object, conf)`, you will be interactively asked for corrections. First: the function checks whether the path is correct. When corrected to an existent folder (here it is "personal_folder"), the function further inspect whether it has known ending (i.e. `txt`, `json`, `feather`, or `png`). If not, it asks you interactively for correction. Third, it checks whether the folder already contain a file of the same name (to avoid unintended overwritting), and if yes, asks you what to do. Finally, it prints out where you can find your file and what type of object it encapsulates. 

```
>>> The path is not valid. Try different path and filename: textfile.wtf
>>> Unsupported file format. Type either "txt", "json", or "png": txt
>>> A file with the same name ("textfile.txt") already exists in this location.
Press Enter to overwrite it or choose different path and filename: textfile2.txt
>>> Your <class 'str'> object has been succefully written as "https://sciencedata.dk/files/textfile2.txt"
```

The same function works with dictionaries, lists, Matplotlib's figures and especially Pandas' dataframes. Pandas' dataframe is my favorite. I send there and back 1GB+ dataframes as json or feather files on a daily basis. See examples below

## read_file()

On the other side, we have the function `sddk.read_file(path_and_filename, object_type)`, which enables us to to read our files back to python as chosen python objects. Currently, the function can read only textfiles as strings, and json files as either dictionary, lists or Pandas's dataframes. You have to specify the type of object as the second argument, the values are either "str", "list", "dict" or "df" within quotation marks, like in these examples:

```python
string_object = read_file("test_string.txt", "str", conf)
string_object
>>> 'string content'
```

```python
list_object = read_file("simple_list.json", "list", conf)
list_object
>>> ['a', 'b', 'c', 'd']
```

```python
dict_object = read_file("simple_dict.json", "list", conf)
dict_object
>>> {'a': 1, 'b': 2, 'c': 3}
```

```python
dataframe_object = read_file("simple_df.json", "df", conf)
>>>     a   b   c
0  a1  b1  c1
1  a2  b2  c2
```

## Examples

### pandas.DataFrame to `.json` and back


```python
import pandas as pd
dataframe_object = pd.DataFrame([("a1", "b1", "c1"), ("a2", "b2", "c2")], columns=["a", "b", "c"])
dataframe_object
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a1</td>
      <td>b1</td>
      <td>c1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a2</td>
      <td>b2</td>
      <td>c2</td>
    </tr>
  </tbody>
</table>




```python
sddk.write_file("simple_dataframe.json", dataframe_object, conf)
> Your <class 'pandas.core.frame.DataFrame'> object has been succefully written as "https://sciencedata.dk/files/simple_dataframe.json"
```

```python
sddk.read_file("simple_dataframe.json", "df", conf)
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a1</td>
      <td>b1</td>
      <td>c1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a2</td>
      <td>b2</td>
      <td>c2</td>
    </tr>
  </tbody>
</table>

Reading a larger file from a public folder


```python
%%time
EDH_sample = sddk.read_file("EDH_sample.json", "df", "8fe7d59de1eafe5f8eaebc0044534606")
EDH_sample.head(5)
# this is an example usage of public folder, see below for explanation.
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>diplomatic_text</th>
      <th>literature</th>
      <th>trismegistos_uri</th>
      <th>id</th>
      <th>findspot_ancient</th>
      <th>not_before</th>
      <th>type_of_inscription</th>
      <th>work_status</th>
      <th>edh_geography_uri</th>
      <th>not_after</th>
      <th>...</th>
      <th>external_image_uris</th>
      <th>religion</th>
      <th>fotos</th>
      <th>geography</th>
      <th>military</th>
      <th>social_economic_legal_history</th>
      <th>coordinates</th>
      <th>text_cleaned</th>
      <th>origdate_text</th>
      <th>objecttype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>D M / NONIAE P F OPTATAE / ET C IVLIO ARTEMONI...</td>
      <td>AE 1983, 0192.; M. Annecchino, Puteoli 4/5, 19...</td>
      <td>https://www.trismegistos.org/text/251193</td>
      <td>HD000001</td>
      <td>Cumae, bei</td>
      <td>0071</td>
      <td>epitaph</td>
      <td>provisional</td>
      <td>https://edh-www.adw.uni-heidelberg.de/edh/geog...</td>
      <td>0130</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>40.8471577,14.0550756</td>
      <td>Dis Manibus Noniae Publi filiae Optatae et Cai...</td>
      <td>71 AD – 130 AD</td>
      <td>[Tafel, 257]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>C SEXTIVS PARIS / QVI VIXIT / ANNIS LXX</td>
      <td>AE 1983, 0080. (A); A. Ferrua, RAL 36, 1981, 1...</td>
      <td>https://www.trismegistos.org/text/265631</td>
      <td>HD000002</td>
      <td>Roma</td>
      <td>0051</td>
      <td>epitaph</td>
      <td>no image</td>
      <td>https://edh-www.adw.uni-heidelberg.de/edh/geog...</td>
      <td>0200</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>41.895466,12.482324</td>
      <td>Caius Sextius Paris qui vixit annis LXX       ...</td>
      <td>51 AD – 200 AD</td>
      <td>[Tafel, 257]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>[ ]VMMIO [ ] / [ ]ISENNA[ ] / [ ] XV[ ] / [ ] / [</td>
      <td>AE 1983, 0518. (B); J. González, ZPE 52, 1983,...</td>
      <td>https://www.trismegistos.org/text/220675</td>
      <td>HD000003</td>
      <td>None</td>
      <td>0131</td>
      <td>honorific inscription</td>
      <td>provisional</td>
      <td>https://edh-www.adw.uni-heidelberg.de/edh/geog...</td>
      <td>0170</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>37.37281,-6.04589</td>
      <td>Publio Mummio Publi filio Galeria Sisennae Rut...</td>
      <td>131 AD – 170 AD</td>
      <td>[Statuenbasis, 57]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>[ ]AVS[ ]LLA / M PORCI NIGRI SER / DOMINAE VEN...</td>
      <td>AE 1983, 0533. (B); A.U. Stylow, Gerión 1, 198...</td>
      <td>https://www.trismegistos.org/text/222102</td>
      <td>HD000004</td>
      <td>Ipolcobulcula</td>
      <td>0151</td>
      <td>votive inscription</td>
      <td>checked with photo</td>
      <td>https://edh-www.adw.uni-heidelberg.de/edh/geog...</td>
      <td>0200</td>
      <td>...</td>
      <td>[http://cil-old.bbaw.de/test06/bilder/datenban...</td>
      <td>names of pagan deities</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>37.4442,-4.27471</td>
      <td>AVSLLA Marci Porci Nigri serva dominae Veneri ...</td>
      <td>151 AD – 200 AD</td>
      <td>[Altar, 29]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>[ ] L SVCCESSVS / [ ] L L IRENAEVS / [ ] C L T...</td>
      <td>AE 1983, 0078. (B); A. Ferrua, RAL 36, 1981, 1...</td>
      <td>https://www.trismegistos.org/text/265629</td>
      <td>HD000005</td>
      <td>Roma</td>
      <td>0001</td>
      <td>epitaph</td>
      <td>no image</td>
      <td>https://edh-www.adw.uni-heidelberg.de/edh/geog...</td>
      <td>0200</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>41.895466,12.482324</td>
      <td>libertus Successus  Luci libertus Irenaeus  C...</td>
      <td>1 AD – 200 AD</td>
      <td>[Stele, 250]</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 40 columns</p>



### pandas.DataFrame to `.feather` and back


```python
sddk.write_file("simple_dataframe.feather", dataframe_object, conf)
> Your <class 'pandas.core.frame.DataFrame'> object has been succefully written as "https://sciencedata.dk/files/simple_dataframe.feather"
```

```python
sddk.read_file("simple_dataframe.feather", "df", conf)
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a1</td>
      <td>b1</td>
      <td>c1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a2</td>
      <td>b2</td>
      <td>c2</td>
    </tr>
  </tbody>
</table>



Reading a larger file from public folder


```python
%%time
EDH_sample = sddk.read_file("EDH_sample.feather", "df", "8fe7d59de1eafe5f8eaebc0044534606")
EDH_sample.head(5)
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>diplomatic_text</th>
      <th>literature</th>
      <th>trismegistos_uri</th>
      <th>id</th>
      <th>findspot_ancient</th>
      <th>not_before</th>
      <th>type_of_inscription</th>
      <th>work_status</th>
      <th>edh_geography_uri</th>
      <th>not_after</th>
      <th>...</th>
      <th>external_image_uris</th>
      <th>religion</th>
      <th>fotos</th>
      <th>geography</th>
      <th>military</th>
      <th>social_economic_legal_history</th>
      <th>coordinates</th>
      <th>text_cleaned</th>
      <th>origdate_text</th>
      <th>objecttype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>D M / NONIAE P F OPTATAE / ET C IVLIO ARTEMONI...</td>
      <td>AE 1983, 0192.; M. Annecchino, Puteoli 4/5, 19...</td>
      <td>https://www.trismegistos.org/text/251193</td>
      <td>HD000001</td>
      <td>Cumae, bei</td>
      <td>0071</td>
      <td>epitaph</td>
      <td>provisional</td>
      <td>https://edh-www.adw.uni-heidelberg.de/edh/geog...</td>
      <td>0130</td>
      <td>...</td>
      <td>NaN</td>
      <td>None</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>40.8471577,14.0550756</td>
      <td>Dis Manibus Noniae Publi filiae Optatae et Cai...</td>
      <td>71 AD – 130 AD</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>C SEXTIVS PARIS / QVI VIXIT / ANNIS LXX</td>
      <td>AE 1983, 0080. (A); A. Ferrua, RAL 36, 1981, 1...</td>
      <td>https://www.trismegistos.org/text/265631</td>
      <td>HD000002</td>
      <td>Roma</td>
      <td>0051</td>
      <td>epitaph</td>
      <td>no image</td>
      <td>https://edh-www.adw.uni-heidelberg.de/edh/geog...</td>
      <td>0200</td>
      <td>...</td>
      <td>NaN</td>
      <td>None</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>41.895466,12.482324</td>
      <td>Caius Sextius Paris qui vixit annis LXX       ...</td>
      <td>51 AD – 200 AD</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>[ ]VMMIO [ ] / [ ]ISENNA[ ] / [ ] XV[ ] / [ ] / [</td>
      <td>AE 1983, 0518. (B); J. González, ZPE 52, 1983,...</td>
      <td>https://www.trismegistos.org/text/220675</td>
      <td>HD000003</td>
      <td>None</td>
      <td>0131</td>
      <td>honorific inscription</td>
      <td>provisional</td>
      <td>https://edh-www.adw.uni-heidelberg.de/edh/geog...</td>
      <td>0170</td>
      <td>...</td>
      <td>NaN</td>
      <td>None</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>37.37281,-6.04589</td>
      <td>Publio Mummio Publi filio Galeria Sisennae Rut...</td>
      <td>131 AD – 170 AD</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>[ ]AVS[ ]LLA / M PORCI NIGRI SER / DOMINAE VEN...</td>
      <td>AE 1983, 0533. (B); A.U. Stylow, Gerión 1, 198...</td>
      <td>https://www.trismegistos.org/text/222102</td>
      <td>HD000004</td>
      <td>Ipolcobulcula</td>
      <td>0151</td>
      <td>votive inscription</td>
      <td>checked with photo</td>
      <td>https://edh-www.adw.uni-heidelberg.de/edh/geog...</td>
      <td>0200</td>
      <td>...</td>
      <td>NaN</td>
      <td>names of pagan deities</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>37.4442,-4.27471</td>
      <td>AVSLLA Marci Porci Nigri serva dominae Veneri ...</td>
      <td>151 AD – 200 AD</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>[ ] L SVCCESSVS / [ ] L L IRENAEVS / [ ] C L T...</td>
      <td>AE 1983, 0078. (B); A. Ferrua, RAL 36, 1981, 1...</td>
      <td>https://www.trismegistos.org/text/265629</td>
      <td>HD000005</td>
      <td>Roma</td>
      <td>0001</td>
      <td>epitaph</td>
      <td>no image</td>
      <td>https://edh-www.adw.uni-heidelberg.de/edh/geog...</td>
      <td>0200</td>
      <td>...</td>
      <td>NaN</td>
      <td>None</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>41.895466,12.482324</td>
      <td>libertus Successus  Luci libertus Irenaeus  C...</td>
      <td>1 AD – 200 AD</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 40 columns</p>




```python
sddk.write_file("EDH_sample.feather", EDH_sample, conf)
> Your <class 'pandas.core.frame.DataFrame'> object has been succefully written as "https://sciencedata.dk/files/EDH_sample.feather"
```

### pandas.DataFrame to `.csv` and back 


```python
import pandas as pd
dataframe_object = pd.DataFrame([("a1", "b1", "c1"), ("a2", "b2", "c2")], columns=["a", "b", "c"]) 
dataframe_object
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a1</td>
      <td>b1</td>
      <td>c1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a2</td>
      <td>b2</td>
      <td>c2</td>
    </tr>
  </tbody>
</table>




```python
sddk.write_file("simple_dataframe.csv", dataframe_object, conf)
> Your <class 'pandas.core.frame.DataFrame'> object has been succefully written as "https://sciencedata.dk/files/simple_dataframe.csv"
```

```python
sddk.read_file("simple_dataframe.csv", "df", conf)
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a1</td>
      <td>b1</td>
      <td>c1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a2</td>
      <td>b2</td>
      <td>c2</td>
    </tr>
  </tbody>
</table>

## list_filenames()

This function enables you to list all files within a directory. You can specify the directory, type of the file you are interested in and the conf variable. For instance, the function belows returns all JSON files within your main directory.

```python
 sddk.list_filenames(filetype="json", conf=conf)
```

## Personal, shared and public folders

**Shared in and out**

One of the main strength of the sciencedata.dk are collaborative features, namely the way you can manage its **shared** and **public** folders.

**Shared** folders always have one of two forms: either (1) a shared folder *you* share with some users or (2) a shared folder someone else shares with you. 

Each shared folder has its **owner**. The folders  are located in their owner's  personal space and can be easily accessed by them from there like any other personal folder.

However, in the case of shared folders you do not own (i.e. which were shared with you by someone else) you also need to know the username of their owner. 

One of the key features of the **sddk** package is that it enables you to access both types of shared folders **using exactly the same command**, regardless you are their owner or not. This enables that all members of a team accessing a folder owned and shared by one member can you use the same code. The function just checks both options and chooses what works.

For instance, a project member with username `member1@inst.org` created a folder in his personal space called `team_folder`,  uploaded there a file called `textfile.txt`, and shared the folder with his teammates with usernames `member2@inst.org` and `member3@inst.org`. All of them can now access the file using the same series of commands:

```python
# configure session with access to the shared folder:
conf = sddk.configure("team_folder", "member1@inst.org")
# read the file located in this shared folder:
sddk.read_file("testfile.txt", "str", conf)
```

**Public files and folders**

Sciencedata.dk also enables to produce public files and folders. These files and folders might be accessed using `sddk.read_file()` function even without having sciencedata.dk account. You just have to know  share link code of the file or folder. To read a public file, you can use:

```python
public_file_code = "3e0a55a4182de313e04523360cecd015"
gospels_cleaned = sddk.read_file("https://sciencedata.dk/public/" + public_file_code, "dict")
```

To read a specific file within a public folder, you can use the code below, i.e. you can replace the `conf` parameter by sharing code of the public folder.

```python
c_aristotelicum = sddk.read_file("https://sciencedata.dk/public/" + public_folder_code + "/c_aristotelicum.json", "df", "31b393e2afe1ee96ce81869c7efe18cb")
```

## Credit

The package is continuously develepod and maintained by [Vojtěch Kaše](http://vojtechkase.cz) as a part of the digital collaborative research workflow of the [SDAM project](https://sdam-au.github.io/sdam-au/) at Aarhus University, Denmark. To cite this package, use:

## Version history

* 2.4 - json encoding bug removed
* 2.3 - json encoding
* 2.2 - setup.py update
* 2.1 - README.md update
* 2.0 - tested with `.txt`, `.json`, `.feather` and `.png`.
* 1.9 - supports public files and folders; supports `.feather` file format (`utf.8` enforced)
* 1.8 - `list_filenames()` function and `configure()` alias added
* 1.7 - figures
* 1.6.1 - bug
* 1.6 - enables writing dataframes as `csv`
* 1.5 - reads individually shared files without necessary configuration
* 1.4 - `json` package dependency
* 1.3 - `conf` corrected
* 1.2 - `conf` variable added
* 1.1 - a simple correction
* 1.0 -  functions `write_file()` and `read_file()` added
* 0.1.2 -  redirection added
* 0.1.1 - added shared folder owner argument to the main configuration function; migration from test.pypi to real pypi
* 0.0.8 - shared folders reading&writing for ordinary users finally functional
* 0.0.7 - configuration of individual session by default
* 0.0.6 - first functional configuration



