from flask import Flask, render_template, request,redirect,url_for, session
from pymongo import MongoClient
import uuid,random,string,os
from datetime import datetime
from flask_session import Session

#client = MongoClient('localhost:27017') (local)
mongodb_hostname = os.environ.get("MONGO_HOSTNAME","localhost")
client = MongoClient('mongodb://'+mongodb_hostname+':27017/')

db = client['DS_Airlines']
collection1 = db['Users']
collection2 = db['Flights']
collection3 = db['Booking']
collection4 = db['Admins']
app = Flask(__name__)
sess = Session()
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)

@app.route("/")
def Start():
     return redirect(url_for('HomePage'))
  
@app.route("/HomePage")
def HomePage():
     return render_template('HomePage.html')

@app.route("/Category",methods=['GET', 'POST'])
def Category():
      if request.method == 'POST':
        if request.form.get('user') == 'Απλός Χρήστης':
           return redirect(url_for('SignUp'))
        elif  request.form.get('admin') == 'Διαχειριστής':
            return redirect(url_for('LogInA'))
      else:
          return render_template('Category.html')
      return render_template('Category.html')

@app.route("/SignUp",methods=['GET','POST'])
def SignUp():
    if request.method == "POST":
        if request.form.get('submit') == 'Εγγραφή':
                 email_f = 0
                 username_f = 0
                 passport_f = 0
                 psw = 0
                 psp = 0
                 digit = 0
                 Email = request.form.get("email")
                 Username = request.form.get("username")
                 Fullname = request.form.get("fullname")
                 Password = request.form.get("password")
                 Passport = request.form.get("passport")
                 if (Email != "" and Username != "" and Fullname != "" and Password != "" and Passport != "") :
                   if (len(Password) >= 8):
                    for i in Password: 
                          if (i.isdigit()):
                            digit+=1                 
                    if not(digit>=1):
                      psw = 1
                   else:
                     psw = 1   
                   if (len(Passport) == 9):
                       str = Passport[:2]
                       dig = Passport[2:]
                       if not(str.isalpha() and dig.isdigit()):
                            psp = 1
                   else:
                         psp = 1        
                   if (psw == 1 and psp == 0):
                      return redirect(url_for('ErrorPassword'))   
                   elif (psw == 0 and psp == 1): 
                      return redirect(url_for('ErrorPassport'))   
                   elif (psw == 1 and psp == 1):
                       return redirect(url_for('ErrorPasswordPassport'))  
                   else:
                        email_found = collection1.find_one({'Email': Email}) 
                        email_found_a = collection4.find_one({'email': Email})
                        username_found = collection1.find_one({'Username': Username})
                        passport_found = collection1.find_one({'Passport': Passport})
                        if email_found or email_found_a:
                           email_f = 1
                        if username_found:
                           username_f = 1
                        if passport_found:
                            passport_f = 1
                        if (email_f == 1 and username_f == 0 and passport_f == 0):     
                            return redirect(url_for('EmailAlreadyExists'))
                        elif (email_f == 0 and username_f == 1 and passport_f == 0):  
                             return redirect(url_for('UsernameAlreadyExists')) 
                        elif (email_f == 0 and username_f == 0 and passport_f == 1):  
                             return redirect(url_for('PassportAlreadyExists'))   
                        elif (email_f == 1 and username_f == 1 and passport_f == 0):  
                             return redirect(url_for('EmailUsernameAlreadyExist')) 
                        elif (email_f == 1 and username_f == 0 and passport_f == 1):  
                             return redirect(url_for('EmailPassportAlreadyExist'))
                        elif (email_f == 0 and username_f == 1 and passport_f == 1):  
                             return redirect(url_for('UsernamePassportAlreadyExist'))  
                        elif (email_f == 1 and username_f == 1 and passport_f == 1):     
                             return redirect(url_for('EmailUsernamePassportAlreadyExist'))  
                        else:                      
                         collection1.insert_one({'Email': Email, 'Username': Username, 'Fullname': Fullname, 'Password': Password, 'Passport': Passport,"Deactivation":"no","Activation_C":""})
                         return redirect(url_for('RegistrationSuccessful'))   
                 else:
                  return redirect(url_for('Error')) 
    else:
          render_template('SignUp.html')     
    return render_template('SignUp.html') 

