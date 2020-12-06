import mysql.connector
from mysql.connector import errorcode
import logging as log


class Part:
    def __init__(self, dictionary,TableName = None):
        for key in dictionary:
            try:
                dictionary[key] = dictionary[key].decode("utf-8") 
            except (UnicodeDecodeError, AttributeError):
                pass

        self.dictionary = dictionary 
        
        self.TableName = TableName
        self.box = dictionary['Box']
        self.stock = dictionary['Stock']
        self.part_number = dictionary['Part Number']
        self.schlib = dictionary['Library Ref']
        self.pcblib = dictionary['Footprint Ref']
        self.datasheet = dictionary['HelpURL']
        try:
            self.supplier = dictionary['Supplier 1']
        except:
            self.supplier = ''

        try:
            self.supplier_part_number = dictionary['Supplier Part Number 1'] 
        except:
            self.supplier_part_number = ''

        self.help_url = dictionary['HelpURL']
        self.manufacturer = dictionary['Manufacturer']
        self.manufacturer_part_number = dictionary['Manufacturer Part Number']
    def __repr__(self):
        return 'Part {} {}'.format(self.dictionary['Part Number'],self.dictionary['Manufacturer'])

class AltiumDatabase:
    def __init__(self,downloadAll = True):
        verbose = True

        if verbose:
            log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        else:
            log.basicConfig(format="%(levelname)s: %(message)s")

        if downloadAll == True:
            cursor = self.Connect()

            if cursor != None:
                self.database = list()
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                log.info("Fetched {} Tables".format(len(tables)))
                
                for table in tables:
                    name = table[0]
                    ##print(name)
                    cursor.execute("SELECT * FROM `" + name + "`;")
                    rows = cursor.fetchall()

                    num_fields = len(cursor.description)
                    field_names = [i[0] for i in cursor.description]

                    before = len(self.database)

                    for i in rows:
                        self.database.append(Part(dict(zip(field_names,i)),name))

                    after = len(self.database)
                    log.info("{}: {} Components".format(name,after-before))
                cursor.close()

    def getPartFromDatabase(self,PartName):
        for part in self.database:
            if part.part_number == PartName:
                return part
        return None

    def GetPartNumbers(self):
        cursor = self.Connect()
        PartNumbers = []
        if cursor != None:
            self.database = list()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            log.info("Fetched {} Tables".format(len(tables)))
            Field = 'Part Number'
            SelectList = []
            FromList = []
            # for table in tables:
            #     SelectList.append("(SELECT `Part Number` from `"+table[0]+"` )")
            SelectList=["(SELECT `Part Number` from `"+table[0]+"` )" for table in tables]
            cursor.execute(' UNION '.join(SelectList))
            rows = cursor.fetchall()
            PartNumbers.extend([x[0] for x in rows])
            return PartNumbers

    def SearchPart(self, PartNumber = ""):
        cursor = self.Connect()
        if cursor != None:
            self.database = list()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            log.info("Fetched {} Tables".format(len(tables)))
            for table in tables:
                cursor.execute("SELECT * FROM `" + table[0] + "` WHERE `Part Number`='"+PartNumber + "'")
                rows = cursor.fetchall()
                if(len(rows)):
                    field_names = [i[0] for i in cursor.description]
                    p=Part(dict(zip(field_names,rows[0])),table[0])
                    return p
        return None
    
    def CorrectTables(self):
        cursor = self.Connect('Altium_Edit@altiumlib','Altium123')
        if cursor != None:
            self.database = list()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            log.info("Fetched {} Tables".format(len(tables)))
           
            RequiredFields = {
                "Box": "TEXT",
                "Stock": "INT"
            }
           
            for key in RequiredFields:
                for table in tables:
                    cursor.execute("DESCRIBE `" + table[0] + "`")    
                    Fields = cursor.fetchall()
                    FieldNames = [i[0] for i in Fields]
                    if (key in FieldNames) == False:
                        ##create proper field in table
                        print("No field, need to create")
                        cursor.execute("ALTER TABLE `" + table[0] + "`" + "ADD COLUMN `"+key+"` "+RequiredFields[key])
                
    def AdjustStock(self,PartNumber,Box,Stock):
        print("Here")
        part = self.SearchPart(PartNumber)
        if part != None:
            cursor = self.Connect('Altium_Edit@altiumlib','Altium123')
            if cursor != None:
                if Box != None:
                    part.box = Box
                sql = "UPDATE `%s` SET `%s` = '%s', `%s` = '%s' WHERE `Part Number` = '%s'"
                val = (part.TableName, "Box", part.box, "Stock", Stock, PartNumber)
                command = sql%val
                cursor.execute(command)
                self.connection.commit()
                print(cursor.rowcount, "record(s) affected")
    
    def AdjustStockMultiple(self,rowList): #Box, PartNumber, Stock
        self.__init__(True)
        cursor = self.Connect('Altium_Edit@altiumlib','Altium123')
        #get parts that are in database
        ret = []
        for x in rowList:
            part = self.getPartFromDatabase(x[1])
            if part != None:
                print("Found part: {}".format(part.part_number))
                cursor = self.Connect('Altium_Edit@altiumlib','Altium123')
                if cursor != None:
                    sql = "UPDATE `%s` SET `%s` = '%s', `%s` = '%s' WHERE `Part Number` = '%s'"
                    val = (part.TableName, "Box", x[0], "Stock", x[2], x[1])
                    command = sql%val
                    cursor.execute(command)
                    self.connection.commit()
                    print(cursor.rowcount, "record(s) affected")


    def Disconnect(self):
        try:
            self.connection.commit()
            # self.cursor.close()
            self.connection.close()
        except (AttributeError):
            pass

    def Connect(self,User='Altium@altiumlib',pswd='Altium123'):
        # Obtain connection string information from the portal
        
        config = {
        'host':'altiumlib.mysql.database.azure.com',
        'user':User,
        'password':pswd,
        'database':'Library'
        # ,
        # 'ssl_ca':'BaltimoreCyberTrustRoot.crt.pem'
        }

        # Construct connection string
        try:        
            self.connection = mysql.connector.connect(**config)
            log.info("Connection established")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                log.error("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                log.error("Database does not exist")
            else:
                log.error(err)
            return None
        else:
             return self.connection.cursor()
        

if __name__ == "__main__":
    conn = AltiumDatabase(False)
    conn.AdjustStock("XAL6030-332MEB",None,10)
    #conn.CorrectTables()
    #stats = conn.Statistics()