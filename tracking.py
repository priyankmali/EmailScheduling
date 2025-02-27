from datetime import datetime
import pandas as pd
from flask import Flask , request , send_file , make_response
import os
from openpyxl import load_workbook
import pytz


app = Flask(__name__)

CSV_FILES = 'csv_emails.csv'
EXCEL_FILES = 'excel_emails.xlsx'

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
    new_entry = pd.DataFrame([receiver_data])

    if not os.path.isfile(EXCEL_FILES):
        new_entry.to_excel(EXCEL_FILES , index=False , engine='openpyxl')
    else:
        existing_df = pd.read_excel(EXCEL_FILES , engine='openpyxl')
        if receiver_data['Email'] in existing_df['Email'].values:
            existing_df.loc[existing_df['Email'] == receiver_data['Email'] , 'Time'] = receiver_data['Time']
        else:
            existing_df = pd.concat([existing_df , new_entry] , ignore_index=True)
        existing_df.to_excel(EXCEL_FILES , index=False , engine='openpyxl')


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
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response

"""
What Happens Without Headers?

The browser may cache the image (pixel.png).
If the recipient opens the email multiple times, 
    the browser may load the image from cache instead of making a new request to your Flask server.
This could result in incorrect tracking because the tracking request might not be sent every time the email is opened.

Cache-Control: no-cache, no-store, must-revalidate  → Prevents the browser from storing the image.
Pragma: no-cache                                    → A legacy directive for older browsers.
Expires: 0                                          → Ensures the response is always considered "expired."
"""



if __name__ == "__main__":
    app.run(port=5000 , debug=True)