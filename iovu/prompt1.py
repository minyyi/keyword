# iOVU 개발자 밈 굿즈 브랜드 고급 프롬프트 생성 시스템 (CSV 저장)
from typing import Dict, List, Tuple
import json
import random
import pandas as pd
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict
import re

class IOVUParameters:
    """iOVU 브랜드 특화 파라미터 클래스"""
    
    def __init__(self):
        # 서비스 분야 (practice_area)
        self.practice_areas = [
            "개발자 밈 굿즈", "너디 패션", "코딩 유머 아이템", "프로그래머 라이프스타일",
            "IT 굿즈", "개발자 커뮤니티", "밈 컬렉션", "개발자 선물", "힐링 개발템",
            "깃허브 문화", "오픈소스 굿즈", "해커톤 굿즈", "스타트업 문화", "개발자 정체성 표현",
            "테크 패션", "프로그래밍 액세서리", "개발자 라이프", "코딩 머천다이즈"
        ]
        
        # 메트릭 (metric)
        self.metrics = {
            "Cost": ["제품 가격", "배송비", "할인율", "멤버십 혜택", "가성비", "쿠폰 혜택"],
            "Market": ["브랜드 인지도", "개발자 커뮤니티 반응", "밈 트렌드 반영도", "바이럴 지수", "시장 점유율"],
            "Quality": ["프린팅 품질", "원단 퀄리티", "디자인 완성도", "내구성", "착용감", "만족도"],
            "Resource": ["재고 관리", "배송 속도", "고객 응답", "커뮤니티 참여도", "A/S 서비스", "교환 정책"]
        }
        
        # 국가/지역 (region)
        self.regions = [
            "한국", "미국", "일본", "중국", "독일", "프랑스", "영국", "캐나다", "호주",
            "서울", "부산", "대구", "인천", "광주", "대전", "울산", "수원", "성남", "용인"
        ]
        
        # 시간 범위 (time_span)
        self.time_spans = [
            "2024년", "2025년", "최근 3개월", "최근 5개월", "2019-2023년",
            "팬데믹(2020-2022년)", "10년 추세(2015-2024년)", "올해", "작년", "최근 1년"
        ]
        
        # 정보 출처 (source_hint)
        self.source_hints = [
            "개발자 커뮤니티", "깃허브 트렌드", "IT 뉴스", "밈 사이트", "개발자 포럼",
            "테크 블로그", "스택오버플로우", "레딧", "트위터", "유튜브", "인스타그램"
        ]
        
        # 언어 비율
        self.language_ratios = ["KO 0.8 : EN 0.2"]
        
        # 의도
        self.intents = ["정보조회", "탐색비교", "거래상담"]
        
        # 난이도
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

@dataclass
class IOVUBrandConfig:
    """iOVU 브랜드 설정"""
    brand_name: str = "iOVU"
    description: str = "개발자를 위한 밈 굿즈 브랜드"
    website: str = "https://iovu-shop.vercel.app/"
    slogan: str = "개발자를 위한 귀여운 반란"
    concept: str = "Dev + Cute = iOVU"
    target: str = "IT 개발자, 너디 감성을 즐기는 사람들"

