# 법무법인 동래 난이도 × 의도 템플릿
from dataclasses import dataclass
from typing import Dict, List
import random

@dataclass
class TemplateConfig:
    """템플릿 설정 클래스"""
    brand_name: str = "동래 법률사무소"
    website: str = "dongrae"
    location: str = "부산 연제구 거제동"
    experience: str = "30년 업력"
    specialty: str = "부산·경남 지역밀착"

class DongraeTemplateGenerator:
    """법무법인 동래 템플릿 생성기"""
    
    def __init__(self):
        self.config = TemplateConfig()
        
        # 난이도 × 의도 매트릭스 템플릿
        self.templates = {
            # 정보조회 (Information Seeking)
            ("쉬움", "정보조회"): [
                "({region}) ({practice_area}) 변호사 ({metric})가 보통 얼마인가요?",
                "({region})에서 ({practice_area}) 전문 로펌을 어디서 찾을 수 있나요?",
                "({practice_area}) 사건의 ({metric})는 대략 어느 정도인가요?"
            ],
            
            ("보통", "정보조회"): [
                "({time_span}) 기준 ({region}) ({practice_area}) 분야의 ({metric})를 알려줘.",
                "({region})에서 ({practice_area}) 전문 변호사의 ({metric})와 ({source_hint}) 정보를 종합해서 설명해주세요.",
                "({practice_area}) 관련 ({metric}) 통계를 ({time_span}) 기간으로 정리해주세요."
            ],
            
            ("어려움", "정보조회"): [
                "({source_hint}) 자료에 따르면, ({time_span}) ({region}) ({practice_area}) 로펌의 ({metric})와 성장 전망을 실명해 주세요.",
                "({practice_area}) 로펌이 제시하는 ({metric}) + ({source_hint})와 합께 비교해 주세요.",
                "({time_span}) 동안 ({region}) ({practice_area}) 시장의 ({metric})별 세부 분석과 ({source_hint}) 기반 예측을 제공해주세요."
            ],
            
            # 탐색비교 (Exploration & Comparison)
            ("쉬움", "탐색비교"): [
                "({practice_area}) 전문 변호사를 어디서 찾을 수 있나요?",
                "({region})에서 ({practice_area}) 전문 로펌 리스트를 확인할 수 있는 공식 통계는?",
                "({practice_area}) 변호사 선택할 때 ({metric}) 기준으로 뭘 봐야 하나요?"
            ],
            
            ("보통", "탐색비교"): [
                "({region})에서 ({practice_area}) 전문 로펌 리스트를 확인할 수 있는 공식 통계는?",
                "({time_span}) 기간 ({region}) ({practice_area}) 상위 10개 로펌을 ({metric}) 기준으로 정리해주세요.",
                "({practice_area}) 분야에서 ({metric})가 우수한 부산 지역 법무법인을 추천해주세요."
            ],
            
            ("어려움", "탐색비교"): [
                "({time_span}) 동안 ({region}) ({practice_area}) 사건건수 상위 10개 로펌을 제시한 ({source_hint}) 보고서를 알려주세요.",
                "({practice_area}) 로펌의 ({metric}) 비교분석과 ({region}) 지역 특성을 반영한 추천 리스트를 작성해주세요.",
                "({source_hint}) 데이터를 기반으로 ({region}) ({practice_area}) 시장의 경쟁구도와 주요 플레이어들의 ({metric}) 분석을 제공해주세요."
            ],
            
            # 거래상담 (Transaction Consultation)
            ("쉬움", "거래상담"): [
                "({region}) ({practice_area}) 사건 변호사 상담료는 대략 얼마인가요?",
                "({practice_area}) 관련해서 법무법인 동래에 상담받을 수 있나요?",
                "({region})에서 ({practice_area}) 사건 처리 기간은 보통 어느 정도인가요?"
            ],
            
            ("보통", "거래상담"): [
                "({time_span}) 기준 ({region}) ({practice_area}) 변호사 ({metric}) 평균은?",
                "법무법인 동래에서 ({practice_area}) 사건의 ({metric})와 서비스 내용을 상담받고 싶습니다.",
                "({practice_area}) 사건의 ({metric}) 기준과 ({region}) 지역 특성을 고려한 변호사 선택 가이드를 제공해주세요."
            ],
            
            ("어려움", "거래상담"): [
                "({practice_area}) 로펌이 제시하는 고정 + 성과보수 촛불 요율 사례를 ({source_hint})와 함께 비교해 주세요.",
                "복잡한 ({practice_area}) 사건에서 법무법인 동래의 ({metric}) 우위와 차별화 포인트를 구체적으로 설명해주세요.",
                "({time_span}) 기간 ({region}) ({practice_area}) 시장 동향을 반영한 법무법인 동래의 서비스 포트폴리오와 ({metric}) 경쟁력을 분석해주세요."
            ]
        }

    def generate_template(self, difficulty: str, intent: str, params: Dict) -> str:
        """특정 난이도와 의도에 맞는 템플릿 생성"""
        templates = self.templates.get((difficulty, intent), [])
        if not templates:
            return f"({params['region']}) ({params['practice_area']}) 관련 ({params['metric']}) 정보를 알려주세요."
        
        template = random.choice(templates)
        
        # 파라미터 치환
        formatted_template = template.format(
            region=params.get('region', '부산'),
            practice_area=params.get('practice_area', '기업법무'),
            metric=params.get('metric', '수임료'),
            time_span=params.get('time_span', '최근3년'),
            source_hint=params.get('source_hint', '대한변협')
        )
        
        return formatted_template

    def generate_all_combinations(self, params: Dict) -> Dict:
        """모든 난이도×의도 조합의 템플릿 생성"""
        difficulties = ["쉬움", "보통", "어려움"]
        intents = ["정보조회", "탐색비교", "거래상담"]
        
        results = {}
        for difficulty in difficulties:
            for intent in intents:
                template = self.generate_template(difficulty, intent, params)
                results[f"{difficulty}.{intent}"] = template
        
        return results

# 템플릿 생성기 인스턴스
template_generator = DongraeTemplateGenerator()

# 샘플 파라미터로 테스트
sample_params = {
    'practice_area': '부동산법무',
    'metric': '승소율',
    'region': '부산',
    'time_span': '최근3년',
    'source_hint': '부산변협'
}

print("=== 법무법인 동래 난이도×의도 템플릿 ===")
print(f"샘플 파라미터: {sample_params}")
print()

# 모든 조합 생성
all_templates = template_generator.generate_all_combinations(sample_params)

for key, template in all_templates.items():
    difficulty, intent = key.split('.')
    print(f"[{difficulty} × {intent}]")
    print(f"템플릿: {template}")
    print()