# [Twitter Customer Service Investigator](http://charsh7.pythonanywhere.com)
This project uses public tweets exchanged between mobile service providers and their customers to help you investigate the Twitter history of YOUR provider and see how it stacks up against the industry's best. [CLICK HERE to check out the web app!](http://charsh7.pythonanywhere.com)

## Overview
In a nutshell, I used Natural Language Processing to analyze twitter conversations between mobile service providers and their customers to compute several customer satisfaction metrics for these companies over a period of three months. This information was used to build an interactive web app that allows a user to comprehensively compare the customer service of any provider with competitors and help the user choose the best provider for their needs.

### Project stages

#### Data collection, cleaning and restructuring 

- Downloaded a dataset of over [3 million customer service related tweets](https://www.kaggle.com/thoughtvector/customer-support-on-twitter) spanning 108 companies over 7 industries. 
- By chaining together tweets that belonged to a unique conversation, I was able to generate 800 thousand coherent conversations out of the 3+ million tweets (see [01_convo_chains.ipynb](https://github.com/harshgits/twitter_customer_service/blob/master/01_convo_chains.ipynb)).

#### Feature Engineering and Analysis

- Using the [Google Cloud Natural Language API](https://cloud.google.com/natural-language/), I performed **sentiment analysis** to generate a sentiment score between -1 (very negative) to +1 (very positive) for every tweet in the corpus (see [gcp_sentiment.py](https://github.com/harshgits/twitter_customer_service/blob/master/gcp_sentiment.py), [02_sentiment.ipynb](https://github.com/harshgits/twitter_customer_service/blob/master/02_sentiment.ipynb) and [03_adding_sentiments_to_tweets_csv.ipynb](https://github.com/harshgits/twitter_customer_service/blob/master/03_adding_sentiments_to_tweets_csv.ipynb)).

- The raw sentiment scores were used to **engineer higher order features** (satisfaction metrics) such as **rate of issue resolution** and **customer sentiment boost** for individual conversations (see [04_create_conversations_table.ipynb](https://github.com/harshgits/twitter_customer_service/blob/master/04_create_conversations_table.ipynb)).

- In order to study the evolution of satisfaction metrics with time, I binned and aggregated the metrics in one hour blocks to get metric time series for each mobile service provider (see [05_creating_times_table.ipynb](https://github.com/harshgits/twitter_customer_service/blob/master/05_creating_times_table.ipynb)).

- The time series were further analyzed over two time periods (two weeks and two months) in order to obtain satisfaction metrics for the companies over their recent vs less-recent past and rank them accordingly ([06_averages_over_time.ipynb](https://github.com/harshgits/twitter_customer_service/blob/master/06_averages_over_time.ipynb)).

#### Interactive web app
- The quantitative results obtained from the data analysis were finally made accessible to the end user in the form of an interactive [web app](http://charsh7.pythonanywhere.com). 
- The interactive functionality was developed with [Bokeh](https://bokeh.pydata.org/en/latest/) in [07_interactive_results.ipynb](https://github.com/harshgits/twitter_customer_service/blob/master/07_interactive_results.ipynb) and the [website](https://github.com/harshgits/twitter_customer_service/blob/master/07_interactive_results.ipynb) was implemented with [Flask](http://flask.pocoo.org/).