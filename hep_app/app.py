# Core pkgs
import streamlit as st, os
import numpy as np, pandas as pd, matplotlib.pyplot as pt
import seaborn as sns
import joblib
import hashlib
import matplotlib
matplotlib.use('Agg')


from db_manager import *
def generate_hashes(password):
    return hashlib.sha256(str.encode(password)).haxdigest()

def verify_hashes(password,hashed_text):
    if generate_hashes(password) == hashed_text:
        return hashed_text
    return False


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
            if password == '12345':
                st.success(f'Welcome {username}')

                activity = st.selectbox('Activity',submenu)
                if activity == 'Plot':
                    st.subheader('Data Vis Plot')

                elif activity == 'Prediction':
                    st.subheader('Prediction Analytics')
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
            add_userdata(new_username)
            st.success('You have successfully created a new account')
            st.info('Login to Get STarted')







if __name__== '__main__':
    main()
