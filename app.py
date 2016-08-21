from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, output_notebook, show
from bokeh.embed import components 
from urllib2 import urlopen
import pandas as pd 
import numpy as np
import ijson
	

app = Flask(__name__)
app_vars = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		#request was a POST
		app_vars['ticker'] = request.form['ticker']
		#Take care of the case where the ticker symbol is invalid
		
		api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % app_vars['ticker']

		f = urlopen(api_url)
		objects = ijson.items(f, 'column_names')
		tmp = list(objects)[0]
		columns = []
		for val in tmp:
		    columns.append(val)

		f = urlopen(api_url)
		objects = ijson.items(f, 'data')
		tmp = list(objects)[0]
		data = []
		for val in tmp:
		    data.append(val)

		data = pd.DataFrame(data, columns=columns)

		#p = figure()
		#p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2)

		p = figure()
		p = p.line(data['Close'])

		script, div = components(p)
		#print script
		return render_template('graph.html', script=script, div=div, ticker=app_vars['ticker'])
		#return render_template('graph.html')

if __name__ == '__main__':
  app.run(port=33507, debug=True)




#from bokeh.embed import components 
#f = open('Test.txt', 'w')
		#f.write('Name of Stock: %s'%app_vars['ticker'])
		#f.close()




