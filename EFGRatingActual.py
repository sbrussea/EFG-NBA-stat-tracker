import requests
from bs4 import BeautifulSoup




#change the converter to convert any stats you want into a combined stat
def converter(twos, threes):
  if (twos == 0.0):
    return threes
  if (threes == 0.0):
    return twos
  return (((twos*2) + (threes*3))/5)


def EFGfinder(year):
  webs = "https://www.basketball-reference.com/leagues/NBA_" + year + "_per_game.html"
  data = requests.get(webs)
  soup = BeautifulSoup(data.text, 'html.parser')
  div = soup.find('div')
  tbody = div.find('tbody')
  tr = tbody.find_all('tr')
  result = []
  for line in tr:
    temp = []
    if ( len(line.find_all('th')) < 2):
      td = line.find_all('td')
      name = td[0].find_all('a')[0].text.strip()
      temp.append(name)

      print(td[1].text.strip())
      pos = td[1].text.strip()
      temp.append(pos)

      TwoPtPCT = td[15].text.strip()
      if (TwoPtPCT != ''):
        data = "2's% " + TwoPtPCT
        temp.append(data)

      ThreePtPCT = td[12].text.strip()
      if (ThreePtPCT != ''):
        data = "3's% " + ThreePtPCT
        temp.append(data)
      
      FGA = td[8].text.strip()
      FGAs = "FGA " + FGA
      FGA = float(td[8].text.strip())
      temp.append(FGAs)
      
      if ((TwoPtPCT != '') and (ThreePtPCT != '')):
        er = converter(float(TwoPtPCT), float(ThreePtPCT))
        efg = "EFG " + str(er)
        temp.append(efg)

      
      if (len(temp) > 4):
        if FGA > 5:
          result.append(temp)
          print(len(temp))

  result.sort(key = lambda x:x[5])

  result.reverse()

  count = 0
  newFileName = "EFG" + year + ".txt"
  with open(newFileName, 'w') as filehandle:
    for player in result:
      count += 1
      filehandle.write(f'{count}) {player}\n')

def main():
  #change the year here to the year you want to start at
  year = 2000
  while (year <= 2020):
    EFGfinder(str(year))
    print(str(year) + "... passed!")
    year += 1
    
  print('Done!')

if __name__ == '__main__':
    main()
  
  