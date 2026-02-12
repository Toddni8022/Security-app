from datetime import datetime
import os

# Function to check for today's report
def check_daily_report():
    today = datetime.now().strftime('%Y-%m-%d')
    report_path = f'./reports/{today}_report.txt'

    if os.path.exists(report_path):
        with open(report_path, 'r') as file:
            summary = file.read().strip() # Read the report summary
        return f'Summary for {today}:\n{{summary}}'  # Return content
    else:
        return 'No audit report was run today.'  # No report found
