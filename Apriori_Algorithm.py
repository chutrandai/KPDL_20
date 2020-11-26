# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 22:38:57 2020

@author: DELL
"""
# step 1: Import the lib
import pandas as pd 
from mlxtend.frequent_patterns import apriori, association_rules 

import xlsxwriter
def hot_encode(x): 
    if(x<= 0): 
        return 0
    if(x>= 1): 
        return 1

def writeExcelXLSX(data, fileName):
    workbook = xlsxwriter.Workbook(fileName) 
    worksheet = workbook.add_worksheet()
    # Start from the first cell. 
    # Rows and columns are zero indexed. 
    row = 0
    col = 0
    # header
    #data.head()
    header = data.columns
    for head in header:
        worksheet.write(0, col, str(head))
        col += 1
    col = 0
    # iterating through content list 
    for head in header:
        row = 1
        for val in data[head]:
            worksheet.write(row, col, str(val))
#            print("val: %s" %val)
#            print("row: %s, col: %s" %(row, col))
            row += 1
        col += 1
    workbook.close() 
    
    
    
    
# step 2: loading and exploring the data
# Loading the Data 
data = pd.read_excel('Online_Retail.xlsx') 
data.head()
# Exploring the columns of the data 
data.columns
# Exploring the different regions of transactions 
data.Country.unique()
#print(data['Country'])
# làm sạch dữ liệu
# Stripping extra spaces in the description 
data['Description'] = data['Description'].str.strip() 

# Dropping the rows without any invoice number 
data.dropna(axis = 0, subset =['InvoiceNo'], inplace = True) 
data['InvoiceNo'] = data['InvoiceNo'].astype('str')

# Dropping all transactions which were done on credit 
data = data[~data['InvoiceNo'].str.contains('C')] 
#  Tách dữ liệu theo khu vực giao dịch
# Transactions done in France 
basket_France = (data[data['Country'] =="France"]
		.groupby(['InvoiceNo', 'Description'])['Quantity'] 
		.sum().unstack().reset_index().fillna(0) 
		.set_index('InvoiceNo'))
# Transactions done in the United Kingdom 
basket_UK = (data[data['Country'] =="United Kingdom"] 
          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
          .sum().unstack().reset_index().fillna(0) 
          .set_index('InvoiceNo')) 
print(basket_UK)
# Transactions done in Portugal 
basket_Por = (data[data['Country'] =="Portugal"] 
          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
          .sum().unstack().reset_index().fillna(0) 
          .set_index('InvoiceNo')) 
  
basket_Sweden = (data[data['Country'] =="Sweden"] 
          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
          .sum().unstack().reset_index().fillna(0) 
          .set_index('InvoiceNo')) 
# Mã hóa dữ liệu nóng
# Encoding the datasets 
basket_encoded = basket_France.applymap(hot_encode) 
basket_France = basket_encoded

basket_encoded = basket_UK.applymap(hot_encode) 
basket_UK = basket_encoded 
  
basket_encoded = basket_Por.applymap(hot_encode) 
basket_Por = basket_encoded 
  
basket_encoded = basket_Sweden.applymap(hot_encode) 
basket_Sweden = basket_encoded 
# building model
# Building the model - FRANCE
#frq_items = apriori(basket_France, min_support = 0.05, use_colnames = True) 
## Collecting the inferred rules in a dataframe 
#rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
#rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
##print(rules)
#writeExcelXLSX(rules, 'france_result.xlsx')
#print("finish-FRANCE!")

# Building the model - UK
frq_items = apriori(basket_UK, min_support = 0.01, use_colnames = True) 
rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
writeExcelXLSX(rules, 'uk_result.xlsx')
print("finish-uk!")

## Building the model - Portuga
#frq_items = apriori(basket_Por, min_support = 0.05, use_colnames = True) 
#rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
#rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
#writeExcelXLSX(rules, 'por_result.xlsx')
#print("finish-por!")

## Building the model - Sweden
#frq_items = apriori(basket_Sweden, min_support = 0.05, use_colnames = True) 
#rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
#rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
#writeExcelXLSX(rules, 'sweden_result.xlsx')
#print("finish-sweden!")

# -----------------
# plot
print(rules)
#import matplotlib.pyplot as plt
#df = rules[:10]
#df.plot(x="antecedents", y=["support", "confidence", "leverage"], kind="bar")
#plt.show()

