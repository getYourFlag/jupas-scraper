from bs4 import BeautifulSoup
from tqdm import tqdm
import json, requests, sys, os

def fetchCatalog(university):
    if os.path.exists(f'data/{university}.html'):
        # Reads downloaded catalog immediately.
        with open(f'data/{university}.html', 'r') as downloadedHtmlFile:
            htmlPage = downloadedHtmlFile.read()

    else:
        if not os.path.exists('./data'):
            os.makedirs('./data')

        print(f'Downloading catalog for {info["universityNames"][university]}')
        htmlPage = fetchPage(f"https://www.jupas.edu.hk/en/programme/{university}/")
        with open(f'data/{university}.html', 'w') as newHtmlFile:
            newHtmlFile.write(htmlPage)

    soup = BeautifulSoup(htmlPage, 'lxml')
    programList = soup.find('table', class_='program_table-hasFC').find('tbody').find_all('tr')
    return programList

def fetchPage(url):
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    return res.text

def getProgram(program, university):
    jupasCode = str(program.find('td', class_='c-no').contents[0].string)

    names = program.find('td', class_='c-ft')
    englishName = str(names.contents[0].string)

    chineseNameDiv = names.find('span', class_='tname-cn')
    chineseName = str(chineseNameDiv.contents[0].string)

    programDict = {
        "code": jupasCode,
        "school": info['universityNames'][university],
        "chineseName": chineseName,
        "englishName": englishName,
        "requirements": {}
    }

    reqPage = BeautifulSoup(
        fetchPage(f"https://www.jupas.edu.hk/en/programme/{university}/{jupasCode}/"), 
        'lxml'
    )
    reqTables = reqPage.find('div', class_='dsereg_tables_container').find_all('table')

    if len(reqTables) == 0: 
        # No specific subject requirements, return the result directly.
        return jupasCode, programDict
    
    compulsoryTable = reqTables[0].find('tbody').find_all('tr')
    electivesTable = reqTables[1].find('tbody').find_all('tr')

    # Get the required grades for compulsory subjects.
    for row in compulsoryTable:
        subjectName = str(row.find('td', class_='dsereg-sub').contents[0].string)
        subject = info['compulsorySubjectNames'][subjectName]
        grade = int(str(row.find('td', class_='dsereg-lv').contents[0].string))
        programDict['requirements'][subject] = grade
    
    electivesList = None
    electiveGrade = 0

    # Get the required grades for elective subjects..
    for row in electivesTable:
        subject = str(row.find('td', class_='dsereg-sub').contents[0].string)
        if 'One of the following' in subject:
            electivesList = []
            continue
        if electivesList is None or 'ANY' in subject: 
            continue
        electiveGrade = int(str(row.find('td', class_='dsereg-lv').contents[0].string))

        refList = info['electiveNames'].get(subject, None)
        if refList is None:
            refInput = input(f"{subject} is undefined in file, please input subject code: ")
            refList = refInput.split(" ")
            info['electiveNames'][subject] = refList

        electivesList += refList

    if electivesList is not None:
        subjectStr = ' '.join(list(set(electivesList))) # Filters out duplicated electives
        programDict['requirements'][subjectStr] = electiveGrade
    
    return jupasCode, programDict

def main():
    global info
    with open('info.json', 'r') as infoFile:
        info = json.load(infoFile)

    programmes = {}
    catalogs = {university: fetchCatalog(university) for university in info['universities']}

    for university, programList in catalogs.items():
        schoolName = info['universityNames'][university]
        print(f"Parsing catalog for {schoolName}")

        # Get each individual program and store them in the programmes dict.
        for program in tqdm(programList):
            code, programDict = getProgram(program, university)
            programmes[code] = programDict
            
    with open('programmes.json', 'w') as jsonFile:
        json.dump(programmes, jsonFile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()