@app.route("/Error")   
def Error():
     return render_template('ErrorMessage.html')

@app.route("/ErrorPassword")   
def ErrorPassword():
     return render_template('Password.html')

@app.route("/ErrorPassport")   
def ErrorPassport():
     return render_template('Passport.html')

@app.route("/ErrorPasswordPassport")   
def ErrorPasswordPassport():
     return render_template('PswPsp.html')

@app.route("/EmailAlreadyExists")   
def EmailAlreadyExists():
     return render_template('EmailAl.html')

@app.route("/UsernameAlreadyExists")   
def UsernameAlreadyExists():
     return render_template('UsernameAl.html')

@app.route("/PassportAlreadyExists")   
def PassportAlreadyExists():
     return render_template('PassportAl.html')

@app.route("/EmailUsernameAlreadyExist")   
def EmailUsernameAlreadyExist():
     return render_template('EmailUsernameAl.html')

@app.route("/EmailPassportAlreadyExist")   
def EmailPassportAlreadyExist():
     return render_template('EmailPassportAl.html')

@app.route("/UsernamePassportAlreadyExist")   
def UsernamePassportAlreadyExist():
     return render_template('UsernamePassportAl.html')

@app.route("/EmailUsernamePassportAlreadyExist")   
def EmailUsernamePassportAlreadyExist():
     return render_template('EmailUsernamePassportAl.html')

@app.route("/RegistrationSuccessful")   
def RegistrationSuccessful():
     return render_template('AccompMessage.html')

@app.route("/LogInU",methods=['GET','POST'])
def LogInU():
    if request.method == "POST":
          if request.form.get('entr') == 'Είσοδος':   
             session["email/username"] = request.form.get("email/username")  
             Password = request.form.get("password")
             email_pass_found = collection1.find_one({'Email': session["email/username"], 'Password': Password}) 
             username_pass_found = collection1.find_one({'Username': session["email/username"],'Password': Password})
             if session["email/username"] != "" and Password != "":
               if (email_pass_found or username_pass_found):
                deact = collection1.find_one(email_pass_found,{"Deactivation":1,"_id":0})['Deactivation']
                deact1 = collection1.find_one(username_pass_found,{"Deactivation":1,"_id":0})['Deactivation']
                if (deact == "no" or deact1 == "no"):
                     return redirect(url_for('AccompLogIn'))
                else:
                     return redirect(url_for('Deact')) 
               else:
                   return redirect(url_for('FailLogIn')) 
             else:
              return redirect(url_for('Error_L'))          
    else:
       return render_template('LogInU.html')        
    return render_template('LogInU.html')      

@app.route("/Error_L")   
def Error_L():
     return render_template('Error_L.html')

@app.route("/AccompLogIn")   
def AccompLogIn():
     return render_template('AccompLogIn.html')

@app.route("/FailLogIn")   
def FailLogIn():
     return render_template('FailLogIn.html')

@app.route("/Deact")   
def Deact():
     return render_template('Deact.html')

@app.route("/Services", methods=['GET', 'POST'])
def Services():
    if request.method == 'POST':
        if request.form.get('search') == 'Αναζήτηση Πτήσης':
           return redirect(url_for('Search'))
        elif request.form.get('booking') == 'Κράτηση Εισιτηρίου':
            return redirect(url_for('Booking'))
        elif  request.form.get('show') == 'Εμφάνιση Υπάρχουσας Κράτησης':
            return redirect(url_for('Ex_Booking'))    
        elif  request.form.get('cancel') == 'Ακύρωση Κράτησης':
            return redirect(url_for('Cancel'))    
        elif  request.form.get('time') == 'Εμφάνιση Όλων Των Κρατήσεων Σε Χρονολογική Σειρά':
            return redirect(url_for('Booking_T'))
        elif  request.form.get('money') == 'Εμφάνιση Ακριβότερης Και Φθηνότερης Κράτησης':
            return redirect(url_for('Booking_M')) 
        elif  request.form.get('direction') == 'Εμφάνιση Όλων Των Κρατήσεων Βάσει Προορισμού':
            return redirect(url_for('Booking_D')) 
        elif  request.form.get('deactivation') == 'Απενεργοποίηση Λογαριασμού':
            return redirect(url_for('Deactivation')) 
        elif  request.form.get('logout') == 'Έξοδος Από Το Σύστημα':
            return redirect(url_for('LogOut'))        
    else: 
         return render_template('Services.html')
    return render_template('Services.html')

