import gspread, time
import csv
from oauth2client.service_account import ServiceAccountCredentials

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#much of this is commented out due to test attempts that I tried. Each attempt was useful in certain scenarios but it completely was dependent on when and where. 
#Left it all to show exactly what I was doing and when.
#Do be aware that I have removed the client_secret.json file as well, for that is only important if you are utilizing gspread.

scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('', scope)
client = gspread.authorize(creds)

sheet = client.open('ServiceAccount').sheet1

#won't work unless the path is set below, which I have conveniently left blank because I ain't letting people steal my stuff >:(
driver = webdriver.Chrome(executable_path="")
driver.get('https://itch.io/my-purchases/bundles')

#username and password blanked out because I don't want that info going out there.
def login(driver):
    user_name = driver.find_element_by_name('username')
    password = driver.find_element_by_name('password')

    user_name.send_keys('')
    password.send_keys('')

    login_button = driver.find_element_by_class_name('button')
    login_button.click()

login(driver)

csv_data = []
with open('read_data.csv') as csv_file:
    file_reader = csv.reader(csv_file)
    for csv_row in file_reader:
        csv_data.append(csv_row)

bundle_link = driver.find_element_by_link_text('Bundle for Racial Justice and Equality')
bundle_link.click()

desired_page = 60
finished_page = 30
current_page = 1
row = driver.find_elements_by_class_name('game_row')

game_list = [["Game Name", "Game Author", "Game URL"]]

#to do - fix game_row - i think we need to make a list for game_row?
#the for loop is broken, and fixing it will make everythig ez

'''
while current_page < desired_page:
    row = driver.find_elements_by_class_name('game_row')
    for rows in row:
        games = rows.find_element_by_class_name('game_title')
        games_creator = rows.find_element_by_class_name('game_author').text
        game_links = rows.find_element_by_tag_name('a')
        uncoded_game_link = game_links.get_attribute('href')
        final_game_link = str(uncoded_game_link)

        game_list = [current_page, games.text, games_creator[3:], final_game_link]
        sheet.append_row(game_list)

    next_page = driver.find_element_by_class_name('next_page')
    next_page.click()
    current_page+=1
    time.sleep(30)
'''
#print(game_list)

'''
for linker in games:
    game_links = linker.find_elements_by_tag_name('a')
    for href in game_links:
        final_game_links = href.get_attribute('href')
        print(final_game_links)

'''

#add encode if things go south
with open('list.csv', 'w', newline='', encoding='UTF8') as file:
    writer = csv.writer(file)
    row = driver.find_elements_by_class_name('game_row')
    for rows in row:
        games1 = rows.find_element_by_class_name('game_title')
        games_creator1 = rows.find_element_by_class_name('game_author').text
        game_links1 = rows.find_element_by_tag_name('a')
        uncoded_game_links = game_links1.get_attribute('href')
        final_game_links = str(uncoded_game_links)
        writer.writerow((current_page, games1.text, games_creator1[3:], final_game_links))   


from string import Template

'''
     
'''

chart_data = [["Bundle Item", "Number In Bundle"]]
csv_data = chart_data

htmlString = Template("""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
      var data = google.visualization.arrayToDataTable([
         ['Bundle Item', 'Number In Bundle'],
      ['Video Games',            483],
      ['Tabletop Games',         61],
      ['Asset Packs',            39],
      ['Reading Material',        8],
      ['Game Engine',             4],
      ['Miscellaneous Software',  5]
      ],
      false);

      var options = {
        title: 'Breakdown of the First Twenty Pages'
      };
      var chart = new google.visualization.PieChart(document.getElementById('piechart'));
      chart.draw(data, options);
  }
</script>
</head>
<body>
    <div id="piechart" style="width: 900px; height: 500px;"></div>
</body>

</html>""")

chart_data_str = ''
for row in chart_data[1:]:
    chart_data_str += '%s,\n'%row

completedHtml = htmlString.substitute(labels=csv_data[0], data=chart_data_str)
with open('Chart.html','w') as f:
 f.write(completedHtml)

#Learned New Way O:
#Need to figure out what elements are needed for the for loop
