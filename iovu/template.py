import pandas as pd
import random

# iOVU 파라미터 정의
practice_areas = [
    "개발자 밈 굿즈", "너디 패션", "코딩 유머 아이템", "프로그래머 라이프스타일",
    "IT 굿즈", "개발자 커뮤니티", "밈 컬렉션", "개발자 선물", "힐링 개발템",
    "깃허브 문화", "오픈소스 굿즈", "해커톤 굿즈", "스타트업 문화", "개발자 정체성 표현"
]

metrics = {
    "Cost": ["제품 가격", "배송비", "할인율", "멤버십 혜택"],
    "Market": ["브랜드 인지도", "개발자 커뮤니티 반응", "밈 트렌드 반영도", "바이럴 지수"],
    "Quality": ["프린팅 품질", "원단 퀄리티", "디자인 완성도", "내구성"],
    "Resource": ["재고 관리", "배송 속도", "고객 응답", "커뮤니티 참여도"]
}

countries = [
    "한국", "미국", "일본", "중국", "독일", "프랑스", "영국", "캐나다", "호주"
]

time_spans = [
    "2024년", "2025년", "최근 1개월", "최근 3개월", "최근 6개월", 
    "2019-2023년", "팬데믹 이후"
]

source_hints = [
    "개발자 커뮤니티", "깃허브 트렌드", "IT 뉴스", "밈 사이트"
]

intents = ["정보", "구매", "선물", "커뮤니티", "트렌드"]
difficulties = ["쉬움", "보통", "어려움"]

# 파라미터 테이블 생성
def create_parameter_table():
    # 모든 메트릭을 하나의 리스트로 합치기
    all_metrics = []
    for category, metric_list in metrics.items():
        all_metrics.extend(metric_list)
    
    parameter_data = {
        'parameter': ['practice_area', 'metric', 'country', 'time_span', 'source_hint', 'language_ratio', 'intent', 'difficulty'],
        'count': [
            f"({len(practice_areas)})",
            f"(4개 그룹 {len(all_metrics)}개)",
            f"({len(countries)})",
            f"({len(time_spans)})",
            f"({len(source_hints)})",
            "",
            "",
            ""
        ],
        'values': [
            " · ".join(practice_areas[:5]) + " · " + " · ".join(practice_areas[5:10]) + " · " + " · ".join(practice_areas[10:]),
            f"Cost: {' · '.join(metrics['Cost'])} Market: {' · '.join(metrics['Market'])} Quality: {' · '.join(metrics['Quality'])} Resource: {' · '.join(metrics['Resource'])}",
            " · ".join(countries) + " · Global",
            " · ".join(time_spans) + " · 10년 추세(2015-2024년)",
            " · ".join(source_hints),
            "KO 0.8 : EN 0.2",
            " · ".join(intents),
            " · ".join(difficulties)
        ]
    }
    
    df = pd.DataFrame(parameter_data)
    return df

# 테이블 생성 및 출력
parameter_table = create_parameter_table()
print("=== iOVU 파라미터 테이블 ===")
print(parameter_table.to_string(index=False))

# CSV로 저장
parameter_table.to_csv('iovu_parameter_table.csv', index=False, encoding='utf-8-sig')
print("\n파라미터 테이블이 'iovu_parameter_table.csv'로 저장되었습니다.")