@app.route("/Search", methods=['GET', 'POST'])
def Search():
     if request.method == 'POST':
        if request.form.get('search') == 'Αναζήτηση':
          location = request.form.get("location")  
          direction = request.form.get("direction") 
          date = request.form.get("date")
          if location == "" or direction == "" or date == "":
               return redirect(url_for('ErrorM'))
          else:   
           date_inv = datetime.strptime(request.form.get("date"),"%Y-%m-%d").strftime("%d-%m-%Y")  
           data_found = collection2.find_one({'date': date_inv,'location': location,'direction': direction})    
           if data_found:
               data_found1 = collection2.find({'date': date_inv,'location': location,'direction': direction})
               return render_template('Flights.html', data_found1=data_found1) 
           else:
              return redirect(url_for('NotFound'))    
     else:
          return render_template('Search.html')
     return render_template('Search.html')

@app.route("/ErrorM")   
def ErrorM():
     return render_template('ErrorM.html')

@app.route("/NotFound")   
def NotFound():
     return render_template('NotFound.html')

@app.route("/Booking",methods=['GET','POST'])
def Booking():
     if request.method == 'POST':
        if request.form.get('submit') == 'Κράτηση Εισιτηρίου':
          card = 0
          digit = 0
          number = 0
          passport = 0
          flight = 0
          number_f = request.form.get("number")  
          name = request.form.get("fullname") 
          passport_n = request.form.get("passport") 
          card_n = request.form.get("card") 
          number_found = collection2.find_one({'number': number_f})
          passport_found = collection1.find_one({'Passport': passport_n})
          myquery = {"number":number_f,"availability": 0 }
          expr = collection2.find_one(myquery)
          expr1 = collection3.find_one({"number":number_f,"Passport":passport_n})
          if number_f != "" and name != "" and passport_n != "" and card_n != "" :
            if not(number_found) or expr:
               number = 1
            if expr1:
                flight = 1    
            if not (passport_found):
               passport = 1
            if len(card_n) == 16:     
             for i in card_n: 
                  if (i.isdigit()):
                         digit+=1  
             if not(digit == 16):
                   card = 1 
            else:
               card = 1
            if (flight == 1):
               return redirect(url_for('FlightExists'))     
            if (number == 1 and passport == 0 and card == 0):
               return redirect(url_for('Number'))    
            elif (number == 0 and passport == 1 and card == 0):
                return redirect(url_for('Pass')) 
            elif (number == 0 and passport == 0 and card == 1):
                return redirect(url_for('Card'))  
            elif (number == 1 and passport == 1 and card == 0):
                return redirect(url_for('NumberPass'))             
            elif (number == 1 and passport == 0 and card == 1):
                return redirect(url_for('NumberCard'))
            elif (number == 0 and passport == 1 and card == 1):
                return redirect(url_for('PassCard'))
            elif (number == 1 and passport == 1 and card == 1):
                return redirect(url_for('NumberPassCard')) 
            else:
               random_number = uuid.uuid4().hex[:6]
               date = collection2.find_one({'number': number_f})["date"]
               time = collection2.find_one({'number': number_f})["time"]
               location = collection2.find_one({'number': number_f})["location"]
               direction = collection2.find_one({'number': number_f})["direction"]
               cost = collection2.find_one({'number': number_f})["cost"]
               duration = collection2.find_one({'number': number_f})["duration"]
               collection3.insert_one({'datetime':(datetime.now()).strftime("%d/%m/%Y %H:%M:%S"),'booking_n': random_number,'number': number_f, 'fullname': name, 'Passport': passport_n, 'card': card_n, 'date':date,'time':time,'location':location,'direction':direction,'cost':cost,'duration':duration})
               collection2.find_one_and_update({'number':number_f},{ '$inc': { 'availability': -1 }})
               data_coll3 = collection3.find({'booking_n':random_number},{"_id":0})
               return render_template('AccompBooking.html',data_coll3=data_coll3)
          else:
               return redirect(url_for('Error_B'))    
     else:
          return render_template('Booking.html')     
     return render_template('Booking.html')  

