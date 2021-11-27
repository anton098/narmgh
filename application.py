from flask import *
from pymongo import MongoClient
import random,string,requests


app = Flask(__name__)
CLIENT= MongoClient('mongodb+srv://christorf32:welcome123%40123@cluster0.3ojjt.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NONE')
db = CLIENT['NARMGH']

Registered_users = db['users']
username = "annorboadu"
apiKey = "ad43cb64139370fa55479c9446b08c8b"
From = "NARMGH"
url = "https://sms.dtechghana.com/api/v1/messages"
headers = {'Content-Type': 'application/json', 'Host': 'sms.dtechghana.com'}



@app.route('/home', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':

        if request.form['prime'] == 'signin':
            # Sign-in Functionality
            myquery= {'Userid':request.form['userid'], 'Password':request.form['pass']}
            #print(myquery)
            Database= list(Registered_users.find(myquery,{'_id':0}))

            if (request.form['userid'] in [i['Userid'] for i in Database] ) and \
                    (request.form['pass'] in [i['Password'] for i in Database]):
                Current_query = {'Userid': request.form['userid'], 'Password': request.form['pass']}
                userdata = list(Registered_users.find(Current_query, {'_id': 0}))
                return render_template('signedin.html',Userdata=userdata)

            return render_template('signedin.html')
        elif request.form['prime'] == 'signup':
            # Signup Functionality
            return render_template('signup.html')

        elif request.form['prime'] == 'sub':
            #Pushing to MongoDB Feature starts here
            try:
                payingmember= request.form['paying_member']
            #default
            except:
                payingmember= "No"
            password= ''.join(random.sample((string.ascii_lowercase + string.digits), 6))
            user_json= {
            'Paying_member': payingmember,
            'Surname': request.form['surname'],
            'FirstName': request.form['firstname'],
            'Middlename': request.form['middlename'],
            'Userid': 'NARMGH21/'+ str(1000),
            'Password': password,
            'Dob': request.form['dob'],
            'Gender': request.form['gender'],
            'Contact_no': request.form['contactno'],
            'Ghana_Card_no': request.form['cardno'],
            'Home_address': request.form['homeaddress'],
            'Regions': request.form['regions'],
            'District': request.form['district'],
            'Place_of_work': request.form['placeofwork'],
            'Rank': request.form['rank'],
            'Staffid': request.form['staffid'],
            'Pin': request.form['pin'],
            'Qualification': request.form['qualification']
            }

            Registered_users.insert_one(user_json)
            #Send sms to the Number
            To = request.form['contactno']
            mesg= "Dear "+ request.form['firstname'] +'\n'+ 'Your Registration has been received at NARMGH'+'\n'+'secretariat.'+\
                  '\n'+'\n' + 'Login details of NARMGH are'+ '\n' +'\n'+ 'UserID: '+ 'NARMGH21/'+ str(1000) + '\n'+ \
                  'Password: ' + password +'\n' + '\n' +'The information submitted is highly protected'+'\n' + 'Thank you.'

            payload = json.dumps({'to': To, 'from': From, 'content': mesg})
            response = requests.post(url, data=payload, headers=headers, auth=(username, apiKey))
            return render_template('registered.html')
    else:
        return render_template('homepage.html')

    return render_template('homepage.html')

if __name__ == '__main__':
    app.run()
