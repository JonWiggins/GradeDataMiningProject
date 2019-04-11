  var allData = []
  
  expectedCount = 0;
  processedCount = 0;

  function processSemester() {
    var dummyDocument = createDummyDocument(this.response);
    var links = dummyDocument.getElementsByTagName("a");
   
    var process = false;
    for(var linkIndex = 0; linkIndex < links.length; linkIndex++) {
      if(process) {
        if(/\/publicReports\?/.test(links[linkIndex].href)) {
          processPage(links[linkIndex].href, processClass);
          expectedCount += 1;
        } else {
          break;
        }
      } else {
        if(links[linkIndex].name === "courses") {
          process = true;
        }
      }
    }
  }

  function processClass() {
    var dummyDocument = createDummyDocument(this.response);
    var tables = dummyDocument.getElementsByTagName("table");
    
    var classNumber = getNumber(tables[0]);
    var semester = getSemester(tables[0]);
    
    for(var table of tables) {
      if(isInstructorTable(table)) {
        var data = readInstructorTable(table);
        
        data.classNumer = classNumber;
        data.semester = semester;
        
        allData.push(data); 
      }
    }
    
    processedCount += 1;
  }

  function getNumber(table) {
    for(var row of table.getElementsByTagName("tr")) {
      var match = /Course:\s+CS\s+(\d+-\d+),\s+.+/.exec(row.innerText);
      
      if(match)
        return match[1];
    }
    
    return "none";
  }

  function getSemester(table) {
    for(var row of table.getElementsByTagName("tr")) {
      var match = /Course:\s+CS\s+\d+-\d+,\s+(.+)/.exec(row.innerText);
      
      if(match)
        return match[1];
    }
    
    return "none";
  }

  function isInstructorTable(table) {
    var instructorRegex = /Instructor\s+Items:\s+(.+)/
    
    for(var line of table.getElementsByTagName("tr")) {
      var match = instructorRegex.exec(line.innerText);
      if(match)
        return true;
    }
    
    return false;
  }

  function readInstructorTable(table) {
    var data = {};
    
    var responseRegex = /(Strongly\s+Agree|Agree|Somewhat\s+Agree|Somewhat\s+Disagree|Disagree|Strongly\s+Disagree)\s+\d{0,3}\.?\d{0,2}?%\s+\((\d+)\)/;
    var instructorRegex = /^Instructor\s+Items:\s+(.+)/;
    
    for(var line of table.getElementsByTagName("tr")) {
      var responseMatch = responseRegex.exec(line.innerText);
      var instructorMatch = instructorRegex.exec(line.innerText);
      
      if(responseMatch) {
        if(responseMatch[1] in data) {
          data[responseMatch[1]] += parseInt(responseMatch[2])
        } else {
          data[responseMatch[1]] = parseInt(responseMatch[2])
        }
      } else if(instructorMatch) {
        data.instructor = instructorMatch[1];
      }
    }
    
    return data;
  }

  function processPage(url, callback) {
    var request = new XMLHttpRequest();
    request.addEventListener("load", callback);
    
    request.open("GET", url);
    request.send();
  }

  function createDummyDocument(html) {
    var dummy = document.createElement("html");
    dummy.innerHTML = html;
    
    return dummy;
  }
  
  function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

function downloadData() {
  download("data.json", JSON.stringify(allData));
}
  
  function done() { 
    return processedCount === expectedCount;
  }

  var pagesToScrape = [
    "https://student.apps.utah.edu/uofu/stu/SCFStudentResults/publicReports?cmd=showClasses&strm=1148&subject=CS",
    "https://student.apps.utah.edu/uofu/stu/SCFStudentResults/publicReports?cmd=showClasses&strm=1154&subject=CS",
    "https://student.apps.utah.edu/uofu/stu/SCFStudentResults/publicReports?cmd=showClasses&strm=1158&subject=CS",
    "https://student.apps.utah.edu/uofu/stu/SCFStudentResults/publicReports?cmd=showClasses&strm=1164&subject=CS",
    "https://student.apps.utah.edu/uofu/stu/SCFStudentResults/publicReports?cmd=showClasses&strm=1168&subject=CS",
    "https://student.apps.utah.edu/uofu/stu/SCFStudentResults/publicReports?cmd=showClasses&strm=1174&subject=CS",
    "https://student.apps.utah.edu/uofu/stu/SCFStudentResults/publicReports?cmd=showClasses&strm=1178&subject=CS",
  ];

  for(var pageToScrape of pagesToScrape) {
    processPage(pageToScrape, processSemester);
  }