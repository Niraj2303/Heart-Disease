import streamlit as st
import re
import sqlite3
import pandas as pd
import pickle
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Heart Disease", page_icon="fevicon.jpg", layout="centered", initial_sidebar_state="auto", menu_items=None)

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
          f"""
          <style>
          .stApp {{
              background: url("https://media.istockphoto.com/id/1359314170/photo/heart-attack-and-heart-disease-3d-illustration.jpg?s=612x612&w=0&k=20&c=K5Y-yzsfs7a7CyuAw-B222EMkT04iRmiEWzhIqF0U9E=");
              background-size: cover
          }}
          </style>
          """,
          unsafe_allow_html=True
      )
set_bg_hack_url()

conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_uesr(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()
     

with st.sidebar: 
        choice = option_menu(
                menu_title="Main menu",
                options=["Home","Login","SignUp","Contact us"],
                icons=["house","book","envelope"]
                )

if choice == "Home":
    st.title("Heart Disease Prediction System")
    st.text('''The Heart Disease Prediction System with Python Webapp is an advanced solution
designed to enhance cardiovascular health monitoring through the integration of 
machine learning and web technologies. Utilizing sophisticated algorithms
implemented in Python, the system analyzes diverse health indicators, 
including cholesterol levels, blood pressure, and medical history, 
to predict the risk of heart disease. The accompanying web application provides
an accessible interface for users to input their health data, receiving
instantaneous predictions and personalized recommendations for preventive 
measures. By harnessing the capabilities of predictive analytics, this system
empowers individuals and healthcare professionals to proactively manage 
cardiovascular health, enabling early detection, intervention, and lifestyle
adjustments. This integrated approach contributes to the prevention of heart
disease, promoting better overall cardiac health and reducing the burden on 
healthcare systems.''')

if choice=="SignUp":
        Fname = st.text_input("First Name")
        Lname = st.text_input("Last Name")
        Mname = st.text_input("Mobile Number")
        Email = st.text_input("Email")
        City = st.text_input("City")
        Password = st.text_input("Password",type="password")
        CPassword = st.text_input("Confirm Password",type="password")
        b2=st.button("SignUp")
        if b2:
            pattern=re.compile("(0|91)?[7-9][0-9]{9}")
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if Password==CPassword:
                if (pattern.match(Mname)):
                    if re.fullmatch(regex, Email):
                        create_usertable()
                        add_userdata(Fname,Lname,Mname,City,Email,Password,CPassword)
                        st.success("SignUp Success")
                        st.info("Go to Logic Section for Login")
                    else:
                        st.warning("Not Valid Email")         
                else:
                    st.warning("Not Valid Mobile Number")
            else:
                st.warning("Pass Does Not Match")
                
if choice=="Login":
    Email = st.sidebar.text_input("Email")
    Password = st.sidebar.text_input("Password",type="password")
    b1=st.sidebar.checkbox("Login")        
    if b1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            result = login_user(Email,Password)
            if result:
                st.success("Logged In as {}".format(Email))
                if Email=="a@a.com":    
                    Email1=st.text_input("delete Email") 
                    if st.button('Delete'):
                         delete_uesr(Email1) 
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                    st.dataframe(clean_db)
                else:
                    
                    menu2 = ["K-Nearest Neighbors", "SVM",
                             "Decision Tree", "Random Forest",
                             "Naive Bayes","ExtraTreesClassifier"]
                    choice2 = st.selectbox("Select ML",menu2)
                    
                    
                    Age1=int(st.slider('age',0,90))
                    sex=st.selectbox("Selecr Sex",["Male","Female"])
                    if sex=="Male":
                        sex1=0
                    else:
                        sex1=1
                    Chestpaintype=st.selectbox("chest pain",["low","mid","High","Very High"])
                    if Chestpaintype=="low":
                        Chestpaintype1=1
                    elif Chestpaintype=="mid":
                        Chestpaintype1=2
                    elif Chestpaintype=="High":
                        Chestpaintype1=3
                    elif Chestpaintype=="Very High":
                        Chestpaintype1=4
                    BP1=int(st.slider('BP',94,200))
                    cholesterol1=float(st.slider('cholesterol',126.0,564.0))
                    FBSover=st.selectbox("select FBS OVER",('YES','no'))
                    if FBSover=="YES":
                        FBSover1=0
                    elif FBSover=="no":
                        FBSover1=1
                    EKGresult=st.selectbox("EKG result",('low','mid','high'))
                    if EKGresult=="low":
                        EKGresult1=0
                    elif EKGresult=="mid":
                        EKGresult1=1
                    elif EKGresult=="high":
                        EKGresult1=2    
                    MAXHR1=int(st.slider('MAXHR',71,202))
                    EXERCISEangina=st.radio("select  Exercise Angina:",('yes','no'))
                    if EXERCISEangina=="yes":
                        EXERCISEangina1=0
                    elif EXERCISEangina=="no":
                        EXERCISEangina1=1
                    STdepression1=float(st.slider('STdepression',0.0,6.2))
                    slopofst1=int(st.slider( "Slop of st",1,3))
                    vesselsfluro=st.radio("select vesselsfluro",('Low','Mid','High'))
                    if vesselsfluro=="Low":
                        vesselsfluro1=0
                    elif vesselsfluro=="Mid":
                        vesselsfluro1=1
                    elif vesselsfluro=="High":
                         vesselsfluro1=3    
                    Thallium=st.selectbox("select Thallium:",('low','mid','high'))
                    if Thallium=="low":
                        Thallium1=3
                    elif Thallium=="mid":
                        Thallium1=6
                    elif Thallium=="high":
                         Thallium1=7 
                         
                    my_array=[Age1,sex1,Chestpaintype1,BP1,cholesterol1,FBSover1,EKGresult1,MAXHR1,
                              EXERCISEangina1,STdepression1,slopofst1,vesselsfluro1,Thallium1] 
                    predict=st.button("predict")
                    model=pickle.load(open("model.pkl",'rb'))
                    
                    
                    if predict:                        
                        tdata=[my_array]
                        #st.write(tdata)
                        if choice2=="K-Nearest Neighbors":
                            test_prediction = model[0].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="SVM":
                            test_prediction = model[1].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)                 
                        if choice2=="Decision Tree":
                            test_prediction = model[2].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="Random Forest":
                            test_prediction = model[3].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="Naive Bayes":
                            test_prediction = model[4].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="ExtraTreesClassifier":
                            test_prediction = model[5].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                
            else:
                st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")  
           
    

    
if choice=="Contact us":
    from PIL import Image
    img=Image.open("streamlit.png")
    st.image(img, width=200)
    st.text("--------------------------")    
    
