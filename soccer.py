from urllib.request import urlretrieve
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
np.set_printoptions(suppress=True,precision = 2)
source = 'https://www.football-data.co.uk/englandm.php'
domain = '{}://{}'.format(urlparse(source).scheme,urlparse(source).netloc)
print("fetching from "+domain)
dfNamelist = []
html = urlopen(source)
bs = BeautifulSoup(html, 'html.parser')
for link in bs.find_all('a', text = 'Premier League'):
	csvLocation = (domain+'/'+link.attrs['href'])
	csvName = link.attrs['href'].replace('mmz4281/','').replace('/E0','')
	dfName = 'df'+link.attrs['href'].replace('mmz4281/','').replace('/E0','').replace('.csv','')
	dfNamelist.append(dfName)
	urlretrieve(csvLocation,csvName)
	attribute = pd.read_csv(csvName,nrows=0)
	vars()[dfName] = pd.read_csv(csvName,names = range(len(attribute.columns)),encoding='ISO-8859-1')
	(vars()[dfName]).columns = (vars()[dfName]).iloc[0]
	(vars()[dfName]) = (vars()[dfName])[1:]
#print(df1920)
#print(dfNamelist)
scoreMatrix = np.zeros((8,8))
ratioMatrix = np.zeros((8,8))
for dfName in dfNamelist:
	df = vars()[dfName]
	for i in range(8):
		for j in range(8):
			scoreMatrix[i][j] += len(df[(df['FTHG'] == str(i)) & (df['FTAG'] == str(j))])
probabilityMatrix = scoreMatrix*100/np.sum(scoreMatrix)
scoreMatrixsum = np.sum(scoreMatrix)
for i in range(8):
	for j in range(8):
		ratioMatrix[i][j] = (scoreMatrix[i][j])*np.sum(scoreMatrix)/(( scoreMatrix.sum(axis = 0)[j])*(scoreMatrix.sum(axis = 1)[i]))
print("Estimates of score probabilities")
print(probabilityMatrix)
print("f(i,j)/(fH(i)*fH(j)")
print(ratioMatrix)