@app.route("/FlightExists")   
def FlightExists():
     return render_template('FlightExists.html')

@app.route("/Error_B")   
def Error_B():
     return render_template('Error_B.html')

@app.route("/Number")   
def Number():
     return render_template('Number.html')

@app.route("/Pass")   
def Pass():
     return render_template('Pass.html')     

@app.route("/Card")   
def Card():
     return render_template('Card.html')

@app.route("/NumberPass")   
def NumberPass():
     return render_template('NumberPass.html')

@app.route("/NumberCard")   
def NumberCard():
     return render_template('NumberCard.html')

@app.route("/PassCard")   
def PassCard():
     return render_template('PassCard.html')

@app.route("/NumberPassCard")   
def NumberPassCard():
     return render_template('NumberPassCard')                    

@app.route("/Ex_Booking", methods=['GET', 'POST'])
def Ex_Booking():
     if request.method == 'POST':
        if request.form.get('submit') == 'Εμφάνιση Υπάρχουσας Κράτησης':
          unique_n = request.form.get("number")  
          data_found = collection3.find_one({'booking_n': unique_n})
          if unique_n != "":
            if data_found:
               Email_Username = session.get('email/username')
               expr = collection1.find_one({"Email":Email_Username},{"Passport":1,"_id":0})
               expr1 = collection1.find_one({"Username":Email_Username},{"Passport":1,"_id":0})
               expr2 = collection3.find_one({"booking_n":unique_n},{"Passport":1,"_id":0})
               if (expr == expr2 or expr1 == expr2):
                  data_found3 = collection3.find({'booking_n': unique_n})
                  return render_template('Accomp_Ex.html', data_found3=data_found3)
               else:
                  return redirect(url_for('NotOwner')) 
            else:
              return redirect(url_for('NotFoundBook'))  
          else:
               return redirect(url_for('Error_Ex'))     
     else:
          return render_template('Ex_Booking.html')
     return render_template('Ex_Booking.html')

@app.route("/Error_Ex")   
def Error_Ex():
     return render_template('Error_Ex.html')

@app.route("/NotFoundBook")   
def NotFoundBook():
     return render_template('NotFoundBook.html')
     
@app.route("/Cancel", methods=['GET', 'POST'])
def Cancel():
     if request.method == 'POST':
        if request.form.get('submit') == 'Ακύρωση Κράτησης':
          unique_n = request.form.get("number")  
          data_found = collection3.find_one({'booking_n': unique_n})
          if unique_n != "":
             if data_found:
               Email_Username = session.get('email/username')
               expr = collection1.find_one({"Email":Email_Username},{"Passport":1,"_id":0})
               expr1 = collection1.find_one({"Username":Email_Username},{"Passport":1,"_id":0})
               expr2 = collection3.find_one({"booking_n":unique_n},{"Passport":1,"_id":0})
               if (expr == expr2 or expr1 == expr2):
                  data_found1 = collection3.find_one({'booking_n': unique_n},{"number":1,"_id":0})
                  card = collection3.find_one({'booking_n': unique_n},{"card":1,'_id':0})['card']
                  cost = collection3.find_one({'booking_n': unique_n},{"cost":1,'_id':0})['cost']
                  collection2.find_one_and_update(data_found1,{ '$inc': { 'availability': 1 }})
                  collection3.delete_one({'booking_n': unique_n})
                  return render_template('Accomp_Can.html', card=card,cost=cost)
               else:
                  return redirect(url_for('NotOwnerC'))
             else:
               return redirect(url_for('NotFoundBookC')) 
          else:
               return redirect(url_for('Error_C'))         
     else:
          return render_template('Cancel.html')
     return render_template('Cancel.html')

