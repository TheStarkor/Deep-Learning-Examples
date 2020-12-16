from gensim import models

model = models.fasttext.load_facebook_model('cc.ko.300.bin')

for w, sim in model.wv.similar_by_word('치킨', 5):
    print(f'{w}: {sim}')
for w, sim in model.wv.most_similar('치킨', topn=5):
    print(f'{w}: {sim}')

print(model.wv.similarity('치킨', '피자'))
print(model.wv.most_similar(positive=['돼지', '소고기'], negative=['야채'], topn=1))