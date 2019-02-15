<img src="../images/Words-Recorder-icon.png" alt="logo" align="right" />

## Words Recorder

Words Recorder is an app to record the word that you are unfamiliar with when you do some reading, based on Python, PyQt5 and MySQL. 

### screenshot

<div align="center">
    <img src="../images/Words-Recorder.png" alt="Words Recorder" height="350" />
</div>

### Installation
First, clone the repo and install the required packages.
```
>> git clone https://github.com/LewisTian/PyQt5-Apps.git
>> cd PyQt5-Apps/words-recorder
>> pip install -r requirements.txt
```
Next, create a MySQL table like 'mysql.sql', and config the 'setting.ini'. The 'path' below must be matched with the 'secure_file_priv' in the 'my.ini'(Windows) / 'mysqld.cnf'(Linux). 
```
# setting.ini
[MySQL]
host = localhost
user = root
password = 
db = 
port = 3306
charset = utf8
path = 
```
Finally, you can run the app.
```
>> python main.py 
```

### Usage
Note that you should connect to the database first.

#### import
You can import data via a file, and the rules of the file format are as follows
- original word and translation are splitted by blanks or tabs.
- phrase and expression should be joined by '-' or '\_' instead of blanks.
- a blank line in the last.

#### export
Export data as a '.csv' file.

#### insert
Put original word and translation in the corresponding input field, then click the 'insert' button or press 'Ctrl+Return'.

#### query
Put original word in the 'origin' input field, then click the 'query' button or press 'Ctrl+Q'.

#### update
You can modify the data in the table('id' column is not permitted), then click the 'update' button or press 'Ctrl+U'. 
**You can modify multiple lines of data at once.**

#### delete
Click the 'delete' button or press 'Ctrl+D'. You can delete multiple lines at once. 

### style sheet
You can write your own style sheet named 'style.qss' in the 'PyQt5-Apps/words-recorder' directory.

### License
GNU General Public License v3.0