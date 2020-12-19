# made with condo env pymqtt

import json
import mysql.connector
from mysql.connector import Error


# This function querys Mysql for the First and Last name of the text recipent. 
def getSenderName(phone, message, timestamp):
  try:
    mySQLConnection = mysql.connector.connect(
      host= '10.8.10.1',
      user= 'ajccljk546',
      password= 'hAUpeSLKPjZ2MaBj',
      database= 'ajcccrm9843'
      )
    
    # phone = incoming_text["phone"]
    # print("Phone value: ", phone)
    # message = incoming_text["message"]

    cursor = mySQLConnection.cursor(buffered=True)
    sql_select_query = """SELECT firstname, lastname, mobile FROM vtiger_contactdetails where mobile= %s"""
    sql_select_query1 = """SELECT firstname, lastname, phone FROM vtiger_contactdetails where phone= %s"""
    sql_select_query2 = """SELECT contactsubscriptionid FROM vtiger_contactsubdetails where homephone= %s"""
    sql_select_query3 = """SELECT firstname, lastname FROM vtiger_contactdetails where contactid=%s"""

    cursor.execute(sql_select_query, (phone,))
    record = cursor.fetchall()

    if not cursor.rowcount:
      # print("Row empty")
      firstname = "Unknown"
      lastname = "Recipient"

      # If mobile number is empty then query phone number
      cursor.execute(sql_select_query1, (phone,))
      record = cursor.fetchall()
      print("Record mobile: ", record)

      # if phone number is empty query db table containing "homephone" and get contactsubscriptionid
      if not cursor.rowcount:
        cursor.execute(sql_select_query2, (phone,))
        record = cursor.fetchall()
        print("Record homephone contactsubscriptionid: ", record)

        # if homephone is empty Firstname = Unknown, Lastname = Recipient
        if not cursor.rowcount:
          firstname = "Unknown"
          lastname = "Recipient"
          new_record = (firstname, lastname, phone)
          print("New Record: ", new_record)
          print("New Record Type: ", type(new_record))
          # insert into list record[]
          record = []
          record.append(new_record)
          print("Record after tuple insert", record)
          for row in record:
            print("Print row: ", row)
            print("\n")
            print("Row type = ", type(row)) # type = Tuple

            
            print("\n")
            firstname = row[0]
            lastname = row[1]
            phone = row[2]
            print("Firstname: ", firstname)
            print("Lastname: ", lastname)
            print("Phone: ", phone)

            # create dict
            contact_info = {
              "firstname": firstname,
              "lastname": lastname,
              "phone": phone,
              "msg": message,
              "timestamp": timestamp
            }

            print("Contact Info: ", contact_info)

            # Convert dict to json
            json_data = json.dumps(contact_info)
            print("JSON Data: ", json_data)

            return json_data
          

        # Query database match contactsubscriptionid to clientid in contacts table
        # Then use clientid to get First and Last name
        print("Record type = ", type(record))

        # remove unwanted character from record to get client id
        bad_chars = ['(', ')', ',', ' ']
        record_string = str(record[0])
        clientid = ''.join(i for i in record_string if not i in bad_chars)

        print("Record index 0: ", record[0])
        
        print("List to string: ", str(record[0]))
        test_text = "text_text"
        print("clientid:", test_text)
        cursor.execute(sql_select_query3, (clientid,))
        record = cursor.fetchall()
        print("Record clientid First Last Name: ", record)
        print("Record type homephone", type(record))

        # get record values and types in prep for new tuple
        print("index 0: ", record[0])
        index0 = record[0]
        sender_name = [n for n in index0]
        print("Sender Name Index0: ", sender_name[0])
        print("Type of Firstname: ", type(sender_name))
        firstname = sender_name[0]
        lastname = sender_name[1]
        print("Sender Name: ", firstname + " " + lastname)
        print("Phone Number: ", phone)

        # create tuple: new_record
        new_record = (firstname, lastname, phone)
        print("New Record: ", new_record)
        print("New Record Type: ", type(new_record))

        # insert into list record[]
        record = []
        record.append(new_record)
        print("Record after tuple insert", record)
        


    for row in record:
      print("Print row: ", row)
      print("\n")
      print("Row type = ", type(row)) # type = Tuple

      
      print("\n")
      firstname = row[0]
      lastname = row[1]
      phone = row[2]
      print("Firstname: ", firstname)
      print("Lastname: ", lastname)
      print("Phone: ", phone)

      # create dict
      contact_info = {
        "firstname": firstname,
        "lastname": lastname,
        "phone": phone,
        "msg": message,
        "timestamp": timestamp
      }

      print("Contact Info: ", contact_info)

      # Convert dict to json
      json_data = json.dumps(contact_info)
      print("JSON Data: ", json_data)

      return json_data


  except mysql.connector.Error as error:
    print("Failed to get record from MySQL table: {}".format(error))

  finally:
    if (mySQLConnection.is_connected()):
      cursor.close()
      mySQLConnection.close()
      print("MySQL connection is closed")

# phone = "626-388-4278"
# #phone = "626-533-3202"
# message = "Hello text"
# timestamp = "2019-11-05T12:29:50.11Z"


# getSenderName(phone, message, timestamp)
