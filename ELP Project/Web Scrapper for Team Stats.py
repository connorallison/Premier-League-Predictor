# Web Scrapper for Team Stats

import requests
from bs4 import BeautifulSoup
import csv

team_urls = {}
with open("ELP Project/epl_teamswiki.csv", "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        team_urls[row[0]] = row[1]


for team, url in team_urls.items():
    try:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table', {'class': 'wikitable'})

        target_table = None
        for table in tables:
            headers = table.find_all('th')
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')
            filtered_rows = []
            for header in headers:
                if 'Season' in header.text.strip():
                    continue
            for row in rows:
                cells = row.find_all(['th', 'td'])
                row_data = [cell.text.strip() for cell in cells]
                if row_data and len(row_data) > 0:
                    # Check if the first column contains a season starting from 2014-15
                    season = row_data[0]
                    if season.startswith("2014-15") or season[:4].isdigit() and int(season[:4]) >= 2014:
                        target_table = table
            if target_table:
                break

        if target_table:  # Only proceed if we found the correct table
            tbody = target_table.find('tbody')
            rows = tbody.find_all('tr')
            filtered_rows = []
            for row in rows:
                cells = row.find_all(['th', 'td'])
                row_data = [cell.text.strip() for cell in cells]
                if row_data and len(row_data) > 0:
                    # Check if the first column contains a season starting from 2014-15
                    season = row_data[0]
                    if season.startswith("2014-15") or season[:4].isdigit() and int(season[:4]) >= 2014:
                        filtered_rows.append(row_data[:10])
            
            # Create CSV file with team name
            csv_file_name = f"{team}.csv"
            with open(csv_file_name, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(filtered_rows)
            print(f"Created CSV for {team}")
    except Exception as e:
        print(f"Error processing {team}: {str(e)}")


