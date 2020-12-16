# FastText

[당근마켓의 카테고리 자동 추천](https://medium.com/daangn/%EA%B8%80%EC%93%B0%EA%B8%B0-%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC-%EC%B6%94%EC%B2%9C%EB%AA%A8%EB%8D%B8-%EA%B0%9C%EB%B0%9C%ED%95%98%EA%B8%B0-cbbcc43e1f7f) 글을 읽고 fasttext를 간단하게 사용해보았습니다.

## FastText

### word2vec

NLP의 기초가 되는 word2vec은 텍스트를 숫자로 바꾸어서 계산을 하려는 과정에서 고안된 아이디어다. 통계를 진행하기 위해서 보통 (0, 고양이), (1, 모자), (2, 자동차)와 같이 숫자와 문자를 일대일 대응시키는 one-hot-encoding을 쓰는데 이는 숫자와 단어와의 관계가 전혀 없다는 문제가 있다. 그래서 이렇게 단어를 벡터로 바꾸는 과정에서 벡터에 단어의 의미를 담고자 했고, 비슷한 의미의 단어들은 비슷한 벡터로 표현을 하고자 했다. (Vision 분야에서는 각 pixel 값 만으로는 이미지의 정보를 충분히 얻지 못해 CNN이 도입되었는데 비슷한 느낌인 것 같다.)
이러한 word2vec의 단점은 같은 단어라도 단어 앞 뒤의 노드들의 의미가 비슷하지 않거나 research와 researches와 같은 "형태적 유사성"을 고려하지 못하고 frequency가 낮은 키워드들에 대해서는 효과적으로 필터링을 진행해주지 못할 뿐 아니라 "out of vocabulary" 문제도 존재한다.

### fasttext

sequence to sequence부터 BERT까지 다양한 모델이 존재하지만, facebook이 자체 공개하기도 했고 당근마켓 글에서도 해당 모델을 사용했기에 이번 글에서도 해당 모델로 진행하였다.  
fasttext 모델의 경우 word2vec을 제안한 T. Mikolov가 저자로 참여하였고 위에서 언급된 "형태적(Morpological) 유사성"과 frequency, "out-of-vocabulary" 문제들을 개선하였는데 이는 fasttext 모델의 원리가 "morpological structure"를 활용하여 단어의 의미 정보를 추출해냈기 때문이다. 이를 통해 "형태적 유사성"을 해결 할 수 있을 뿐 아니라, 빈도가 낮거나 존재하지 않았던 단어들도 처리 할 수 있게 되었다.

## Install

### Fast Text 설치
```
$ virtualenv fasttext --python=python3.7 # 3.7 버전을 사용하라고 한다. (2020.12.16 기준 3.9 버전에서는 에러가 발생한다.)
$ source fasttext/bin/activate
$ pip3 install gensim
```

### pre-trained 모델 다운로드
[홈페이지](https://fasttext.cc/docs/en/crawl-vectors.html)에서 다운받을 수 있고 한국어 분류를 위해 한국어 모델(cc.ko.300.*)을 다운로드 받았습니다.

## Demo

### Directory
```
fasttext
├── fasttext         // virtualenv
├── cc.ko.300.bin    // pre-trained model
└── run.py           // main file
```

### Simple Example (deprecation!)
```python
from gensim.models import FastText

model = FastText.load_fasttext_format('./cc.ko.300.bin')

print(model.most_similar('치킨'))
```
- results
```
[('탄두리', 0.5830886363983154), ('뿌링클', 0.5815541744232178), ('BHC', 0.5803220868110657), ('피자랑', 0.572679877281189), ('파닭', 0.5700914859771729), ('치킨이', 0.5688289403915405), ('비비큐', 0.5602543950080872), ('캐슈', 0.5591146945953369), ('순살', 0.5546345710754395), ('배달오신', 0.551413893699646)]
```

간단한 예제를 테스트 하기 위해 블로그의 코드로 테스트를 진행해보았는데 `load_fasttext_format()`와 `most_similar()` 모두 deprecationWarning이 떴다.(역시 공식 도큐를 읽어야 한다.) 하지만, 일단 모델이 제대로 불러와졌고 gensim이 제대로 설치되었음을 확인 할 수 있다.

### Updated Version
```python
from gensim import models

ko_model = models.fasttext.load_facebook_model('cc.ko.300.bin')

for w, sim in ko_model.wv.similar_by_word('치킨', 10):
    print(f'{w}: {sim}')
```

- results
```
탄두리: 0.5830886363983154
뿌링클: 0.5815541744232178
BHC: 0.5803220868110657
피자랑: 0.572679877281189
파닭: 0.5700914859771729
치킨이: 0.5688289403915405
비비큐: 0.5602543950080872
캐슈: 0.5591146945953369
순살: 0.5546345710754395
배달오신: 0.551413893699646
```

위와 동일한 예제이고 함수들을 최신 문법에 맞게 바꾸어주었다. 그 결과 위와 동일한 값이 warning 메세지 없이 출력되는 것을 확인 할 수 있다.

### More

```python
from gensim import models

model = models.fasttext.load_facebook_model('cc.ko.300.bin')

for w, sim in model.wv.similar_by_word('치킨', 5):
    print(f'{w}: {sim}')

print(model.wv.most_similar('치킨', topn=5))
print(mode.wv.similarity('치킨', '피자'))
print(loaded_model.wv.most_similar(positive=['돼지', '소고기'], negative=['야채'], topn=1))
```

## 결론

페이스북에서 제공해주는 FastText 라이브러리를 사용해보았는데 사용법이 단순하고 pre-trained 모델을 제공해줘서 쉽게 사용 해 볼 수 있었다. 하지만, 그렇게 좋은 결과를 얻을 수는 없었고 이는 차후에 프로젝트를 진행하게 되면 추가 데이터를 사용해서 학습을 진행할 예정이다.

## 참고자료
[당근마켓의 카테고리 자동 추천](https://medium.com/daangn/%EA%B8%80%EC%93%B0%EA%B8%B0-%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC-%EC%B6%94%EC%B2%9C%EB%AA%A8%EB%8D%B8-%EA%B0%9C%EB%B0%9C%ED%95%98%EA%B8%B0-cbbcc43e1f7f)
[Advances in Pre-Training Distributed Word Representations](https://arxiv.org/abs/1712.09405)
[fasttext 공식 홈페이지](https://fasttext.cc/docs/en/support.html)
[쉽게 쓰여진 word2vec](https://dreamgonfly.github.io/blog/word2vec-explained/)
[Attention mechanism in NLP](https://lovit.github.io/machine%20learning/2019/03/17/attention_in_nlp/)
[A introduction of fastText](https://byeongkijeong.github.io/fastText/)
[gensim - tutorial - fastText](https://frhyme.github.io/python-libs/gensim2_fasttext/)
[FastText Pre-trained 한국어 모델 사용하기](https://inahjeon.github.io/fasttext/)