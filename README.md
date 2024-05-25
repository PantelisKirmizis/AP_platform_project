# Stock Portfolio Tracker Platform
This project is built in satisfaction of the requirements for the Advanced Programming course of my MSc in Finance. It builds a portfolio tracking platform using Dash. It allows users to visualize the performance of their stock portfolio through various graphs and tables, and provides the latest news for the stock with the highest participation in the portfolio. Additionally, it generates a downloadable PDF report.

## Features
- Interactive dashboard with multiple graphs and a table.
- Displays the latest news for the stock with the highest portfolio participation.
- Option to switch between graphs using current data and initial data.
- Exportable PDF report of the portfolio.

## Prerequisites
Before you begin, ensure you have met the requirements presented on the requirements.txt file.

## Installation
To install and run the application easily follow the following steps.
1. Clone the repository:
   https://github.com/PantelisKirmizis/AP_platform_project.git
2. Navigate to the project directory.
3. Run the application.

## How to use
To easily use and navigate the platform follow the folloing steps.
1. Run the application.
2. Open your web browser and go to http://127.0.0.1:8050 to access the dashboard.
3. Enter the stock tickers, exactly as they appear on Yahoo Finance, and investment amounts in a dictionary format {Ticker1: Value1, Ticker2: Value2, ...}.
4. Enter the benchmark ticker, exactly as it appears on Yahoo Finance.
5. Select the date range for analysis in a dd/mm/yyyy format.
6. Click the "Submit" button to generate the graphs and the table.
7. Click the "Initial/Current" buttons to navigate between the graphs using current data and initial data.
8. Use the "Export Report to PDF" button to download a PDF report of your portfolio.