class IOVUTemplateGenerator:
    """iOVU 브랜드 템플릿 생성기"""
    
    def __init__(self):
        self.config = IOVUBrandConfig()
        
        # 난이도 × 의도별 템플릿 (괄호 없는 자연스러운 문장)
        self.templates = {
            # 정보조회 - 쉬움
            ("쉬움", "정보조회"): [
                "{region}에서 {practice_area} {metric}가 보통 얼마인가요?",
                "{region}에서 {practice_area} 브랜드를 어디서 찾을 수 있나요?",
                "{practice_area}의 {metric}는 대략 어느 정도인가요?",
                "iOVU {practice_area} 제품 {metric} 정보 알려주세요",
                "{practice_area} 시장에서 {metric} 평균이 궁금해요",
                "{practice_area} 관련 {metric} 정보가 필요해요",
                "{region} 지역 {practice_area} {metric}은 어떤가요?",
                "iOVU {practice_area} {metric}에 대해 알려주세요"
            ],
            
            # 정보조회 - 보통
            ("보통", "정보조회"): [
                "{time_span} 기준 {region} {practice_area} 분야의 {metric}를 분석해주세요",
                "{region}에서 {practice_area} 브랜드의 {metric}와 {source_hint} 정보를 종합해서 설명해주세요",
                "{practice_area} 관련 {metric} 통계를 {time_span} 기간으로 정리해주세요",
                "{source_hint}에서 화제가 된 {practice_area}의 {metric} 트렌드는?",
                "{time_span} {region} {practice_area} 시장의 {metric} 변화 분석해주세요",
                "{practice_area} 분야 {metric} 현황을 {time_span} 기준으로 알려주세요",
                "{region} {practice_area} 시장에서 {metric} 동향을 {source_hint} 기반으로 설명해주세요"
            ],
            
            # 정보조회 - 어려움
            ("어려움", "정보조회"): [
                "{source_hint} 데이터에 따르면, {time_span} {region} {practice_area} 브랜드의 {metric}와 성장 전망을 분석해주세요",
                "{practice_area} 브랜드가 제시하는 {metric}를 {source_hint}와 함께 비교 분석해주세요",
                "{time_span} 동안 {region} {practice_area} 시장의 {metric}별 세부 분석과 {source_hint} 기반 예측을 제공해주세요",
                "글로벌 {practice_area} 시장에서 {region}의 {metric} 경쟁력과 iOVU의 포지셔닝 전략 분석해주세요",
                "{source_hint} 트렌드와 {time_span} 시장 데이터를 결합한 {practice_area}의 {metric} 예측 모델을 설명해주세요",
                "{time_span} 기간 {region} {practice_area} 시장의 {metric} 변화 패턴을 {source_hint} 데이터로 심층 분석해주세요"
            ],
            
            # 탐색비교 - 쉬움
            ("쉬움", "탐색비교"): [
                "{practice_area} 제품을 어디서 찾을 수 있나요?",
                "{region}에서 {practice_area} 브랜드 리스트 알려주세요",
                "{practice_area} 선택할 때 {metric} 기준으로 뭘 봐야 하나요?",
                "iOVU 같은 {practice_area} 브랜드 추천해주세요",
                "{metric}가 좋은 {practice_area} 브랜드는?",
                "{practice_area} 브랜드 비교해서 알려주세요",
                "{region}에서 인기 있는 {practice_area} 쇼핑몰은?",
                "{practice_area} 전문 브랜드를 찾고 있어요"
            ],
            
            # 탐색비교 - 보통
            ("보통", "탐색비교"): [
                "{region}에서 {practice_area} 브랜드를 {metric} 기준으로 비교해주세요",
                "{time_span} 기간 {region} {practice_area} 상위 브랜드를 {metric} 기준으로 정리해주세요",
                "{practice_area} 분야에서 {metric}가 우수한 브랜드를 추천해주세요",
                "{source_hint}에서 인기 있는 {practice_area} 브랜드들의 {metric} 비교해주세요",
                "{time_span} {practice_area} 트렌드를 반영한 브랜드 추천해주세요",
                "{region} {practice_area} 시장에서 {metric} 기준 상위 브랜드들을 소개해주세요",
                "{practice_area} 브랜드들의 {metric} 특징을 {time_span} 기준으로 비교해주세요"
            ],
            
            # 탐색비교 - 어려움
            ("어려움", "탐색비교"): [
                "{time_span} 동안 {region} {practice_area} 시장 점유율 상위 브랜드를 {source_hint} 데이터로 분석해주세요",
                "{practice_area} 브랜드의 {metric} 비교분석과 {region} 시장 특성을 반영한 추천 리스트를 작성해주세요",
                "{source_hint} 데이터 기반 {region} {practice_area} 시장의 경쟁구도와 주요 브랜드들의 {metric} 분석해주세요",
                "글로벌 {practice_area} 시장에서 {metric} 우위를 가진 브랜드들의 전략 분석과 iOVU 포지셔닝을 평가해주세요",
                "{time_span} 트렌드와 {source_hint} 데이터를 종합한 {practice_area} 브랜드 투자 가치 평가해주세요",
                "{region} {practice_area} 시장에서 {metric} 혁신을 주도하는 브랜드들의 전략을 {source_hint} 기준으로 분석해주세요"
            ],
            
            # 거래상담 - 쉬움
            ("쉬움", "거래상담"): [
                "{region} {practice_area} 제품 가격은 대략 얼마인가요?",
                "{practice_area} 관련해서 iOVU에서 구매할 수 있나요?",
                "{region}에서 {practice_area} 배송 기간은 보통 어느 정도인가요?",
                "iOVU {practice_area} 제품 주문하고 싶어요",
                "{practice_area} 할인 혜택이 있나요?",
                "iOVU {practice_area} {metric} 상담받고 싶어요",
                "{practice_area} 제품 구매 문의드려요",
                "{region}에서 iOVU {practice_area} 구매 가능한가요?"
            ],
            
            # 거래상담 - 보통
            ("보통", "거래상담"): [
                "{time_span} 기준 {region} {practice_area} {metric} 평균 가격은?",
                "iOVU에서 {practice_area} 제품의 {metric}와 서비스 내용을 상담받고 싶습니다",
                "{practice_area} 제품의 {metric} 기준과 {region} 배송을 고려한 구매 가이드를 제공해주세요",
                "{source_hint}에서 추천하는 {practice_area} 제품 구매 전략을 알려주세요",
                "{metric}를 고려한 {practice_area} 최적 구매 옵션을 상담받고 싶어요",
                "iOVU {practice_area} 제품 {metric} 비교해서 구매 추천해주세요",
                "{region} 기준 {practice_area} 제품 {metric} 정보와 구매 방법 알려주세요"
            ],
            
            # 거래상담 - 어려움
            ("어려움", "거래상담"): [
                "{practice_area} 브랜드가 제시하는 대량 구매 할인 정책을 {source_hint}와 함께 비교해주세요",
                "복잡한 {practice_area} 커스터마이징에서 iOVU의 {metric} 우위와 차별화 포인트를 설명해주세요",
                "{time_span} 기간 {region} {practice_area} 시장 동향을 반영한 iOVU의 투자 가치와 {metric} 경쟁력을 분석해주세요",
                "글로벌 {practice_area} 시장에서 iOVU의 B2B 파트너십 전략과 {metric} 최적화 방안을 제안해주세요",
                "{source_hint} 트렌드와 {time_span} 시장 분석을 기반한 {practice_area} 장기 투자 전략을 상담받고 싶어요",
                "{region} {practice_area} 시장에서 iOVU의 {metric} 혁신 전략과 맞춤형 솔루션을 {source_hint} 기준으로 제안해주세요"
            ]
        }

    def generate_template(self, difficulty: str, intent: str, params: Dict) -> str:
        """특정 난이도와 의도에 맞는 템플릿 생성"""
        templates = self.templates.get((difficulty, intent), [])
        if not templates:
            return f"{params['region']} {params['practice_area']} 관련 {params['metric']} 정보를 알려주세요"
        
        template = random.choice(templates)
        formatted_template = template.format(
            region=params.get('region', '한국'),
            practice_area=params.get('practice_area', '개발자 밈 굿즈'),
            metric=params.get('metric', '제품 가격'),
            time_span=params.get('time_span', '최근 3개월'),
            source_hint=params.get('source_hint', '개발자 커뮤니티')
        )
        
        return formatted_template

