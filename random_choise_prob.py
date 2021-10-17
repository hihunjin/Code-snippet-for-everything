from numpy.random import choice
# draw = choice(list_of_candidates, number_of_items_to_pick,
#               p=probability_distribution)
draw = choice(['봄', '여름', '가을', '겨울'], 10,
              p=[0.4,0.3,0.2,0.1])
print(draw)
# array(['여름', '가을', '여름', '봄', '봄', '봄', '봄', '봄', '가을', '여름'], dtype='<U2')
