
# NDCG (Normalized Discouted Cumulative Gain)

- 추천 시스템에서 랭킹 추천 분야에 많이 쓰이는 평가 지표
- 기존 정보 검색에서 많이 쓰였으며, 상위 랭킹의 리스트가 하위 랭킹 리스트보다 확연하게 중요한 도메인에서 유용한 평가 기준.

## 1. CG (Cumulative Gain)

관련성의 평균.

$$ CG = \sum_{i=1}^{n} relevance_i $$

모두 동일한 가중치를 가짐 -> 랭킹 높은것에 높은 가중치를 주기가 어려움.