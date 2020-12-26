import random
import string
import datetime
from my_DB_Packages.mysql_db_connector import Mysql_DataBase
from faker import Faker

fake = Faker()

DB_For_Project = Mysql_DataBase("localhost", "root", "Bg8187915", "DB_For_Project", "3306")


def getRandomPassword():
    passwordLength = int(random.choice([10, 11, 12, 13, 14, 15, 16]))
    password_characters = string.ascii_letters + string.digits
    password = []

    for x in range(passwordLength):
        password.append(random.choice(password_characters))

    return ''.join(password)


def getRandomBirthDate():
    import datetime

    start_date = datetime.date(year=1940, month=1, day=1)
    end_date = datetime.date(year=2005, month=1, day=1)
    date = fake.date_between(start_date=start_date, end_date=end_date)

    return date


def listToQueryString(lst):
    var_string = ', '.join(lst)
    query_string = 'INSERT INTO table VALUES (%s);' % var_string
    return query_string


def insertCUSTOMERS():
    import names

    for i in range(900):
        email = fake.email()
        firstName = names.get_first_name()
        lastName = names.get_last_name()
        password = getRandomPassword()
        birthDate = str(getRandomBirthDate())

        varlist = [email, password, firstName, lastName, birthDate]

        query_string = 'INSERT INTO Customers VALUES (\'' + email + '\', ' \
                                                                    '\'' + password + '\',' \
                                                                                      '\'' + firstName + '\',' \
                                                                                                         '\'' + lastName + '\',' \
                                                                                                                           '\'' + birthDate + '\');'
        DB_For_Project.sendQuery(query_string)
        DB_For_Project.myDB.commit()
        DB_For_Project.queryToPandas('select * from Customers')
        DB_For_Project.myDB.commit()


def insertLOCATIONS():
    location_id_counter = 1

    for i in range(800):
        location_id = location_id_counter
        country = fake.country()
        city = fake.city()
        street = fake.street_name()
        house_num = random.randrange(200)
        zip_code = fake.ipv4_private()

        query_string = 'INSERT INTO Locations VALUES (' + str(
            location_id) + ', \'' + country + '\' , \'' + city + '\' , \'' + street + '\', ' + str(
            house_num) + ', \'' + zip_code + '\');'
        print(query_string)
        try:
            DB_For_Project.sendQuery(query_string)
            DB_For_Project.myDB.commit()
            location_id_counter += 1

        except:
            print('problem with query')

def random_Email_Customers():
    customersDF = DB_For_Project.queryToPandas('SELECT Email FROM Customers')
    customer_id_list = customersDF['Email'].tolist()

    return random.choice(customer_id_list)


def random_Locaion():
    locations_DF = DB_For_Project.queryToPandas('SELECT LocationID FROM Locations')
    location_id_list = locations_DF['LocationID'].tolist()

    return str(random.choice(location_id_list))


def insertPRODUCTS():
    product_id_counter = 11

    for i in range(960):
        price = round(random.uniform(30.0, 1000.9), 2)
        host_email = random_Email_Customers()

        product_id_counter += 1

        query_string = 'INSERT INTO Products VALUES(' + str(product_id_counter) + ', ' + str(
            price) + ', \'' + host_email + '\');'

        DB_For_Project.sendQuery(query_string)
        DB_For_Project.myDB.commit()


def insertREVIEWS():
    for i in range(1000):
        host_email = random_Email_Customers()
        review_datetime = fake.date_time_this_year()
        rating = random.randrange(1, 6)
        description = fake.text(30)

        query_string = 'INSERT INTO Reviews VALUES(\'' + host_email + '\', \'' + str(review_datetime) + '\', ' + str(
            rating) + ', \'' + description + '\');'

        DB_For_Project.sendQuery(query_string)
        DB_For_Project.myDB.commit()


def insertSEARCHS():
    for i in range(1000):
        ip_address = fake.ipv4_private()
        email = random_Email_Customers()
        dt_search = fake.date_time_this_year()
        dt_start = dt_search + datetime.timedelta(days=random.randrange(3, 100))
        dt_end = dt_start + datetime.timedelta(days=random.randrange(1, 14))

        query_string = 'INSERT INTO Searchs VALUES(\'' + ip_address + '\', \'' + email + '\', \'' + str(
            dt_search) + '\', \'' + str(dt_start.date()) + '\' , \' ' + str(dt_end.date()) + '\');'

        DB_For_Project.sendQuery(query_string)
        DB_For_Project.myDB.commit()


def insertPROPERTIES():
    property_id_counter = 12

    for i in range(189):
        property_id = str(property_id_counter)
        style = random.choice(['Apartment', 'Penthouse', 'Private House'])
        number_bedrooms = random.randrange(1, 5)
        number_bathrooms = str(random.randrange(1, number_bedrooms + 1))
        guest_capacity = str(random.randrange(number_bedrooms, number_bedrooms * 2))

        query_string = 'INSERT INTO Properties VALUES(' + property_id + ', \'' + style + '\', ' + str(
            number_bedrooms) + ', ' + number_bathrooms + ' ,' + guest_capacity + ');'
        DB_For_Project.sendQuery(query_string)
        DB_For_Project.myDB.commit()
        property_id_counter += 1


def random_Product():
    product_DF = DB_For_Project.queryToPandas('SELECT ProductID FROM Products')
    product_id_list = product_DF['ProductID'].tolist()

    return str(random.choice(product_id_list))


def random_Property():
    property_DF = DB_For_Project.queryToPandas('SELECT PropertyID FROM Properties')
    property_id_list = property_DF['PropertyID'].tolist()

    return str(random.choice(property_id_list))


