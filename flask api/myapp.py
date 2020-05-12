from flask import Flask, render_template, request, redirect, url_for, session, g, flash 
import requests
from sklearn.externals import joblib
import pickle
import math
import os
import numpy as np
import pandas as pd
import ast
# import sklearn
# from sklearn.preprocessing import StandardScaler
##############################################################################################
from az import main_func

########################################################
app = Flask(__name__) 
 
@app.route('/')
def page():
    return render_template('home.html')
 
@app.route('/send', methods=['GET', 'POST'])
def send():
	return render_template('form.html')

@app.route('/get_val',methods=['GET','POST'])
def get_val():
	if request.method=='GET':
		return render_template('form.html')
	if request.method=='POST':
		R=request.form['R']
		F=request.form['F']
		M=request.form['M']
		R=float(R)
		F=float(F)
		M=float(M)
		# os.chdir('/home/rahul/Documents/cus_seg/flask api')
		scaler = joblib.load('my_scaler.pkl')
		r=math.log(R)
		f=math.log(F)
		m=math.log(M)
		print(r)
		dic={'m':[m],'r':[r],'f':[f]}
		df=pd.DataFrame(dic)
		print(df)
		transformed=scaler.transform(df)
		print(transformed)
		result=main_func(transformed)
		# byte_str = b"{'one': 1, 'two': 2}"
		dict_str = result.decode("UTF-8")
		mydata = ast.literal_eval(dict_str)
		di=mydata
		cluster=di['Results']['output1'][0]['Assignments']
		cluster=int(cluster)
		data=[]
		if(cluster==2 or cluster==6):
			data.append(cluster)
			data.append("This customer belongs to premium class of customers")
			data.append("This customer is one of the best cutomer you have")
			if(cluster==2):
				data.append("As it belongs to the cluster that are not recent you can construct schemes to erradicate that")
			data.append("It belongs to the cluster that have most optimal values of R F M,So your statergies for them should be to keep these values consistent")
		elif(cluster==5 or cluster==1 or cluster==4):
			data.append(cluster)
			if(cluster==1 or cluster==4):
				data.append("This customer belongs to the high spending cluster of customer")
			else:
				data.append("This customer belongs to the Highest Spedning cluster of customers")
			data.append("As,this customer's frequency is low,You have to preodically send notifications of different products to increase their frequency")
		elif(cluster==1 or cluster==3):
			data.append(cluster)
			data.append("This customer belongs to loyal class of customers")
			data.append("As these customers spend less you can offer this customer special discount")
		# print(data)
		# print(type(di))
		# print(di['Results']['output1'][0]['Assignments'])
		return render_template('senti.html',result=data)
	return render_template('home.html')



recom_dict={0:[15107.0,12398.0,12556.0,12596.0,],
1:[12455.0,12599.0,12643.0,12676.0,],
2:[12498.0,13058.0,13277.0,13502.0,],
3:[12362.0,12415.0,12417.0,12433.0,],
4:[18037.0, 13003.0, 18037.0],
5:[12347.0, 12423.0, 12464.0, 12528.0, 12584.0],
6:[12352.0, 12388.0, 12395.0, 12428.0, 12431.0],
}

@app.route('/recom', methods=['GET', 'POST'])
def recom():
	if request.method=='GET':
		cluster=request.args.get('sid')
		cus_ids=recom_dict[int(cluster)]
		prods=pickle.load(open('recom.pkl','rb'))
		products=prods[cus_ids[0]][0]
		return render_template('hash.html',product=products[:5])





if (__name__ == "__main__"):
	app.debug = True
	app.run(threaded = True)
