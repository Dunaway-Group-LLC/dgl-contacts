#! /usr/bin/python3.6
#
# # Reads downloaded .csv from GAIC website, containing agents contact info
# # Extracts new licenses for just ended month (parameter)
# # Creates two Contacts objects - one to hold Contact(s) with personal email
# #  [ contactsPers ]
# # and one to hold those with company emails [ contactsFirm ]
# # Creates Contact object from each line in .csv
# # # Checks email on new Contact and adds it to contactsPers or contactsFirm
# # # based on FirmEmails
#
# /home/les/Downloads/GAIC-LifeLic-CurrentMonth.csv
# # imports
# will it save? yes it did

import sys
import getopt
import csv
from dglContactsClasses import Contact, Contacts
from gaicClasses import FirmEmails
from dglPickleToS3BucketClasses import S3pickleBucket, getPickleBucket


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def readCsv(fn, month, bucketName, keyName):
    """
    .csv header for download from GAIC
    License Number,License Type,First Name,Middle Name,Last Name,
    Line One Address,Line Two Address,City,State,Zip,NPN,Business Tel,
    Email,Qualification Date,Expiration Date

    """
    try:
        contactsPers = Contacts(bucketName, keyName)  # contacts-pers email

        contactsFirm = Contacts(bucketName, "firm-contacts")
        # Will be stored in dgl-contacts bucket with object id firm-contacts
        contactsPers = contactsPers.loadContacts(pb)
        if contactsPers.contacts == {}:     # couldn't load Contacts
            raise FileNotFoundError("Unable to load Contacts object")
        firm_emails = FirmEmails()  # list of email domains from ins firms
        if firm_emails == []:
            raise FileNotFoundError("Unable to load FirmEmails object")

        with open(fn, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # print(row['First Name'], row['Last Name'])# Just test reading
                # Create Contact for each row in .csv- incomplete
                contact = Contact(
                    row["Email"], row["First Name"],
                    row["Last Name"], "PRODUCT",
                    {
                        "Qualification Date": row["Qualification Date"],
                        "Expiration Date": row["Expiration Date"]
                    }
                )
                print(
                    "Contact: ", contact.first_name, contact.last_name,
                    contact.email)
                # Add each to Contacts - either pers or firm by email domain
                if contact.email == "n/a":
                    contact.email = "none@none.com"
                email_domain = contact.email.split("@")[1]
                print("Domain", email_domain)
                if firm_emails.inFirmEmails(email_domain):
                    contactsFirm.addContact(contact)
                else:
                    contactsPers.addContact(contact)
# Store the new contactsFirm - both pers & firm_emails
        contactsPers.storeContacts()
        contactsFirm.storeContacts()
    except (FileNotFoundError, csv.Error) as e:
        print(e)
        print(e.args)
        quit(99)
#
# # Main
#


def main(argv=None):
    if argv is None:
        argv = sys.argv

        print("main Argv: ", argv)
    try:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
            print(args)
        except (getopt.error) as msg:
            raise Usage(msg)
        # Get current month from args
        fn = args[0]
        month = args[1]
        bucketName = args[2]
        keyName = args[3]
        print("Args:", args, "Month: ", month)
        # Connect bucket
        pb = getPickleBucket(bucketName)     # bucket exists?
        # Read .csv, keeping only current month items
        readCsv(fn, month)
    except (Usage) as err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2


if __name__ == "__main__":
        sys.exit(main())
