#https://python-route53.readthedocs.io/en/latest/quickstart.html


import route53 ##will require pip install
import urllib.request
import time
import json
from pathlib import Path


class update_ip:

    def __init__(self):
         self.aws_access_key_id = None
         self.aws_secret_access_key = None
         self.domain = None
         self.currentIP = None
         pass


    def get_config(self):
        filePath = Path("config.json")
        if filePath.is_file():
            with open(filePath) as json_file:
                data = json.load(json_file)
                self.aws_access_key_id = data["aws_access_key_id"]
                self.aws_secret_access_key = data["aws_secret_access_key"]
                self.domain = data["domain"]
                pass
            pass
        else:
            print("Config File Not Found.")
            return 1


    def get_IP(self):
        req = urllib.request.Request('https://api.ipify.org') ##Get IP from web API.
        with urllib.request.urlopen(req) as response:
            self.currentIP = response.read().decode('utf-8')
            pass
        print("Current IP = " + self.currentIP)
        return self.currentIP

    def update_IP(self):

        if (self.domain == None or self.domain == ''):
            print("Settings Incomplete.")
            return 1

        if self.currentIP == None or self.currentIP == '':
            print("Settings Incomplete.")
            return 1

        print("Connecting to AWS Route53...")
    
        conn = route53.connect(
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key,)
        


        for zone in conn.list_hosted_zones():
            print(zone.name)
            for record_set in zone.record_sets:
                print("\t" + record_set.name)
                print("\t\t" + record_set.zone_id)
                pass
            pass

        print("...")
        # Note that this is a fully-qualified domain name.
        name_to_match = self.domain
        for record_set in zone.record_sets:
            if record_set.name == name_to_match:
                print(record_set)
                # Stopping early may save some additional HTTP requests,
                # # since zone.record_sets is a generator.
                break
            pass

        ##Check whether existing IP matches current IP.
        if record_set.records == [self.currentIP]:
            print("No Change Required.")
        else:
            #Changing record set
            ##record_set.records = ['8.8.8.7']
            record_set.records = [self.currentIP]
            record_set.save()
            print("IP Updated.")
            pass
        pass


    pass ##End of Class







instance = update_ip()
instance.get_config()
instance.get_IP()
instance.update_IP()
pass