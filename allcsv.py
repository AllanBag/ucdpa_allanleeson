import pandas as pd
import os
import glob

path = 'C:\\Users\\Allan\PycharmProjects\mobyproject'
csv_files = glob.glob(os.path.join(path, "*.csv"))

# loop over the list of csv files
alldata = pd.DataFrame()

for f in csv_files:
    # read the csv file
    df = pd.read_csv(f)
    # append the content
    alldata =  pd.concat([alldata, df])

###print a whole year of data
print(alldata)
