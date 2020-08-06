import os
import json
from selenium import webdriver
import time
import glob
from matplotlib import pyplot as plt, pylab
import numpy as np
import scipy
from sklearn.linear_model import LinearRegression


directory = 'JsonFiles'
if not os.path.exists(directory):
    os.mkdir(directory)

path = os.path.join(os.getcwd(),directory)
prefs = {
    "download.default_directory": path
    }
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)

# REPLACE PATH WITH YOUR OWN
browser = webdriver.Chrome(chrome_options=options, executable_path=r'/Users/USER/Downloads/chromedriver')
# above is my path to chromedriver, REPLACE PATH WITH YOUR OWN.
browser.maximize_window()
browser.get('https://www.json-generator.com')
time.sleep(1) 


counter = 5
while counter:    
    # click submit button
    python_button = browser.find_elements_by_xpath("//a[@class='btn' and @id='generate']")[0]
    python_button.click()
    
    # click submit button
    python_button = browser.find_elements_by_xpath("//a[@download='generated.json']")[0]
    python_button.click()
    
    counter -= 1


for filename in os.listdir(path):
    with open (os.path.join(path,filename)) as json_file:
        data = json.load(json_file)

        """pull balances from json file"""
        bal = list(map(lambda i: i['balance'], data))
        print(bal)
         
        """format balances for calculation"""
        bal = map(lambda balance: balance.strip('$'), bal)
        bal = map(lambda balance: balance.replace(',' , ''), bal)
        bal = list(map(float, bal))
        print('sum of balances: ' , sum(bal))
        print('Number of balances: ',len(bal))
        print('Average Balance: ' + str(sum(bal)/len(bal)))


        """Pull longitude and latitude data"""
        longitude =  list(map(lambda i: i['longitude'], data))
        latitude = list(map(lambda i: i['latitude'], data))
        long_x = np.squeeze(np.fromiter(longitude, float))
        lat_y = np.squeeze(np.fromiter(latitude, float))
        
        def scatterplot(x, y):
            """Create scatter plot"""
            plt.scatter(x, y, c='b')
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.title('Longitude vs. latitude')
            return plt.show()
        
        """Retrieve age from json file, set variables using squeeze/fromiter"""
        age = list(map(lambda i: i['age'], data))
        age_x, bal_y = np.squeeze(np.fromiter(age, float)) , np.squeeze(np.fromiter(bal, float))
        
        def regression(x,y,degree):
            """create regression models, calculate r-squared"""
            par = np.polyfit(x, y, degree, full=True)
            slope = par[0][0]
            intercept = par[0][1]
            pred_age = list(map(lambda i: slope * i + intercept, x))
            plt.scatter(x, y, c='b')
            plt.xlabel('Age')
            plt.ylabel('Balance')
            if degree == 1:
                plt.title('Regression Line Using Degree 1')
            else:
                plt.title('Regression Line Using Degree 2')
            plt.plot(x, pred_age, '--r')
            lr = scipy.stats.linregress(y, pred_age)
            print(' \nPearson Linear Regression Calculations: \nCorrelation: ' + str(lr.rvalue))
            rsqr = lr.rvalue**2
            print('R-Squared: ' + str(rsqr))
            return plt.show()
       
        
        scatterplot(long_x, lat_y)
        regression(age_x, bal_y, 1)
        