@app.route("/NotOwnerC")   
def NotOwnerC():
     return render_template('NotOwnerC.html')

@app.route("/NotFoundBookC")   
def NotFoundBookC():
     return render_template('NotFoundBookC.html')
    
@app.route("/Error_C")   
def Error_C():
     return render_template('Error_C.html')

@app.route("/Booking_T", methods=['GET', 'POST'])
def Booking_T():
     if request.method == 'POST':
       if request.form.get('submit') == 'Εμφάνιση Κρατήσεων':
           Email_Username = session.get('email/username')
           expr = collection1.find_one({"Email":Email_Username},{"Passport":1,"_id":0})
           expr1 = collection1.find_one({"Username":Email_Username},{"Passport":1,"_id":0})
           if (expr):
               expr2 = collection3.find_one(expr,{"Passport":1,"_id":0})
           else:
               expr2 = collection3.find_one(expr1,{"Passport":1,"_id":0})  
           if expr2:  
               data_f = collection3.find(expr2,{ "_id": 0,"datetime":0 })
               if request.form.get('booking') == 'Παλαιότερες Κρατήσεις':
                 data_sort = data_f.sort("datetime")
                 return render_template('ShowBook.html',data_sort=data_sort) 
               elif request.form.get('booking') == 'Νεότερες Κρατήσεις':
                 data_sort = data_f.sort("datetime",-1)
                 return render_template('ShowBook.html',data_sort=data_sort) 
               else:
                    return redirect(url_for('Error_F'))     
           else:
                return redirect(url_for('NotBook'))
     else:
          return render_template('BookT.html')
     return render_template('BookT.html')

@app.route("/Error_F")   
def Error_F():
     return render_template('Error_F.html')

@app.route("/NotBook")   
def NotBook():
     return render_template('NotBook.html')

@app.route("/Booking_M", methods=['GET', 'POST'])
def Booking_M():
     if request.method == 'POST':
        if request.form.get('search') == 'Πατήστε Εδώ Για Να Δείτε Την Ακριβότερη Και Την Φθηνότερη Κράτηση':
           Email_Username = session.get('email/username')
           expr = collection1.find_one({"Email":Email_Username},{"Passport":1,"_id":0})
           expr1 = collection1.find_one({"Username":Email_Username},{"Passport":1,"_id":0})
           if (expr):
               expr2 = collection3.find_one(expr,{"Passport":1,"_id":0})
           else:
               expr2 = collection3.find_one(expr1,{"Passport":1,"_id":0})  
           if expr2:  
                 passport = collection3.find_one(expr1,{"Passport":1,"_id":0})["Passport"]
                 max = collection3.find_one(expr2,sort=[("cost", -1)])["cost"]
                 min = collection3.find_one(expr2,sort=[("cost", +1)])["cost"]
                 data_max = collection3.count_documents({'Passport':passport,'cost':max})
                 data_min = collection3.count_documents({'Passport':passport,'cost':min})
                 if data_max >1 and data_min == 1:
                     max_data = collection3.find({'Passport':passport,'cost':max},{"_id":0,"datetime":0}).sort("datetime").limit(1)
                     min_data = collection3.find({'Passport':passport,'cost':min},{"_id":0,"datetime":0})
                 elif data_max == 1 and data_min > 1:
                    max_data = collection3.find({'Passport':passport,'cost':max},{"_id":0,"datetime":0})
                    min_data = collection3.find({'Passport':passport,'cost':min},{"_id":0,"datetime":0}).sort("datetime").limit(1)
                 elif data_max > 1 and data_min > 1:   
                     max_data = collection3.find({'Passport':passport,'cost':max},{"_id":0,"datetime":0}).sort("datetime").limit(1)
                     min_data = collection3.find({'Passport':passport,'cost':min},{"_id":0,"datetime":0}).sort("datetime").limit(1)
                 else:
                     max_data = collection3.find({'Passport':passport,'cost':max},{"_id":0,"datetime":0})
                     min_data = collection3.find({'Passport':passport,'cost':min},{"_id":0,"datetime":0})
                 return render_template('M_Book.html',max_data=max_data,min_data=min_data)      
           else:
                return redirect(url_for('NotBook'))
     else:
          return render_template('Auto.html')
     return render_template('Auto.html')                 

