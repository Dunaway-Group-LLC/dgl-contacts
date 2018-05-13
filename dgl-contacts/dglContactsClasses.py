#
# # Definition of Contacts objects
#

#
# # imports
#
import boto3
from botocore.exceptions import ClientError
import pickle
from io import BytesIO

#
# # class defs
#


class Contact:
    """class Contact
            first_name, last_name, email, attrs
                atttrs depends on application using the object
    """

    def __init__(
            self, email,  first_name="",  last_name="",  product="", attrs={}
            ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.product = product    # Name of product associated with Contact
        self.attrs = attrs    # new empty dict of attributes for each contact


class Contacts:

    """class Contacts - holds all contacts for all Products
        - stored pickled in s3 bucket dgl-contacts
    """
#
# # function defs
#

    def __init__(self,  bucketName):
        self.contacts = {}          # Dictionary holding Contacts, key is email
        self.bucketName = bucketName    # Bucket name holding Contacts object

    def addContact(self,  Contact):
        print("Add Contact")
        pass

    def getContact(self, Contact):
        pass

    def updateContact(self,  Contact):
        pass

    def loadContacts(contacts):
        """loadContacts(contacts)  # contacts is empty instance of Contacts
                Gets pickled Contacts object from S2
                unpickle
                returns Contacts

                 Boto 3

        """
        s3 = boto3.resource('s3')   # get S3.Object
#
# # Prove we can talk to bucket
#
        bucket = s3.Bucket(contacts.bucketName)
        for obj in bucket.objects.all():
            print(obj.key)

        contacts = BytesIO()   # unpickled comes as bytes
        try:
            contacts = s3.Object(
                contacts.bucketName,
                'contacts').get()["Body"].read()    # get pickled Contacts
            contacts = pickle.load(contacts)  # unpickle
        except ClientError:
            print("The object does not exist.")
            createContactsBucket(contacts.bucketName)   # No existing bucket
        return(contacts)


def storeContacts(self):
        """
            Pickle and save in s3
        """


def confirmContact():
        """confirmContact()
                Sends SES email to new contact
        """
        print("In confirmContact")
        pass


def createContactsBucket(bucket):
    """
        Create Contacts - put new Contacts object in S3 bucket 'dgl-contacts'
    """
    print("bucket type:", type(bucket))

    s3 = boto3.resource('s3')                   # get S3.Object

    contacts = Contacts(bucket)        # Contacts object with empty dictionary
    body = pickle.dumps(contacts)      # serialized Contacts object
    try:
        s3.Object(contacts.bucket, 'contacts').put(Body=body)
    except Exception as e:
        print(type(e))
        print(e.args)
        print(e)

    for obj in contacts.bucket.objects.all():
        print(obj.key)


"""

pickle_buffer = BytesIO()
s3_resource = boto3.resource('s3')

new_df.to_csv(pickle_buffer, index=False)
s3_resource.Object(bucket,path).put(Body=pickle_buffer.getvalue())

"""


class Product:
    """class Product - a Product is something being marketed
            name, desc, campaigns, dates
    """

    def __init__(self, name,  desc, start_date,  due_date):
        self.name = name
        self.desc = desc
        self.dates = {"start_date": start_date, "due_date": due_date}

    def set_dates(self, dates):
        self.dates = dates


class Message:
    """
        class Message
        name, desc, text, freebie
    """

    def __init__(self, name, desc, text,  freebie):
        self.name = name
        self.desc = desc
        self.text = text
        self.freebie = freebie              # Something the user can download


class Campaign:
    """class Campaign - a Campaign - holds some Messages, last_sent[date_time,
        message_name], interval for sending
           name, desc, last_sent, interval

    """

    def __init__(self, name,  desc,  interval):
        self.name = name
        self.desc = desc
        self.interval = interval
        self.messages = {}
        self.last_sent = [0, "none"]
        self.messages = []


class Campaigns:
    """class Campaigns - contains all campaigns - stored pickled in s3
            campaigns

    """

    def __init__(self):
        self.campaigns = {}         # All campaigns - name : Campaign

    def loadCampaigns(self, campaigns):
        """loadContacts(contacts)  # contacts is empty instance of Campaigns
                Checks that self.campaigns = {}
                Gets pickled Campaigns object from S3
                unpickle
                returns self.campaigns

                 Boto 3

        """
        pass

    def storeCampaigns(self):
        """
            Pickle and save in s3
        """

    def addCampaign(self, name, desc,  interval):
        if name in self.campaigns:
            return False
        else:
            self.campaigns[name] = Campaign(name, desc, interval)
            return True

    def delCampaign(self, name):
        if name in self.campaigns:
            del self.campaigns[name]
            return True
        else:
            return False

    def chgCampaign(self, name, desc, interval, messages):
        if name in self.campaigns:
            self.campaigns[name] = Campaign(name, desc, interval)
            self.campaigns[name].messages = messages
            return True
        else:
            return False
