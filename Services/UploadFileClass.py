#!/usr/bin/python3


from Services.API_Caller import CallAPI
import hashlib
import os
import platform
import datetime
import math
import sys
from requests_toolbelt import MultipartEncoder


class Upload:

    def __init__(self, Credentials, AsUser='', filename='', full_path=''):
        self.AppKey = Credentials.AppKey
        self.AccessToken = Credentials.AccessToken
        self.AsUser = AsUser
        self.filename = filename
        self.max_chunk_size = 5242880
        if platform.system() == 'Windows':
            separator = '\\'
        else:
            separator = '/'
        self.full_path = full_path + separator + self.filename

    def read_in_chunks(self, file_object):
        while True:
            data = file_object.read(self.max_chunk_size)
            if not data:
                break
            yield data

    def creation_date(self):
        if platform.system() == 'Windows':
            return datetime.datetime.fromtimestamp(os.path.getctime(self.full_path)).isoformat()
        else:
            stat = os.stat(self.full_path)
            try:
                return datetime.datetime.fromtimestamp(stat.st_ctime).isoformat()
            except AttributeError:
                return datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()

    def Upload(self, Syncpoint_ID, Path):
        Method = "POST"
        creation_date = self.creation_date()
        last_write_time = datetime.datetime.fromtimestamp(os.path.getmtime(self.full_path)).isoformat()
        url = "saveFile.php?filepath=" + Path
        login_headers = {'As-User': '%s' % self.AsUser, "User-Agent": "API_Application"}
        file_size = os.path.getsize(self.full_path)
        if file_size < self.max_chunk_size:
            login_headers["Content-Range"] = "0-*/*"
            multipart_body = [('fileData', ('%s' % self.filename, open('%s' % self.full_path, 'rb'),
                                            'application/octet-stream')),
                              ('sha256', (None, hashlib.sha256(self.full_path.encode('utf-8')).hexdigest(), None)),
                              ('sessionKey', (None, 'Bearer ' + self.AccessToken, None)),
                              ('virtualFolderId', (None, '%s' % Syncpoint_ID, None)),
                              ('creationTimeUtc', (None, creation_date, None)),
                              ('lastWriteTimeUtc', (None, last_write_time, None)),
                              ('fileDone', (None, '', None))]
            request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers, data='', file=multipart_body,
                              base_url="https://data.syncplicity.com/").MakeRequest()
            return request

        else:
                first_call_headers = {'As-User': '%s' % self.AsUser,
                                      "User-Agent": "API_Application",
                                      'Content-Range': "*/*"}
                first_call_body = MultipartEncoder({'sessionKey': (None, 'Bearer ' + self.AccessToken, None)})
                first_call_headers['Content-Type'] = first_call_body.content_type
                first_call_response = CallAPI(url, self.AppKey, self.AccessToken, Method, first_call_headers,
                                              data=first_call_body,
                                              base_url="https://data.syncplicity.com/").MakeRequest()
                if first_call_response.status_code == 308:
                    login_headers['If-Match'] = first_call_response.headers['ETag']
                else:
                    sys.exit('Failed to create session for chunked upload')
                chunk_count = math.ceil(file_size / self.max_chunk_size)
                f = open(self.full_path, 'rb')

                content_range_index = 0
                sent_chunk_count = 1

                for chunk in self.read_in_chunks(f):
                    login_headers['Content-Range'] = '%s-*/*' % content_range_index
                    content_range_index += self.max_chunk_size
                    if sent_chunk_count == chunk_count:
                        multipart_body = MultipartEncoder({'fileData': (self.filename, chunk,
                                                                        'application/octet-stream'),
                                                           'sha256': (None, hashlib.sha256(chunk).hexdigest(), None),
                                                           'sessionKey': (None, 'Bearer ' + self.AccessToken, None),
                                                           'virtualFolderId': (None, '%s' % Syncpoint_ID, None),
                                                           'creationTimeUtc': (None, creation_date, None),
                                                           'lastWriteTimeUtc': (None, last_write_time, None),
                                                           'fileDone': (None, '', None)})
                    else:
                        multipart_body = MultipartEncoder({'fileData': (self.filename, chunk,
                                                                        'application/octet-stream'),
                                                           'sha256': (None, hashlib.sha256(chunk).hexdigest(), None),
                                                           'sessionKey': (None, 'Bearer ' + self.AccessToken, None),
                                                           'virtualFolderId': (None, '%s' % Syncpoint_ID, None),
                                                           'creationTimeUtc': (None, creation_date, None),
                                                           'lastWriteTimeUtc': (None, last_write_time, None)})
                    login_headers['Content-Type'] = multipart_body.content_type
                    sent_chunk_count += 1
                    request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers,
                                      data=multipart_body, base_url="https://data.syncplicity.com/").MakeRequest()
                    if request.status_code == 308:
                        login_headers['If-Match'] = request.headers['ETag']
                    else:
                        f.close()
                        return request