def random_Live_Experience():
    live_experiences_DF = DB_For_Project.queryToPandas('SELECT LiveExperienceID FROM LiveExperiences')
    live_experiences_list = live_experiences_DF['LiveExperienceID'].tolist()

    return str(random.choice(live_experiences_list))


def random_Online_Experience():
    online_experiences_DF = DB_For_Project.queryToPandas('SELECT OnlineExperienceID FROM OnlineExperiences')
    online_experiences_list = online_experiences_DF['OnlineExperienceID'].tolist()

    return str(random.choice(online_experiences_list))


def insertSERVICES():
    for i in range(700):
        property_id = random_Property()
        service = random.choice(['WIFI', 'Swimming Pool', 'Hot water', 'AC'])

        query_string = 'INSERT INTO Services VALUES(' + property_id + ', \'' + service + '\');'
        print(query_string)
        try:
            DB_For_Project.sendQuery(query_string)
            DB_For_Project.myDB.commit()
        except Exception as e:
            print('exception: ' + str(e))


def insertMEASURES():
    for i in range(400):
        property_id = random_Property()
        measure = random.choice(['Fire Extinguisher', 'Fire Alarm', 'Fire Escape stairs', 'Guard'])

        query_string = 'INSERT INTO Services VALUES(' + property_id + ', \'' + measure + '\');'
        print(query_string)
        try:
            DB_For_Project.sendQuery(query_string)
            DB_For_Project.myDB.commit()
        except Exception as e:
            print('exception: ' + str(e))


def random_ip_and_datetime():
    searchs_DF = DB_For_Project.queryToPandas('SELECT IPAdress, `DT-search` FROM Searchs')
    ip_list = searchs_DF['IPAdress'].tolist()
    dt_list = searchs_DF['DT-search'].tolist()

    search_id_list = []

    for i in range(len(ip_list)):
        search_id_list.append([ip_list[i], dt_list[i]])

    return random.choice(search_id_list)


def insertORDERS():
    order_id_counter = 1

    for i in range(1000):
        order_id = str(order_id_counter)
        product_id = random_Product()
        dt_buy = str(fake.date_time_this_year())
        search_id = random_ip_and_datetime()
        ip_adress = search_id[0]
        dt_search = str(search_id[1])
        query_string = 'INSERT INTO Orders VALUES(' + order_id + ', ' + product_id + ', \'' + dt_buy + '\', \'' + str(
            ip_adress) + '\', \'' + dt_search + '\');'
        print(query_string)
        DB_For_Project.sendQuery(query_string)
        DB_For_Project.myDB.commit()
        order_id_counter += 1


def insert_Live_Experiences():
    product_id_counter = 201

    for i in range(299):
        live_id = str(product_id_counter)
        description = fake.text(30)
        duration = str(random.randrange(10, 100))
        location = random_Locaion()

        query_string = 'INSERT INTO LiveExperiences VALUES(' + live_id + ', \'' + description + '\', ' + duration + ', ' + location + ');'
        DB_For_Project.sendQuery(query_string)
        DB_For_Project.myDB.commit()
        product_id_counter += 1


def insert_Online_Experiences():
    product_id_counter = 500

    for i in range(471):
        online_id = str(product_id_counter)
        tonnage = random.randrange(0, 50)
        max_capacity = str(random.randrange(tonnage, tonnage + 20))
        location = 'NULL'
        query_string = 'INSERT INTO OnlineExperiences VALUES(' + online_id + ', ' + str(
            tonnage) + ', ' + max_capacity + ', ' + location + ');'

        DB_For_Project.sendQuery(query_string)
        DB_For_Project.myDB.commit()
        product_id_counter += 1


def insert_Live_Languages():
    for i in range(550):
        live_id = random_Live_Experience()
        language = fake.language_name()

        try:
            query_string = 'INSERT INTO LiveLanguages VALUES(' + live_id + ', \'' + language + '\');'
            print(query_string)
            DB_For_Project.sendQuery(query_string)
            DB_For_Project.myDB.commit()

        except Exception as e:
            print('exception: ' + str(e))


def insert_Online_Languages():

    for i in range(550):
        online_id = random_Online_Experience()
        language = fake.language_name()

        try:
            query_string = 'INSERT INTO OnlineLanguages VALUES(' + online_id + ', \'' + language + '\');'
            print(query_string)
            DB_For_Project.sendQuery(query_string)
            DB_For_Project.myDB.commit()

        except Exception as e:
            print('exception: ' + str(e))


print(DB_For_Project.queryToPandas('select * from customers'))

# insertCUSTOMERS()
# insertLOCATIONS()
# insertPRODUCTS()
# insertREVIEWS()
# insertSEARCHS()
# insertPROPERTIES()
# insertSERVICES()
# insertMEASURES()
# insertORDERS()
# insert_Live_Experiences()
# insert_Online_Experiences()
# insert_Live_Languages()
# insert_Online_Languages()

# def insert_Retrieved():
# #     search_id = random_ip_and_datetime()
# #     ip_address = str(search_id[0])
# #     dt_search = str(search_id[1])
# #     product_id = str(random_Product())
# #
# #     query_string = 'INSERT INTO Retrieved VALUES(\'' + str(ip_address) + '\', \'' + dt_search + '\', ' + product_id + ');'
# #     print(query_string)
# #     DB_For_Project.sendQuery(query_string)
# #     # DB_For_Project.myDB.commit()
# # insert_Retrieved()
