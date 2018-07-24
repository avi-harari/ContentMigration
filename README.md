Content Migration For Syncplicity Please use Main.py in order to execute the script.

This program will walk through a local file tree and replicate it to Syncplicity.

It can create a new syncpoint (top level folder) in Syncplicity and store the file tree under that syncpoint or create the exact same tree with current top lever folder as the syncpoint.

Before using the script, please enter your credentials in ConfigurationFile.

In case you do not have the credentials and would like to learn how to obtain these, please go to https://developer.syncplicity.com/overview .

Supported OSs: Windows (tested on Windows10), Linux (tested on Ububtu)

Requirements: Python3 with requests module installed.

Caveats:

* HTTP 500 is treated as success due to a bug. This is a workaround and should not be used in production.
* If 2 Syncpoints exist with the same name, one will randomly be chosen.

usage: Main.py [-h] -s SYNCPOINT -f FOLDER [--as-user AS_USER] [--create-syncpoint]

Content Migration API Options

positional arguments: values

Arguments:

    -h, --help - show this help message and exit

    -s SYNCPOINT, --syncpoint SYNCPOINT - enter syncpoint name

    -f FOLDER, --folder FOLDER - enter path to folder

    --as-user AS_USER - enter user email in order to commit in name of a certain user

    --create-syncpoint - create syncpoint using the entered syncpoint name and upload content of chosen folder under created syncpoint

    --just-content - migrate only the content under the specified top level folder (in folder flag)

Examples:

    ./Main.py -s "Test Syncpoint" -f C:\Test\TestFolder
    ./Main.py -s "Test Syncpoint" -f C:\Test\TestFolder --as-user user@email.com
    ./Main.py -s "Test Syncpoint" -f "C:\Test\Test Folder" --create-syncpoint
    ./Main.py -s TestSyncpoint -f C:\Test\TestFolder --create-syncpoint --as-user user@email.com

