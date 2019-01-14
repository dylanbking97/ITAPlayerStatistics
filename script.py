from urllib.request import urlopen 
from bs4 import BeautifulSoup

#gets html of webpage
#BeautifulSoup turns html into an easily traversible html object 

url = input('Enter player url: ')
html = urlopen(url)
bsObj = BeautifulSoup(html, "lxml")

#gets, prints the name of the selected player

name = bsObj.find(id="ContentPlaceHolder1_drpPlayer").find(selected="selected")
print(name.get_text())

#gets list of all matches within the html table content id

matchlist = bsObj.find(id="ContentPlaceHolder1_pnSingleMatch").findAll("tr")

resultMatrix = []
wins = []
losses = []
unfinished = [] 

#the result and corresponding score of each match played is appended into resultMatrix
#strip() removes spaces to standardize score input: (6-3,6-3).strip() == (6-3, 6-3).strip()
for match in matchlist:
    resultMatrix.append([match.findAll("td")[5].get_text().strip(), match.findAll("td")[6].get_text().strip().replace(" ", "")])

#iterates through resultMatrix to create lists for wins, losses, and unfinished matches

for x in range(len(resultMatrix)):
    if resultMatrix[x][0] == "Win":
        wins.append([resultMatrix[x][0], resultMatrix[x][1]])
    elif resultMatrix[x][0] == "Loss":
        losses.append([resultMatrix[x][0], resultMatrix[x][1]])
    elif resultMatrix[x][0] == "U":
        unfinished.append([resultMatrix[x][0], resultMatrix[x][1]])
        
print(len(matchlist)-1, "matches")
print(len(wins),"wins")
print(len(losses), "losses")
print(len(unfinished), "unfinished")
print("\n")

#calculates player win percentage
#unfinished matches are not included 

winpercent = round((len(wins)/(len(losses)+len(wins))*100), 1)
print(winpercent, "% win percentage")

#iterates through resultMatrix for matches that went to a third set
#third set matches are identified by # of commas in the match score: (6-3,3-6,6-3) = 2 commas
splitsets = []
for match in resultMatrix:
    commas = str(match[1]).count(',')
    if commas == 2:
        splitsets.append(match)

#calculates percentage of matches that split sets (unfinished matches included)

splitpercent = round(((len(splitsets))/(len(matchlist)-1))*100, 1)
print(splitpercent,"% split sets")
print("\n")

splitwon = 0
splitlost = 0
for match in splitsets:
    if match[0] == 'Win':
        splitwon += 1
    elif match[0] == 'Loss':
        splitlost += 1

print("Resilience statistics: ")

#calculates the percentage of third sets won
splitwinpercent = round((splitwon/(splitlost+splitwon)) *100, 1)
print(splitwinpercent, "% third sets won")

#a competitive set will be defined as 6-4 or closer
#the following 8 scenarios of competitive sets are based on 3 variables for the first two sets of the match (2^3 = 8):
    #1) Whether the set was won or lost by the player
    #2) Whether the set was 1st set or 2nd set
    #3) Whether or not the player won the overall match (if match won, an individual won set would be reported 6-3, otherwise it would be reported 3-6)
competitivesetswon = 0
competitivesetslost = 0
for match in resultMatrix:
    if match[1] != '' and match[1] != "Score":
        if match[0] == 'Win' and (int((str(match[1])[0])) + int((str(match[1])[2])) > 9) and (str(match[1])[0] > str(match[1])[2]):
            competitivesetswon += 1
        elif match[0] == 'Win' and str(match[1])[3] != '(' and str(match[1])[4].isnumeric() and (int((str(match[1])[4])) + int((str(match[1])[6])) > 9) and (str(match[1])[4] > str(match[1])[6]):
            competitivesetswon += 1
        elif match[0] == 'Loss' and (int((str(match[1])[0])) + int((str(match[1])[2])) > 9) and (str(match[1])[0] < str(match[1])[2]):
            competitivesetswon += 1
        elif match[0] == 'Loss' and str(match[1])[3] != '(' and str(match[1])[4].isnumeric() and (int((str(match[1])[4])) + int((str(match[1])[6])) > 9) and (str(match[1])[4] < str(match[1])[6]):
            competitivesetswon += 1
        elif match[0] == 'Win' and (int((str(match[1])[0])) + int((str(match[1])[2])) > 9) and (str(match[1])[0] < str(match[1])[2]):
            competitivesetslost += 1
        elif match[0] == 'Win' and str(match[1])[3] != '(' and str(match[1])[4].isnumeric() and (int((str(match[1])[4])) + int((str(match[1])[6])) > 9) and (str(match[1])[4] < str(match[1])[6]):
            competitivesetslost += 1
        elif match[0] == 'Loss' and (int((str(match[1])[0])) + int((str(match[1])[2])) > 9) and (str(match[1])[0] > str(match[1])[2]):
            competitivesetslost += 1
        elif match[0] == 'Loss' and str(match[1])[3] != '(' and str(match[1])[4].isnumeric() and (int((str(match[1])[4])) + int((str(match[1])[6])) > 9) and (str(match[1])[4] > str(match[1])[6]):
            competitivesetslost += 1
            
#all third sets will be counted as competitive sets, no matter the score
for match in splitsets:
    if match[0] == 'Win':
        competitivesetswon += 1
    elif match[0] == 'Loss':
        competitivesetslost += 1
    
#calculates competitive set percentage won
competitivepercentwon = round((competitivesetswon/(competitivesetslost+competitivesetswon)) * 100, 1)
print(competitivepercentwon, "% competitive sets won")

#this code gathers the data from when the player lost the first set
#a resilient player will improve from set to set, even in the case of a loss        
betterscore = 0
worseorsame = 0
for match in resultMatrix:
    if match[1] != '' and match[1] != "Score":
        if match[0] == 'Win' and (str(match[1])[0] < str(match[1])[2]):
            betterscore += 1
        elif match[0] == 'Loss' and (str(match[1])[0] > str(match[1])[2]) and str(match[1])[3] != '(' and str(match[1])[4].isnumeric() and (int((str(match[1])[4])) + int((str(match[1])[6])) > (int((str(match[1])[0])) + int((str(match[1])[2])))):
            betterscore +=1
        elif match[0] == 'Loss' and (str(match[1])[0] > str(match[1])[2]) and str(match[1])[3] != '(' and str(match[1])[4].isnumeric() and (int((str(match[1])[4])) < int((str(match[1])[6]))):
            betterscore +=1
        elif match[0] == 'Loss' and (str(match[1])[0] > str(match[1])[2]):
            worseorsame +=1

#calculates percent of second set score improvement
secondsetbetter = round((betterscore/(betterscore+worseorsame))*100, 1)
print(secondsetbetter, "% second set resilience")
