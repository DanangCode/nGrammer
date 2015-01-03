nGrammer
========

This is a flask based Python server. it retrieves data from Google Ngrams and displays them in a nvd3 javascript stackchart.

the code for calling Google was taken from the https://github.com/econpy/google-ngrams project.

the rest server accepts Get and Post requests with the parameters query, startdate, enddate and corupus.

A running example can be found here. https://ngrammer.herokuapp.com/ngram?query=socialism&startdate=1800
