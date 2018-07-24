#!/usr/bin/python3

from Services.UserAPIsClass import ClassUserAPIs
import os
import sys
import platform
from Services.AuthenticationClass import Authentication
from Services.FileFolderMetadataClass import FileFolderMetadataClass
from Services.UploadFileClass import Upload
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Content Migration API Options')
    parser.add_argument('-s', '--syncpoint', dest='syncpoint', action='store', required=True, help='enter syncpoint name')
    parser.add_argument('-f', '--folder', dest='folder', action='store', required=True, default='', help='enter path to folder')
    parser.add_argument('--as-user', dest='as_user', action='store', required=False, default='', help='enter user email in order to commit in name of a certain user')
    parser.add_argument('--create-syncpoint', dest='create_sp', action='store_true', required=False, help='create syncpoint using the entered syncpoint name and upload content of chosen folder under created syncpoint')
    parser.add_argument('--just-content', dest='just_content', action='store_true', required=False, help='migrate only the content under the specified top level folder (in folder flag)')
    return parser.parse_args()


args = parse_args()

start_path = r"%s" % args.folder
Credentials = Authentication()
User_ID = ''
if args.as_user != '':
    User_ID = ClassUserAPIs(Credentials).GetUser(args.as_user)['Id']
    if User_ID is None:
        sys.exit('could not find such user, exiting')

if platform.system() == 'Windows':
    separator = '\\'
    top_folder_name = start_path.split('%s' % separator)[-1]
else:
    separator = '/'
    top_folder_name = start_path.split('%s' % separator)[-2]

if args.create_sp:
    syncpoint_class = FileFolderMetadataClass(Credentials, AsUser=User_ID)
    print('Checking if Syncpoint exists...')
    check_if_sp_exists = syncpoint_class.GetSyncpointID(args.syncpoint)
    if check_if_sp_exists is None:
        print('Syncpoint does not exist, creating Syncpoint...')
        new_sp = syncpoint_class.CreateSyncpoint(args.syncpoint)
        Syncpoint_ID = new_sp[0]['Id']
    else:
        print('Syncpoint already exists, continuing using specified Syncpoint')
        Syncpoint_ID = check_if_sp_exists
else:
    Syncpoint_ID = FileFolderMetadataClass(Credentials, AsUser=User_ID).GetSyncpointID(args.syncpoint)
    if Syncpoint_ID is None:
        sys.exit('No such Syncpoint, exiting')

file_list = {}
index = 1
for path, dirs, files in os.walk(start_path):
    for filename in files:
        file_list['file%s' % index] = {}
        file_list['file%s' % index]['filename'] = filename
        file_list['file%s' % index]['filepath'] = path
        index += 1

for file in file_list:
    filename = file_list[file]['filename']
    filepath = file_list[file]['filepath']
    split_filepath = str(filepath.split(top_folder_name)[1])
    if args.just_content:
        syncpoint_path = split_filepath.replace('%s' % separator, '%5C') + '%5C' + filename
    else:
        syncpoint_path = '%5C' + top_folder_name + '%5C' + split_filepath.replace('%s' % separator, '%5C') + '%5C' + filename
    UploadFile = Upload(Credentials, AsUser=User_ID, filename='%s' % filename, full_path=filepath).Upload(Syncpoint_ID, syncpoint_path)
    if UploadFile.status_code == 500 or 200:
        print('Successfully uploaded %s' % filename)
