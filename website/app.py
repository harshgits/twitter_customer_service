# This script will serve the relevant bokeh elements to
# the bootstrap website.

from bokeh.embed import components
from flask import Flask, request, render_template
from bokeh_dash import get_comp_results, cnames, histstrs

app = Flask(__name__)
@app.route('/')
def index():

	# cname from website
	cname = request.args.get("cname")
	if cname is None:
		cname = cnames[0]

	# histstr from website
	histstr = request.args.get("histstr")
	if histstr is None:
		histstr = histstrs[0]

	# creating and serving bokeh object
	bokeh_obj = get_comp_results(cname, histstr)
	bokeh_script, bokeh_div = components(bokeh_obj)
	kwargs = {
		"bokeh_script": bokeh_script,
		"bokeh_div": bokeh_div,
		"current_cname": cname,
		"cnames": cnames,
		"current_histstr": histstr,
		"histstrs": histstrs,}
	return render_template("index.html", **kwargs)

if __name__ == "__main__":
	app.run(debug = True)