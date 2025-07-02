# iOVU 파라미터 정의

# 1. practice_area (서비스 분야)
practice_areas = [
    "개발자 밈 굿즈", "너디 패션", "코딩 유머 아이템", "프로그래머 라이프스타일",
    "IT 굿즈", "개발자 커뮤니티", "밈 컬렉션", "개발자 선물", "힐링 개발템",
    "깃허브 문화", "오픈소스 굿즈", "해커톤 굿즈", "스타트업 문화", "개발자 정체성 표현"
]

# 2. metrics (측정 지표 - 4개 그룹, 각 그룹당 4개씩 총 16개)
metrics = {
    "Cost": ["제품 가격", "배송비", "할인율", "멤버십 혜택"],
    "Market": ["브랜드 인지도", "개발자 커뮤니티 반응", "밈 트렌드 반영도", "바이럴 지수"],
    "Quality": ["프린팅 품질", "원단 퀄리티", "디자인 완성도", "내구성"],
    "Resource": ["재고 관리", "배송 속도", "고객 응답", "커뮤니티 참여도"]
}

# 3. countries (국가)
countries = [
    "한국", "미국", "일본", "중국", "독일", "프랑스", "영국", "캐나다", "호주"
]

# 4. time_span (기간)
time_spans = [
    "2024년", "2025년", "최근 1개월", "최근 3개월", "최근 6개월", 
    "2019-2023년", "팬데믹 이후", "Z세대", "밀레니얼"
]

# 5. source_hint (정보 출처)
source_hints = [
    "개발자 커뮤니티", "깃허브 트렌드", "IT 뉴스", "밈 사이트", 
    "개발자 블로그", "스타트업 뉴스", "해커톤 후기", "테크 인플루언서"
]

# 6. language_ratio (언어 비율)
language_ratio = "KO 0.8 : EN 0.2"  # 한국어 80%, 영어 20%

# 7. intent (의도)
intents = ["정보", "구매", "선물", "커뮤니티", "트렌드"]

# 8. difficulty (난이도)
difficulties = ["쉬움", "보통", "어려움"]

print("iOVU 파라미터 정의 완료!")
print(f"Practice Areas: {len(practice_areas)}개")
print(f"Metrics: {sum(len(v) for v in metrics.values())}개")
print(f"Countries: {len(countries)}개")
print(f"Time Spans: {len(time_spans)}개")
print(f"Source Hints: {len(source_hints)}개")