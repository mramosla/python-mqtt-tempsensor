# made with condo env pymqtt

import json
import mysql.connector
from mysql.connector import Error

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
    cursor.execute(sql_select_query, (phone,))
    record = cursor.fetchall()

    if not cursor.rowcount:
      print("Row empty")
      firstname = "Unknown"
      lastname = "Recipient"

      # create dict
      contact_info = {
        "firstname": firstname,
        "lastname": lastname,
        "phone": phone,
        "msg": message,
        "timestamp": timestamp
      }

      print("Contact Info If: ", contact_info)

      # Convert dict to json
      json_data = json.dumps(contact_info)
      print("JSON Data If: ", json_data)

      return json_data

    for row in record:
      print(row)
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
