import requests


class CallAPI:

    def __init__(self, url, AppKey, AccessToken, Method, AdditionalHeaders, data='', file='',
                 base_url="https://api.syncplicity.com/"):
        self.url = base_url + url
        self.AppKey = AppKey
        self.AccessToken = AccessToken
        self.Method = Method
        self.AdditionalHeaders = AdditionalHeaders
        self.Headers = {'Authorization': 'Bearer %s' % self.AccessToken, 'AppKey': '%s' % self.AppKey}
        self.Headers.update(AdditionalHeaders)
        self.data = data
        self.file = file

    def MakeRequest(self):
        if self.data != "":
            # request = requests.request(self.Method, self.url, headers=self.Headers, data=self.data,
            # proxies={"http":"HTTP_PROXY", "https":"HTTPS_PROXY"},
            #  verify=r'PATH\TO\CERTIFICATE')
            request = requests.request(self.Method, self.url, headers=self.Headers, data=self.data)
        elif self.file != "":
            # request = requests.request(self.Method, self.url, headers=self.Headers, data=self.data, files=self.file,
            # proxies={"http": "HTTP_PROXY", "https":"HTTPS_PROXY"},
            # verify=r'PATH\TO\CERTIFICATE')
            request = requests.request(self.Method, self.url, headers=self.Headers, data=self.data, files=self.file)
        else:
            # request = requests.request(self.Method, self.url, headers=self.Headers,
            # proxies={"http": "HTTP_PROXY", "https":"HTTPS_PROXY"},
            # verify=r'PATH\TO\CERTIFICATE')
            request = requests.request(self.Method, self.url, headers=self.Headers)
        return request
