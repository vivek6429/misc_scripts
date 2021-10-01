from pyautocad import Autocad, APoint
from pyautocad.contrib.tables import Table
from datetime import datetime
import itertools
import threading
import time
import sys
import csv
name="Tagoveralllayout"
filename = name+".csv"
done = False
now=datetime.now()
status=" "

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\r'+status + c)
        sys.stdout.flush()
        time.sleep(0.1)
    print("EXITING")

th = threading.Thread(target=animate)
th.daemon=True
th.start()

import logging   
logging.basicConfig(filename=name+".log", filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger=logging.getLogger() 
logger.setLevel(logging.INFO) 



###########################################################################
acad = Autocad(create_if_not_exists=True)
acad.prompt("Hello, Autocad from Python\n")
print("Current DWG open:",acad.doc.Name)
logger.info(str("File open:"+ acad.doc.Name))

titles = []
rows = []
status="loading file"
print()
try:
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        # extracting field names through first row
        titles = next(csvreader)
        logger.info("Skipping titles...")
        for row in csvreader:
            rows.append(row)
            logger.info("GOT DATA "+str(row))
except :
    print("opening file failed exiting")
    logger.exception("WAS NOT ABLE TO OPEN THE CSV FILE")
    quit()

status="working"
# we now have data in rows
# changing format
orgval=[]
newval=[]
valsthatareused=[]
for r in rows:
    orgval.append(r[0])
    newval.append((r[1]))

for text in acad.iter_objects('Text'):  
    flag=0
    for o,n in zip(orgval,newval):
        try:
            if(text.TextString==o.strip()):
                print("\nFound :",o,"  to be replaced by ",n," at",text.InsertionPoint)
                logger.info( text.TextString + "is replaced by " + n)
                text.TextString=n
                valsthatareused.append([o,n])
                flag=1
                break
            if flag==0:
                logger.info( text.TextString +" @ "+str(text.InsertionPoint)+ " is not replaced")
        except :
            print("something went wrong with comparison...")
            logger.error("something went wrong with comparison...")
    


status="writing changes performed to csv"


try:
    with open(name+"-ReplacedItems.csv", 'w') as csvfile:
        fieldnames = ['OriginalText', 'NewText']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for i in valsthatareused:
            writer.writerow({'OriginalText': i[0] , 'NewText': i[1] })

except :
    print("opening replceditems csv failed.exiting..")
    logger.exception("WAS NOT ABLE TO OPEN THE CSV FILE")
    done = True
    quit()

print("Completed")
done = True
quit()