# from app import app
from nvd3 import stackedAreaChart
from ast import literal_eval
from pandas import DataFrame  # http://github.com/pydata/pandas
import re
import requests               # http://github.com/kennethreitz/requests
from flask import request
from flask import Flask

app = Flask(__name__, static_url_path='')
# app.config.from_object('config')



# @app.route('/')
# def root():
#     return app.send_static_file('index.html')


@app.route('/ngram', methods = ['GET','POST'])
def root():

    req_json = request.json
    print(req_json)

    if (request.method=='GET') :
        query = request.args.get('query', default='feminism')
        corpus = request.args.get('corpus', default='eng_us_2012')
    #query = 'feminism'
    # corpus = 'eng_us_2012'
    # request.data()
    if (request.method=='POST') :
        if (request.json) :
            corpus = request.json.get('corpus','eng_us_2012')
            query = request.json.get('query','feminism')
        else :
            corpus = request.form.get('corpus','eng_us_2012')
            query = request.form.get('query','feminism')

    startDate = 1880
    endDate = 2008

    df = getNgrams(query, corpus, startDate, endDate, 0, False)[2]

    type = query
    chart = stackedAreaChart(height=450,
                         x_axis_format="", y_axis_format="2f", jquery_on_ready=False)


    chart.set_containerheader("\n\n<h1>The term '" + type + "' as a percentage of all published American English words (1880-2008)</h1>\n\n")

    extra_serie = {"tooltip": {"y_start": "", "y_end": " "}}


    maxnum = df.max()[1]

    for value in df.columns.values:
        d=df[value]
        if (value != "year"):
            chart.add_serie(name=value, y=(d.values/maxnum*100).astype("int"), x=d.keys(), extra=extra_serie )
        else:
            print "skipping year"

    chart.buildhtml()
    content = chart.htmlcontent

    return content




corpora = dict(eng_us_2012=17, eng_us_2009=5, eng_gb_2012=18, eng_gb_2009=6,
               chi_sim_2012=23, chi_sim_2009=11, eng_2012=15, eng_2009=0,
               eng_fiction_2012=16, eng_fiction_2009=4, eng_1m_2009=1,
               fre_2012=19, fre_2009=7, ger_2012=20, ger_2009=8, heb_2012=24,
               heb_2009=9, spa_2012=21, spa_2009=10, rus_2012=25, rus_2009=12,
               ita_2012=22)

def getNgrams(query, corpus, startYear, endYear, smoothing, caseInsensitive):

    params = dict(content=query, year_start=startYear, year_end=endYear,
                  corpus=corpora[corpus], smoothing=smoothing,
                  case_insensitive=caseInsensitive)
    if params['case_insensitive'] is False:
        params.pop('case_insensitive')
    if '?' in params['content']:
        params['content'] = params['content'].replace('?', '*')
    if '@' in params['content']:
        params['content'] = params['content'].replace('@', '=>')
    req = requests.get('http://books.google.com/ngrams/graph', params=params)
    res = re.findall('var data = (.*?);\\n', req.text)
    data = {qry['ngram']: qry['timeseries'] for qry in literal_eval(res[0])}
    df = DataFrame(data)
    df.insert(0, 'year', range(startYear, endYear+1))
    df.index=df['year']
    return req.url, params['content'], df

if __name__ == '__main__':
    app.run()