class IOVUIntegratedSystem:
    """iOVU 통합 프롬프트 생성 시스템"""
    
    def __init__(self):
        self.params = IOVUParameters()
        self.template_gen = IOVUTemplateGenerator()
        
        self.brand_info = {
            "name": "iOVU",
            "description": "개발자를 위한 밈 굿즈 브랜드",
            "website": "https://iovu-shop.vercel.app/",
            "slogan": "개발자를 위한 귀여운 반란",
            "concept": "Dev + Cute = iOVU",
            "target": "IT 개발자, 너디 감성을 즐기는 사람들",
            "specialties": ["개발자 밈", "너디 패션", "코딩 유머", "힐링 개발템"],
            "products": ["티셔츠", "후드티", "에코백", "스티커", "머그컵", "노트북 스티커"],
            "features": ["고품질 프린팅", "편안한 착용감", "트렌디한 디자인", "합리적 가격"]
        }

    def extract_keywords_from_query(self, user_query: str) -> Dict:
        """사용자 질의에서 키워드 추출"""
        extracted = {
            "practice_area": None,
            "region": None,
            "metric": None,
            "intent": None,
            "difficulty": None
        }
        
        # 간단한 키워드 매칭
        for area in self.params.practice_areas:
            if area in user_query or any(word in user_query for word in area.split()):
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
        
        # 의도 분류
        if any(word in user_query for word in ["얼마", "어떻게", "무엇", "언제", "왜"]):
            extracted["intent"] = "정보조회"
        elif any(word in user_query for word in ["추천", "비교", "어디서", "찾아", "리스트"]):
            extracted["intent"] = "탐색비교"
        elif any(word in user_query for word in ["구매", "주문", "상담", "문의", "도움"]):
            extracted["intent"] = "거래상담"
        else:
            extracted["intent"] = "정보조회"
        
        # 난이도 분류 (문장 길이 기반)
        if len(user_query) < 20:
            extracted["difficulty"] = "쉬움"
        elif len(user_query) < 50:
            extracted["difficulty"] = "보통"
        else:
            extracted["difficulty"] = "어려움"
        
        return extracted

    def generate_iovu_prompt(self, user_query: str) -> Dict:
        """iOVU 특화 프롬프트 생성"""
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
        
        # 4. 자연스러운 질의 문장 반환
        return {
            "prompt": base_template,
            "extracted_keywords": extracted_keywords,
            "final_parameters": params,
            "template_used": base_template,
            "brand_info": self.brand_info
        }

    def batch_generate_samples(self, num_samples: int = 10) -> List[Dict]:
        """배치 샘플 생성"""
        sample_queries = [
            "한국에서 개발자 밈 굿즈 가격이 얼마나 해요?",
            "너디 패션 브랜드 추천해주세요",
            "코딩 유머 티셔츠 어디서 사나요?",
            "프로그래머 라이프스타일 제품이 뭐가 있나요?",
            "개발자 선물로 좋은 굿즈 있나요?",
            "힐링 개발템 브랜드 비교해주세요",
            "깃허브 문화 관련 굿즈 찾고 있어요",
            "해커톤에서 쓸 굿즈 주문하고 싶어요",
            "스타트업 팀티 맞춤 제작 가능한가요?",
            "개발자 정체성 표현할 수 있는 아이템 추천해주세요",
            "iOVU 제품 품질은 어떤가요?",
            "테크 패션 트렌드가 궁금해요",
            "프로그래밍 액세서리 구매하고 싶어요",
            "개발자 라이프 굿즈 추천해주세요",
            "코딩 머천다이즈 시장 동향은?"
        ]
        
        results = []
        for i in range(min(num_samples, len(sample_queries))):
            query = sample_queries[i]
            result = self.generate_iovu_prompt(query)
            result["sample_id"] = f"iovu_sample_{i+1:02d}"
            result["query"] = query
            results.append(result)
        
        return results

    def export_to_csv(self, samples: List[Dict], filename: str = None):
        """CSV 파일로 저장"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"iovu_prompts_{timestamp}.csv"
        
        # JSON 데이터를 평면화하여 DataFrame 생성
        flattened_data = []
        for sample in samples:
            flattened_row = {
                'prompt': sample.get('prompt', ''),
                'query': sample.get('query', ''),
                'sample_id': sample.get('sample_id', ''),
                'template_used': sample.get('template_used', ''),
                
                # extracted_keywords 평면화
                'extracted_keywords_practice_area': sample.get('extracted_keywords', {}).get('practice_area', ''),
                'extracted_keywords_region': sample.get('extracted_keywords', {}).get('region', ''),
                'extracted_keywords_metric': sample.get('extracted_keywords', {}).get('metric', ''),
                'extracted_keywords_intent': sample.get('extracted_keywords', {}).get('intent', ''),
                'extracted_keywords_difficulty': sample.get('extracted_keywords', {}).get('difficulty', ''),
                
                # final_parameters 평면화
                'final_parameters_practice_area': sample.get('final_parameters', {}).get('practice_area', ''),
                'final_parameters_metric': sample.get('final_parameters', {}).get('metric', ''),
                'final_parameters_region': sample.get('final_parameters', {}).get('region', ''),
                'final_parameters_time_span': sample.get('final_parameters', {}).get('time_span', ''),
                'final_parameters_source_hint': sample.get('final_parameters', {}).get('source_hint', ''),
                'final_parameters_language_ratio': sample.get('final_parameters', {}).get('language_ratio', ''),
                'final_parameters_intent': sample.get('final_parameters', {}).get('intent', ''),
                'final_parameters_difficulty': sample.get('final_parameters', {}).get('difficulty', ''),
                
                # brand_info 평면화
                'brand_info_name': sample.get('brand_info', {}).get('name', ''),
                'brand_info_description': sample.get('brand_info', {}).get('description', ''),
                'brand_info_website': sample.get('brand_info', {}).get('website', ''),
                'brand_info_slogan': sample.get('brand_info', {}).get('slogan', ''),
                'brand_info_concept': sample.get('brand_info', {}).get('concept', ''),
                'brand_info_target': sample.get('brand_info', {}).get('target', ''),
                'brand_info_specialties': ', '.join(sample.get('brand_info', {}).get('specialties', [])),
                'brand_info_products': ', '.join(sample.get('brand_info', {}).get('products', [])),
                'brand_info_features': ', '.join(sample.get('brand_info', {}).get('features', []))
            }
            flattened_data.append(flattened_row)
        
        # DataFrame 생성 및 CSV 저장
        df = pd.DataFrame(flattened_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"✅ iOVU 프롬프트 데이터가 CSV로 {filename}에 저장되었습니다.")
        print(f"📊 총 {len(df)}개 행, {len(df.columns)}개 컬럼")
        return filename

    def export_to_json(self, samples: List[Dict], filename: str = None):
        """JSON 파일로 저장 (기존 기능 유지)"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"iovu_prompts_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(samples, f, ensure_ascii=False, indent=2)
        
        print(f"✅ iOVU 프롬프트 데이터가 JSON으로 {filename}에 저장되었습니다.")
        return filename

