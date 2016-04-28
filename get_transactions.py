#!/usr/bin/python
import os
import urllib
import urllib2
import cookielib
from optparse import OptionParser
import datetime
import csv
import MySQLdb

mint_username = "Mint Username"
mint_password = "Mint Password" 
db_host = "localhost"
db_user = "root"
db_password = ""
db_schema = "mint"
db_table = "transactions"    

class mintlib():
    
    def __init__(self):
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  # need cookies for the JSESSION ID
        urllib2.install_opener(self.opener)


    def login(self, username, password):
        request = urllib2.Request("https://wwws.mint.com/loginUserSubmit.xevent?task=L",  urllib.urlencode(locals()))
        request.add_header("User-Agent", "Mozilla/5.0") # Mint kicks to a "Upgrade to IE 7.0" page without this
        response = self.opener.open(request)
        
    def download(self, file):
        # write CSV file of all Mint transactions for this account to a file
        response = self.opener.open("https://wwws.mint.com/transactionDownload.event?") 
        open(file, "w").write(response.read())
        
    def logout(self):
        response = self.opener.open("https://wwws.mint.com/logout.event")         

def getOptions():
    arguments = OptionParser()
    arguments.add_options(["--username", "--password", "--file"])
    arguments.set_default("file", "mint_transactions.csv")
    return arguments.parse_args()[0] # options

def create_csv():
    options = getOptions()
    mint = mintlib()
    # instead of using options from the command line. Just going to hardcode username and pwd.
    # mint.login(options.username, options.password)
    mint.login(mint_username, mint_password)
    mint.download(options.file)

    csv_data = csv.reader(file('mint_transactions.csv'))
    x = 1
    for row in csv_data:
         x = x+1    

    print x

    if x == 38:
        create_csv()


if __name__ == '__main__':      
    create_csv()
    
    #connect to database and create database object called mydb
    mydb = MySQLdb.connect(host = db_host, user = db_user, passwd = db_password, db = db_schema)

    cursor = mydb.cursor()

    #check if table already exists.
    table_exists = "SELECT count(*) FROM information_schema.tables WHERE table_schema = '%s' AND table_name = '%s';" % (db_schema, db_table)
    cursor.execute(table_exists)

    data = cursor.fetchall()
    for row in data:
        number_of_tables = row[0]

    if number_of_tables == 1:   
        #drop table
        print "%s table already exists. Dropping table..." % db_table
        drop_table = "DROP TABLE %s ;" % db_table
        cursor.execute(drop_table)
        mydb.commit()
        print "Dropped the %s table from the %s schema." % (db_table, db_schema)

        #create table
        print "Creating table..."
        create_table = "CREATE TABLE %s (tx_date VARCHAR(100), description VARCHAR(100)," \
        "original_description VARCHAR(100), amount VARCHAR(100), transaction_type VARCHAR(100)," \
        "category VARCHAR(100),account_name VARCHAR(100),labels VARCHAR(100), notes VARCHAR(100));" % db_table
        cursor.execute(create_table)
        mydb.commit()
        print "Created %s." % db_table

    else:
        #create table
        print "Creating table..."
        create_table = "CREATE TABLE %s (tx_date VARCHAR(100), description VARCHAR(100)," \
        "original_description VARCHAR(100), amount VARCHAR(100), transaction_type VARCHAR(100)," \
        "category VARCHAR(100),account_name VARCHAR(100),labels VARCHAR(100), notes VARCHAR(100));" % db_table
        cursor.execute(create_table)
        mydb.commit()
        print "Created %s." % db_table 

    #Load CSV data to database.
    print "Loading data to table..."
    csv_data = csv.reader(file('mint_transactions.csv'))
    #skip 1st row in csv file since it's just the header.
    next(csv_data)

    for row in csv_data:
            cursor.execute("INSERT INTO transactions(tx_date,description,original_description,amount,transaction_type, category,account_name,labels,notes) VALUES(%s, %s, %s,%s, %s, %s,%s,%s,%s)", row)
            print row

    mydb.commit()
    print "Load successful!"

    cursor.close()
    mydb.close()

       
    print "Done"
