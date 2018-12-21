# dashboard with plots etc

# change directory to THIS directory
import os
os.chdir(
	os.path.dirname(
		os.path.abspath(__file__)
		)
	)

## read in the timeseries
import pandas as pd

timeseriescsv_path = "../timeseries.csv"
timeserie_df = pd.read_csv(timeseriescsv_path)

# fix index
timeserie_df = timeserie_df.set_index("time")
timeserie_df.index = pd.to_datetime(timeserie_df.index)

## getting the company names and twitter handles
companiescsv_path = "../companies.csv"
comp_df = pd.read_csv(companiescsv_path)
cnames = sorted(comp_df["company_name"].values)

## getting the static metrics
staticmetricscsv_path = "../static_metrics.csv"
statmet_df = pd.read_csv(staticmetricscsv_path
	).set_index("company")

## bar chart for static metrics
from bokeh.plotting import figure
from bokeh.io import show
from bokeh.models import ColumnDataSource

# display text dict
metric_props = {
	"issue_was_resolved": {"name": "RESOLUTION RATE"},
	"cust_sent_improvement": {"name": "CUST. SENT. BOOST"}
	}

def get_metric_bar(metric, comp, histstr,
	metric_props = metric_props, 
	timeserie_df = timeserie_df, 
	comp_df = comp_df,
	statmet_df = statmet_df):
	
	# the hist prepend string
	hspre = "_".join(histstr.split())
	
	# get the averages
	met_avg_ser = statmet_df[hspre + "_" + metric]

	# company twitter handle
	comp_th = comp_df[
		comp_df["company_name"] == comp    
		]["twitter_handle"].iloc[0]

	# get mets for comp
	comp_met = met_avg_ser[comp_th]
	
	# get met for ind
	ind_met = met_avg_ser.values.mean()

	# get top company details
	top_comp_th = met_avg_ser.idxmax()
	tc_met = met_avg_ser[top_comp_th]
	tc_name = comp_df[
		comp_df["twitter_handle"] == top_comp_th
		]["company_name"].iloc[0] + " (best)"

	xlabels = [comp, "Ind. avg.", tc_name]
	ys = [comp_met, ind_met, tc_met]

	p = figure(title = metric_props[metric]["name"] + " (on average)",
			   x_range = xlabels, 
			   plot_width = 300, plot_height = 200,
			  )

	source = ColumnDataSource(data={"xlabels": xlabels, "ys": ys, 
									"colors": ["blue", "gray", "red"]})
	p.vbar(source = source, x = "xlabels", top = "ys", 
		   color = "colors", width = 0.4)
	
	return p

## plotting timeseries

# histstr to timedel dict
histstr2timedel_d = {"2 months": pd.Timedelta(days = 62), 
					 "2 weeks": pd.Timedelta(days = 14)}
histstrs = list(histstr2timedel_d)

def get_metric_timeplot(metric, comp, histstr,
	timeserie_df = timeserie_df, 
	comp_df = comp_df):

	p = figure(title = "Performance with time",
			x_axis_type="datetime", 
			plot_width = 300, plot_height = 200)

	# company twitter handle
	comp_th = comp_df[
		comp_df["company_name"] == comp    
		]["twitter_handle"].iloc[0]
	
	# keeping only relevant times
	ts_df = timeserie_df.loc[
		timeserie_df.index[-1] - histstr2timedel_d[histstr]
		: None]

	r_comp = p.line(x = ts_df.index, 
				y = ts_df[comp_th + "__" + metric],
				)

	r_avg = p.line(x = ts_df.index, 
				y = ts_df["indavg__" + metric],
				color = "gray", alpha = 0.7,
				)
	
	return p

## combine plots into block
from bokeh.layouts import column

def get_met_block(metric, comp, histstr):
	return column([get_metric_bar(metric, comp, histstr),
				  get_metric_timeplot(metric, comp, histstr)])

