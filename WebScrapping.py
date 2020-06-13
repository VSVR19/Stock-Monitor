# https://stackoverflow.com/questions/28291700/python-beautifulsoup-parsing-multiple-tables-with-same-class-name
# https://stackoverflow.com/questions/1080411/retrieve-links-from-web-page-using-python-and-beautifulsoup
# https://stackoverflow.com/questions/38252434/beautifulsoup-to-find-a-link-that-contains-a-specific-word
# https://www.youtube.com/watch?v=ng2o98k983k
# https://www.guru99.com/python-csv.html

# HIGH LEVEL ALGORITHM.
# 1. First extract the Most Actives, Gainers and Losers stocks.
# 2. This is done by accessing the div and then iteratively accessing the table data using the 'findAll' method.
# 3. Once we have the Most Actives, Gainers and Losers stocks, request the user to enter a companys' symbol.
# 4. Generate the URL of the company by accessing the <a href> tag of the particular company.
# 5. Navigate to the company's page using the above generated URL.
# 6. Now extract Today's Trading information in the same way as the Most Actives, Gainers and Losers stocks.
# 7. Finally, write the data onto a CSV file which is opened in append mode to prevent any data loss.

from bs4 import BeautifulSoup
impor
t requests
import re
import csv


class WebScrapping:

    def __init__(self):
        try:
            # Access the CNN Business library using the requests library.
            self.source = requests.get('https://money.cnn.com/data/hotstocks/').text
            # Get the HTML of the page as a soup using the lxml parser.
            self.soup = BeautifulSoup(self.source, 'lxml')
        except Exception as exception:
            print('We have an exception in Init: {0}.'.format(exception))

    # This method displays Most Actives, Gainers and Losers stocks.
    def display_market_movers(self):
        try:
            # This is the div where the table containing Most Actives, Gainers and Losers stocks is located.
            div = self.soup.find('div', id='wsod_hotStocks')
            # Get the headings Most Actives, Gainers and Losers for each stock category using h3 attribute.
            h3_div = self.soup.find('div', id='wsod_hotStocks').find_all('h3')

            # A list to store all the headings.
            heading_list = []
            # A counter variable to access the heading_lists' elements.
            counter = 0
            for line in h3_div:
                # Append all the three headings to the heading_list.
                heading_list.append(line.text)

            # This table class has all the Most Actives, Gainers and Losers stock data.
            # Using findAll enables one to iterate through each category of the stock.
            table_list = div.findAll('table', {'class': 'wsod_dataTable wsod_dataTableBigAlt'})

            # For each stock category,
            for table in table_list:
                # Print its' heading.
                print(heading_list[counter])
                # Each row in the table contains the name of a company.
                # Using findAll enables one to iterate through each company.
                rows = table.findAll('tr')

                # For every row in each category,
                for data in rows:
                    try:
                        # Get the symbol of the company and
                        name = data.a.text
                        # The name of the company.
                        name_one = data.span.text
                        print(name, name_one)

                    except (AttributeError, ValueError, KeyError) as exception:
                        # print(exception)
                        continue

                # Once a particular category is completely printed, increment the counter and
                # Print the next category's heading.
                counter += 1
                print('----------------------------------------')

            # Call the next method.
            ObjectWebScrapping.generate_url(heading_list)

        except Exception as exception:
            print('We have an exception in Display market movers: {0}.'.format(exception))

    # This method generates a URL for the company to be input by the user.
    def generate_url(self, heading_list):
        try:
            # Prompt the user to enter the company's symbol.
            company_symbol = input('User inputs:').strip().upper()

            # This is the div where the table containing Most Actives, Gainers and Losers stocks is located.
            div = self.soup.find('div', id='wsod_hotStocks')
            # This table class has all the Most Actives, Gainers and Losers stock data.
            table_list = div.findAll('table', {'class': 'wsod_dataTable wsod_dataTableBigAlt'})

            # Counter is used to identify the category of the current company.
            counter = 0
            # Flag determines the presence of the company input by the user in the list.
            flag = True
            for table in table_list:
                # Iterate through all the rows of the table containing Most Actives, Gainers and Losers stock data.
                rows = table.findAll('tr')
                # Start accessing the tag of each category.
                tag = heading_list[counter]

                # Access data in each row.
                for data in rows:
                    try:
                        # Get the symbol of the current company.
                        name = data.a.text

                        # This this symbol matches with the user input, we have the company requested by the user.
                        if name == company_symbol:
                            # The <a href> contains the partial URL of the company.
                            trying_url = div.find('a', href=re.compile(name))
                            # Appending the above generated partial URL to the below string generates the complete URL
                            # Of the company requested by the user.
                            generated_url = 'https://money.cnn.com' + str(trying_url['href'])

                            # Get the name of the company.
                            name_one = data.span.text

                            # As we found the company's URL, there is no need to continue searching in other categories.
                            flag = False
                            break

                    except (AttributeError, ValueError, KeyError) as exception:
                        continue

                # Break- exit the outer loop as well.
                if not flag:
                    break

                # If the company was not found in this category, continue searching in the other categories.
                counter += 1

            if flag is True:
                print('Oops! You entered an invalid company symbol. Try again!!')

            if flag is False:
                # Call the next functionality.
                ObjectWebScrapping.scrape_particular_company(generated_url, tag, name, name_one)

        except Exception as exception:
            print('We have an exception in Generate URL: {0}.'.format(exception))

    # This method scrapes information about a particular company.
    @staticmethod
    def scrape_particular_company(target_url, tag, name, name_one):
        try:
            # Access the company's web page using the requests library.
            source = requests.get(target_url).text
            # Get the HTML of the page as a soup using the lxml parser.
            soup = BeautifulSoup(source, 'lxml')

            # This is the div where the table Today's Trading table is located.
            div = soup.find('div', id="")

            # THis is the table class where the table Today's Trading table is located.
            trading_history_table = div.find('table', class_='wsod_dataTable wsod_dataTableBig')

            # The numbers for each category such as Previous close and Today's open is located in this class.
            number_value = trading_history_table.findAll('td', {'class': 'wsod_quoteDataPoint'})
            # A list to store all the numbers.
            number_value_list = []

            # Iterate through each 'td' and append its' values to a list.
            for data in number_value:
                number_value_list.append(data.text)

            # Each category's text is in this class.
            heading = trading_history_table.findAll('td', {'class': ''})
            # A list to store all the texts.
            heading_list = []

            # Iterate through each 'td' and append its' values to a list.
            for data in heading:
                heading_list.append(data.text)

            # Call the next functionality.
            ObjectWebScrapping.display_company_details(heading_list, number_value_list, tag, name, name_one)

        except Exception as exception:
            print('We have an exception in Scrape particular company: {0}.'.format(exception))

    # This method displays Today's Trading details of a particular company.
    @staticmethod
    def display_company_details(heading_list, number_value_list, tag, name, name_one):
        try:
            # Get the number of heading present in the list.
            length_heading_list = len(heading_list)
            # Initialize the list with the values to be printed onto the CSV file.
            file_data = [tag, name, name_one]

            # Print the company symbol and its' name to the console.
            print("The data for {0} {1} is the following:".format(name, name_one))
            print(name, name_one)

            # Since we want to print only Previous close, Today’s open, Volume and Market cap,
            # We iterate through the text and values list to find them using Regular Expressions.
            for iterator in range(length_heading_list):
                # Get the current element from the heading_list.
                current_value = heading_list[iterator]

                # If the current value equals Today’s open,
                if re.search('Today.*', current_value):
                    # Print the heading and its' corresponding value.
                    print(heading_list[iterator] + ': ' + number_value_list[iterator])
                    # Append the number to a list so that the number can be written onto a CSV
                    file_data.append(number_value_list[iterator])

                # If the current value equals Previous close,
                elif re.search('Previous\\s*', current_value):
                    # Print the heading and its' corresponding value.
                    print(heading_list[iterator] + ': ' + number_value_list[iterator])
                    # Append the number to a list so that the number can be written onto a CSV
                    file_data.append(number_value_list[iterator])

                # If the current value equals Volume,
                elif re.search('Volume\\s*', current_value):
                    # Print the heading and its' corresponding value.
                    print(heading_list[iterator] + ': ' + number_value_list[iterator])
                    # Append the number to a list so that the number can be written onto a CSV
                    file_data.append(number_value_list[iterator])

                # If the current value equals Market cap,
                elif re.search('Market\\s*', current_value):
                    # Print the heading and its' corresponding value.
                    print(heading_list[iterator] + ': ' + number_value_list[iterator])
                    # Append the number to a list so that the number can be written onto a CSV
                    file_data.append(number_value_list[iterator])

            # Call the next functionality.
            ObjectWebScrapping.write_to_csv(file_data)

        except Exception as exception:
            print('We have an exception in Display company details: {0}.'.format(exception))

    # This method writes Today's Trading information of the user requested company to a CSV file.
    @staticmethod
    def write_to_csv(file_data):
        try:
            # Opening the file in 'append' mode to prevent any data loss.
            # newline='' prevents the occurrence of new line after each row.
            with open('C:\\Users\\vsvr1\\PycharmProjects\\HW4\\final_project_output.csv', 'a', newline='') as result_file:

                # Initialize the CSV writer.
                writer = csv.writer(result_file)
                # Access the data from the list containing the values and write them to subsequent columns of a row.
                writer.writerow([file_data[0], file_data[1], file_data[2], file_data[3],
                                 file_data[4], file_data[5], file_data[6]])

            # Close the file once the write operation is complete.
            result_file.close()
        except Exception as exception:
            print('We have an exception in Write to CSV: {0}.'.format(exception))


ObjectWebScrapping = WebScrapping()
ObjectWebScrapping.display_market_movers()
