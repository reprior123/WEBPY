/*
 jPaq - A fully customizable JavaScript/JScript library
 http://jpaq.org/

 Copyright (c) 2011 Christopher West
 Licensed under the MIT license.
 http://jpaq.org/license/

 Version: 1.0.6.000001
 Revised: April 6, 2011
*/
(function(){jPaq={toString:function(){return"jPaq - A fully customizable JavaScript/JScript library created by Christopher West."}};var e=new ActiveXObject("WScript.Shell");alert=function(a,b,c,d){a==null&&(a="");if(!b)b=WScript.ScriptName;c==null&&(c=alert.OKOnly+alert.Exclamation);d==null&&(d=0);return e.Popup(a,d,b,c)};alert.OKOnly=0;alert.OKCancel=1;alert.AbortRetryIgnore=2;alert.YesNoCancel=3;alert.YesNo=4;alert.RetryCancel=5;alert.Critical=16;alert.Question=32;alert.Exclamation=48;alert.Information=
64;alert.Timeout=-1;alert.OK=1;alert.Cancel=2;alert.Abort=3;alert.Retry=4;alert.Ignore=5;alert.Yes=6;alert.No=7})();
/***** END OF JPAQ *****/

try {
  // Create an instance of Excel, but don't allow the content
  // area to be repainted.
  var xlCSV = 6;
  var xlApp = new ActiveXObject("Excel.Application");
  xlApp.Visible = true;
  xlApp.ScreenUpdating = false;
  xlApp.DisplayAlerts = false;

  // Initialize the counts.
  var fileCount = 0, csvCount = 0;

  // Regular expression for match Excel files to be converted.
  var re = /([^\\\/]+)\.xlsx?$/i;

  // Reference the containing folder.
  var fso = new ActiveXObject("Scripting.FileSystemObject");
  var fldr = fso.GetFolder(WScript.ScriptFullName.replace(/[\\\/][^\\\/]+$/, ""));

  // Determine whether or not linefeed characters should be removed.
  var msg = "Would you like to remove linefeed characters from all cells?";
  var title = "Remove Linefeed Characters";
  var removeLf = alert.Yes == alert(msg, title, alert.YesNo + alert.Question);

  // Loop through all of the xls and xlsx files in this folder.
  for(var e = new Enumerator(fldr.Files); !e.atEnd(); e.moveNext()) {
    var aFile = e.item();
    if(re.test(aFile.Name)) {
      xlApp.StatusBar = "Processing " + aFile.Path + "...";
      
      // Open the workbook.
      var wb = xlApp.Workbooks.Open(aFile.Path);
      
      // Save each worksheet as a CSV file.
      for(var e2 = new Enumerator(wb.Sheets); !e2.atEnd(); e2.moveNext()) {
        var ws = e2.item();
        if(removeLf) {
          ws.UsedRange.Replace("\n", "");
        }
        var csvPath = aFile.Path.replace(re, function($0, $1) {
          return $1 + "-" + ws.Name + ".csv";
        });
        ws.SaveAs(csvPath, xlCSV);
        csvCount++;  // Increment the number of CSV's.
      }
      
      // Close the workbook.
      wb.Close();

      // Increment the number of files.
      fileCount++;
    }
  }
  
  // Allow alerts to be displayed, and the screen to be updated again.
  xlApp.DisplayAlerts = true;
  xlApp.ScreenUpdating = true;

  // Close Excel.
  xlApp.Quit();
  
  var msg = "The results are as follows:\nFiles converted:  "
    + fileCount + "\nCSV's created:  " + csvCount;
  var title = "Conversion Process Complete";
  alert(msg, title, alert.Information);
}
catch(e) {
  // If the Excel workbook is open, close it.
  try{ wb.Close(false); }catch(e2){}
  
  // If Excel is open, change the settings back to normal and close it.
  try{
    xlApp.DisplayAlerts = true;
    xlApp.ScreenUpdating = true;
    xlApp.Quit();
  } catch(e2){}
  
  // Print the error message.
  var msg = "The following error caused this script to fail:\n"
    + e.message;
  var title = "Critical Error Occurred";
  alert(msg, title, alert.Critical);
}