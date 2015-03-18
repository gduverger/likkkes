Likkkes
=======

[This script](https://github.com/gduverger/likkkes/blob/master/likkkes.py) retrieves “likes” for the most popular [Dribbble](https://dribbble.com/) shots (of the current week, by default) and export a matrix in the following format (with `X`, `Y`, `Z`… as user ids):

	shot_id	| views_count	| likes_count	| comments_count	| attachments_count	| rebounds_count	| buckets_count	| created_at			| user_id	| user_location	| user_followers_count	| user_followings_coount	| user_shots_count	| X	| Y	| Z	| …
	1967328	| 4976			| 765			| 87				| 1					| 0					| 37			| 2015-03-10T19:35:58Z	| 4593		| Minneapolis	| 5967					| 208						| 128				| 0	| 1	| 1	| …
	1970483	| 4272			| 656			| 27				| 0					| 0					| 61			| 2015-03-12T16:11:30Z	| 31752		| Palo Alto, Ca	| 29311					| 1524						| 532				| 0	| 0	| 0	| …
	…

See the resulting [CSV](https://github.com/gduverger/likkkes/blob/master/likkkes.csv) and [JSON](https://github.com/gduverger/likkkes/blob/master/likkkes.json) files.

After using a k-means clustering technique (see [XLSX file](https://github.com/gduverger/likkkes/blob/master/likkkes.xlsx)) on the resulting data, **I did not find any biases in Dribbble members' “likes”** ([tweet](https://twitter.com/gduverger/status/577174550061948930)). Please contact me at [@gduverger](https://twitter.com/gduverger) if you reach a different conclusion or if you find (an) issue(s) in the script. Thanks!

Unsuccesful attempt at clustering “likes”:

![K-means clustering](https://github.com/gduverger/likkkes/blob/master/likkkes.png)

Setting a virtual environment (optional)
----------------------------------------

	$ cd likkkes/
	$ mkdir venv
	$ virtualenv venv/likkkes --no-site-packages --verbose
	$ source venv/likkkes/bin/activate

Update the configuration file (required)
---------------------------------------

Create a text file named `likkkes.conf` with your Dribbble Client Access Token in it ([register an application](https://dribbble.com/account/applications/new)).

Installing the dependencies (required)
--------------------------------------

	$ pip install -r requirements.txt

Executing the script
--------------------

	$ python likkkes.py --format=csv --verbose

### --help

	$ python likkkes.py --help
	Usage: likkkes.py [OPTIONS]

	Options:
	  --verbose / --no-verbose        Verbosity (False by default).
	  --follow / --no-follow          Fetch next page results or not (False by
	                                  default).
	  -p, --shots-per-page INTEGER    The number of shots returned per page (10 by
	                                  default).
	  -q, --likes-per-page INTEGER    The number of likes returned per page (100
	                                  by default).
	  --headings / --no-headings      Include the table headings (True by default,
	                                  CSV only).
	  -t, --timeframe TEXT            A period of time to limit the results to
	                                  (False by default).
	  -f, --format [csv|json]         The file format to export the results to.
	  -s, --sort [comments|recent|views]
	                                  The sort field ("recent" by default).
	  --help                          Show this message and exit.
