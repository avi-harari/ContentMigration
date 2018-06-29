# ContentMigration
Content Migration For Syncplicity
Please use Main.py in order to execute the script.
Before using the script, please enter your credentials in ConfigurationFile.

usage: Main.py [-h] -s SYNCPOINT -f FOLDER [--as-user AS_USER]
               [--create-syncpoint]
               [values [values ...]]

Content Migration API Options

positional arguments:
  values

optional arguments:
  -h, --help            show this help message and exit
  -s SYNCPOINT, --syncpoint SYNCPOINT
                        enter syncpoint name
  -f FOLDER, --folder FOLDER
                        enter path to folder
  --as-user AS_USER     enter user email in order to commit in name of a
                        certain user
  --create-syncpoint    create syncpoint using the entered syncpoint name and
                        upload content of chosen folder under created
                        syncpoint
                        
