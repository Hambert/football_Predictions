import datetime
from sendMail import sendMail
import getPredictions as bp
import os.path
from dotenv import load_dotenv


if __name__ == "__main__":
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")

    preds = bp.fetch_bet_predictions(writeToFile=False, date=today, apiKey=os.getenv("API-KEY"))
    filteredPred = bp.getFilteredPredictions(preds=preds, expired=False)

    if filteredPred != "":
        sendMail( mailBody = filteredPred, mailSubject ='Match predictions for '+ today)
    else:
        print("No suitable predictions")