def generate_massive_iovu_prompts(num_prompts: int = 1000):
    """대량 iOVU 프롬프트 생성 (CSV 저장)"""
    print(f"=== {num_prompts}개 iOVU 프롬프트 생성 시작 ===")
    
    system = IOVUIntegratedSystem()
    
    # 다양한 질의 패턴 생성
    base_queries = [
        "개발자 밈 굿즈 찾고 있어요",
        "너디 패션 브랜드 추천해주세요", 
        "코딩 유머 아이템 가격이 궁금해요",
        "프로그래머 라이프스타일 제품 문의",
        "개발자 선물 추천해주세요",
        "힐링 개발템 어디서 사나요",
        "깃허브 문화 굿즈 주문하고 싶어요",
        "해커톤 굿즈 대량 구매 가능한가요",
        "스타트업 문화 아이템 커스터마이징",
        "개발자 정체성 표현 굿즈 추천",
        "테크 패션 트렌드 알고 싶어요",
        "프로그래밍 액세서리 구매하려고요",
        "개발자 라이프 굿즈 상담받고 싶어요",
        "코딩 머천다이즈 시장 정보 필요해요",
        "iOVU 제품 품질 어떤가요"
    ]
    
    # 변형 요소들
    prefixes = ["", "급하게 ", "전문적으로 ", "고품질로 ", "트렌디하게 ", "합리적으로 "]
    suffixes = ["", " 도움주세요", " 상담받고 싶어요", " 문의드려요", " 알려주세요", " 추천해주세요"]
    
    # 질의 확장
    all_queries = []
    for base in base_queries:
        for prefix in prefixes:
            for suffix in suffixes:
                regions = ["한국", "서울", "부산", "미국", "일본"]
                for region in regions:
                    variants = [
                        f"{prefix}{base}{suffix}".strip(),
                        f"{region}에서 {prefix}{base}{suffix}".strip(),
                        f"iOVU {base}",
                        f"{base} 브랜드 비교"
                    ]
                    all_queries.extend(variants)
    
    # 추가 다양한 질의 생성
    while len(all_queries) < num_prompts:
        base = random.choice(base_queries)
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        region = random.choice(system.params.regions)
        area = random.choice(system.params.practice_areas)
        metric = random.choice([m for metrics in system.params.metrics.values() for m in metrics])
        
        additional_variants = [
            f"{prefix}{region}에서 {area} {base}{suffix}",
            f"{area} {metric} 정보 {base}",
            f"{region} {base} {metric} 비교",
            f"{base} {area} 전문 브랜드",
            f"iOVU 같은 {area} 브랜드",
            f"{metric} 좋은 {area} 추천",
            f"{area} 시장에서 {metric} 트렌드",
            f"{region} {area} {metric} 현황"
        ]
        
        all_queries.extend(additional_variants)
    
    # 중복 제거 및 목표 개수만큼 선택
    unique_queries = list(set(all_queries))
    selected_queries = unique_queries[:num_prompts]
    
    # 프롬프트 생성
    prompts = []
    for i, query in enumerate(selected_queries):
        if i % 100 == 0:
            print(f"진행률: {i}/{len(selected_queries)} ({i/len(selected_queries)*100:.1f}%)")
        
        try:
            result = system.generate_iovu_prompt(query)
            result["sample_id"] = f"iovu_prompt_{i+1:04d}"
            result["query"] = query
            prompts.append(result)
        except Exception as e:
            print(f"오류 발생 (인덱스 {i}): {str(e)}")
            continue
    
    # CSV 파일로 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"iovu_massive_{timestamp}.csv"
    
    # CSV 저장
    system.export_to_csv(prompts, csv_filename)
    
    # 통계 정보
    intent_stats = {}
    difficulty_stats = {}
    for prompt in prompts:
        intent = prompt['final_parameters']['intent']
        difficulty = prompt['final_parameters']['difficulty']
        intent_stats[intent] = intent_stats.get(intent, 0) + 1
        difficulty_stats[difficulty] = difficulty_stats.get(difficulty, 0) + 1
    
    print(f"\n=== 총 {len(prompts)}개 iOVU 프롬프트 생성 완료 ===")
    print(f"📁 CSV 파일 저장: {csv_filename}")
    print(f"\n📈 의도별 분포: {intent_stats}")
    print(f"📊 난이도별 분포: {difficulty_stats}")
    
    # 샘플 출력
    print(f"\n=== 샘플 결과 (상위 5개) ===")
    for i, prompt in enumerate(prompts[:5], 1):
        print(f"{i}. 입력: {prompt['query']}")
        print(f"   출력: {prompt['prompt']}")
        print(f"   의도: {prompt['final_parameters']['intent']}, 난이도: {prompt['final_parameters']['difficulty']}")
        print()
    
    return prompts

