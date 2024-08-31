from flask import Flask, render_template, send_file, request
from automate_news import extract_news_list
from apscheduler.schedulers.background import BackgroundScheduler
import json
import os

# __________________SETUP FLASK APP__________________#
app = Flask(__name__)

# __________________SETUP DATABASE__________________#
with open('websites.json', 'r') as json_file:
    list_of_websites = json.load(json_file)

# __________________FUNCTIONS__________________#
def construct_csv_path() -> list:
    csv_folder = 'csv_folder'
    csv_files = []
    for csv_file in os.listdir(csv_folder):
        if csv_file.endswith('.csv'):
            csv_files.append(os.path.join(csv_folder, csv_file))
    return csv_files
        

def update_news_list():
    extract_news_list(list_of_website=list_of_websites)
    

# __________________ROUTES__________________#
@app.route('/')
def index():
    # List of available CSV files
    csv_files = construct_csv_path()
    return render_template('index.html', csv_files=csv_files)

@app.route('/download', methods=['GET'])
def download_file():
    # Get the file name from the query parameter
    file_name = request.args.get('file_name')
    
    if file_name in construct_csv_path():
        # Path to your CSV file
        path = file_name
        return send_file(path, as_attachment=True)
    else:
        return "File not found", 404



if __name__ == '__main__':

    scheduler = BackgroundScheduler()
    scheduler.add_job(update_news_list, 'interval', hours=1)
    scheduler.start()
    
    app.run(debug=True)