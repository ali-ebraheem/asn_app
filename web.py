from flask import Flask
from flask import render_template , request 
import requests 
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import pandas as convert

app = Flask(__name__)
@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        usr=request.form["name"]
        url =f'https://www.bigdatacloud.com/asn-lookup/{usr}'
        asn=[]
        company=[]

        asn1 = requests.get(url)
        soup = BeautifulSoup(asn1.text, 'html.parser')
        table = soup.find('div',class_ ='row insights-asn-view-details')
        team =table.find('ol',class_ ='data-table active index')
        for team1 in team.find_all('dt'):
                 company2 = team1.find_all('a')
                 for company3 in company2:
                    asn.append(company3.text)      

        company1 = requests.get(url)
        soup = BeautifulSoup(company1.text, 'html.parser')
        table = soup.find('div',class_ ='row insights-asn-view-details')
        team =table.find('ol',class_ ='data-table active index')
        for team1 in team.find_all('dd') :
             company.append(team1.text) 

        combined=[asn,company]
        export=zip_longest(*combined)                            
        with open('information.csv','w') as myfile:
             wr=csv.writer(myfile)            
             wr.writerow(["peers","company"])
             wr.writerows(export)
        con=convert.read_csv("information.csv")    
        con.to_html("table.html")
        
        return render_template("table.html")
    else:
        return render_template("home.html")

if __name__ == "__main__":
    app.run(debug = True)