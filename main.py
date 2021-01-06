import random
import string
import datetime

from faker import Faker

fake = Faker()

############### Unique For Gal ##############
from sql_packages.sql_Server_Connection import Sql_Server_DataBase
DB_For_Project = Sql_Server_DataBase("LAPTOP-E1556I4A\SQLEXPRESS", "AirBNB")


############### Random Info Function #######################

def get_Random_Password():
    password_Length = int(random.choice([10, 11, 12, 13, 14, 15, 16]))
    password_characters = string.ascii_letters
    password_numbers = string.digits
    password = []

    for x in range(int(password_Length / 2)):
        password.append(random.choice(password_characters))
        password.append(random.choice(password_numbers))

    return ''.join(password)


def getRandomBirthDate():
    start_date = datetime.date(1940, 1, 1)
    end_date = datetime.date(2005, 2, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return str(random_date)


def random_Product():
    product_DF = DB_For_Project.query_To_Pandas('SELECT ProductID FROM Products')
    product_id_list = product_DF['ProductID'].tolist()

    return str(random.choice(product_id_list))


def random_Property():
    property_DF = DB_For_Project.query_To_Pandas('SELECT PropertyID FROM Properties')
    property_id_list = property_DF['PropertyID'].tolist()

    return str(random.choice(property_id_list))


def random_Live_Experience():
    live_experiences_DF = DB_For_Project.query_To_Pandas('SELECT LiveExperienceID FROM LiveExperiences')
    live_experiences_list = live_experiences_DF['LiveExperienceID'].tolist()

    return str(random.choice(live_experiences_list))


def random_Online_Experience():
    online_experiences_DF = DB_For_Project.query_To_Pandas('SELECT OnlineExperienceID FROM OnlineExperiences')
    online_expreriences_list = online_experiences_DF['OnlineExperienceID'].tolist()

    return str(random.choice(online_expreriences_list))


def random_ip_and_datetime():
    searchs_DF = DB_For_Project.query_To_Pandas('SELECT IPAddress,[DT-search], type FROM Searchs')
    ip_list = searchs_DF['IPAddress'].tolist()
    dt_list = searchs_DF['DT-search'].tolist()
    type_list = searchs_DF['type'].tolist()
    search_id_list = []

    for i in range(len(ip_list)):
        search_id_list.append([ip_list[i], dt_list[i], type_list[i]])

    return random.choice(search_id_list)


def random_ip_and_dt_not_ordered(counter):
    searchs_DF = DB_For_Project.query_To_Pandas('select IPAddress,[DT-search],type from Searchs except select '
                                                's.IPAddress,s.[DT-search], s.type from Orders as o join PaymentMethods'
                                                ' as pay on o.creditcardnumber=pay.CardNumber join Searchs as s on '
                                                'pay.[DT-Search]=s.[DT-search] and pay.IPAddress=s.IPAddress')
    ip_list = searchs_DF['IPAddress'].tolist()
    dt_list = searchs_DF['DT-search'].tolist()
    type_list = searchs_DF['type'].tolist()
    search_id_list = []
    for i in range(len(ip_list)):
        search_id_list.append([ip_list[i], dt_list[i], type_list[i]])

    return search_id_list[counter]


def random_Orders(counter):
    orders_customers_join_DF = DB_For_Project.query_To_Pandas(
        'select S.Email, O.OrderID from Orders as o join paymentmethods as pay on o.creditcardnumber=pay.CardNumber '
        'join Searchs as S on pay.IPAddress=S.IPAddress and pay.[DT-Search]=s.[DT-search] join Customers as c on'
        ' c.Email=s.Email order by OrderID')

    order_id_list = orders_customers_join_DF['OrderID'].tolist()
    email_list = orders_customers_join_DF['Email'].tolist()

    return [order_id_list[counter], email_list[counter]]


def random_Email_Customers():
    customersDF = DB_For_Project.query_To_Pandas('SELECT Email FROM Customers')
    customer_id_list = customersDF['Email'].tolist()

    return random.choice(customer_id_list)


def random_Locaion():
    locations_DF = DB_For_Project.query_To_Pandas('SELECT LocationID FROM Locations')
    location_id_list = locations_DF['LocationID'].tolist()

    return str(random.choice(location_id_list))


def random_payment_method():
    payment_method_DF = DB_For_Project.query_To_Pandas('SELECT cardNumber FROM PaymentMethods')
    payment_method_list = payment_method_DF['cardNumber'].tolist()
    return str(random.choice(payment_method_list))


def random_language():
    languages = ['English', 'French', 'German', 'Japanese', 'Italian', 'Russian', 'Spanish', 'Chinese (Simplified)',
                 'Arabic',
                 'Hindi', 'Portuguese', 'Turkish', 'Indonesian', 'Dutch', 'Korean', 'Bengali', 'Thai', 'Punjabi',
                 'Greek',
                 'Sign', 'Hebrew', 'Polish', 'Malay', 'Tagalog', 'Danish', 'Swedish', 'Norwegian', 'Finnish', 'Czech',
                 'Hungarian', 'Ukrainian']

    return random.choice(languages)


############### End Of Random Info Function #######################

def insertCUSTOMERS():

    for i in range(600):
        email = fake.email()
        firstName = fake.first_name()
        lastName = fake.last_name()
        password = get_Random_Password()
        birthDate = getRandomBirthDate()

        query_string = 'INSERT INTO Customers VALUES (\'' + email + '\', ' \
                                                                    '\'' + password + '\',' \
                                                                                      '\'' + firstName + '\',' \
                                                                                                         '\'' + lastName + '\',' \
                                                                                                                           '\'' + birthDate + '\');'
        try:
            print(query_string)
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()
        except Exception as e:
            print(e)


def insertLOCATIONS():
    location_id_counter = 1

    countries_dict = {'Argentina': ['Buenos Aires', 'Cordoba', 'Rosario', 'Mendoza', 'Mar del' 'Plata', 'Salta'],
                      'Brazil': ['Rio de Janeiro', 'Salvador', 'Fortaleza', 'Manaus', 'Porto Alegre', 'Natal',
                                 'Osasco'],
                      "Germany": ["Berlin", "Munich", "Cologne", "Dortmund", "Hamburg", "Bremen", "Hanover", "Bochum"],
                      "Spain": ["Madrid", "Barcelona", "Valencia", "Bilbao", "Las Palmas"],
                      "Israel": ["Tel Aviv", "Haifa", "Eilat", "Beer Sheva", "Jerusalem"],
                      "USA": ["New York", "Los Angeles", "Chicago", "San Antonio", "Philadelphia", "Dallas",
                              "San Diego",
                              "Austin", "San Jose", "El Paso", "Boston", "Denver", "Las Vegas", "Mesa", "Atlanta"],
                      "Russia": ["Moscow", "Kazan", "Novosibirsk", "Omsk", "Ufa", "Perm"]
                      }

    for i in range(800):
        countries = list(countries_dict.keys())
        location_id = location_id_counter
        country = random.choice(list(countries_dict.keys()))
        city = random.choice(countries_dict.get(country))
        street = fake.street_name()
        house_num = random.randrange(200)
        zip_code = fake.postcode()

        query_string = 'INSERT INTO Locations VALUES (' + str(
            location_id) + ', \'' + country + '\' , \'' + city + '\' , \'' + street + '\', ' + str(
            house_num) + ', \'' + zip_code + '\');'
        print(query_string)
        try:
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()
            location_id_counter += 1

        except Exception as e:
            print(e)


def insertPRODUCTS():
    product_id_counter = 0

    for i in range(400):
        price = round(random.uniform(30.0, 1000.9), 2)
        host_email = random_Email_Customers()

        query_string = 'INSERT INTO Products VALUES(' + str(product_id_counter) + ', ' + str(
            price) + ', \'' + host_email + '\', NULL);'
        print(query_string)
        try:
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()
            product_id_counter += 1
        except Exception as e:
            print(e)


def insertREVIEWS():
    order_id_counter = 1
    for i in range(600):
        try:
            order_customer_list = random_Orders(order_id_counter)
            email = order_customer_list[1]
            review_datetime = fake.date_time_this_year()
            rating = random.randrange(1, 6)
            description = fake.text(30)
            order_id = order_customer_list[0]
            query_string = 'INSERT INTO Reviews VALUES(\'' + email + '\', \'' + str(
                review_datetime) + '\', ' + str(rating) + ', \'' + description + '\', ' + str(order_id) + ');'
            print(query_string)
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()
            order_id_counter += random.choice([1, 2])
        except Exception as e:
            print(e)


def insertSEARCHS():
    for i in range(1500):
        try:
            ip_address = fake.ipv4_private()
            email = random_Email_Customers()
            type = random.choice(['Online Experience', 'Live Experience', 'Property'])
            number_of_guests = str(random.randint(1,5))
            dt_search = fake.date_time_this_century()
            dt_start = dt_search + datetime.timedelta(days=random.randrange(3, 100))
            dt_end = dt_start + datetime.timedelta(days=random.randrange(1, 14))

            query_string = 'INSERT INTO Searchs VALUES(\'' + ip_address + '\', \'' + email + '\', \'' + str(
                dt_search) + '\',  \'' + type + '\' , '+ str(number_of_guests) +',\'' + str(dt_start.date()) \
                           + '\' , \' ' + str(dt_end.date()) + '\');'

            print(query_string)
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()
        except Exception as e:
            print(e)


def insertPROPERTIES():
    property_id_counter = 0

    for i in range(170):
        property_id = str(property_id_counter)
        style = random.choice(['Apartment', 'Penthouse', 'Private House'])
        number_bedrooms = random.randrange(1, 5)
        number_bathrooms = str(random.randrange(1, number_bedrooms + 1))
        guest_capacity = str(random.randrange(number_bedrooms, number_bedrooms * 2))
        location = str(random_Locaion())
        query_string = 'INSERT INTO Properties VALUES(' + property_id + ', \'' + style + '\', ' + str(
            number_bedrooms) + ', ' + number_bathrooms + ' ,' + guest_capacity + ', ' + location + ');'

        print(query_string)
        DB_For_Project.send_Query(query_string)
        DB_For_Project.myDB.commit()
        property_id_counter += 1


def insertSERVICES():
    for i in range(300):
        property_id = random_Property()
        service = random.choice(['WIFI', 'Swimming Pool', 'Hot water', 'AC', 'valet', 'Elevator', 'Garden'])

        query_string = 'INSERT INTO Services VALUES(' + property_id + ', \'' + service + '\');'
        print(query_string)
        try:
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()
        except Exception as e:
            print('exception: ' + str(e))


def insertMEASURES():
    for i in range(300):
        property_id = random_Property()
        measure = random.choice(['Fire Extinguisher', 'Fire Alarm', 'Fire Escape stairs', 'Guard'])

        query_string = 'INSERT INTO SecurityMeasures VALUES(' + property_id + ', \'' + measure + '\');'
        print(query_string)
        try:
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()
        except Exception as e:
            print('exception: ' + str(e))


def insertORDERS():
    order_id_counter = 1

    for i in range(1400):
        order_id = str(order_id_counter)
        product_id = random_Product()
        search_id = random_ip_and_datetime()
        dt_buy = search_id[1] + datetime.timedelta(days=random.randrange(0, 2))
        payment_method = random_payment_method()
        query_string = 'INSERT INTO Orders VALUES(' + order_id + ', ' + product_id + ', \'' + str(dt_buy) + '\', \'' + payment_method + '\');'
        print(query_string)
        try:
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()
            order_id_counter += 1
        except Exception as e:
            print(e)


def insert_Live_Experiences():
    product_id_counter = 169

    for i in range(130):
        live_id = str(product_id_counter)
        description = fake.text(30)
        duration = str(random.randrange(10, 100))
        tonnage = 0
        max_capacity = random.randint(10,40)
        location = random_Locaion()
        query_string = 'INSERT INTO LiveExperiences VALUES(' + live_id + ', \'' + description + '\', ' + duration \
                       + ', '+ str(tonnage) + ', ' + str(max_capacity) + ', ' + location + ');'
        print(query_string)

        try:
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()
            product_id_counter += 1
        except Exception as e:
            print(e)


def insert_Online_Experiences():
    product_id_counter = 300

    for i in range(120):
        online_id = str(product_id_counter)
        tonnage = random.randrange(0, 50)
        max_capacity = str(random.randrange(tonnage, tonnage + 20))
        query_string = 'INSERT INTO OnlineExperiences VALUES(' + online_id + ', ' + str(
            tonnage) + ', ' + max_capacity + ');'
        try:
            print(query_string)
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()
            product_id_counter += 1
        except Exception as e:
            print(e)


def insert_Live_Languages():
    for i in range(150):
        live_id = random_Live_Experience()
        language = random_language()

        try:
            query_string = 'INSERT INTO LiveLanguages VALUES(' + live_id + ', \'' + language + '\');'
            print(query_string)
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()

        except Exception as e:
            print('exception: ' + str(e))


def insert_Online_Languages():
    for i in range(150):
        online_id = random_Online_Experience()
        language = random_language()

        try:
            query_string = 'INSERT INTO OnlineLanguages VALUES(' + online_id + ', \'' + language + '\');'
            print(query_string)
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()

        except Exception as e:
            print('exception: ' + str(e))


def insert_Payment_Methods():
    order_id_counter = 1
    for i in range(1600):
        card_provider = random.choice(['visa', 'amex', 'mastercard'])
        card_number = str(fake.credit_card_number(card_type=card_provider))
        experation_date = random.choice([str(fake.credit_card_expire()[0:3]) + random.choice(['18', '19', '20', '21', '22']), str(fake.credit_card_expire())])
        search_id = random_ip_and_datetime()
        ip_address = search_id[0]
        dt_search = str(search_id[1])
        query_string = 'INSERT INTO [PaymentMethods] VALUES(\'' + card_number + '\', \'' + experation_date + '\',  \'' + card_provider + '\', \'' + ip_address + '\', \'' + dt_search + '\');'
        print(query_string)
        try:
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()
            order_id_counter += 1
        except Exception as e:
            print(e)


def insert_Retrieved():
    for i in range(600):
        try:
            search_id = random_ip_and_dt_not_ordered(i)
            ip_address = str(search_id[0])
            dt_search = str(search_id[1])
            if search_id[2] == 'Online Experience':
                product_id = str(random_Online_Experience())
            elif search_id[2] == 'Live Experience':
                product_id = str(random_Live_Experience())
            else:
                product_id = str(random_Property())

            query_string = 'INSERT INTO Retrieved VALUES(\'' + str(
                ip_address) + '\', \'' + dt_search + '\', ' + product_id + ');'
            print(query_string)
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()
        except Exception as e:
            print(e)


def insert_Favorites():
    for i in range(700):
        email = random_Email_Customers()
        product_id = random_Product()
        dt_add = str(fake.date_time_this_year())
        query_string = 'INSERT INTO Favorites VALUES(\'' + email + '\', ' + product_id + ', \'' + dt_add + '\');'
        print(query_string)
        try:
            DB_For_Project.send_Query(query_string)
            DB_For_Project.myDB.commit()
        except Exception as e:
            print(e)


def insert_Distinct_Lookups():
    insert_countries = 'insert into Countries select distinct country from Locations'
    insert_cities = 'insert into Cities select distinct city from Locations'
    DB_For_Project.send_Query(insert_countries)
    DB_For_Project.myDB.commit()


insertCUSTOMERS()
insertLOCATIONS()
insertPRODUCTS()
insertSEARCHS()
insertPROPERTIES()
insert_Live_Experiences()
insert_Online_Experiences()
insertSERVICES()
insertMEASURES()
insert_Payment_Methods()
insertORDERS()
insertREVIEWS()
insert_Live_Languages()
insert_Online_Languages()
insert_Retrieved()
insert_Favorites()
insert_Distinct_Lookups()
