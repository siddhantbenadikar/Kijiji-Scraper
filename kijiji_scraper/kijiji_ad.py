import re

class KijijiAd():

    def __init__(self, ad, year):
        self.title = ad.find('a', {"class": "title"}).text.strip()
        self.id = ad['data-listing-id']
        self.ad = ad
        self.info = {}

        self.__locate_info()
        self.__parse_info()
        self.__parse_mileage()
        self.__parse_price()
        # add year info
        if year:
            self.info["Year"] = year

    def __locate_info(self):
        # Locate ad information
        self.info["Title"] = self.ad.find('a', {"class": "title"})
        self.info["Image"] = str(self.ad.find('img'))
        self.info["Url"] = self.ad.get("data-vip-url")
        self.info["Details"] = self.ad.find(
            'div', {"class": "details"})
        self.info["Description"] = self.ad.find(
            'div', {"class": "description"})
        self.info["Date"] = self.ad.find(
            'span', {"class": "date-posted"})
        self.info["Location"] = self.ad.find('div', {"class": "location"})
        self.info["Price"] = self.ad.find('div', {"class": "price"})
        self.info["DataSource"] = str(self.ad.find('img').get('data-src'))

    def __parse_info(self):
        # Parse Details and Date information
        self.info["Details"] = ' '.join(self.info["Details"].text.strip().split()) \
            if self.info["Details"] is not None else ""
        self.info["Date"] = self.info["Date"].text.strip() \
            if self.info["Date"] is not None else ""

        # Parse remaining ad information
        for key, value in self.info.items():
            if value:
                if key == "Url":
                    self.info[key] = 'http://www.kijiji.ca' + value

                elif key == "Description":
                    value = value.text.strip() \
                        .replace(self.info["Details"], '')
                    value = ' '.join(value.split())
                    self.info[key] = value

                elif key == "Location":
                    value = value.text.strip() \
                        .replace(self.info["Date"], '')
                    value = ' '.join(value.split())
                    self.info[key] = value
                    
                elif key == "Image":
                    self.info[key] = '<img src =\"' + (self.info["DataSource"]) + '\"/>'

                elif key not in ["DataSource", "Details", "Date"]:
                    self.info[key] = value.text.strip()

    def __parse_mileage(self):
        details = self.info["Details"]
        if details:
            d = re.findall('([^ \r\n]+) km?([\r\n]| |$)', details, re.IGNORECASE)
            if len(d):
                mileage = d[0][0].replace(',', '')
                mileage = int(mileage)
                self.info["Mileage"] = mileage

    def __parse_price(self):
        price = self.info["Price"]
        # edge case when price is 'please contact'
        # check if price contains a digit, if it does assume it's a number
        if bool(re.search(r'\d', price)):
            self.info["PriceFloat"] = float(re.sub(r'[^\d.]', '', price))
