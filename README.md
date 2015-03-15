Likkkes
=======

Setting a virtual environmemt (optional)
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

	pip install -r requirements.txt

Executing the script
--------------------

	$ python likkkes.py --format=csv --verbose

### Help

	$ python likkkes.py --help
	Usage: likkkes.py [OPTIONS]

	Options:
	  --verbose / --no-verbose      Verbosity (False by default).
	  --follow / --no-follow        Fetch next page results or not (False by
	                                default).
	  -s, --shots-per-page INTEGER  The number of shots returned per page (10 by
	                                default).
	  -l, --likes-per-page INTEGER  The number of likes returned per page (100 by
	                                default).
	  -t, --timeframe TEXT          A period of time to limit the results to
	                                ("week" by default).
	  -f, --format [csv|json]       The file format to export the results to.
	  --help                        Show this message and exit.
