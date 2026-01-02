''''''
# '''
# DATABASE CREATION
# '''
import sqlite3 as sq
database=sq.connect('management.db')
curs=database.cursor()
# query="""
# create table student(
# sid integer primary key AutoIncrement,
# sname text not null,
# phno integer  not null check (length(phno)=10),
# dob date not null,
# gender varchar(2) not null,
# address text not null,
# photo blob not null
# )"""


# curs.execute(query)

# '''
# FRONT END PAGE


import streamlit as st
from time import sleep
# functoions
def login():
    user_name=st.text_input('USER_NAME:')
    password=st.text_input('PASSWORD',type='password')
    login=st.button('LOGIN',type='primary')
    if login:
        if user_name=='admin' and password=='Admin@123':
            st.session_state.is_logged=True
            st.success('login successful')
            st.rerun()
def add():
    name=st.text_input('enter your name:')
    phno =st.text_input('enter your phno')
    dob=st.date_input('choose the date:')
    gender=st.radio('choose your gender',['male','female'])
    address=st.text_area('enter your address')
    photo=st.file_uploader('upload your photo',type=['jpg','png','svg','img'])
    insert=st.button('INSERT',type='primary')
    if insert:
        try:
            query="insert into student (sname,phno,dob,gender,address,photo) values(?,?,?,?,?,?)"
            photo_in_binary=photo.read()
            curs.execute(query,(name,phno,dob,gender,address,photo_in_binary))
            database.commit()
        except sq.DatabaseError as e:
            st.error('not update')
        else:
            st.write('you record duccesfully update')
           

def remove():
    _name=st.text_input('enter name: ')
    phno=st.text_input('enter phone: ')
    button=st.button('Delet',type='primary')
    query="""
        
         delete from student
         where sname=? and phno=?

     """
    if button:
        
        try:
           curs.execute(query,(_name,phno))
           database.commit()
       

           if curs.rowcount == 0:
               st.warning("Record not found ❗")
           else:
               sleep(0.5)
               st.success("Record deleted successfully 🗑️")

        except sq.DatabaseError as e:
            sleep(0.5)
            st.error("Database error occurred")

 
def update():

    n1=st.text_input('enetr update name:')
    p1=st.text_input('enetr phone number:')
    find=st.button('find',type='primary')

    if'versione' not in st.session_state:
        st.session_state.versione=False
    
    if st.session_state.versione:
        li=['name','phno','date of birth','gender','address','photo']
        radio=st.radio('select the update',li)
        if radio=='name':
           col='sname'
           name=st.text_input('enter your name:')
        elif radio=='phno':
           col='phno'
           name=st.text_input('enter your phno')

        elif radio=='date of birth':
           col='dob'
           name=st.date_input('choose the date:')
        elif radio=='gender':
           col='gender'
           name=st.radio('choose your gender',['male','female'])
        elif radio=='address':
           col='address'
           name=st.text_area('enter your address')
        elif radio=='photo':
           col='photo'
           name8=st.file_uploader('upload your photo',type=['jpg','png','svg','img'])
           if name8 != None:
               name=name8.read()


        upd=st.button('update',type='primary')
        if upd:
          try:
             curs.execute(f'update  student set {col}=? where sname=? and phno=?',(name,n1,p1))
             database.commit()
          except sq.DatabaseError as e:
             st.error(f"Database error: {e}")
          else:
             st.write('you profile update')
    
        
                 
    if find:
        try:
            res=curs.execute('select sname,phno from student where sname = ?  ;',(n1,)).fetchall()[0]
            if res[0]==n1 :
              st.session_state.versione=True
              
            else:
              st.error('you record not present in table')
        except sq.DatabaseError as e:
            st.error(f"Database error: {e}")
            
def display():
    n1 = st.text_input('Enter name:')
    ph1 = st.text_input('Enter the phone number')
    show = st.button('Find', type='primary')

    if show:
        try:
            res = curs.execute(
                'SELECT * FROM student WHERE sname=? AND phno=?;',
                (n1, ph1)
            ).fetchone()

            if res is None:
                st.error('Your record is not present')
            else:
                st.success(
                    f"""
                    Name: {res[1]}
                    Phone Number: {res[2]}
                    Date of Birth: {res[3]}
                    """
                )

        except sq.DatabaseError as e:
            st.error(f'Database error: {e}')

        
    
     

    
   

    



# we are creating the variable called is_logged in the session state
if 'is_logged' not in st.session_state:
    st.session_state.is_logged=False
# if is_logged is True then if will be executed
if st.session_state.is_logged:
    menu=['add a student','remove the student','update the student','display the students']
    option=st.radio('CHOOSE:',menu)
    if option=='add a student':
        add()
    elif option == 'remove the student':
        remove()
    elif option == 'update the student':
        update()
    elif option=='display the students':
        display()
    
else:
    login()










