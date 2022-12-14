import sqlite3
from user import User
from country import Country
from city import City
from hotel import Hotel
from tour import Tour
from tourist import Tourist
import Pyro4


@Pyro4.expose
class Agency:
    def __init__(self):
        self.users = dict()

        dbFile = 'TravelAgency.sqlite'
        self.db = sqlite3.connect(dbFile)
        self.cursor = self.db.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Users ( id INTEGER , name TEXT, login TEXT, password TEXT, role TEXT );')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Countries ( id INTEGER , name TEXT, region TEXT, language TEXT, currency TEXT, religion TEXT );')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Cities ( id INTEGER , name TEXT, country_id INTEGER, popuation INTEGER, airports INTEGER, climat TEXT );')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Hotels ( id INTEGER , name TEXT, city_id INTEGER, stars INTEGER, rooms INTEGER );')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Tours_for_sale ( id INTEGER , hotel_id INTEGER, people INTEGER, days INTEGER, food INTEGER, transport TEXT, price REAL );')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Selled_Tours ( id INTEGER , hotel_id INTEGER, people INTEGER, days INTEGER, food INTEGER, transport TEXT, price REAL );')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Tourists ( id INTEGER , name TEXT, tour_id INTEGER, age INTEGER, nationality TEXT );')


    @Pyro4.expose
    def verification(self, login, password):
        try:
            self.cursor.execute('SELECT * FROM Users WHERE login = ?', (login,))
            user = self.cursor.fetchall()
            if len(user) == 0:
                return ('No user with this login', False, 'Error')
            if user[0][3] == password:
                return ('Welcome, ' + user[0][1], True, user[0][4])
            else:
                return ('Incorrect password', False, 'Error')
        except:
            self.db.rollback()
            return ('Verification ERROR!', False, 'Error')


    @Pyro4.expose
    def registration(self, name, login, password, password_copy):
        if password != password_copy:
            return 'Check your password'
        self.cursor.execute('SELECT * FROM Users WHERE login = ?', (login,))
        user = self.cursor.fetchall()
        if len(user) > 0:
            return 'User with this login already exist'
        else:
            self.cursor.execute('SELECT MAX(id) FROM Users')
            maxId = self.cursor.fetchall()
            if maxId[0][0]:
                id = maxId[0][0] + 1
            else:
                id = 1
        try:
            self.cursor.execute('INSERT INTO Users (id, name, login, password, role) VALUES (?, ?, ?, ?, ?)',
                (id, name, login, password, 'user'))
            self.db.commit()
            return 'Registration successful'
        except:
            self.db.rollback()
            return 'Registration ERROR!'


    @Pyro4.expose
    def getCountries(self):
        ret = ''
        self.cursor.execute('SELECT * FROM Countries')
        results = self.cursor.fetchall()
        if len(results) == 0:
            return 'No countries in DB'

        for row in results:
            countryId = row[0]
            countryName = row[1]
            countryRegion = row[2]
            countryLanguage = row[3]
            countryCurrency = row[4]
            countryReligion = row[5]
            ret = ret + 'Country id: ' + str(countryId) + ', name: ' + countryName + ', region: ' + countryRegion + ', language: ' + countryLanguage + ', currency: ' + countryCurrency + ', religion: ' + countryReligion + '\n'
        return ret


    @Pyro4.expose
    def getCities(self):
        ret = ''
        self.cursor.execute('SELECT * FROM Cities')
        results = self.cursor.fetchall()
        if len(results) == 0:
            return 'No cities in DB'

        for row in results:
            cityId = row[0]
            cityName = row[1]
            self.cursor.execute('SELECT Countries.name FROM Countries JOIN Cities ON Countries.id = Cities.country_id WHERE Cities.id = ?', (cityId,))
            countryName = self.cursor.fetchone()[0]
            cityPopulation = row[3]
            cityAirports = row[4]
            cityClimat = row[5]
            ret = ret + 'City id: ' + str(cityId) + ', name: ' + cityName + ', country: ' + countryName + ', population: ' + str(cityPopulation) + ', airports number: ' + str(cityAirports) + ', climat: ' + cityClimat + '\n'
        return ret


    @Pyro4.expose
    def getHotels(self):
        ret = ''
        self.cursor.execute('SELECT * FROM Hotels')
        results = self.cursor.fetchall()
        if len(results) == 0:
            return 'No hotels in DB'

        for row in results:
            hotelId = row[0]
            hotelName = row[1]
            self.cursor.execute('SELECT Cities.name FROM Cities JOIN Hotels ON Cities.id = Hotels.city_id WHERE Hotels.id = ?', (hotelId,))
            cityName = self.cursor.fetchone()[0]
            hotelStars = row[3]
            hotelRooms = row[4]
            ret = ret + 'Hotel id: ' + str(hotelId) + ', name: ' + hotelName + ', city: ' + cityName + ', stars: ' + str(hotelStars) + ', rooms: ' + str(hotelRooms) + '\n'
        return ret

    @Pyro4.expose
    def getTours(self):
        ret = ''
        self.cursor.execute('SELECT * FROM Tours_for_sale')
        results = self.cursor.fetchall()
        if len(results) == 0:
            return 'No tours in DB'

        for row in results:
            tourId = row[0]
            self.cursor.execute('SELECT Hotels.name FROM Hotels JOIN Tours_for_sale ON Hotels.id = Tours_for_sale.hotel_id WHERE Tours_for_sale.id = ?', (tourId,))
            hotelName = self.cursor.fetchone()[0]
            tourPeople = row[2]
            tourDays = row[3]
            tourFood = row[4]
            tourTransport = row[5]
            tourPrice = row[6]
            tourAmount = row[7]
            ret = ret + 'Tour id: ' + str(tourId) + ', hotel: ' + hotelName + ', people: ' + str(tourPeople) + ', days: ' + str(tourDays) + ', meals per day: ' + str(tourFood) + ', transport: ' + tourTransport + ', price: ' + str(tourPrice) + ', amount: ' + str(tourAmount) + '\n'
        return ret

    @Pyro4.expose
    def getSelledTours(self):
        ret = ''
        self.cursor.execute('SELECT * FROM Selled_Tours')
        results = self.cursor.fetchall()
        if len(results) == 0:
            return 'No selled tours in DB'

        for row in results:
            tourId = row[0]
            self.cursor.execute('SELECT Hotels.name FROM Hotels JOIN Selled_Tours ON Hotels.id = Selled_Tours.hotel_id WHERE Selled_Tours.id = ?', (tourId,))
            hotelName = self.cursor.fetchone()[0]
            tourPeople = row[2]
            tourDays = row[3]
            tourFood = row[4]
            tourTransport = row[5]
            tourPrice = row[6]
            ret = ret + 'Tour id: ' + str(tourId) + ', hotel: ' + hotelName + ', people: ' + str(tourPeople) + ', days: ' + str(tourDays) + ', meals per day: ' + str(tourFood) + ', transport: ' + tourTransport + ', price: ' + str(tourPrice) + '\n'
        return ret

    @Pyro4.expose
    def getTourists(self):
        ret = ''
        self.cursor.execute('SELECT * FROM Tourists')
        results = self.cursor.fetchall()
        if len(results) == 0:
            return 'No tourists in DB'

        for row in results:
            touristId = row[0]
            touristName = row[1]
            tour_id = row[2]
            touristAge = row[3]
            touristNationality = row[4]
            ret = ret + 'Tourist id: ' + str(touristId) + ', name: ' + touristName + ', tour id: ' + str(tour_id) + ', age: ' + str(touristAge) + ', nationality: ' + touristNationality + '\n'
        return ret

    @Pyro4.expose
    def getCountry(self, country):
        try:
            self.cursor.execute('SELECT * FROM Countries WHERE id = ?', (country,))
            results = self.cursor.fetchall()
            if len(results) == 0:
                return 'Incorrect id'

            for row in results:
                countryId = row[0]
                countryName = row[1]
                countryRegion = row[2]
                countryLanguage = row[3]
                countryCurrency = row[4]
                countryReligion = row[5]
                return 'Country id: ' + str(countryId) + ', name: ' + countryName + ', region: ' + countryRegion + ', language: ' + countryLanguage + ', currency: ' + countryCurrency + ', religion: ' + countryReligion + '\n'
        except:
            self.db.rollback()
            return 'Country getting ERROR!'


    @Pyro4.expose
    def getCity(self, city):
        try:
            self.cursor.execute('SELECT * FROM Cities WHERE id = ?', (city,))
            results = self.cursor.fetchall()
            if len(results) == 0:
                return 'Incorrect id'

            for row in results:
                cityId = row[0]
                cityName = row[1]
                self.cursor.execute(
                    'SELECT Countries.name FROM Countries JOIN Cities ON Countries.id = Cities.country_id WHERE Cities.id = ?',
                    (cityId,))
                countryName = self.cursor.fetchone()[0]
                cityPopulation = row[3]
                cityAirports = row[4]
                cityClimat = row[5]
                return 'City id: ' + str(
                cityId) + ', name: ' + cityName + ', country: ' + countryName + ', population: ' + str(
                cityPopulation) + ', airports number: ' + str(cityAirports) + ', climat: ' + cityClimat + '\n'
        except:
            self.db.rollback()
            return 'City getting ERROR!'


    @Pyro4.expose
    def getHotel(self, hotel):
        try:
            self.cursor.execute('SELECT * FROM Hotels WHERE id = ?', (hotel,))
            results = self.cursor.fetchall()
            if len(results) == 0:
                return 'Incorrect id'

            for row in results:
                hotelId = row[0]
                hotelName = row[1]
                self.cursor.execute('SELECT Cities.name FROM Cities JOIN Hotels ON Cities.id = Hotels.city_id WHERE Hotels.id = ?',
                                    (hotelId,))
                cityName = self.cursor.fetchone()[0]
                hotelStars = row[3]
                hotelRooms = row[4]
                return 'Hotel id: ' + str(
                    hotelId) + ', name: ' + hotelName + ', city: ' + cityName + ', stars: ' + str(
                    hotelStars) + ', rooms: ' + str(hotelRooms) + '\n'
        except:
            self.db.rollback()
            return 'Hotel getting ERROR!'


    @Pyro4.expose
    def getTour(self, tour):
        try:
            self.cursor.execute('SELECT * FROM Tours_for_sale WHERE id = ?', (tour,))
            results = self.cursor.fetchall()
            if len(results) == 0:
                return 'Incorrect id'

            for row in results:
                tourId = row[0]
                self.cursor.execute(
                    'SELECT Hotels.name FROM Hotels JOIN Tours_for_sale ON Hotels.id = Tours_for_sale.hotel_id WHERE Tours_for_sale.id = ?',
                    (tourId,))
                hotelName = self.cursor.fetchone()[0]
                tourPeople = row[2]
                tourDays = row[3]
                tourFood = row[4]
                tourTransport = row[5]
                tourPrice = row[6]
                tourAmount = row[7]
                return 'Tour id: ' + str(tourId) + ', hotel: ' + hotelName + ', people: ' + str(
                    tourPeople) + ', days: ' + str(tourDays) + ', meals per day: ' + str(
                    tourFood) + ', transport: ' + tourTransport + ', price: ' + str(tourPrice) + ', amount: ' + str(tourAmount) + '\n'
        except:
            self.db.rollback()
            return 'Tour getting ERROR!'


    @Pyro4.expose
    def getTourPeople(self, tour):
        try:
            self.cursor.execute('SELECT people FROM Tours_for_sale WHERE id = ?', (tour,))
            results = self.cursor.fetchall()
            if len(results) == 0:
                return 'Incorrect id'

            for row in results:
                tourPeople = row[0]
                return tourPeople
        except:
            self.db.rollback()
            return 'Tour people getting ERROR!'


    @Pyro4.expose
    def getSelledTour(self, tour):
        try:
            self.cursor.execute('SELECT * FROM Selled_Tours WHERE id = ?', (tour,))
            results = self.cursor.fetchall()
            if len(results) == 0:
                return 'Incorrect id'

            for row in results:
                tourId = row[0]
                self.cursor.execute(
                    'SELECT Hotels.name FROM Hotels JOIN Selled_Tours ON Hotels.id = Selled_Tours.hotel_id WHERE Selled_Tours.id = ?',
                    (tourId,))
                hotelName = self.cursor.fetchone()[0]
                tourPeople = row[2]
                tourDays = row[3]
                tourFood = row[4]
                tourTransport = row[5]
                tourPrice = row[6]
                return 'Tour id: ' + str(tourId) + ', hotel: ' + hotelName + ', people: ' + str(
                    tourPeople) + ', days: ' + str(tourDays) + ', meals per day: ' + str(
                    tourFood) + ', transport: ' + tourTransport + ', price: ' + str(tourPrice) + '\n'
        except:
            self.db.rollback()
            return 'Tour getting ERROR!'


    @Pyro4.expose
    def getTourist(self, tourist):
        try:
            self.cursor.execute('SELECT * FROM Tourists WHERE id = ?', (tourist,))
            results = self.cursor.fetchall()
            if len(results) == 0:
                return 'Incorrect id'

            for row in results:
                touristId = row[0]
                touristName = row[1]
                tour_id = row[2]
                touristAge = row[3]
                touristNationality = row[4]
                return 'Tourist id: ' + str(touristId) + ', name: ' + touristName + ', tour id: ' + str(
                    tour_id) + ', age: ' + str(touristAge) + ', nationality: ' + touristNationality + '\n'
        except:
            self.db.rollback()
            return 'Tourist getting ERROR!'


    @Pyro4.expose
    def addCountry(self, name, region, language, currency, religion):
        self.cursor.execute('SELECT MAX(id) FROM Countries')
        maxId = self.cursor.fetchall()
        if maxId[0][0]:
            id = maxId[0][0] + 1
        else:
            id = 1

        try:
            self.cursor.execute('INSERT INTO Countries (id, name, region, language, currency, religion) VALUES (?, ?, ?, ?, ?, ?)', (id, name, region, language, currency, religion))
            self.db.commit()
            return 'Country added'
        except:
            self.db.rollback()
            return 'Country adding ERROR!'


    @Pyro4.expose
    def addCity(self, name, country_id, population, airports, climat):
        if self.getCountry(country_id) == 'Incorrect id':
            return 'Country does not exist!'
        self.cursor.execute('SELECT MAX(id) FROM Cities')
        maxId = self.cursor.fetchall()
        if maxId[0][0]:
            id = maxId[0][0] + 1
        else:
            id = 1

        try:
            self.cursor.execute('INSERT INTO Cities (id, name, country_id, population, airports, climat) VALUES (?, ?, ?, ?, ?, ?)', (id, name, country_id, population, airports, climat))
            self.db.commit()
            return 'City added'
        except:
            self.db.rollback()
            return 'City adding ERROR!'


    @Pyro4.expose
    def addHotel(self, name, city_id, stars, rooms):
        if self.getCity(city_id) == 'Incorrect id':
            return 'City does not exist!'
        self.cursor.execute('SELECT MAX(id) FROM Hotels')
        maxId = self.cursor.fetchall()
        if maxId[0][0]:
            id = maxId[0][0] + 1
        else:
            id = 1

        try:
            self.cursor.execute('INSERT INTO Hotels (id, name, city_id, stars, rooms) VALUES (?, ?, ?, ?, ?)', (id, name, city_id, stars, rooms))
            self.db.commit()
            return 'Hotel added'
        except:
            self.db.rollback()
            return 'Hotel adding ERROR!'


    @Pyro4.expose
    def addTour(self, hotel_id, people, days, food, transport, price, amount):
        if self.getHotel(hotel_id) == 'Incorrect id':
            return 'Hotel does not exist!'
        self.cursor.execute('SELECT MAX(id) FROM Tours_for_sale')
        maxId = self.cursor.fetchall()
        if maxId[0][0]:
            id = maxId[0][0] + 1
        else:
            id = 1

        try:
            self.cursor.execute('INSERT INTO Tours_for_sale (id, hotel_id, people, days, food, transport, price, avaliable) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (id, hotel_id, people, days, food, transport, price, amount))
            self.db.commit()
            return 'Tour added'
        except:
            self.db.rollback()
            return 'Tour adding ERROR!'


    @Pyro4.expose
    def addTourist(self, name, tour_id, age, nationality):
        self.cursor.execute('SELECT MAX(id) FROM Tourists')
        maxId = self.cursor.fetchall()
        if maxId[0][0]:
            id = maxId[0][0] + 1
        else:
            id = 1

        try:
            self.cursor.execute(
                'INSERT INTO Tourists (id, name, tour_id, age, nationality) VALUES (?, ?, ?, ?, ?)',
                (id, name, tour_id, age, nationality))
            self.db.commit()
            return 'Tourist added'
        except:
            self.db.rollback()
            return 'Tourist adding ERROR!'


    @Pyro4.expose
    def updateCountry(self, country, param, val):
        if self.getCountry(country) == 'Incorrect id':
            return 'Country does not exist!'
        if param == 1:
            sqlp = "name = '" + val + "'"
        elif param == 2:
            sqlp = "region = '" + val + "'"
        elif param == 3:
            sqlp = "language = '" + val + "'"
        elif param == 4:
            sqlp = "currency = '" + val + "'"
        else:
            sqlp = "religion = '" + val + "'"

        try:
            self.cursor.execute("UPDATE Countries SET " + sqlp + " WHERE id = " + str(country))
            self.db.commit()
            return 'Country updated'
        except:
            self.db.rollback()
            return 'Country updating ERROR!'


    @Pyro4.expose
    def updateCity(self, city, param, val):
        if self.getCity(city) == 'Incorrect id':
            return 'City does not exist!'
        if param == 1:
            sqlp = "name = '" + val + "'"
        elif param == 2:
            if self.getCountry(int(val)) == 'Incorrect id':
                return 'Country does not exist!'
            sqlp = "country_id = '" + val + "'"
        elif param == 3:
            sqlp = "population = '" + val + "'"
        elif param == 4:
            sqlp = "airports = '" + val + "'"
        else:
            sqlp = "climat = '" + val + "'"

        try:
            self.cursor.execute("UPDATE Cities SET " + sqlp + " WHERE id = " + str(city))
            self.db.commit()
            return 'City updated'
        except:
            self.db.rollback()
            return 'City updating ERROR!'


    @Pyro4.expose
    def updateHotel(self, hotel, param, val):
        if self.getHotel(hotel) == 'Incorrect id':
            return 'Hotel does not exist!'
        if param == 1:
            sqlp = "name = '" + val + "'"
        elif param == 2:
            if self.getCity(int(val)) == 'Incorrect id':
                return 'City does not exist!'
            sqlp = "city_id = '" + val + "'"
        elif param == 3:
            sqlp = "stars = '" + val + "'"
        else:
            sqlp = "rooms = '" + val + "'"

        try:
            self.cursor.execute("UPDATE Hotels SET " + sqlp + " WHERE id = " + str(hotel))
            self.db.commit()
            return 'Hotel updated'
        except:
            self.db.rollback()
            return 'Hotel updating ERROR!'


    @Pyro4.expose
    def updateTour(self, tour, param, val):
        if self.getTour(tour) == 'Incorrect id':
            return 'Tour does not exist!'
        if param == 1:
            if self.getHotel(int(val)) == 'Incorrect id':
                return 'Hotel does not exist!'
            sqlp = "hotel_id = '" + val + "'"
        elif param == 2:
            sqlp = "people = '" + val + "'"
        elif param == 3:
            sqlp = "days = '" + val + "'"
        elif param == 4:
            sqlp = "food = '" + val + "'"
        elif param == 5:
            sqlp = "transport = '" + val + "'"
        elif param == 6:
            sqlp = "price = '" + val + "'"
        else:
            sqlp = "avaliable = '" + val + "'"

        try:
            self.cursor.execute("UPDATE Tours_for_sale SET " + sqlp + " WHERE id = " + str(tour))
            self.db.commit()
            return 'Tour updated'
        except:
            self.db.rollback()
            return 'Tour updating ERROR!'


    @Pyro4.expose
    def deleteTour(self, tour):
        if self.getTour(tour) == 'Incorrect id':
            return 'Tour does not exist'

        try:
            self.cursor.execute('DELETE FROM Tours_for_sale WHERE id = ?', (tour,))
            self.db.commit()
            return 'Tour deleted'
        except:
            self.db.rollback()
            return 'Tour deleting ERROR!'


    @Pyro4.expose
    def deleteHotel(self, hotel):
        if self.getHotel(hotel) == 'Incorrect id':
            return 'Hotel does not exist'

        try:
            self.cursor.execute('SELECT id FROM Tours_for_sale WHERE hotel_id = ?', (hotel,))
            tours = self.cursor.fetchall()
            for tour in tours:
                mes = self.deleteTour(tour[0])
            self.cursor.execute('DELETE FROM Hotels WHERE id = ?', (hotel,))
            self.db.commit()
            return 'Hotel deleted'
        except:
            self.db.rollback()
            return 'Hotel deleting ERROR!'


    @Pyro4.expose
    def deleteCity(self, city):
        if self.getCity(city) == 'Incorrect id':
            return 'City does not exist'

        try:
            self.cursor.execute('SELECT id FROM Hotels WHERE city_id = ?', (city,))
            hotels = self.cursor.fetchall()
            for hotel in hotels:
                mes = self.deleteHotel(hotel[0])
            self.cursor.execute('DELETE FROM Cities WHERE id = ?', (city,))
            self.db.commit()
            return 'City deleted'
        except:
            self.db.rollback()
            return 'City deleting ERROR!'


    @Pyro4.expose
    def deleteCountry(self, country):
        if self.getCountry(country) == 'Incorrect id':
            return 'Country does not exist'

        try:
            self.cursor.execute('SELECT id FROM Cities WHERE country_id = ?', (country,))
            cities = self.cursor.fetchall()
            for city in cities:
                mes = self.deleteCity(city[0])
            self.cursor.execute('DELETE FROM Countries WHERE id = ?', (country,))
            self.db.commit()
            return 'Country deleted'
        except:
            self.db.rollback()
            return 'Country deleting ERROR!'


    @Pyro4.expose
    def getCountryCities(self, country):
        ret = ''
        self.cursor.execute('SELECT * FROM Cities WHERE country_id = ?', (country,))
        results = self.cursor.fetchall()
        if len(results) == 0:
            return 'No cities in this country or incorrect country id'

        for row in results:
            cityId = row[0]
            cityName = row[1]
            self.cursor.execute('SELECT Countries.name FROM Countries JOIN Cities ON Countries.id = Cities.country_id WHERE Cities.id = ?',(cityId,))
            countryName = self.cursor.fetchone()[0]
            cityPopulation = row[3]
            cityAirports = row[4]
            cityClimat = row[5]
            ret = ret + 'City id: ' + str(
                cityId) + ', name: ' + cityName + ', country: ' + countryName + ', population: ' + str(
                cityPopulation) + ', airports number: ' + str(cityAirports) + ', climat: ' + cityClimat + '\n'
        return ret


    @Pyro4.expose
    def getCityHotels(self, city):
        ret = ''
        self.cursor.execute('SELECT * FROM Hotels WHERE city_id = ?', (city,))
        results = self.cursor.fetchall()
        if len(results) == 0:
            return 'No hotels in this city or incorrect city id'

        for row in results:
            hotelId = row[0]
            hotelName = row[1]
            self.cursor.execute(
                'SELECT Cities.name FROM Cities JOIN Hotels ON Cities.id = Hotels.city_id WHERE Hotels.id = ?',
                (hotelId,))
            cityName = self.cursor.fetchone()[0]
            hotelStars = row[3]
            hotelRooms = row[4]
            ret = ret + 'Hotel id: ' + str(
                hotelId) + ', name: ' + hotelName + ', city: ' + cityName + ', stars: ' + str(
                hotelStars) + ', rooms: ' + str(hotelRooms) + '\n'
        return ret


    @Pyro4.expose
    def getHotelTours(self, hotel):
        ret = ''
        self.cursor.execute('SELECT * FROM Tours_for_sale WHERE hotel_id = ?', (hotel,))
        results = self.cursor.fetchall()
        if len(results) == 0:
            return 'No tours in this hotel or incorrect hotel id'

        for row in results:
            tourId = row[0]
            self.cursor.execute(
                'SELECT Hotels.name FROM Hotels JOIN Tours_for_sale ON Hotels.id = Tours_for_sale.hotel_id WHERE Tours_for_sale.id = ?',
                (tourId,))
            hotelName = self.cursor.fetchone()[0]
            tourPeople = row[2]
            tourDays = row[3]
            tourFood = row[4]
            tourTransport = row[5]
            tourPrice = row[6]
            tourAmount = row[7]
            ret = ret + 'Tour id: ' + str(
                tourId) + ', hotel name: ' + hotelName + ', people: ' + str(tourPeople) + ', days: ' + str(
                tourDays) + ', meals number: ' + str(tourFood) + ', transport: ' + tourTransport + ', price: ' + str(tourPrice) + ', amount: ' + str(tourAmount) + '\n'
        return ret


    @Pyro4.expose
    def buyTour(self, tour):
        self.cursor.execute('SELECT * FROM Tours_for_sale WHERE id = ?', (tour,))
        results = self.cursor.fetchall()
        if len(results) == 0:
            return 'Incorrect id'

        for row in results:
            tourId = row[0]
            hotel_id = row[1]
            tourPeople = row[2]
            tourDays = row[3]
            tourFood = row[4]
            tourTransport = row[5]
            tourPrice = row[6]
            tourAmount = row[7]
            if tourAmount == 1:
                self.deleteTour(tourId)
            else:
                self.updateTour(tourId, 7, str(tourAmount - 1))
            self.cursor.execute('SELECT MAX(id) FROM Selled_Tours')
            maxId = self.cursor.fetchall()
            if maxId[0][0]:
                id = maxId[0][0] + 1
            else:
                id = 1
            self.cursor.execute(
                'INSERT INTO Selled_Tours (id, hotel_id, people, days, food, transport, price) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (id, hotel_id, tourPeople, tourDays, tourFood, tourTransport, tourPrice))
            self.db.commit()
            return ('Tour bought! Enjoy your trip!', id)


    @Pyro4.expose
    def getStatistic(self):
        try:
            f = open('statistic.txt', 'w')
            self.cursor.execute('SELECT COUNT(id) FROM Selled_Tours')
            tourBought = self.cursor.fetchone()[0]
            f.write('Money statistic:\n')
            f.write('Tours selled: ' + str(tourBought) + '\n')
            self.cursor.execute('SELECT SUM(price) FROM Selled_Tours')
            receipts = self.cursor.fetchone()[0]
            f.write('Total receipts: ' + str(receipts) + '$\n')
            self.cursor.execute('SELECT AVG(price) FROM Selled_Tours')
            avg_price = self.cursor.fetchone()[0]
            f.write('Average tour price: ' + str(avg_price) + '$\n')
            self.cursor.execute('SELECT MIN(price) FROM Selled_Tours')
            res = self.cursor.fetchone()
            self.cursor.execute('SELECT Selled_Tours.id, Selled_Tours.price, Hotels.name, Cities.name, Countries.name, Selled_Tours.people, Selled_Tours.days, Selled_Tours.food, Selled_Tours.transport FROM Selled_Tours JOIN Hotels ON Selled_Tours.hotel_id = Hotels.id JOIN Cities ON Hotels.city_id = Cities.id JOIN Countries ON Cities.country_id = Countries.id WHERE Selled_Tours.price = ?', (res[0],))
            min_price = self.cursor.fetchall()
            for row in min_price:
                f.write('Cheapest Tour: ' + str(row[0]) + ',    price: ' + str(row[1]) + ',    hotel: ' + str(row[2]) + ',    city: ' + str(row[3]) + ',    country: ' + str(row[4]) + ',    people: ' + str(row[5]) + ',    days: ' + str(row[6]) + ',    meals number: ' + str(row[7]) + ',    transport: ' + str(row[8]) + '\n')
            f.write('\n')
            self.cursor.execute('SELECT MAX(price) FROM Selled_Tours')
            res = self.cursor.fetchone()
            self.cursor.execute('SELECT Selled_Tours.id, Selled_Tours.price, Hotels.name, Cities.name, Countries.name, Selled_Tours.people, Selled_Tours.days, Selled_Tours.food, Selled_Tours.transport FROM Selled_Tours JOIN Hotels ON Selled_Tours.hotel_id = Hotels.id JOIN Cities ON Hotels.city_id = Cities.id JOIN Countries ON Cities.country_id = Countries.id WHERE Selled_Tours.price = ?', (res[0],))
            max_price = self.cursor.fetchall()
            for row in max_price:
                f.write('Most expensive Tour: ' + str(row[0]) + ',    price: ' + str(row[1]) + ',    hotel: ' + str(row[2]) + ',    city: ' + str(row[3]) + ',    country: ' + str(row[4]) + ',    people: ' + str(row[5]) + ',    days: ' + str(row[6]) + ',    meals number: ' + str(row[7]) + ',    transport: ' + str(row[8]) + '\n')
            f.write('\n\n')
            f.write('Transport statistic:\n')
            self.cursor.execute('SELECT transport, COUNT(id) FROM Selled_Tours GROUP BY transport')
            transports = self.cursor.fetchall()
            f.write('Tourists used ' + str(len(transports)) + ' types of transport\n')
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in transports:
                f.write(row[0] + ': ' + str(row[1]) + ' tours\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = row[0]
                elif row[1] == mostV:
                    most += (', ' + row[0])
                if row[1] < lessV:
                    lessV = row[1]
                    less = row[0]
                elif row[1] == lessV:
                    less += (', ' + row[0])
            f.write('Most popular tranports: ' + most + '.  It was used ' + str(mostV) + ' times\n')
            f.write('Less popular tranports: ' + less + '.  It was used ' + str(lessV) + ' times\n')
            f.write('\n\n')
            f.write('Food statistic:\n')
            self.cursor.execute('SELECT food, COUNT(id) FROM Selled_Tours GROUP BY food')
            foods = self.cursor.fetchall()
            f.write('Tourists used ' + str(len(foods)) + ' types of food menu\n')
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in foods:
                f.write(str(row[0]) + ': ' + str(row[1]) + ' tours\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = str(row[0])
                elif row[1] == mostV:
                    most += (', ' + str(row[0]))
                if row[1] < lessV:
                    lessV = row[1]
                    less = str(row[0])
                elif row[1] == lessV:
                    less += (', ' + str(row[0]))
            f.write('Most popular food menu: ' + most + '.  It was used ' + str(mostV) + ' times\n')
            f.write('Less popular food menu: ' + less + '.  It was used ' + str(lessV) + ' times\n')
            f.write('\n\n')
            f.write('Tours duration statistic:\n')
            self.cursor.execute('SELECT AVG(days) FROM Selled_Tours')
            avg_days = self.cursor.fetchone()[0]
            f.write('Average tour duration : ' + str(avg_days) + ' days\n')
            self.cursor.execute('SELECT MIN(days) FROM Selled_Tours')
            res = self.cursor.fetchone()
            self.cursor.execute('SELECT Selled_Tours.id, Selled_Tours.days, Selled_Tours.price, Hotels.name, Cities.name, Countries.name, Selled_Tours.people, Selled_Tours.food, Selled_Tours.transport FROM Selled_Tours JOIN Hotels ON Selled_Tours.hotel_id = Hotels.id JOIN Cities ON Hotels.city_id = Cities.id JOIN Countries ON Cities.country_id = Countries.id WHERE Selled_Tours.days = ?', (res[0],))
            min_days = self.cursor.fetchall()
            for row in min_days:
                f.write('Shortest Tour: ' + str(row[0]) + ',    duration: ' + str(row[1]) + ' days,    price: ' + str(row[2]) + ',    hotel: ' + str(row[3]) + ',    city: ' + str(row[4]) + ',    country: ' + str(row[5]) + ',    people: ' + str(row[6]) + ',    meals number: ' + str(row[7]) + ',    transport: ' + str(row[8]) + '\n')
            f.write('\n')
            self.cursor.execute('SELECT MAX(days) FROM Selled_Tours')
            res = self.cursor.fetchone()
            self.cursor.execute('SELECT Selled_Tours.id, Selled_Tours.days, Selled_Tours.price, Hotels.name, Cities.name, Countries.name, Selled_Tours.people, Selled_Tours.food, Selled_Tours.transport FROM Selled_Tours JOIN Hotels ON Selled_Tours.hotel_id = Hotels.id JOIN Cities ON Hotels.city_id = Cities.id JOIN Countries ON Cities.country_id = Countries.id WHERE Selled_Tours.days = ?', (res[0],))
            max_days = self.cursor.fetchall()
            for row in max_days:
                f.write('Longest Tour: ' + str(row[0]) + ',    duration: ' + str(row[1]) + ' days,    price: ' + str(row[2]) + ',    hotel: ' + str(row[3]) + ',    city: ' + str(row[4]) + ',    country: ' + str(row[5]) + ',    people: ' + str(row[6]) + ',    meals number: ' + str(row[7]) + ',    transport: ' + str(row[8]) + '\n')
            f.write('\n\n')
            f.write('Tourist group size statistic:\n')
            self.cursor.execute('SELECT people, COUNT(id) FROM Selled_Tours GROUP BY people')
            foods = self.cursor.fetchall()
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in foods:
                f.write(str(row[0]) + ': ' + str(row[1]) + ' tours\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = str(row[0])
                elif row[1] == mostV:
                    most += (', ' + str(row[0]))
                if row[1] < lessV:
                    lessV = row[1]
                    less = str(row[0])
                elif row[1] == lessV:
                    less += (', ' + str(row[0]))
            f.write('Most common size of tourist group: ' + most + '.  It was used ' + str(mostV) + ' times\n')
            f.write('Less common size of tourist group: ' + less + '.  It was used ' + str(lessV) + ' times\n')
            f.write('\n')
            self.cursor.execute('SELECT AVG(people) FROM Selled_Tours')
            avg_days = self.cursor.fetchone()[0]
            f.write('Average size of tourist group : ' + str(round(avg_days)) + ' people\n')
            self.cursor.execute('SELECT MIN(people) FROM Selled_Tours')
            res = self.cursor.fetchone()
            self.cursor.execute('SELECT Selled_Tours.id, Selled_Tours.people, Selled_Tours.price, Hotels.name, Cities.name, Countries.name, Selled_Tours.days, Selled_Tours.food, Selled_Tours.transport FROM Selled_Tours JOIN Hotels ON Selled_Tours.hotel_id = Hotels.id JOIN Cities ON Hotels.city_id = Cities.id JOIN Countries ON Cities.country_id = Countries.id WHERE Selled_Tours.people = ?', (res[0],))
            min_people = self.cursor.fetchall()
            for row in min_people:
                f.write('Smallest tourist group in: ' + str(row[0]) + ',    tourists: ' + str(row[1]) + ',    price: ' + str(row[2]) + ',    hotel: ' + str(row[3]) + ',    city: ' + str(row[4]) + ',    country: ' + str(row[5]) + ',    days: ' + str(row[6]) + ',    meals number: ' + str(row[7]) + ',    transport: ' + str(row[8]) + '\n')
            f.write('\n')
            self.cursor.execute('SELECT MAX(people) FROM Selled_Tours')
            res = self.cursor.fetchone()
            self.cursor.execute('SELECT Selled_Tours.id, Selled_Tours.people, Selled_Tours.price, Hotels.name, Cities.name, Countries.name, Selled_Tours.days, Selled_Tours.food, Selled_Tours.transport FROM Selled_Tours JOIN Hotels ON Selled_Tours.hotel_id = Hotels.id JOIN Cities ON Hotels.city_id = Cities.id JOIN Countries ON Cities.country_id = Countries.id WHERE Selled_Tours.people = ?', (res[0],))
            max_people = self.cursor.fetchall()
            for row in max_people:
                f.write('Biggest tourist group in: ' + str(row[0]) + ',    tourists: ' + str(row[1]) + ',    price: ' + str(row[2]) + ',    hotel: ' + str(row[3]) + ',    city: ' + str(row[4]) + ',    country: ' + str(row[5]) + ',    days: ' + str(row[6]) + ',    meals number: ' + str(row[7]) + ',    transport: ' + str(row[8]) + '\n')
            f.write('\n\n')
            f.write("Tourist's age statistic:\n")
            self.cursor.execute('SELECT AVG(age) FROM Tourists')
            avg_age = self.cursor.fetchone()[0]
            f.write('Average age of tourist : ' + str(round(avg_age)) + ' years\n')
            self.cursor.execute('SELECT MIN(age) FROM Tourists')
            res = self.cursor.fetchone()
            self.cursor.execute('SELECT Tourists.age, Tourists.name, Tourists.nationality, Selled_Tours.id, Hotels.name, Cities.name, Countries.name FROM Tourists JOIN Selled_Tours ON Tourists.tour_id = Selled_Tours.id JOIN Hotels ON Selled_Tours.hotel_id = Hotels.id JOIN Cities ON Hotels.city_id = Cities.id JOIN Countries ON Cities.country_id = Countries.id WHERE Tourists.age = ?', (res[0],))
            min_age = self.cursor.fetchall()
            for row in min_age:
                f.write("Youngest tourist's age: " + str(row[0]) + ',    name: ' + str(row[1]) + ',    nationality: ' + str(row[2]) + ',    tour: ' + str(row[3]) + ',    hotel: ' + str(row[4]) + ',    city: ' + str(row[5]) + ',    country: ' + str(row[6]) + '\n')
            f.write('\n')
            self.cursor.execute('SELECT MAX(age) FROM Tourists')
            res = self.cursor.fetchone()
            self.cursor.execute('SELECT Tourists.age, Tourists.name, Tourists.nationality, Selled_Tours.id, Hotels.name, Cities.name, Countries.name FROM Tourists JOIN Selled_Tours ON Tourists.tour_id = Selled_Tours.id JOIN Hotels ON Selled_Tours.hotel_id = Hotels.id JOIN Cities ON Hotels.city_id = Cities.id JOIN Countries ON Cities.country_id = Countries.id WHERE Tourists.age = ?', (res[0],))
            max_age = self.cursor.fetchall()
            for row in max_age:
                f.write("Oldest tourist's age: " + str(row[0]) + ',    name: ' + str(row[1]) + ',    nationality: ' + str(row[2]) + ',    tour: ' + str(row[3]) + ',    hotel: ' + str(row[4]) + ',    city: ' + str(row[5]) + ',    country: ' + str(row[6]) + '\n')
            f.write('\n\n')
            f.write("Tourist's nationality statistic:\n")
            self.cursor.execute('SELECT nationality, COUNT(id) FROM Tourists GROUP BY nationality')
            nation = self.cursor.fetchall()
            f.write('Tourists of ' + str(len(nation)) + ' nations bought tours\n')
            f.write('\n')
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in nation:
                f.write(row[0] + ': ' + str(row[1]) + ' tourists\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = row[0]
                elif row[1] == mostV:
                    most += (', ' + row[0])
                if row[1] < lessV:
                    lessV = row[1]
                    less = row[0]
                elif row[1] == lessV:
                    less += (', ' + row[0])
            f.write('\n')
            f.write('Most tourists: ' + most + '.  There were ' + str(mostV) + ' tourists\n')
            f.write('Less tourists: ' + less + '.  There were ' + str(lessV) + ' tourists\n')
            f.write('\n\n')
            f.write("Hotels statistic:\n")
            self.cursor.execute('SELECT name, COUNT(Hotels.id) FROM Hotels JOIN Selled_Tours ON Hotels.id = Selled_Tours.hotel_id GROUP BY name')
            hotels = self.cursor.fetchall()
            f.write('Tourists lived in ' + str(len(hotels)) + ' different hotels\n')
            f.write('\n')
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in hotels:
                f.write(row[0] + ': ' + str(row[1]) + ' tours\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = row[0]
                elif row[1] == mostV:
                    most += (', ' + row[0])
                if row[1] < lessV:
                    lessV = row[1]
                    less = row[0]
                elif row[1] == lessV:
                    less += (', ' + row[0])
            f.write('\n')
            f.write('Most popular hotel: ' + most + '.  Sold ' + str(mostV) + ' tours\n')
            f.write('Less popular hotel: ' + less + '.  Sold ' + str(lessV) + ' tours\n')
            f.write('\n\n')
            f.write("Hotel's stars statistic:\n")
            self.cursor.execute(
                'SELECT stars, COUNT(Hotels.id) FROM Hotels JOIN Selled_Tours ON Hotels.id = Selled_Tours.hotel_id GROUP BY stars')
            stars = self.cursor.fetchall()
            f.write('Tourists lived in hotels of ' + str(len(stars)) + ' different comfort levels\n')
            f.write('\n')
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in stars:
                f.write(str(row[0]) + ' stars: ' + str(row[1]) + ' tours\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = str(row[0])
                elif row[1] == mostV:
                    most += (', ' + str(row[0]))
                if row[1] < lessV:
                    lessV = row[1]
                    less = str(row[0])
                elif row[1] == lessV:
                    less += (', ' + str(row[0]))
            f.write('\n')
            f.write('Most popular comfort level: ' + most + ' stars.  Sold ' + str(mostV) + ' tours\n')
            f.write('Less popular comfort level: ' + less + ' stars.  Sold ' + str(lessV) + ' tours\n')
            f.write('\n\n')
            f.write("Hotel's size statistic:\n")
            self.cursor.execute('SELECT AVG(rooms) FROM Hotels JOIN Selled_Tours ON Selled_Tours.hotel_id = Hotels.id')
            avg_rooms = self.cursor.fetchone()[0]
            f.write('Average size of hotel : ' + str(round(avg_rooms)) + ' rooms\n')
            self.cursor.execute('SELECT MIN(rooms) FROM Hotels JOIN Selled_Tours ON Selled_Tours.hotel_id = Hotels.id')
            res = self.cursor.fetchone()
            self.cursor.execute('SELECT Hotels.rooms, Hotels.name, Hotels.stars, Cities.name, Countries.name FROM Hotels JOIN Cities ON Hotels.city_id = Cities.id JOIN Countries ON Cities.country_id = Countries.id JOIN Selled_Tours ON Selled_Tours.hotel_id = Hotels.id WHERE Hotels.rooms = ?', (res[0],))
            min_rooms = self.cursor.fetchall()
            for row in min_rooms:
                f.write("Smallest hotel sold: " + str(row[0]) + ' rooms,    name: ' + str(row[1]) + ',    stars: ' + str(row[2]) + ',    city: ' + str(row[3]) + ',    country: ' + str(row[4]) + '\n')
            f.write('\n')
            self.cursor.execute('SELECT MAX(rooms) FROM Hotels JOIN Selled_Tours ON Selled_Tours.hotel_id = Hotels.id')
            res = self.cursor.fetchone()
            self.cursor.execute('SELECT Hotels.rooms, Hotels.name, Hotels.stars, Cities.name, Countries.name FROM Hotels JOIN Cities ON Hotels.city_id = Cities.id JOIN Countries ON Cities.country_id = Countries.id JOIN Selled_Tours ON Selled_Tours.hotel_id = Hotels.id WHERE Hotels.rooms = ?', (res[0],))
            max_rooms = self.cursor.fetchall()
            for row in max_rooms:
                f.write("Biggest hotel sold: " + str(row[0]) + ' rooms,    name: ' + str(row[1]) + ',    stars: ' + str(row[2]) + ',    city: ' + str(row[3]) + ',    country: ' + str(row[4]) + '\n')
            f.write('\n\n')
            f.write("Cities statistic:\n")
            self.cursor.execute(
                'SELECT Cities.name, COUNT(Cities.id) FROM Cities JOIN Hotels ON Cities.id = Hotels.city_id JOIN Selled_Tours ON Hotels.id = Selled_Tours.hotel_id GROUP BY Cities.name')
            cities = self.cursor.fetchall()
            f.write('Tourists visited ' + str(len(cities)) + ' different cities\n')
            f.write('\n')
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in cities:
                f.write(row[0] + ': ' + str(row[1]) + ' tours\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = row[0]
                elif row[1] == mostV:
                    most += (', ' + row[0])
                if row[1] < lessV:
                    lessV = row[1]
                    less = row[0]
                elif row[1] == lessV:
                    less += (', ' + row[0])
            f.write('\n')
            f.write('Most popular city: ' + most + '.  Sold ' + str(mostV) + ' tours\n')
            f.write('Less popular city: ' + less + '.  Sold ' + str(lessV) + ' tours\n')
            f.write('\n\n')
            f.write("City's population statistic:\n")
            self.cursor.execute('SELECT AVG(population) FROM Cities JOIN Hotels ON Cities.id = Hotels.city_id JOIN Selled_Tours ON Selled_Tours.hotel_id = Hotels.id')
            avg_pop = self.cursor.fetchone()[0]
            f.write('Average population of city : ' + str(round(avg_pop)) + '\n')
            self.cursor.execute('SELECT MIN(population) FROM Cities JOIN Hotels ON Cities.id = Hotels.city_id JOIN Selled_Tours ON Selled_Tours.hotel_id = Hotels.id')
            res = self.cursor.fetchone()
            self.cursor.execute('SELECT Cities.population, Cities.name, Countries.name FROM Cities JOIN Countries ON Cities.country_id = Countries.id JOIN Hotels ON Hotels.city_id = Cities.id JOIN Selled_Tours ON Selled_Tours.hotel_id = Hotels.id WHERE Cities.population = ?', (res[0],))
            min_pop = self.cursor.fetchall()
            for row in min_pop:
                f.write("Smallest city visited: " + str(row[0]) + ' people,    name: ' + str(row[1]) + ',    country: ' + str(row[2]) + '\n')
            f.write('\n')
            self.cursor.execute('SELECT MAX(population) FROM Cities JOIN Hotels ON Cities.id = Hotels.city_id JOIN Selled_Tours ON Selled_Tours.hotel_id = Hotels.id')
            res = self.cursor.fetchone()
            self.cursor.execute('SELECT Cities.population, Cities.name, Countries.name FROM Cities JOIN Countries ON Cities.country_id = Countries.id JOIN Hotels ON Hotels.city_id = Cities.id JOIN Selled_Tours ON Selled_Tours.hotel_id = Hotels.id WHERE Cities.population = ?', (res[0],))
            max_pop = self.cursor.fetchall()
            for row in max_pop:
                f.write("Biggest city visited: " + str(row[0]) + ' people,    name: ' + str(row[1]) + ',    country: ' + str(row[2]) + '\n')
            f.write('\n\n')
            f.write("City's airports statistic:\n")
            self.cursor.execute(
                'SELECT Cities.airports, COUNT(Cities.id) FROM Cities JOIN Hotels ON Cities.id = Hotels.city_id JOIN Selled_Tours ON Hotels.id = Selled_Tours.hotel_id GROUP BY Cities.airports')
            airports = self.cursor.fetchall()
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in airports:
                f.write(str(row[0]) + ': ' + str(row[1]) + ' tours\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = str(row[0])
                elif row[1] == mostV:
                    most += (', ' + str(row[0]))
                if row[1] < lessV:
                    lessV = row[1]
                    less = str(row[0])
                elif row[1] == lessV:
                    less += (', ' + str(row[0]))
            f.write('\n')
            f.write('Most popular cities with : ' + str(most) + ' airports.  Sold ' + str(mostV) + ' tours\n')
            f.write('Less popular cities with : ' + str(less) + ' airports.  Sold ' + str(lessV) + ' tours\n')
            f.write('\n\n')
            f.write("City's climat statistic:\n")
            self.cursor.execute(
                'SELECT Cities.climat, COUNT(Cities.id) FROM Cities JOIN Hotels ON Cities.id = Hotels.city_id JOIN Selled_Tours ON Hotels.id = Selled_Tours.hotel_id GROUP BY Cities.climat')
            climats = self.cursor.fetchall()
            f.write('Tourists visited ' + str(len(climats)) + ' cities with different climat\n')
            f.write('\n')
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in climats:
                f.write(row[0] + ': ' + str(row[1]) + ' tours\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = row[0]
                elif row[1] == mostV:
                    most += (', ' + row[0])
                if row[1] < lessV:
                    lessV = row[1]
                    less = row[0]
                elif row[1] == lessV:
                    less += (', ' + row[0])
            f.write('\n')
            f.write('Most popular climat: ' + most + '.  Sold ' + str(mostV) + ' tours\n')
            f.write('Less popular climat: ' + less + '.  Sold ' + str(lessV) + ' tours\n')
            f.write('\n\n')
            f.write("Countries statistic:\n")
            self.cursor.execute(
                'SELECT Countries.name, COUNT(Countries.id) FROM Countries JOIN Cities ON Countries.id = Cities.country_id JOIN Hotels ON Cities.id = Hotels.city_id JOIN Selled_Tours ON Hotels.id = Selled_Tours.hotel_id GROUP BY Countries.name')
            countr = self.cursor.fetchall()
            f.write('Tourists visited ' + str(len(countr)) + ' different countries\n')
            f.write('\n')
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in countr:
                f.write(row[0] + ': ' + str(row[1]) + ' tours\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = row[0]
                elif row[1] == mostV:
                    most += (', ' + row[0])
                if row[1] < lessV:
                    lessV = row[1]
                    less = row[0]
                elif row[1] == lessV:
                    less += (', ' + row[0])
            f.write('\n')
            f.write('Most popular country: ' + most + '.  Sold ' + str(mostV) + ' tours\n')
            f.write('Less popular country: ' + less + '.  Sold ' + str(lessV) + ' tours\n')
            f.write('\n\n')
            f.write("Regions statistic:\n")
            self.cursor.execute(
                'SELECT Countries.region, COUNT(Countries.id) FROM Countries JOIN Cities ON Countries.id = Cities.country_id JOIN Hotels ON Cities.id = Hotels.city_id JOIN Selled_Tours ON Hotels.id = Selled_Tours.hotel_id GROUP BY Countries.region')
            regions = self.cursor.fetchall()
            f.write('Tourists visited ' + str(len(regions)) + ' different regions\n')
            f.write('\n')
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in regions:
                f.write(row[0] + ': ' + str(row[1]) + ' tours\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = row[0]
                elif row[1] == mostV:
                    most += (', ' + row[0])
                if row[1] < lessV:
                    lessV = row[1]
                    less = row[0]
                elif row[1] == lessV:
                    less += (', ' + row[0])
            f.write('\n')
            f.write('Most popular region: ' + most + '.  Sold ' + str(mostV) + ' tours\n')
            f.write('Less popular region: ' + less + '.  Sold ' + str(lessV) + ' tours\n')
            f.write('\n\n')
            f.write("Languages statistic:\n")
            self.cursor.execute(
                'SELECT Countries.language, COUNT(Countries.id) FROM Countries JOIN Cities ON Countries.id = Cities.country_id JOIN Hotels ON Cities.id = Hotels.city_id JOIN Selled_Tours ON Hotels.id = Selled_Tours.hotel_id GROUP BY Countries.language')
            regions = self.cursor.fetchall()
            f.write('Tourists visited ' + str(len(regions)) + ' countries with different languages\n')
            f.write('\n')
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in regions:
                f.write(row[0] + ': ' + str(row[1]) + ' tours\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = row[0]
                elif row[1] == mostV:
                    most += (', ' + row[0])
                if row[1] < lessV:
                    lessV = row[1]
                    less = row[0]
                elif row[1] == lessV:
                    less += (', ' + row[0])
            f.write('\n')
            f.write('Most popular countries with language: ' + most + '.  Sold ' + str(mostV) + ' tours\n')
            f.write('Less popular countries with language: ' + less + '.  Sold ' + str(lessV) + ' tours\n')
            f.write('\n\n')
            f.write("Currencies statistic:\n")
            self.cursor.execute(
                'SELECT Countries.currency, COUNT(Countries.id) FROM Countries JOIN Cities ON Countries.id = Cities.country_id JOIN Hotels ON Cities.id = Hotels.city_id JOIN Selled_Tours ON Hotels.id = Selled_Tours.hotel_id GROUP BY Countries.currency')
            currencies = self.cursor.fetchall()
            f.write('Tourists visited ' + str(len(currencies)) + ' countries with different currencies\n')
            f.write('\n')
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in currencies:
                f.write(row[0] + ': ' + str(row[1]) + ' tours\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = row[0]
                elif row[1] == mostV:
                    most += (', ' + row[0])
                if row[1] < lessV:
                    lessV = row[1]
                    less = row[0]
                elif row[1] == lessV:
                    less += (', ' + row[0])
            f.write('\n')
            f.write('Most popular countries with currency: ' + most + '.  Sold ' + str(mostV) + ' tours\n')
            f.write('Less popular countries with currency: ' + less + '.  Sold ' + str(lessV) + ' tours\n')
            f.write('\n\n')
            f.write("Religions statistic:\n")
            self.cursor.execute(
                'SELECT Countries.religion, COUNT(Countries.id) FROM Countries JOIN Cities ON Countries.id = Cities.country_id JOIN Hotels ON Cities.id = Hotels.city_id JOIN Selled_Tours ON Hotels.id = Selled_Tours.hotel_id GROUP BY Countries.religion')
            religions = self.cursor.fetchall()
            f.write('Tourists visited ' + str(len(religions)) + ' countries with different religions\n')
            f.write('\n')
            most = ''
            mostV = 0
            less = ''
            lessV = 999999999
            for row in religions:
                f.write(row[0] + ': ' + str(row[1]) + ' tours\n')
                if row[1] > mostV:
                    mostV = row[1]
                    most = row[0]
                elif row[1] == mostV:
                    most += (', ' + row[0])
                if row[1] < lessV:
                    lessV = row[1]
                    less = row[0]
                elif row[1] == lessV:
                    less += (', ' + row[0])
            f.write('\n')
            f.write('Most popular countries with religion: ' + most + '.  Sold ' + str(mostV) + ' tours\n')
            f.write('Less popular countries with religion: ' + less + '.  Sold ' + str(lessV) + ' tours\n')
            f.close()

        except:
            return ''
