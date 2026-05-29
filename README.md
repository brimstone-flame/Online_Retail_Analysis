# Online Retail Data Analysis
A complete online retail transaction data analysis project developed with Python, covering data preprocessing, business indicator calculation, behavioral analysis, customer stratification and data visualization.

## Project Overview
Based on real retail order data, this project completes full-cycle data analysis. We first clean and standardize raw data, then calculate core business KPIs, explore sales rules from time and regional dimensions, analyze customer consumption characteristics, and divide users into different value groups. Multiple charts are used to visually display analysis results.

## Analysis Content
Data loading and basic exploration includes checking dataset size, field attributes, statistical distribution and missing values.
Data cleaning work fills missing product descriptions by product code, filters invalid data such as negative quantity and abnormal price, converts data types and calculates total amount of each order.
We calculate overall business metrics including total sales, total order quantity, average order value, total customer number and average customer consumption.
From time dimension, we analyze monthly sales and order volume changing trends.
From regional dimension, we rank sales volume by country and extract the top 10 regions.
We also conduct customer behavior analysis to count total consumption and order frequency of each customer, and find all customers with the highest consumption.
For customer value stratification, we adopt tertile segmentation to divide customers into low value, middle value and high value groups, and count user distribution and sales contribution ratio of each group.
Line chart, bar chart and pie chart are applied to present analysis results intuitively.

## Technology Stack
Programming language: Python
Core libraries: pandas, matplotlib

## Environment Configuration
Install dependent libraries before running the code.
Run the command: pip install pandas matplotlib

## File Structure
The project contains analysis.py as the main analysis code, data.csv as the raw retail dataset, .gitignore for Git configuration and README.md for project introduction. The original data file is ignored by Git.

## How to Run
Clone the repository to local, put the dataset data.csv into the project folder, then run the main script with python analysis.py.

## Analysis Conclusions
Monthly sales show obvious periodic fluctuations.
Sales are highly concentrated, and a small number of core countries contribute most of the revenue.
Customer consumption presents a typical long-tail distribution. High-value customers account for about one-third of total users but create the majority of sales.
Customers are grouped by tertile, so the number of people in each group is roughly equal.

## Notes
The original data file data.csv is large and will not be uploaded to the repository. Please prepare the dataset manually.
Stable network is required when cloning the repository and accessing GitHub.