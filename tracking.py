from datetime import datetime
import pandas as pd
from flask import Flask , request , send_file , make_response
import os
from openpyxl import load_workbook
import pytz


app = Flask(__name__)

CSV_FILES = 'csv_emails.csv'

IST = pytz.timezone('Asia/Kolkata')

# def save_to_csv(receiver_data):

#     new_entry = pd.DataFrame([receiver_data])
    
#     if not os.path.isfile(CSV_FILES):
#         new_entry.to_csv(CSV_FILES, index=False)
#     else:
#         existing_df = pd.read_csv(CSV_FILES)

#         if receiver_data['Email'] in existing_df['Email'].values:
#             existing_df.loc[existing_df['Email'] == receiver_data['Email'], 'Time'] = receiver_data['Time']
#         else:
#             existing_df = pd.concat([existing_df, new_entry], ignore_index=True)

#         existing_df.to_csv(CSV_FILES, index=False)


def save_to_excel(receiver_data):
    pass


@app.route("/track")
def track_email():

    receiver_email = request.args.get('email', 'Unknown')
    
    indian_time = datetime.now(IST)
    
    receiver_data = {
        "Date" : indian_time.strftime('%d-%m-%Y'),
        "Time": indian_time.strftime('%H:%M:%S'),
        "Email": receiver_email,
        "Status" : "Seen"
    }

    # save_to_csv(receiver_data)
    save_to_excel(receiver_data)

    response = make_response(send_file('pixel.png', mimetype='image/png'))
    
    return response



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000 , debug=True)