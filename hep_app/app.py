# Core pkgs
import streamlit as st, os
import numpy as np, pandas as pd, matplotlib.pyplot as pt
import seaborn as sns
import joblib
import hashlib
import matplotlib
matplotlib.use('Agg')

# DB
from db_manager import *

# hashing the password
def generate_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def verify_hashes(password,hashed_text):
    if generate_hashes(password) == hashed_text:
        return hashed_text
    return False

gender_dict = {'male':1,'female':2}
feature_dict = {'No':1,'Yes':2}

def get_value(val,my_dict):
    for key,value in my_dict.items():
        if val == key:
            return value

def get_key(val):
    for key,value in my_dict.items():
        if val == key:
            return key

def get_fvalue(val):
    feature_dict = {'No':1,'Yes':2}
    for key,value in feature_dict.items():
        if val == key:
            return value


feature_names_best = ['age', 'sex', 'steroid', 'antivirals', 'fatigue', 'spiders',
                      'ascites','varices', 'bilirubin', 'alk_phosphate', 'sgot', 
                      'albumin', 'protime','histology']


# Load ML Models
def load_model(model_file):
    with open(os.path.join(model_file), 'rb') as f:
        model = joblib.load(f)
    return model

def main():
    '''Mortality prediction App'''
    st.title('Disease Mortality Prediction App')

    menu = ['Home','Login','Signup']
    submenu = ['Plot','Prediction']

    choice = st.sidebar.selectbox('Menu',menu)
    if choice == 'Home':
        st.subheader('Home')
        st.text('What is Hepatities?')

    elif choice == 'Login':
        username = st.sidebar.text_input('Username')
        password = st.sidebar.text_input('Passwprd',type='password')
        if st.sidebar.checkbox('Login'):
            create_usertable()
            hashed_password = generate_hashes(password)
            result = login_user(username,verify_hashes(password,hashed_password))
            if result:
                st.success(f'Welcome {username}')

                activity = st.selectbox('Activity',submenu)
                if activity == 'Plot':
                    st.subheader('Data Vis Plot')
                    df = pd.read_csv('data/clean_hepatitis_dataset.csv')
                    st.dataframe(df)

                    df['class'].value_counts().plot(kind='bar')
                    st.pyplot()

                    # Freq Dist Plot
                    freq_df = pd.read_csv('data/freq_df_hepatitis_dataset.csv')
                    st.bar_chart(freq_df['count'])

                    if st.checkbox('Area Chart'):
                        all_columns = df.columns.to_list()
                        feat_choices = st.multiselect('Choose a Feature',all_columns)
                        new_df = df[feat_choices]
                        st.area_chart(new_df)


                elif activity == 'Prediction':
                    st.subheader('Prediction Analytics')

                    age = st.number_input('Age',7,80)
                    sex = st.radio('Sex',tuple(gender_dict.keys()))
                    steroid = st.radio('Do you take Steroids?',tuple(feature_dict.keys()))
                    antivirals = st.radio('Do you take Antivirals?',tuple(feature_dict.keys()))
                    fatigue = st.radio("Do You Have Fatigue",tuple(feature_dict.keys()))
                    spiders = st.selectbox('Presence of Spider Neavi',tuple(feature_dict.keys()))
                    ascites = st.selectbox('Ascites',tuple(feature_dict.keys()))
                    varices = st.selectbox('Presence of Varices',tuple(feature_dict.keys()))
                    bilirubin = st.number_input('Bilirubin Content',0.0,8.0)
                    alk_phosphate = st.number_input('Alkaline Phospate Content',0.0,296.0)
                    sgot = st.number_input('Sgot',0.0,648.0)
                    albumin = st.number_input('Albumin',0.0,6.4)
                    protime = st.number_input('Prothrombin Time',0.0,100.0)
                    histology = st.selectbox('Histology',tuple(feature_dict.keys()))
                    feature_list = [age,get_value(sex,gender_dict),get_fvalue(steroid),
                                    get_fvalue(antivirals),get_fvalue(fatigue),
                                    get_fvalue(spiders),get_fvalue(ascites),
                                    get_fvalue(varices),bilirubin,alk_phosphate,
                                    sgot,albumin,int(protime),get_fvalue(histology)]
                    st.write(feature_list)
                    st.write(len(feature_list))
                    pretty_result = {"age":age,"sex":sex,"steroid":steroid,"antivirals":antivirals,"fatigue":fatigue,"spiders":spiders,"ascites":ascites,"varices":varices,"bilirubin":bilirubin,"alk_phosphate":alk_phosphate,"sgot":sgot,"albumin":albumin,"protime":protime,"histolog":histology}
                    st.json(pretty_result)
                    single_sample = np.array(feature_list).reshape(1,-1)

                    # ML
                    model_choice = st.selectbox("Select Model",["LR","KNN","DecisionTree"])
                    if st.button("Predict"):
                        if model_choice == "KNN":
                            loaded_model = load_model("models/knn_hepB_model.pkl")
                            prediction = loaded_model.predict(single_sample)
                            pred_prob = loaded_model.predict_proba(single_sample)
                        elif model_choice == "DecisionTree":
                            loaded_model = load_model("models/decisionTreeClassifier_hepB_model.pkl")
                            prediction = loaded_model.predict(single_sample)
                            pred_prob = loaded_model.predict_proba(single_sample)
                        else:
                            loaded_model = load_model("models/logistic_regresion_hepB_model.pkl")
                            prediction = loaded_model.predict(single_sample)
                            pred_prob = loaded_model.predict_proba(single_sample)

                        st.write(pred_prob[0][1])
                        if prediction == 1:
                            st.warning('Patient Dies')
                        else:
                            st.success('Patient Lives')

                        if pred_prob[0][1] < 0.45:
                            st.warning(f'There is a higher probability of the Patient Dying')
                        elif pred_prob[0][1] > 0.55:
                            st.success(f'There is a higher probability that Patient Lives')
                        else:
                            st.info(f'There is aproximately equal chances of the patient living or dying')



            else:
                st.warning('Incorect Username or Password')

    elif choice == 'Signup':
        new_username = st.text_input('user name')
        new_password = st.text_input('Password',type = 'password')
        confirm_password = st.text_input('Confirm Password',type='password')
        if new_password == confirm_password:
            st.success('Password Confirmed')
        else:
            st.warning('Password not thesame')

        if st.button('Submit'):
            create_usertable()
            hashed_new_password = generate_hashes(new_password)
            add_userdata(new_username, hashed_new_password)
            st.success('You have successfully created a new account')
            st.info('Login to Get Started')







if __name__== '__main__':
    main()
