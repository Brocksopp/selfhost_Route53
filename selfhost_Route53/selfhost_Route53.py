#https://python-route53.readthedocs.io/en/latest/quickstart.html


import route53 ##will require pip install
import urllib.request
import time
import datetime
import json
from pathlib import Path


class update_ip:

    def __init__(self):
         self.aws_access_key_id = None
         self.aws_secret_access_key = None
         self.hostZone = None
         #self.domain = None
         self.subDomain = None
         self.currentIP = None
         self.conn = None ##Variable for Amazon connection
         pass
     
    def main(self):
         
         while(True):

             try:
                 now = datetime.datetime.now()
                 print(now.strftime("%Y-%m-%d %H:%M:%S"))
                 self.run_ip_update()
                 time.sleep(1*120)
             except:
                 print("Something went wrong..")
                 time.sleep(1*60)
             pass          
         pass

    def run_ip_update(self):
        if (self.get_config() == 0):
            return 0
        self.get_PublicIP()
        self.get_connection()
        self.get_DomainDetails()
        self.update_IP()
        pass


    def get_config(self):
        print(Path.cwd())
        filePath = Path("./data/config.json") #+ Path.home()
        if filePath.is_file():
            with open(filePath) as json_file:
                data = json.load(json_file)
                self.aws_access_key_id = data["aws_access_key_id"]
                self.aws_secret_access_key = data["aws_secret_access_key"]
                self.hostedZone = data["hostedZone"]
                #self.domain = data["domain"]
                self.subDomain = data["subDomain"]
                print("Config File Loaded.")
                pass
            pass
        else:
            print("Config File Not Found.")
            return 0
        pass



    def get_PublicIP(self):
        req = urllib.request.Request('https://api.ipify.org') ##Get IP from web API.
        with urllib.request.urlopen(req) as response:
            self.currentIP = response.read().decode('utf-8')
            pass
        print("Current IP = " + self.currentIP)
        return self.currentIP


    def get_connection(self):

        print("Connecting to AWS Route53...")
        self.conn = route53.connect(
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key,)

        ## Verify connection was successful??

        pass


    def get_DomainDetails(self):
        for zone in self.conn.list_hosted_zones():
            print("Hosted Zone: " + zone.name)
            for record_set in zone.record_sets:
                print("\t" + record_set.name + ", Type: " + record_set.rrset_type)
                for records in record_set.records:
                    print("\t\t" + records)
                pass
            pass
        pass


    def update_IP(self):
        #TODO - Better handling of no config file!

        if (self.subDomain == None or self.subDomain == []):
            print("Settings Incomplete.")
            return 1

        if self.currentIP == None or self.currentIP == '':
            print("Settings Incomplete.")
            return 1

        # Note that this is a fully-qualified domain name.
        for zone in self.conn.list_hosted_zones():
            if zone.name == (self.hostedZone + "."):
                for record_set in zone.record_sets:
                    for prefix in self.subDomain:
                        address = (prefix + "." + self.hostedZone)
                        if record_set.name == (address + "."):
                            #print(record_set.name)
                            # Stopping early may save some additional HTTP requests,
                            # # since zone.record_sets is a generator.

                            ##Check whether existing IP matches current IP.
                            if record_set.records == [self.currentIP]:
                                print("No Change Required: " + address)
                            else:
                                #Changing record set
                                ###record_set.records = ['8.8.8.7']
                                record_set.records = [self.currentIP]
                                record_set.save()
                                print("IP Updated: " + address)
                                pass
                            break
                    pass
        pass

    pass ##End of Class







instance = update_ip()
#instance.run_ip_update()
instance.main()
pass