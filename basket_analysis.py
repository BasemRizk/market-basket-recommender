import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import warnings
warnings.filterwarnings("ignore")

df=pd.read_csv('data.csv', encoding= 'unicode_escape')
df['Description']=df['Description'].str.strip()
df.dropna(axis=0,subset=['InvoiceNo'],inplace=True)
df['InvoiceNo']=df['InvoiceNo'].astype('str')
df=df[~df['InvoiceNo'].str.contains('C')]





invoices=(df[df['Country']=='France']
          .groupby(['InvoiceNo','Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('InvoiceNo'))
def my_encode_units(x):
    if x <=0:
        return 0
    else:
        return 1
invoices_sets=invoices.applymap(my_encode_units)
try:
    invoices_sets.drop('POSTAGE',inplace=True,axis=1)
except Exception as e:
    pass
model=apriori(invoices_sets,min_support=0.07,use_colnames=True)
my_rules=association_rules(model,metric='lift',min_threshold=1)
x=my_rules[(my_rules['lift']>=3)&
          (my_rules['confidence']>=0.5)]
x['antecedents'] = x['antecedents'].map(lambda x: list(x))
x['antecedents'] = x['antecedents'].map(lambda x: x[0])
x['consequents'] = x['consequents'].map(lambda x: list(x))
x['consequents'] = x['consequents'].map(lambda x: x[0])
x=x.drop_duplicates(subset=['antecedents','consequents'],keep='last')
def get_items():
    return list(x['antecedents'].unique())
def find_combos(item):
    res=x[x['antecedents']==item]
    return res[['consequents']]