# GPT-4o 테스트용 간단한 실행 함수
def prepare_for_gpt4o(prompts: List[Dict]) -> List[str]:
    """GPT-4o에 바로 사용할 수 있는 프롬프트 리스트 반환"""
    return [prompt['prompt'] for prompt in prompts]

# 테스트 실행
if __name__ == "__main__":
    print("=== iOVU 브랜드 고급 프롬프트 생성 시스템 (CSV 저장) ===")
    
    iovu_system = IOVUIntegratedSystem()
    
    # 단일 테스트
    test_query = "한국에서 개발자 밈 굿즈 가격이 얼마나 해요?"
    result = iovu_system.generate_iovu_prompt(test_query)
    
    print(f"입력 질의: {test_query}")
    print(f"생성된 프롬프트: {result['prompt']}")
    print(f"추출된 키워드: {result['extracted_keywords']}")
    
    # 선택 메뉴
    print(f"\n선택하세요:")
    print("1. 기본 샘플 생성 (15개) - CSV 저장")
    print("2. 대량 생성 (1000개) - CSV 저장")
    print("3. 사용자 지정 개수 - CSV 저장")
    print("4. JSON 형식으로도 저장")
    
    choice = input("번호를 입력하세요 (1-4): ").strip()
    
    if choice == "1":
        samples = iovu_system.batch_generate_samples(15)
        iovu_system.export_to_csv(samples)
        
        print("\n✅ 생성된 iOVU 프롬프트들:")
        for i, sample in enumerate(samples, 1):
            print(f"{i}. {sample['prompt']}")
            
    elif choice == "2":
        generate_massive_iovu_prompts(1000)
        
    elif choice == "3":
        try:
            num = int(input("생성할 개수를 입력하세요: "))
            generate_massive_iovu_prompts(num)
        except ValueError:
            print("잘못된 숫자입니다.")
            
    elif choice == "4":
        samples = iovu_system.batch_generate_samples(15)
        csv_file = iovu_system.export_to_csv(samples)
        json_file = iovu_system.export_to_json(samples)
        
        print(f"\n✅ 두 형식으로 모두 저장:")
        print(f"📄 CSV: {csv_file}")
        print(f"📄 JSON: {json_file}")
        
        print("\n생성된 iOVU 프롬프트들:")
        for i, sample in enumerate(samples[:5], 1):
            print(f"{i}. {sample['prompt']}")
            
    else:
        print("기본 샘플 생성을 실행합니다.")
        samples = iovu_system.batch_generate_samples(15)
        iovu_system.export_to_csv(samples)