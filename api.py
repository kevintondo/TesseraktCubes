import flask
from flask import request, jsonify
import mysql.connector
import serial





app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/UseLED', methods=['GET'])
def home():
    query_parameters = request.args
    cpt=0
    dst = query_parameters.get('dst')
    RColor = query_parameters.get('RColor')
    GColor = query_parameters.get('GColor')
    BColor = query_parameters.get('BColor')
  
    
    if (int(RColor)  > 255):
        cpt=cpt+1
    if (int(RColor) < 0):
        cpt=cpt+1
    if (int(GColor)  > 255 ):
        cpt=cpt+1
    if ( int(GColor) < 0):
        cpt=cpt+1
    if (int(BColor) > 255):
        cpt=cpt+1
    if ( int(BColor) < 0):
        cpt=cpt+1
    if ( dst == 0):
        cpt=cpt+1    
    
    if (cpt== 0):
        ser = serial.Serial('/dev/ttyUSB0',115200)
        data='{'+str.encode(str(dst)+';'+'3'+';'+str(RColor)+';'+str(GColor)+';'+str(BColor))+';0}'
        print data
        ser.write(data)
       
        return "ok"
    else:
        return "Error: params invalid"
    
    
@app.route('/GetConnectedBox', methods=['GET'])
def GetConnectedBox():
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="passwordroot",database="tesseraktbdd")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * from box_list where `is_connected` = 1;")
    myresult = mycursor.fetchall()
    #push to Kevin 
    return str(myresult)

@app.route('/RunBtn', methods=['GET'])
def RunBtn():
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="passwordroot",database="tesseraktbdd")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id_box, coord_x, coord_y from userresponse;")
    myresult = mycursor.fetchall()
    #push to Kevin 
    return str(myresult)

        
@app.route('/newID', methods=['GET'])
def newID():
    ser = serial.Serial('/dev/ttyUSB0',115200)
    ser.write('{'+str.encode(str(2)+';'+'1'+';'+str(3)+';0;0;0}'))
    return 'ok'

@app.route('/EventFacesCo', methods=['GET'])
def EventFacesCo():
    query_parameters = request.args
    cpt=0
    value=0
    b0 = query_parameters.get('b0')
    f0 = query_parameters.get('f0')
    b1 = query_parameters.get('b1')
    f1 = query_parameters.get('f1')
    
    
    if((b0 =='255' or b1 == '255')and (b0 =='255' or b1 =='255')):
        #add directly in 0,0
        print 'first'
        if(str(255)==str(b0)):
            print 'b0'
            boite_mere=b0
            boite_fille=b1
            face_mere=f0
            face_fille=f1
        else:
            print 'b1'
            boite_mere=b1
            boite_fille=b0
            face_mere=f1
            face_fille=f0
            
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="passwordroot",database="tesseraktbdd")
        mycursor= mydb.cursor()
        query="INSERT INTO `userresponse`( `id_box`, `email`, `coord_x`, `coord_y`) VALUES ("+str(1)+","+('email')+","+str(0)+","+str(0)+");"
        print query
        mycursor.execute(query)
        mydb.commit()
        mydb.disconnect()
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="passwordroot",database="tesseraktbdd")
        mycursor= mydb.cursor()
        query="UPDATE `box_list` SET `date_last_connection`= NOW(),`is_connected`= 1 WHERE `id_box` ="+str(boite_fille)
        print query
        mycursor.execute(query)
        mydb.commit()
        mydb.disconnect()
    elif(((b0 =='1' or b1 == '1') and (b0 =='2' or b1 =='2'))or((b0 =='1' and b1 == '1') )):
        
        if(str(1)==str(b0)):
            print 'b0'
            boite_mere=b0
            boite_fille=b1
            face_mere=f0
            face_fille=f1
        else:
            print 'b1'
            boite_mere=b1
            boite_fille=b0
            face_mere=f1
            face_fille=f0
            
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="passwordroot",database="tesseraktbdd")
        mycursor= mydb.cursor()
        query="INSERT INTO `userresponse`( `id_box`, `email`, `coord_x`, `coord_y`) VALUES ("+str(2)+","+('email')+","+str(0)+","+str(1)+");"
        print query
        mycursor.execute(query)
        mydb.commit()
        mydb.disconnect()
        
    elif(((b0 =='2' or b1 == '2') and (b0 =='3' or b1 =='3'))or((b0 =='2' and b1 == '2') )):
        
        if(str(2)==str(b0)):
            print 'b0'
            boite_mere=b0
            boite_fille=b1
            face_mere=f0
            face_fille=f1
        else:
            print 'b1'
            boite_mere=b1
            boite_fille=b0
            face_mere=f1
            face_fille=f0
            
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="passwordroot",database="tesseraktbdd")
        mycursor= mydb.cursor()
        query="INSERT INTO `userresponse`( `id_box`, `email`, `coord_x`, `coord_y`) VALUES ("+str(3)+","+'email'+","+str(0)+","+str(2)+");"
        print query
        mycursor.execute(query)
        mydb.commit()
        mydb.disconnect()
        
       
      
            
    return 'ok'
    
    
@app.route('/EventFacesDisco', methods=['GET'])
def EventFacesDisco():
    query_parameters = request.args
    cpt=0
    value=0
    b0 = query_parameters.get('b0')
    f0 = query_parameters.get('f0')
    
    if(b0 =='255'):
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="passwordroot",database="tesseraktbdd")
        mycursor= mydb.cursor()
        query="delete from `userresponse` where 1"
        mycursor.execute(query)
        mydb.commit()
        mydb.disconnect()
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="passwordroot",database="tesseraktbdd")
        mycursor= mydb.cursor()
        query="UPDATE `box_list` SET `date_last_connection`= NOW(),`is_connected`= 0 WHERE 1"
        print query
        mycursor.execute(query)
        mydb.commit()
        mydb.disconnect()
        return 'ok';
    elif(b0 =='1'):
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="passwordroot",database="tesseraktbdd")
        mycursor= mydb.cursor()
        query="delete from `userresponse` WHERE `id_box` =2 or `id_box` =3"
        mycursor.execute(query)
        mydb.commit()
        mydb.disconnect()
      
        return 'ok';
    elif(b0 =='2'):
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="passwordroot",database="tesseraktbdd")
        mycursor= mydb.cursor()
        query="delete from `userresponse` WHERE `id_box` =3"
        mycursor.execute(query)
        mydb.commit()
        mydb.disconnect()
     
        return 'ok';
    

app.run(host='0.0.0.0')