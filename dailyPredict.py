import datetime
from sendMail import sendMail
import getPredictions 
import os.path
from dotenv import load_dotenv


if __name__ == "__main__":
	now = datetime.datetime.now()
	today = now.strftime("%Y-%m-%d")

	preds = getPredictions.fetch_bet_predictions(writeToFile=False, date=today, apiKey=os.getenv("API-KEY"))
	
	sendMail(mailBody = getPredictions.getFilteredPredictions( preds=preds, expired=False ), mailSubject ='Match Prediction for '+ today )
