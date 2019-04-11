import json

responseTypes = ["Strongly Agree", "Agree", "Somewhat Agree", "Somewhat Disagree", "Disagree", "Strongly Disagree"]

def processData(filePath):
    with open(filePath, "r") as file:
        jsonData = json.loads(file.read())
        
    processedData = {}
    for data in jsonData:
        if not data["instructor"] in processedData:
            processedData[data["instructor"]] = {}
            
        for responseType in responseTypes:
            if not responseType in processedData[data["instructor"]]:
                processedData[data["instructor"]][responseType] = data[responseType]
            else:
                processedData[data["instructor"]][responseType] += data[responseType]
    
    return processedData
    
def printCSV(data):
    # print header
    print("\"Instructor Name\"", end="")
    for responseType in responseTypes:
        print("," + responseType, end="")
    
    print()

    # print content
    for instructor in data:
        print("\"" + instructor + "\"", end="")
        
        for responseType in responseTypes:
            print("," + str(data[instructor][responseType]), end="")
            
        print()
        
        
data = processData("data.json")
printCSV(data)