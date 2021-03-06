import csv, json, os, re
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup

class hotOneHundred:
    week   = ""
    chart  = []

# initialize the hotOneHundred class
    def __init__( self ):
        self.week   = {}

# extract the week from page data
    def get_week( self, data ):
        self.week   = re.split( r'[="]', str(data.find( 'div', {'data-chart-code': 'HSI'} )) )[5]
        return self.week

# get all songs for a week
# append songs to class chart object
    def get_chart( self, data ):
        self.get_week( data )
        for oltag in data.find_all( 'ol', {'class': 'chart-list__elements'} ):
            for litag in data.find_all( 'li', {'class': 'chart-list__element display--flex'} ):
                self.chart.append( self.get_song( litag ) )

# extract song details from list item
    def get_song( self, list_item ):
        song = {}
        song['week']      = self.week
        song['rank']      = list_item.find( 'span', {'class': 'chart-element__rank__number'} ).text
        song['title']     = list_item.find( 'span', {'class': 'chart-element__information__song text--truncate color--primary'} ).text
        song['artist']    = list_item.find( 'span', {'class': 'chart-element__information__artist text--truncate color--secondary'} ).text
        song['peak']      = list_item.find( 'span', {'class': 'chart-element__information__delta__text text--peak'} ).text
        song['last']      = list_item.find( 'span', {'class': 'chart-element__information__delta__text text--last'} ).text
        song['weeks']     = list_item.find( 'span', {'class': 'chart-element__information__delta__text text--week'} ).text
        return json.dumps(song)

# write the top 100 to a csv file
def write_csv( hot, filename='default_output.csv' ):
    with open( filename, 'a+' ) as csvfile:
        header     = json.loads( hot.chart[0] ).keys()
        csvwriter  = csv.DictWriter( csvfile, fieldnames=header )
        if not os.path.isfile( filename ) or os.stat( filename ).st_size == 0:
            csvwriter.writeheader()
        for song in hot.chart:
            csvwriter.writerow( json.loads(song) )
    csvfile.close()

# return the html of the requested page
def get_page( url ):
    req = Request( url )
    req.add_header( 'User-Agent', 'Mozilla/5.0' )
    return urlopen( req ).read()

# main routine
def main():
    page_html = get_page( 'https://www.billboard.com/charts/hot-100' )
    soup = BeautifulSoup( page_html, "lxml" )

    hot = hotOneHundred()
    hot.get_chart( soup )

    write_csv( hot, 'test_output.csv' )


if __name__ == "__main__":
    main()
