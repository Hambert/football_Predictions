import requests
import json
import sys
import os.path
import datetime
from sendMail import sendMail
from dotenv import load_dotenv

def getPerformaceData(apiKey):
	""" Get prediction performance from API """
	url = "https://football-prediction-api.p.rapidapi.com/api/v2/performance-stats"
	querystring = {"market":"classic"}
	headers = {
		'x-rapidapi-key': apiKey,
		'x-rapidapi-host': "football-prediction-api.p.rapidapi.com"
	}
	r = requests.request("GET", url, headers=headers, params=querystring)

	if r.status_code == 200:
		return r.text
	else:
		return False



def write_predictions_to_file(data, path, date='2020-12-12'):
	""" Writes data to specified path"""

	try:
		f = open(path + date + "_pred.json", "w")
		f.write(str(data))
		print("Wrote predictions to "+ path + date + "_pred.json" )
	except Exception as e:
		print("Something went wrong while writing to file.")
		print(e)
		sys.exit(1)
	finally:
		f.close()


def fetch_bet_predictions(writeToFile=False, date='2020-12-12', apiKey=''):
	""" Received Predictions and save them to file"""
	if apiKey == '':
		print('insert api key')
		return False

	try:
		print("Getting bet predictions from: 'football-prediction-api.p.rapidapi.com' ")
		headers = {
			'x-rapidapi-key': apiKey,
			'x-rapidapi-host': "football-prediction-api.p.rapidapi.com"
			}
		
		print('Get predictions for : %s' % date)
		url = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
		querystring = {"iso_date": date,"market":"classic","federation":"UEFA"}
		response = requests.request("GET", url, headers=headers, params=querystring)
		
		
		data = json.loads(response.text)

		if writeToFile:
			write_predictions_to_file(response.text, '/tmp/', today)

		print("Gathered %s predictions." % len(data['data']))
		return data
		
	except Exception as e:
		print("Error while getting predictions. Exiting.")
		print(e)
		sys.exit(1)


def predFromFile(date='2020-12-12'):
	""" Read predictions from file """
	try:
	
		with open("/tmp/"+date+"_pred.json") as outfile:
			data = json.load(outfile)
		
			print("Gathered %s predictions from file." % len(data['data']))
			return data
			
	except Exception as e:
		print("Error while reading predictions from file. Exiting.")
		print(e)
		sys.exit(1)


def getFilteredPredictions(preds, expired=False):
	""" Return filtered predictions """
	predsLen = len(preds['data'])
	i=0
	threshold = 1.3
	bet_output = ''

	if expired:
		print('All predictions with an odd lower then '+ str(threshold))
	else:
		print('Only not expired predictions with an odd lower then '+ str(threshold))

	for p in preds['data']:
		i += 1
		if not p['is_expired'] or expired:
			if p['odds'][p['prediction']] < threshold:
				bet_output = bet_output + "[%s/%s] " % (i, predsLen )
				bet_output = bet_output + "Country: %s, Competition: %s, %s vs. %s, Odds: %s, Prediction: %s, Start: %s\n" % (
					p['competition_cluster'],
					p['competition_name'],
					p['home_team'],
					p['away_team'],
					p['odds'][p['prediction']],
					p['prediction'],
					p['start_date'])

	return bet_output


if __name__ == "__main__":

	load_dotenv()

	now = datetime.datetime.now()
	today = now.strftime("%Y-%m-%d")

	if os.path.isfile("/tmp/"+today+"_pred.json"):
		preds = predFromFile()
	else:

		preds = fetch_bet_predictions(writeToFile=True, date=today, apiKey=os.getenv("API-KEY") )

	#sendMail( getFilterPredictions( preds ), 'Match prediction for '+ today )
	#sendMail(getPerformaceData(apiKey=os.getenv("API-KEY")), 'Prediction stats for '+ today )
	print( getFilteredPredictions( preds=preds, expired=True) )



