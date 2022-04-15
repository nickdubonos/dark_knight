from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from data import df
train_X,test_X,train_Y,test_Y=train_test_split(df['URL'],df['Label'],test_size=0.1,random_state=12)
vectorization = TfidfVectorizer()

train_XV = vectorization.fit_transform(train_X)

test_XV = vectorization.transform(test_X)

from sklearn.naive_bayes import MultinomialNB

mnb = MultinomialNB()

mnb=mnb.fit(train_XV,train_Y)