@app.route("/Booking_D", methods=['GET', 'POST'])
def Booking_D():
     if request.method == 'POST':
        if request.form.get('entr') == 'Είσοδος':
           Email_Username = session.get('email/username')
           expr = collection1.find_one({"Email":Email_Username},{"Passport":1,"_id":0})
           expr1 = collection1.find_one({"Username":Email_Username},{"Passport":1,"_id":0})
           dir = request.form.get("direction")
           if dir != "":
            if (expr):
                expr2 = collection3.find_one(expr,{"Passport":1,"_id":0})
            else:
               expr2 = collection3.find_one(expr1,{"Passport":1,"_id":0})  
            dir_f = collection2.find_one({"direction":dir},{"direction":1,"_id":0})
            if dir_f:
              if expr2:  
                 passport = collection3.find_one(expr1,{"Passport":1,"_id":0})["Passport"]
                 direction = collection3.find_one({"Passport":passport},{"direction":1,"_id":0})
                 if direction: 
                    data_d = collection3.find_one({'Passport':passport,'direction':dir},{'_id':0,'datetime':0})
                    if data_d :  
                      found = collection3.find({'Passport':passport,'direction':dir},{'_id':0,'datetime':0})   
                      return render_template('D_Book.html',found=found)  
                    else: 
                       return redirect(url_for('NotBook'))  
                 else:
                     return redirect(url_for('No_Dir_F'))       
              else:
                return redirect(url_for('NotBook'))
            else:
                return redirect(url_for('Direction'))  
           else:
               return redirect(url_for('Error_D'))         
     else:
          return render_template('Show_D.html')
     return render_template('Show_D.html')                 

@app.route("/Direction")   
def Direction():
     return render_template('Direction.html')

@app.route("/Error_D")   
def Error_D():
     return render_template('Error_D.html')

@app.route("/No_Dir_F")   
def No_Dir_F():
     return render_template('No_Dir_F.html')

@app.route("/Deactivation", methods=['GET', 'POST'])
def Deactivation():
     if request.method == 'POST':
        if request.form.get('deactivation') == 'Πατήστε Εδώ Για Να Απενεργοποιήσετε Τον Λογαριασμό Σας':
           Email_Username = session.get('email/username')
           expr = collection1.find_one({"Email":Email_Username})
           expr1 = collection1.find_one({"Username":Email_Username})
           N = 12
           random_number = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=N))
           if expr:
                collection1.find_one_and_update(expr,{"$set":{"Deactivation":"yes","Activation_C":random_number,"Password":random_number}})
           else:
               collection1.find_one_and_update(expr1,{"$set":{"Deactivation":"yes","Activation_C":random_number}})    
           return render_template('Deactivation.html',random_number=random_number)      
     else:
          return render_template('Auto1.html')
     return render_template('Auto1.html')  

@app.route("/Activation", methods=['GET', 'POST'])
def Activation():
     if request.method == 'POST':
        if request.form.get('entr') == 'Ενεργοποίηση':
           passport = request.form.get('passport') 
           code = request.form.get('activ_c')
           data_f = collection1.find_one({'Passport':passport,'Activation_C':code})
           if passport != "" and code != "":
              if data_f:
                collection1.find_one_and_update({'Passport':passport},{"$set":{"Deactivation":"no","Activation_C":""}})
                return redirect(url_for('ActivationAccomp'))  
              else:
                return redirect(url_for('ActivationF'))
           else:
               return redirect(url_for('Error_Act'))      
     else:
          return render_template('Activation.html')
     return render_template('Activation.html')  

@app.route("/Error_Act")
def Error_Act():
     return render_template('Error_Act.html')

@app.route("/ActivationAccomp")
def ActivationAccomp():
     return render_template('ActivationAccomp.html')

@app.route("/ActivationF")
def ActivationF():
     return render_template('ActivationF.html')

