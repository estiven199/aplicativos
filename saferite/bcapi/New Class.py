class API:
    def __init__(self):
        self.endpoint = ''
        self.add_1 = ''
        self.add_2 = ''
        self.header = None
        self.data_prefix = ''
        self.collection = {}

    def _standard_call(self, module, call_type, var_1='', var_2='', data=None, **kwargs):
        
        self.url = self.endpoint + self.add_1 + var_1 + module + self.add_2 + var_2
        additional_args = locals()['kwargs']

        if self.data_prefix == '':
            self.data = data
        else:
            self.data = {self.data_prefix : data}

        if len(additional_args) == 0:
            self.params = None
        else:
            self.params = additional_args

        if call_type == 'GET':
            self.request = requests.get(url=self.url, headers=self.header, params=self.params,data=self.data).text
        elif call_type == 'POST':
            self.request = requests.post(url=self.url, headers=self.header, params=self.params,data=self.data).text
        elif call_type == 'PUT':
            self.request = requests.put(url=self.url, headers=self.header, params=self.params,data=self.data).text
        elif call_type == 'DELETE':
            self.request = requests.delete(url=self.url, headers=self.header, params=self.params,data=self.data).text

        self.r = json.loads(self.request)
        return self.r
        
    def call_function(self, function, **kwargs):
        additional_args = locals()['kwargs']
        module = self.collection[function]['module']
        method = self.collection[function]['method']
        if 'var_1' in self.collection[function]:
            var_1 = self.collection[function]['var_1']
        else:
            var_1 = ''
            
        if 'additional_data' in self.collection[function]:
            required = self.collection[function]['additional_data']
            given = list(additional_args.keys())
            if set(required).issubset(given):
                return self._standard_call(module,method,var_1=var_1,**additional_args)
            else:
                missing = set(required).difference(set(given))
                if len(missing) == 1:
                    return "Required parameter is missing: " + str(missing)
                return "Required parameters are missing: " + str(missing)

        return self._standard_call(module,method,var_1=var_1)