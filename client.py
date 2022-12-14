import Pyro4

def standartCommandMenu():
    print('Choose an operation: \n' +
          '1.Get all \n' +
          '2.Get by id \n' +
          '3.Add \n' +
          '4.Update \n' +
          '5.Delete \n' +
          '6.Exit menu')
    command = int(input())
    return command

def cutCommandMenu():
    print('Choose an operation: \n' +
          '1.Get all \n' +
          '2.Get by id \n' +
          '3.Exit menu')
    command = int(input())
    return command

def adminMenu():
    while True:
        print('Choose a table to look or update: \n' +
            '1.Countries \n' +
            '2.Cities \n' +
            '3.Hotels \n' +
            '4.Available Tours \n' +
            '5.Selled Tours \n' +
            '6.Tourists \n' +
            '7.Get Statistics \n' +
            '8.Exit')
        command = int(input())
        if command == 1:
            while True:
                op = standartCommandMenu()
                if op == 1:
                    serverMessage = agency.getCountries()
                    print(serverMessage)
                elif op == 2:
                    print('Enter country id: ')
                    country = int(input())
                    serverMessage = agency.getCountry(country)
                    print(serverMessage)
                elif op == 3:
                    print('Country name: ')
                    name = input()
                    print('Region: ')
                    region = input()
                    print('Language: ')
                    language = input()
                    print('Currency: ')
                    currency = input()
                    print('Religion: ')
                    religion = input()
                    serverMessage = agency.addCountry(name, region, language, currency, religion)
                    print(serverMessage)
                elif op == 4:
                    print('Enter country id: ')
                    country = int(input())
                    while True:
                        print('What to change: \n' +
                            '1.Name \n' +
                            '2.Region \n' +
                            '3.Language \n' +
                            '4.Currency \n' +
                            '5.Religion \n' +
                            '6.Exit')
                        param = int(input())
                        if param == 6:
                            break
                        elif param < 1 or param > 6:
                            print('Unknown command!')
                        else:
                            print('New value: ')
                            val = input()
                            serverMessage = agency.updateCountry(country, param, val)
                            print(serverMessage)
                elif op == 5:
                    print('Enter country id: ')
                    country = int(input())
                    serverMessage = agency.deleteCountry(country)
                    print(serverMessage)
                elif op == 6:
                    break
                else:
                    print('Unknown command!')
        elif command == 2:
            while True:
                op = standartCommandMenu()
                if op == 1:
                    serverMessage = agency.getCities()
                    print(serverMessage)
                elif op == 2:
                    print('Enter city id: ')
                    city = int(input())
                    serverMessage = agency.getCity(city)
                    print(serverMessage)
                elif op == 3:
                    print('City name: ')
                    name = input()
                    print('Country id: ')
                    country_id = int(input())
                    print('Population: ')
                    population = int(input())
                    print('Number of airports: ')
                    airports = int(input())
                    print('Climat: ')
                    climat = input()
                    serverMessage = agency.addCity(name, country_id, population, airports, climat)
                    print(serverMessage)
                elif op == 4:
                    print('Enter city id: ')
                    city = int(input())
                    while True:
                        print('What to change: \n' +
                            '1.Name \n' +
                            '2.Country_id \n' +
                            '3.Population \n' +
                            '4.Number of airports \n' +
                            '5.Climat \n' +
                            '6.Exit')
                        param = int(input())
                        if param == 6:
                            break
                        elif param < 1 or param > 6:
                            print('Unknown command!')
                        else:
                            print('New value: ')
                            val = input()
                            serverMessage = agency.updateCity(city, param, val)
                            print(serverMessage)
                elif op == 5:
                    print('Enter city id: ')
                    city = int(input())
                    serverMessage = agency.deleteCity(city)
                    print(serverMessage)
                elif op == 6:
                    break
                else:
                    print('Unknown command!')
        elif command == 3:
            while True:
                op = standartCommandMenu()
                if op == 1:
                    serverMessage = agency.getHotels()
                    print(serverMessage)
                elif op == 2:
                    print('Enter hotel id: ')
                    hotel = int(input())
                    serverMessage = agency.getHotel(hotel)
                    print(serverMessage)
                elif op == 3:
                    print('Hotel name: ')
                    name = input()
                    print('City id: ')
                    city_id = int(input())
                    print('Stars: ')
                    stars = int(input())
                    print('Number of rooms: ')
                    rooms = int(input())
                    serverMessage = agency.addHotel(name, city_id, stars, rooms)
                    print(serverMessage)
                elif op == 4:
                    print('Enter hotel id: ')
                    hotel = int(input())
                    while True:
                        print('What to change: \n' +
                            '1.Name \n' +
                            '2.City_id \n' +
                            '3.Stars \n' +
                            '4.Number of rooms \n' +
                            '5.Exit')
                        param = int(input())
                        if param == 5:
                            break
                        elif param < 1 or param > 5:
                            print('Unknown command!')
                        else:
                            print('New value: ')
                            val = input()
                            serverMessage = agency.updateHotel(hotel, param, val)
                            print(serverMessage)
                elif op == 5:
                    print('Enter hotel id: ')
                    hotel = int(input())
                    serverMessage = agency.deleteHotel(hotel)
                    print(serverMessage)
                elif op == 6:
                    break
                else:
                    print('Unknown command!')
        elif command == 4:
            while True:
                op = standartCommandMenu()
                if op == 1:
                    serverMessage = agency.getTours()
                    print(serverMessage)
                elif op == 2:
                    print('Enter tour id: ')
                    tour = int(input())
                    serverMessage = agency.getTour(tour)
                    print(serverMessage)
                elif op == 3:
                    print('Hotel id: ')
                    hotel_id = int(input())
                    print('People: ')
                    people = int(input())
                    print('Days: ')
                    days = int(input())
                    print('Meals number: ')
                    food = int(input())
                    print('Transport: ')
                    transport = input()
                    print('Price in $: ')
                    price = float(input())
                    print('Avaliable tours: ')
                    avaliable = int(input())
                    serverMessage = agency.addTour(hotel_id, people, days, food, transport, price, avaliable)
                    print(serverMessage)
                elif op == 4:
                    print('Enter tour id: ')
                    tour = int(input())
                    while True:
                        print('What to change: \n' +
                            '1.Hotel_id \n' +
                            '2.People \n' +
                            '3.Days \n' +
                            '4.Meals number \n' +
                            '5.Transport \n' +
                            '6.Price \n' +
                            '7.Avaliable \n' +
                            '8.Exit')
                        param = int(input())
                        if param == 8:
                            break
                        elif param < 1 or param > 8:
                            print('Unknown command!')
                        else:
                            print('New value: ')
                            val = input()
                            serverMessage = agency.updateTour(tour, param, val)
                            print(serverMessage)
                elif op == 5:
                    print('Enter tour id: ')
                    tour = int(input())
                    serverMessage = agency.deleteTour(tour)
                    print(serverMessage)
                elif op == 6:
                    break
                else:
                    print('Unknown command!')
        elif command == 5:
            while True:
                op = cutCommandMenu()
                if op == 1:
                   serverMessage = agency.getSelledTours()
                   print(serverMessage)
                elif op == 2:
                    print('Enter tour id: ')
                    tour = int(input())
                    serverMessage = agency.getSelledTour(tour)
                    print(serverMessage)
                elif op == 3:
                    break
                else:
                    print('Unknown command!')
        elif command == 6:
            while True:
                op = cutCommandMenu()
                if op == 1:
                    serverMessage = agency.getTourists()
                    print(serverMessage)
                elif op == 2:
                    print('Enter tourist id: ')
                    tourist = int(input())
                    serverMessage = agency.getTourist(tourist)
                    print(serverMessage)
                elif op == 3:
                    break
                else:
                    print('Unknown command!')
        elif command == 7:
            agency.getStatistic()
        elif command == 8:
            break
        else:
            print('Unknown command!')
            continue