@app.route("/LogInA",methods=['GET','POST'])
def LogInA():
    if request.method == "POST":
          if request.form.get('entr') == 'Είσοδος':   
             email= request.form.get("email")  
             password = request.form.get("password")
             session['email_found'] = collection4.find_one({'email': email, 'password': password}) 
             if email != "" and password != "":
                  if (session['email_found']):
                      f_time = collection4.find_one({'email': email, 'password': password},{'first_time':1,'_id':0})['first_time']
                      if f_time == "no" :
                        return redirect(url_for('AccompLogInA'))
                      else:
                         return redirect(url_for('Change_Pass'))       
                  else:
                     return redirect(url_for('FailLogInA')) 
             else:
              return redirect(url_for('Error_L_A'))          
    else:
       return render_template('LogInA.html')        
    return render_template('LogInA.html')      

@app.route("/AccompLogInA")
def AccompLogInA():
     return render_template('AccompLogInA.html')

@app.route("/FailLogInA")
def FailLogInA():
     return render_template('FailLogInA.html')

@app.route("/Error_L_A")
def Error_L_A():
     return render_template('Error_L_A.html')

@app.route("/Change_Pass",methods=['GET','POST'])
def Change_Pass():
   if request.method == "POST":
          if request.form.get('entr') == 'Αλλαγή':  
             new_pass =  request.form.get("password")
             passw = session['email_found']["password"]
             if new_pass != '': 
               if new_pass == passw :
                    return redirect(url_for('SamePass')) 
               else:
                    collection4.find_one_and_update(session['email_found'],{"$set":{"password":new_pass,"first_time":"no"}})
                    return redirect(url_for('AccompLogInA'))   
             else:
                  return redirect(url_for('Error_Pass'))          
   else:
         return render_template('PasswordC.html')
   return render_template('PasswordC.html')

@app.route("/Error_Pass")
def Error_Pass():
     return render_template('Error_Pass.html')    

@app.route("/SamePass")
def SamePass():
     return render_template('SamePass.html')    

@app.route("/ServicesA", methods=['GET', 'POST'])
def ServicesA():
    if request.method == 'POST':
        if request.form.get('insert') == 'Εισαγωγή Νέου Διαχειριστή':
           return redirect(url_for('New_Admin'))
        elif request.form.get('create') == 'Δημιουργία Πτήσης':
            return redirect(url_for('Create_F'))
        elif  request.form.get('change') == 'Αλλαγή/Διόρθωση Τιμής Πτήσης':
            return redirect(url_for('Change_C'))
        elif  request.form.get('delete') == 'Διαγραφή Πτήσης':
            return redirect(url_for('Delete_F')) 
        elif  request.form.get('logout') == 'Έξοδος Από Το Σύστημα':
            return redirect(url_for('LogOut'))     
    else: 
         return render_template('ServicesA.html')
    return render_template('ServicesA.html')

@app.route("/New_Admin",methods=['GET','POST'])
def New_Admin():
    if request.method == "POST":
          if request.form.get('entr') == 'Εισαγωγή':  
             email= request.form.get("email")  
             fullname = request.form.get("fullname")
             email_f1 = collection1.find_one({"Email":email})
             email_f4 = collection4.find_one({"email":email})
             if email != '' and fullname != '':
               if email_f1 or email_f4:
                 return redirect(url_for('Email_Ex'))
               else:
                 N = 8
                 random_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=N))
                 collection4.insert_one({"email":email,"fullname":fullname,"password":random_pass,"first_time":"yes"})
                 return render_template ("Success_C.html",random_pass=random_pass)
             else: 
                 return redirect(url_for("Error_Comp")) 
    else:           
         return render_template('New_Admin.html')
    return render_template('New_Admin.html')

@app.route("/Error_Comp")
def Error_Comp():
     return render_template('Error_Comp.html')     

@app.route("/Email_Ex")
def Email_Ex():
     return render_template('Email_Ex.html')  

