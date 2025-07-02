# 법무법인 동래 단순 질의 생성 시스템 (완전한 파일)
from typing import Dict, List, Tuple
import json
import random
import pandas as pd
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict
import re

class DongraeLawParameters:
    """법무법인 동래 특화 파라미터 클래스"""
    
    def __init__(self):
        self.practice_areas = [
            "기업법무", "계약법무", "소송및분쟁해결", "지적재산권", "금융법무",
            "부동산법무", "노동법무", "조세법무", "형사법무",
            "개인정보보호", "IT통신법무", "환경법무", "의료헬스케어법무", "건설인프라법무"
        ]
        
        self.metrics = {
            "Cost": ["수임료", "착수금", "성공보수", "시간당비용", "총비용"],
            "Market": ["시장점유율", "고객만족도", "승소율", "해결율", "브랜드인지도"],
            "Quality": ["전문성", "사건처리속도", "고객대응품질", "법적정확성", "서비스품질"],
            "Resource": ["변호사인원", "파트너수", "전문인력", "지원인력", "시설규모"]
        }
        
        self.regions = [
            "부산", "부산연제구", "부산서면", "부산해운대", "창원", 
            "김해", "양산", "울산", "경남", "부울경"
        ]
        
        self.time_spans = [
            "2024년", "2025년", "최근3년", "최근5년", "2019-2023년",
            "팬데믹이후", "10년추세"
        ]
        
        self.source_hints = [
            "대한변협", "부산변협", "법률신문", "법무부통계", "법원행정처",
            "KISDI", "대법원", "부산지법", "부산법원", "부산지방법원"
        ]
        
        self.language_ratios = ["KO 0.9 : EN 0.1"]
        self.intents = ["정보조회", "탐색비교", "거래상담"]
        self.difficulties = ["쉬움", "보통", "어려움"]

    def get_random_parameters(self) -> Dict:
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

@dataclass
class TemplateConfig:
    brand_name: str = "법무법인 동래"
    website: str = "dongraelaw.shop"
    location: str = "부산 연제구 거제동"
    experience: str = "29년 업력"
    specialty: str = "부산·경남 지역밀착"

class DongraeTemplateGenerator:
    def __init__(self):
        self.config = TemplateConfig()
        
        self.templates = {
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
                "({source_hint}) 자료에 따르면, ({time_span}) ({region}) ({practice_area}) 로펌의 ({metric})와 성장 전망을 설명해 주세요.",
                "({practice_area}) 로펌이 제시하는 ({metric}) + ({source_hint})와 함께 비교해 주세요.",
                "({time_span}) 동안 ({region}) ({practice_area}) 시장의 ({metric})별 세부 분석과 ({source_hint}) 기반 예측을 제공해주세요."
            ],
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
        templates = self.templates.get((difficulty, intent), [])
        if not templates:
            return f"({params['region']}) ({params['practice_area']}) 관련 ({params['metric']}) 정보를 알려주세요."
        
        template = random.choice(templates)
        formatted_template = template.format(
            region=params.get('region', '부산'),
            practice_area=params.get('practice_area', '기업법무'),
            metric=params.get('metric', '수임료'),
            time_span=params.get('time_span', '최근3년'),
            source_hint=params.get('source_hint', '대한변협')
        )
        
        return formatted_template

