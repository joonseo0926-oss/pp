
# 오차함수 열확산 시뮬레이션

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 공개 링크 만들기

GitHub 저장소에 `app.py`와 `requirements.txt`를 올린 뒤,
Streamlit Community Cloud 같은 호스팅 서비스에 연결하면 공개 URL을 만들 수 있습니다.
그 URL을 한글 문서의 하이퍼링크나 QR코드에 넣으면 됩니다.

## 모델 설명

T(x,t) = Ts + (Ti - Ts) erf[x / (2√(αt))]

원형 히트맵은 1차원 해를 원형 단면에 회전시킨 단순화된 시각화입니다.
실제 배터리의 정밀 해석 모델은 아닙니다.