@app.route("/Create_F",methods=['GET','POST'])
def Create_F():
    if request.method == "POST":
          if request.form.get('entr') == 'Δημιουργία': 
               time = request.form.get("time")
               date = request.form.get("date")
               location = request.form.get("location") 
               direction = request.form.get("direction") 
               cost = request.form.get("cost")
               duration = request.form.get("duration")
               if time != '' and date != '' and location != '' and direction != '' and cost != '' and duration != '' :
                    collection2.find_one({'time':time,'date':date})
                    duration_h = str(request.form.get("hours"))
                    duration_m = str(request.form.get("minutes"))
                    duration = duration_h+" h "+duration_m+" min"
                    date_inv = datetime.strptime(request.form.get("date"),"%Y-%m-%d").strftime("%d-%m-%Y")
                    number = location[0]+direction[0]+ date_inv[8:10]+ date_inv[3:5]+ date_inv[0:2] + time[0:2] 
                    collection2.insert_one({'date': date_inv,'time':time,'location':location,'direction':direction,'cost':float(cost),'duration':duration,'availability':220,'number':number})
                    return redirect(url_for('Accomp_Creation'))
               else:
                    return redirect(url_for('Fail_Creation'))
    else:
          return render_template('Create_F.html')
    return render_template('Create_F.html')

@app.route("/Accomp_Creation")
def Accomp_Creation():
     return render_template('Accomp_Creation.html')

@app.route("/Fail_Creation")
def Fail_Creation():
     return render_template('Fail_Creation.html')

@app.route("/Change_C",methods=['GET','POST'])
def Change_C():
     if request.method == "POST":
          if request.form.get('entr') == 'Διόρθωση': 
            code = request.form.get("code")
            cost = request.form.get("cost") 
            data_f = collection2.find_one({'number':code})
            if code != '' and cost != '':
              if data_f:
                 availability = collection2.find_one({'number':code},{'_id':0,'availability':1})['availability']
                 if availability == 220:
                    collection2.find_one_and_update(data_f,{"$set":{"cost":float(cost)}})
                    return redirect(url_for('Accomp_Change_C'))
                 else:
                    return redirect(url_for('Error_Change_C'))
              else:
                   return redirect(url_for('Error_Data_F'))
            else:
                 return redirect(url_for('Error_Compl'))  
     else:
        return render_template('Change_C.html')
     return render_template('Change_C.html')

@app.route("/Accomp_Change_C")
def Accomp_Change_C():
     return render_template('Accomp_Change_C.html')     

@app.route("/Error_Change_C")
def Error_Change_C():
     return render_template('Error_Change_C.html')     

@app.route("/Error_Data_F")
def Error_Data_F():
     return render_template('Error_Data_F.html')     

@app.route("/Error_Compl")
def Error_Compl():
     return render_template('Error_Compl.html')         

@app.route("/Delete_F",methods=['GET','POST'])
def Delete_F():
     if request.method == "POST":
          if request.form.get('entr') == 'Διαγραφή': 
            code = request.form.get("code") 
            data_f = collection2.find_one({'number':code})
            if code != '' :
              if data_f:
                 availability = collection2.find_one({'number':code},{'_id':0,'availability':1})['availability']
                 if availability == 220:
                    collection2.find_one_and_delete(data_f)
                    return redirect(url_for('Accomp_Delete'))
                 else:
                    return redirect(url_for('Error_Delete'))
              else:
                   return redirect(url_for('Error_Data_Found'))
            else:
                 return redirect(url_for('Error_Com'))  
     else:
        return render_template('Delete_F.html')
     return render_template('Delete_F.html')     

@app.route("/Accomp_Delete")
def Accomp_Delete():
     return render_template('Accomp_Delete.html')     

@app.route("/Error_Delete")
def Error_Delete():
     return render_template('Error_Delete.html')     

@app.route("/Error_Com")
def Error_Com():
     return render_template('Error_Com.html')  

@app.route("/Error_Data_Found")
def Error_Data_Found():
     return render_template('Error_Data_Found.html')   

@app.route("/LogOut")
def LogOut():
     return render_template('Log_Out.html')           

if __name__ == '__main__':
 app.run(debug=True, host='0.0.0.0', port=5000)