def userMenu():
    while True:
        serverMessage = agency.getCountries()
        print(serverMessage)
        if serverMessage == 'No countries in DB':
            break
        print('Choose an id of country to visit or Q to exit: ')
        country = input()
        if country == 'Q':
            break
        else:
            while True:
                serverMessage = agency.getCountryCities(int(country))
                print(serverMessage)
                if serverMessage == 'No cities in this country or incorrect country id':
                    break
                print('Choose an id of city to visit or Q to exit: ')
                city = input()
                if city == 'Q':
                    break
                else:
                    while True:
                        serverMessage = agency.getCityHotels(int(city))
                        print(serverMessage)
                        if serverMessage == 'No hotels in this city or incorrect city id':
                            break
                        print('Choose an id of hotel to visit or Q to exit: ')
                        hotel = input()
                        if hotel == 'Q':
                            break
                        else:
                            while True:
                                serverMessage = agency.getHotelTours(int(hotel))
                                print(serverMessage)
                                if serverMessage == 'No tours in this hotel or incorrect hotel id':
                                    break
                                print('Choose an id of tour to buy or Q to exit: ')
                                tour = input()
                                if tour == 'Q':
                                    break
                                else:
                                    print('Confirm to buy tour ' + tour + '? Y/N:')
                                    opt = input()
                                    if opt == 'N':
                                        continue
                                    elif opt == 'Y':
                                        serverMessage = agency.buyTour(int(tour))
                                        print(serverMessage[0])
                                        bought_id = serverMessage[1]
                                        serverMessage = agency.getTourPeople(int(tour))
                                        print('Fill the information about ' + str(serverMessage) + ' people who will travel:')
                                        for i in range(serverMessage):
                                            print('Tourist name and surname: ')
                                            name = input()
                                            print('Tourist age: ')
                                            age = int(input())
                                            print('Tourist nationality: ')
                                            nationality = input()
                                            serverMessage = agency.addTourist(name, bought_id, age, nationality)
                                            print(serverMessage)
                                    else:
                                        print('Unknown option')





if __name__ == '__main__':
    ns = Pyro4.locateNS()
    uri = ns.lookup('agency')
    agency = Pyro4.Proxy(uri)

    while True:
        print('Autentification...\n' +
            '1.Sign in \n' +
            '2.Sign up \n' +
            '3.Exit')
        command = int(input())
        if command == 1:
            print('Enter your login: ')
            login = input()
            print('Enter your password:')
            password = input()
            serverMessage = agency.verification(login, password)
            print(serverMessage[0])
            if serverMessage[1]:
                if serverMessage[2] == 'admin':
                    adminMenu()
                elif serverMessage[2] == 'user':
                    userMenu()
                else:
                    print('Access error')
        elif command == 2:
            print('Enter your name and surname: ')
            name = input()
            print('Create your login: ')
            login = input()
            print('Create your password:')
            password = input()
            print('Repeat your password:')
            password_copy = input()
            serverMessage = agency.registration(name, login, password, password_copy)
            print(serverMessage)
        elif command == 3:
            quit()
        else:
            print('Unknown command!')