class DongrageLawIntegratedSystem:
    """법무법인 동래 통합 AI 서비스 시스템 (단순 질의 생성)"""
    
    def __init__(self):
        self.params = DongraeLawParameters()
        self.template_gen = DongraeTemplateGenerator()
        
        self.brand_info = {
            "name": "법무법인 동래",
            "english_name": "Dongrae Law Firm", 
            "website": "https://www.dongraelaw.shop/",
            "location": "부산광역시 연제구 법원남로 18, 세헌빌딩 5층",
            "phone": "(051) 501-8500",
            "established": "1995년",
            "experience": "29년",
            "specialties": ["부산·경남 지역밀착", "실무경험", "합리적 수임료"],
            "slogan": "법률 그 이상의 가치를 추구합니다",
            "target_regions": ["부산", "창원", "김해", "양산", "울산", "경남"]
        }

    def extract_keywords_from_query(self, user_query: str) -> Dict:
        extracted = {
            "practice_area": None,
            "region": None,
            "metric": None,
            "intent": None,
            "difficulty": None
        }
        
        # 간단한 키워드 매칭
        for area in self.params.practice_areas:
            if area in user_query:
                extracted["practice_area"] = area
                break
        
        for region in self.params.regions:
            if region in user_query:
                extracted["region"] = region
                break
        
        for metric_category, metrics in self.params.metrics.items():
            for metric in metrics:
                if metric in user_query:
                    extracted["metric"] = metric
                    break
            if extracted["metric"]:
                break
        
        if any(word in user_query for word in ["얼마", "어떻게", "무엇"]):
            extracted["intent"] = "정보조회"
        elif any(word in user_query for word in ["추천", "비교", "어디서"]):
            extracted["intent"] = "탐색비교"
        elif any(word in user_query for word in ["상담", "문의", "도움"]):
            extracted["intent"] = "거래상담"
        else:
            extracted["intent"] = "정보조회"
        
        if len(user_query) < 20:
            extracted["difficulty"] = "쉬움"
        elif len(user_query) < 50:
            extracted["difficulty"] = "보통"
        else:
            extracted["difficulty"] = "어려움"
        
        return extracted

    def generate_dongrae_prompt(self, user_query: str) -> Dict:
        """단순한 질의 문장만 생성 (역할 지정 없음)"""
        # 1. 키워드 추출
        extracted_keywords = self.extract_keywords_from_query(user_query)
        
        # 2. 누락된 파라미터 랜덤 보완
        params = self.params.get_random_parameters()
        for key, value in extracted_keywords.items():
            if value:
                params[key] = value
        
        # 3. 템플릿 생성
        difficulty = params.get("difficulty", "보통")
        intent = params.get("intent", "정보조회")
        
        base_template = self.template_gen.generate_template(difficulty, intent, params)
        
        # 4. 단순한 질의 문장만 반환
        simple_prompt = base_template
        
        return {
            "prompt": simple_prompt,  # 단순한 질의 문장만
            "extracted_keywords": extracted_keywords,
            "final_parameters": params,
            "template_used": base_template,
            "brand_info": self.brand_info
        }

    def batch_generate_samples(self, num_samples: int = 10) -> List[Dict]:
        sample_queries = [
            "부산에서 이혼 변호사 비용이 얼마나 하나요?",
            "교통사고 났는데 어떻게 해야 하나요?",
            "부동산 매매계약서 검토받고 싶어요",
            "회사 설립할 때 필요한 법률 서비스가 뭐가 있나요?",
            "임금체불 문제로 고민인데 상담받을 수 있나요?",
            "상속 문제로 분쟁이 생겼는데 도움받을 수 있나요?",
            "건설업체와 계약분쟁이 있어서 변호사가 필요해요",
            "세무조사 대응 관련해서 상담받고 싶습니다",
            "특허출원 절차와 비용이 궁금해요",
            "개인정보 유출 사고 대응방법을 알려주세요"
        ]
        
        results = []
        for i in range(min(num_samples, len(sample_queries))):
            query = sample_queries[i]
            result = self.generate_dongrae_prompt(query)
            result["sample_id"] = f"dongrae_sample_{i+1:02d}"
            result["query"] = query
            results.append(result)
        
        return results

    def export_to_json(self, samples: List[Dict], filename: str = None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dongrae_simple_prompts_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(samples, f, ensure_ascii=False, indent=2)
        
        print(f"단순 프롬프트 데이터가 {filename}에 저장되었습니다.")
        return filename

# 대량 생성 함수 추가
def generate_massive_simple_prompts(num_prompts: int = 1000):
    """대량 단순 프롬프트 생성"""
    print(f"=== {num_prompts}개 단순 프롬프트 생성 시작 ===")
    
    system = DongrageLawIntegratedSystem()
    
    # 다양한 질의 패턴 생성
    base_queries = [
        "부산에서 교통사고 변호사를 찾고 있어요",
        "이혼 절차와 비용이 궁금합니다",
        "회사 설립 관련 법무 서비스가 필요해요",
        "부동산 계약서 검토받고 싶어요",
        "임금체불 문제를 해결하고 싶어요",
        "세무조사 대응 방법을 알고 싶어요",
        "특허 출원 절차가 궁금해요",
        "계약 분쟁이 발생했어요",
        "상속 관련 상담이 필요해요",
        "노동법 위반 신고하고 싶어요"
    ]
    
    # 변형 요소들
    prefixes = ["", "급하게 ", "전문적으로 ", "신속하게 ", "정확하게 "]
    suffixes = ["", " 도움주세요", " 상담받고 싶어요", " 문의드려요", " 알려주세요"]
    
    # 질의 확장
    all_queries = []
    for base in base_queries:
        for prefix in prefixes:
            for suffix in suffixes:
                query = f"{prefix}{base}{suffix}".strip()
                all_queries.append(query)
    
    # 추가 질의 생성 (목표 개수까지)
    while len(all_queries) < num_prompts:
        base = random.choice(base_queries)
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        region = random.choice(system.params.regions)
        area = random.choice(system.params.practice_areas)
        
        variants = [
            f"{prefix}{region}에서 {area} {base}{suffix}",
            f"{area} 전문가 {base}",
            f"{region} 지역 {base}",
            f"{base} 법무법인 동래에서"
        ]
        
        all_queries.extend(variants)
    
    # 목표 개수만큼 선택
    selected_queries = all_queries[:num_prompts]
    
    # 프롬프트 생성
    prompts = []
    for i, query in enumerate(selected_queries):
        if i % 100 == 0:
            print(f"진행률: {i}/{len(selected_queries)} ({i/len(selected_queries)*100:.1f}%)")
        
        try:
            result = system.generate_dongrae_prompt(query)
            result["sample_id"] = f"simple_prompt_{i+1:04d}"
            result["query"] = query
            prompts.append(result)
        except Exception as e:
            print(f"오류 발생 (인덱스 {i}): {str(e)}")
            continue
    
    # 파일 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dongrae_simple_massive_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== 총 {len(prompts)}개 단순 프롬프트 생성 완료 ===")
    print(f"파일 저장: {filename}")
    
    # 샘플 출력
    print(f"\n=== 샘플 결과 (상위 5개) ===")
    for i, prompt in enumerate(prompts[:5], 1):
        print(f"{i}. 입력: {prompt['query']}")
        print(f"   출력: {prompt['prompt']}")
        print()
    
    return prompts

# 테스트 실행
if __name__ == "__main__":
    print("=== 법무법인 동래 단순 질의 생성 시스템 ===")
    
    dongrae_system = DongrageLawIntegratedSystem()
    
    # 단일 테스트
    test_query = "부산에서 교통사고 변호사 비용이 얼마나 하나요?"
    result = dongrae_system.generate_dongrae_prompt(test_query)
    
    print(f"입력 질의: {test_query}")
    print(f"생성된 프롬프트: {result['prompt']}")
    print(f"추출된 키워드: {result['extracted_keywords']}")
    
    # 선택 메뉴
    print(f"\n선택하세요:")
    print("1. 기본 샘플 생성 (10개)")
    print("2. 대량 생성 (1000개)")
    print("3. 사용자 지정 개수")
    
    choice = input("번호를 입력하세요 (1-3): ").strip()
    
    if choice == "1":
        samples = dongrae_system.batch_generate_samples(10)
        dongrae_system.export_to_json(samples)
        
        print("\n생성된 단순 프롬프트들:")
        for i, sample in enumerate(samples, 1):
            print(f"{i}. {sample['prompt']}")
            
    elif choice == "2":
        generate_massive_simple_prompts(1000)
        
    elif choice == "3":
        try:
            num = int(input("생성할 개수를 입력하세요: "))
            generate_massive_simple_prompts(num)
        except ValueError:
            print("잘못된 숫자입니다.")
            
    else:
        print("기본 샘플 생성을 실행합니다.")
        samples = dongrae_system.batch_generate_samples(10)
        dongrae_system.export_to_json(samples)