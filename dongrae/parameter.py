# 법무법인 동래 파라미터 정의
import random
from typing import Dict, List

class DongraeLawParameters:
    """법무법인 동래 특화 파라미터 클래스"""
    
    def __init__(self):
        # 1. 법무 전문분야 (practice_area)
        self.practice_areas = [
            "기업법무", "계약법무", "소송및분쟁해결", "지적재산권", "금융법무",
            "부동산법무", "노동법무", "조세법무", "형사법무", "국제법무",
            "개인정보보호", "IT통신법무", "환경법무", "의료헬스케어법무", "건설인프라법무"
        ]
        
        # 2. 평가 메트릭 (metric) - 법무 특화
        self.metrics = {
            "Cost": ["수임료", "착수금", "성공보수", "시간당비용", "총비용"],
            "Market": ["시장점유율", "고객만족도", "승소율", "해결율", "브랜드인지도"],
            "Quality": ["전문성", "사건처리속도", "고객대응품질", "법적정확성", "서비스품질"],
            "Resource": ["변호사인원", "파트너수", "전문인력", "지원인력", "시설규모"]
        }
        
        # 3. 지역 (region) - 부산/경남 중심
        self.regions = [
            "부산", "부산연제구", "부산서면", "부산해운대", "창원", 
            "김해", "양산", "울산", "경남", "부울경"
        ]
        
        # 4. 시간범위 (time_span)
        self.time_spans = [
            "2024년", "2025년", "최근3년", "최근5년", "2019-2023년",
            "팬데믹이후", "10년추세"
        ]
        
        # 5. 정보출처 (source_hint)
        self.source_hints = [
            "대한변협", "부산변협", "법률신문", "법무부통계", "법원행정처",
            "KISDI", "대법원", "부산지법"
        ]
        
        # 6. 언어비율 (language_ratio)
        self.language_ratios = ["KO 0.9 : EN 0.1"]  # 한국어 중심
        
        # 7. 의도 (intent)
        self.intents = ["정보조회", "탐색비교", "거래상담"]
        
        # 8. 난이도 (difficulty)
        self.difficulties = ["쉬움", "보통", "어려움"]

    def get_random_parameters(self) -> Dict:
        """랜덤 파라미터 조합 생성"""
        return {
            "practice_area": random.choice(self.practice_areas),
            "metric": random.choice([metric for metrics in self.metrics.values() for metric in metrics]),
            "region": random.choice(self.regions),
            "time_span": random.choice(self.time_spans),
            "source_hint": random.choice(self.source_hints),
            "language_ratio": self.language_ratios[0],
            "intent": random.choice(self.intents),
            "difficulty": random.choice(self.difficulties)
        }

# 파라미터 인스턴스 생성
dongrae_params = DongraeLawParameters()

# 샘플 파라미터 출력
print("=== 법무법인 동래 파라미터 테이블 ===")
print(f"practice_area: {dongrae_params.practice_areas}")
print(f"metrics: {dongrae_params.metrics}")
print(f"regions: {dongrae_params.regions}")
print(f"time_spans: {dongrae_params.time_spans}")
print(f"source_hints: {dongrae_params.source_hints}")
print(f"intents: {dongrae_params.intents}")
print(f"difficulties: {dongrae_params.difficulties}")

print("\n=== 랜덤 파라미터 조합 예시 ===")
for i in range(3):
    params = dongrae_params.get_random_parameters()
    print(f"조합 {i+1}: {params}")