## get statmets for specific metric
def get_statmets(metric, cname, histstr):
	# hist prepend str
	hspre = "_".join(histstr.split())

	# company twitter handle
	comp_th = comp_df[
		comp_df["company_name"] == cname
		]["twitter_handle"].iloc[0]
	
	# pre statmet str
	presm_str = hspre + "_" + str(metric)
	if metric is None: # looking for combined statmet
		presm_str = hspre

	# get rank
	ranks = statmet_df[presm_str + "_rank"]
	rank = statmet_df[presm_str + "_rank"][comp_th]

	# get topper
	topper_th = ranks.index[ranks == 1][0]
	topper = comp_df[
		comp_df["twitter_handle"] == topper_th
		]["company_name"].iloc[0]

	# get averageness
	avgness = statmet_df[presm_str + "_averageness"][comp_th]
	
	return {"rank": rank, "topper": topper, "avgness": avgness}

## text report for company
from bokeh.models.widgets import Div
from bokeh.layouts import widgetbox

def get_text_div(cname, histstr):

	statmet_groups = dict([
		(m, get_statmets(m, cname, histstr)) for m in 
			["issue_was_resolved", "cust_sent_improvement", None]
		])

	avgness_to_color_d = {
		"below average": "#000000", # black
		"average": "#808080", # gray
		"above average": "#99cc00", # green
		}

	met_to_heading_d = {
		None: "Overall Satisfaction",
		"issue_was_resolved": "Issue Resolution Rate",
		"cust_sent_improvement": "Customer Sentiment Boost"
		}

	def get_metric_report(metric, 
		statmet_groups = statmet_groups,
		met_to_heading_d = met_to_heading_d):
		
		# starting metric_report with heading and rank
		met_rep = \
			"""
			<h4 style="text-align: left;"><span style="color: #000000;"><span style="color: #ff6600;">""" + \
			met_to_heading_d[metric] + \
			""":</span>&nbsp;</span><span style="color: #000000;"><span style="color: #3366ff;">"""+ \
			"Rank " + str(statmet_groups[metric]["rank"]) + \
			"""</span> out of 8 </span></h4>"""
		
		# averageness
		met_rep += \
			"""
			<p style="text-align: left;"><span style="color: #000000;"><span style="color: """ + \
			avgness_to_color_d[statmet_groups[metric]["avgness"]] + \
			""";">&nbsp;&nbsp;&nbsp;""" + \
			statmet_groups[metric]["avgness"]
		
		# topper
		met_rep += \
			"""</span>&nbsp;(1st rank: <span style="color: #ff6600;">""" + \
			statmet_groups[metric]["topper"] + \
			"""</span><span style="color: #ff6600;">)</span></span></p>
			"""
		
		return met_rep
	
	comp_header = """
		<h3 style="text-align: left;"><span style="color: #ff6600;">""" + \
		"""Twitter Customer Service Rankings for</span></h3>
		<h3 style="text-align: left;"><em><b>"""+cname+"""</b></em></h3>
		"""
	text_report = \
		comp_header + \
		"""<div style="height:20px;font-size:1px;">&nbsp;</div>""" + \
		get_metric_report(None) + \
		"""<div style="height:10px;font-size:1px;">&nbsp;</div>""" + \
		get_metric_report("issue_was_resolved") + \
		"""<div style="height:10px;font-size:1px;">&nbsp;</div>""" + \
		get_metric_report("cust_sent_improvement")

	divbox = widgetbox(Div(text = text_report,
	width=370, height=300))

	return divbox

## combine blocks
from bokeh.layouts import row, Spacer

def get_comp_results(company, period):
	
	# renaming arguments to more informative variable names
	cname = company
	histstr = period

	# getting blocks
	text_block = get_text_div(cname, histstr)
	empty_block = Div(text = " ", width = 10)
	improvement_block = get_met_block("cust_sent_improvement", cname, histstr)
	resolution_block = get_met_block("issue_was_resolved", cname, histstr)

	return row([text_block,
		Spacer(width = 100),
		resolution_block,
		Spacer(width = 10),
		improvement_block])

if __name__ == '__main__':
	show(get_comp_results(company = cnames[0], period = histstrs[0]))