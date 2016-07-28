#
# Author : akgeni
# Date : 28/7/2016
#


import graphlab
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline

wiki = graphlab.SFrame('people_wiki.gl/')
print(wiki)

# Add a new column word_count for each article 
wiki['word_count'] = graphlab.text_analytics.count_words(wiki['text'])

# Create nearest neighbors model using graphlab
model = graphlab.nearest_neighbors.create(wiki, label='name',
                                          features=['word_count'],
                                          method='brute_force',
                                          distance='euclidean'
                                         )

def get_top_words(name, k=10):
	'''Returns the top words for given name
	'''
	row = wiki[wiki['name' == name]]
	row_word_count = row['word_count'].stack('word_count', new_column_name=['word', 'count'])
	return row_word_count.sort('count', ascending=False)[:k]


def getDistanceEuclidean(first_person, second_person):
    '''returs the diatance between two persons. Input is the word_count of
    their articles. 
    '''
    return graphlab.toolkits.distances.euclidean(first_person, second_person)

                                         
# Lets find out the top words for Barack Obama and Francisco Barrio
barack_top_words = get_top_words('Barack Obama')
barrio_top_words = get_top_words('Francisco Barrio')
print("Top words in Obama article\n", barack_top_words)
print("Top words in Francisco Barrio article\n",barrio_top_words)

# Now we will join barack_top_words and  barrio_top_words so that we 
# could see, which words are more frequent in both arcticles
combined_words = barack_top_words.join(barrio_top_words, on='word')
combined_words.sort('obama', ascending=False)




barack = wiki[wiki['name'] == 'Barack Obama']['word_count'][0]
bush = wiki[wiki['name'] == 'George W. Bush']['word_count'][0]
joe = wiki[wiki['name'] == 'Joe Biden']['word_count'][0]

print 'Distance between Barack Obama and George Bush is %r' % \
      getDistanceEuclidean(barack, bush)
print 'Distance between Barack Obama and Joe Biden is %r' % \
      getDistanceEuclidean(barack, joe)
print 'Distance between George Bush and  Joe Biden is %r' % \
      getDistanceEuclidean(bush, joe)    
    
# We get the following result
'''
Distance between Barack Obama and George Bush is 34.39476704383968
Distance between Barack Obama and Joe Biden is 33.075670817082454
Distance between George Bush and  Joe Biden is 32.7566787083184
'''

                                  
