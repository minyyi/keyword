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
        
        # ✅ 정보 밀도 향상을 위한 키워드 강화 템플릿
        self.templates = {
            ("쉬움", "정보조회"): [
                "{region}지방법원 관할 {practice_area} 전문 변호사의 {metric} 평균 비용이 궁금해요",
                "{region} {practice_area} 분야 법무법인 동래의 {metric} 상담 서비스가 어떻게 되나요",
                "{practice_area} 사건 {metric} 기준과 {region} 법조계 현황을 알고 싶어요",
                "{region} 지역 {practice_area} 전문 변호사 {metric} 정보와 대한변협 인증 자료가 필요해요",
                "{practice_area} 관련 {metric} 통계와 {region} 법원 관할 절차를 설명해주세요"
            ],
            ("보통", "정보조회"): [
                "{time_span} 기준 {region}지방법원 관할 {practice_area} 전문 변호사의 {metric} 통계와 {source_hint} 인증 자료를 분석해주세요",
                "{region} {practice_area} 분야 법무법인의 {metric} 현황과 판례 검토를 통한 {source_hint} 데이터 분석이 필요합니다",
                "{practice_area} 사건의 {metric} 기준과 {region} 법조계 특성을 고려한 {source_hint} 통계 정보를 제공해주세요",
                "{time_span} 동안 {region} {practice_area} 변호사 {metric} 평균과 {source_hint} 공식 발표 자료를 종합해주세요",
                "{region} {practice_area} 분야 {metric} 현황을 {time_span} 기준 {source_hint} 데이터로 상세 분석해주세요"
            ],
            ("어려움", "정보조회"): [
                "{source_hint} 공식 발표 자료에 따른 {time_span} {region}지방법원 관할 {practice_area} 로펌의 {metric} 통계와 시장 성장 전망을 종합 분석해주세요",
                "{practice_area} 전문 법무법인이 제시하는 {metric} 체계와 {source_hint} 인증 기준을 {region} 법조계 특성과 함께 비교 분석해주세요",
                "{time_span} 기간 {region} {practice_area} 법무 시장의 {metric} 세부 분석과 {source_hint} 기반 향후 전망을 제공해주세요",
                "{source_hint} 데이터로 분석한 {region}지방법원 {practice_area} 분야 {metric} 트렌드와 법무법인 동래의 경쟁력을 설명해주세요",
                "{time_span} 기간 {region} {practice_area} 로펌들의 {metric} 경쟁력을 {source_hint} 공식 통계와 판례 분석으로 평가해주세요"
            ],
            ("쉬움", "탐색비교"): [
                "{practice_area} 전문 변호사를 {region}지방법원 관할 지역에서 어떻게 찾을 수 있나요",
                "{region} {practice_area} 전문 로펌 리스트를 확인할 수 있는 대한변협 공식 통계는 어디서 보나요",
                "{practice_area} 변호사 선택할 때 {metric} 기준과 {region} 법조계 특성을 어떻게 고려해야 하나요",
                "{region} {practice_area} 로펌 추천과 법무법인 동래 상담 서비스를 비교해주세요",
                "{practice_area} 분야 우수한 변호사를 {region} 지역에서 찾는 방법과 기준을 알려주세요"
            ],
            ("보통", "탐색비교"): [
                "{region}지방법원 관할 {practice_area} 전문 로펌 리스트를 확인할 수 있는 {source_hint} 공식 통계 자료는 어디서 구할 수 있나요",
                "{time_span} 기간 {region} {practice_area} 상위 10개 로펌을 {metric} 기준과 {source_hint} 평가로 정리해주세요",
                "{practice_area} 분야에서 {metric}가 우수한 {region} 지역 법무법인을 {source_hint} 인증 기준으로 추천해주세요",
                "{region} {practice_area} 로펌들의 {metric} 비교와 법무법인 동래의 차별화 포인트를 분석해주세요",
                "{time_span} 동안 {region} {practice_area} 분야 로펌 순위를 {source_hint} 공식 자료로 알려주세요"
            ],
            ("어려움", "탐색비교"): [
                "{time_span} 동안 {region}지방법원 관할 {practice_area} 사건 처리 상위 10개 로펌을 제시한 {source_hint} 공식 보고서와 통계 자료를 분석해주세요",
                "{practice_area} 전문 로펌의 {metric} 비교분석과 {region} 지역 법조계 특성을 반영한 맞춤형 추천 리스트를 작성해주세요",
                "{source_hint} 공식 데이터를 기반으로 {region} {practice_area} 법무 시장의 경쟁구도와 주요 플레이어들의 {metric} 세부 분석을 제공해주세요",
                "{time_span} 기간 {source_hint}가 발표한 {region} {practice_area} 로펌 {metric} 공식 랭킹과 법무법인 동래의 포지셔닝을 분석해주세요",
                "{region}지방법원 {practice_area} 시장에서 {metric} 기준 상위 로펌들의 경쟁력을 {source_hint} 자료와 판례 분석으로 비교해주세요"
            ],
            ("쉬움", "거래상담"): [
                "{region} {practice_area} 사건 전문 변호사 상담료와 법무법인 동래 서비스 비용이 궁금해요",
                "{practice_area} 관련해서 법무법인 동래에 상담받을 수 있는 절차와 비용을 알려주세요",
                "{region}지방법원 관할 {practice_area} 사건 처리 기간과 변호사 {metric}이 어느 정도인가요",
                "{practice_area} 사건 {metric}와 법무법인 동래의 29년 업력 기반 전문성이 궁금해요",
                "{region}에서 {practice_area} 전문 변호사 찾고 합리적 수임료 상담받고 싶어요"
            ],
            ("보통", "거래상담"): [
                "{time_span} 기준 {region} {practice_area} 변호사 {metric} 평균과 법무법인 동래의 원스톱 서비스를 비교해주세요",
                "법무법인 동래에서 {practice_area} 사건의 {metric}와 29년 업력 기반 전문 서비스 내용을 상담받고 싶습니다",
                "{practice_area} 사건의 {metric} 기준과 {region} 지역 법조계 특성을 고려한 변호사 선택 가이드와 상담 절차를 제공해주세요",
                "{region} {practice_area} 전문 변호사 {metric} 상담과 법무법인 동래의 Busan Legal First-Mover 서비스를 받고 싶어요",
                "{practice_area} 관련 {metric}와 절차를 {region} 법조계 기준으로 설명하고 합리적 수임료 상담도 받고 싶어요"
            ],
            ("어려움", "거래상담"): [
                "{practice_area} 전문 로펌이 제시하는 착수금과 성공보수 체계를 {source_hint} 기준과 함께 비교하고 법무법인 동래 상담을 받고 싶어요",
                "복잡한 {practice_area} 사건에서 법무법인 동래의 {metric} 우위와 29년 업력 기반 차별화 포인트를 구체적으로 설명하고 상담 절차도 안내해주세요",
                "{time_span} 기간 {region} {practice_area} 시장 동향을 반영한 법무법인 동래의 원스톱 서비스 포트폴리오와 {metric} 경쟁력을 분석하고 상담받고 싶어요",
                "{source_hint} 기준으로 {region} {practice_area} 분야 {metric} 최적화 전략을 제안하고 법무법인 동래의 Busan Legal First-Mover 서비스 상담을 받고 싶어요",
                "복합적인 {practice_area} 사건에서 {region} 지역 {metric} 경쟁력을 {time_span} 트렌드와 함께 분석하고 법무법인 동래 전문 상담을 받고 싶어요"
            ]
        }

    def generate_template(self, difficulty: str, intent: str, params: Dict) -> str:
        templates = self.templates.get((difficulty, intent), [])
        if not templates:
            # 기본 템플릿도 정보 밀도 강화
            return f"{params['region']}지방법원 관할 {params['practice_area']} 전문 변호사의 {params['metric']} 정보와 법무법인 동래 상담 서비스를 알려주세요"
        
        template = random.choice(templates)
        formatted_template = template.format(
            region=params.get('region', '부산'),
            practice_area=params.get('practice_area', '기업법무'),
            metric=params.get('metric', '수임료'),
            time_span=params.get('time_span', '최근3년'),
            source_hint=params.get('source_hint', '대한변협')
        )
        
        return formatted_template

# 추가로 번역투 표현 개선 함수도 강화
def improve_prompt_naturalness(prompt: str) -> str:
    """번역투 표현을 자연스러운 한국어로 개선하고 정보 밀도 추가"""
    improvements = {
        '를 알려줘요': '가 궁금해요',
        '를 알려줘': '를 알려주세요', 
        '를 제공해주세요': '를 설명해주세요',
        '기준으로': '바탕으로',
        '관련해서': '에 대해',
        '정리해주세요': '분석해주세요',
        '설명해 주세요': '설명해주세요',
        '비교해 주세요': '비교해주세요'
    }
    
    # 정보 밀도 추가 키워드
    density_enhancers = {
        '부산': '부산지방법원 관할',
        '변호사': '전문 변호사',
        '로펌': '법무법인',
        '비용': '비용 체계',
        '상담': '전문 상담'
    }
    
    improved = prompt
    
    # 번역투 개선
    for old, new in improvements.items():
        improved = improved.replace(old, new)
    
    # 정보 밀도 강화 (이미 강화된 단어가 없는 경우만)
    for old, new in density_enhancers.items():
        if old in improved and new not in improved:
            improved = improved.replace(old, new, 1)  # 첫 번째만 교체
    
    return improved

# clean_prompt 함수도 수정
def enhanced_clean_prompt(self, prompt: str) -> str:
    """프롬프트에서 괄호 제거, 정리 및 정보 밀도 강화"""
    # 1. 모든 괄호와 내용 제거
    cleaned = re.sub(r'\([^)]*\)', '', prompt)
    
    # 2. 연속된 공백을 하나로 정리
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # 3. 앞뒤 공백 제거
    cleaned = cleaned.strip()
    
    # 4. 번역투 표현 개선 및 정보 밀도 강화
    cleaned = improve_prompt_naturalness(cleaned)
    
    # 5. 문장 끝 정리
    if not cleaned.endswith(('?', '.', '요', '다', '까')):
        if '?' in prompt or '궁금' in cleaned or '알려' in cleaned:
            if not cleaned.endswith('요'):
                cleaned += '요'
        else:
            if not cleaned.endswith('.'):
                cleaned += '.'
    
    return cleaned

class DongrageLawIntegratedSystem:
    """법무법인 동래 통합 AI 서비스 시스템 (괄호 없는 단순 질의 생성)"""
    
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

    def clean_prompt(self, prompt: str) -> str:
        """프롬프트에서 괄호 제거 및 정리"""
        # 1. 모든 괄호와 내용 제거
        cleaned = re.sub(r'\([^)]*\)', '', prompt)
        
        # 2. 연속된 공백을 하나로 정리
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # 3. 앞뒤 공백 제거
        cleaned = cleaned.strip()
        
        # 4. 문장 끝 정리
        if not cleaned.endswith(('?', '.', '요', '다', '까')):
            if '?' in prompt or '궁금' in cleaned or '알려' in cleaned:
                if not cleaned.endswith('요'):
                    cleaned += '요'
            else:
                if not cleaned.endswith('.'):
                    cleaned += '.'
        
        return cleaned

    def generate_dongrae_prompt(self, user_query: str) -> Dict:
        """괄호 없는 자연스러운 질의 문장 생성"""
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
        
        # 4. ✅ 괄호 제거 및 정리
        clean_prompt = self.clean_prompt(base_template)
        
        return {
            "prompt": clean_prompt,  # 괄호 없는 깨끗한 질의 문장
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

    def export_to_csv(self, samples: List[Dict], filename: str = None):
        """CSV 파일로 저장"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dongrae_clean_prompts_{timestamp}.csv"
        
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
                'brand_info_english_name': sample.get('brand_info', {}).get('english_name', ''),
                'brand_info_website': sample.get('brand_info', {}).get('website', ''),
                'brand_info_location': sample.get('brand_info', {}).get('location', ''),
                'brand_info_phone': sample.get('brand_info', {}).get('phone', ''),
                'brand_info_established': sample.get('brand_info', {}).get('established', ''),
                'brand_info_experience': sample.get('brand_info', {}).get('experience', ''),
                'brand_info_specialties': ', '.join(sample.get('brand_info', {}).get('specialties', [])),
                'brand_info_slogan': sample.get('brand_info', {}).get('slogan', ''),
                'brand_info_target_regions': ', '.join(sample.get('brand_info', {}).get('target_regions', []))
            }
            flattened_data.append(flattened_row)
        
        # DataFrame 생성 및 CSV 저장
        df = pd.DataFrame(flattened_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"✅ 괄호 없는 깨끗한 프롬프트 데이터가 CSV로 {filename}에 저장되었습니다.")
        print(f"📊 총 {len(df)}개 행, {len(df.columns)}개 컬럼")
        return filename

    def export_to_json(self, samples: List[Dict], filename: str = None):
        """JSON 파일로 저장 (기존 기능 유지)"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dongrae_clean_prompts_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(samples, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 괄호 없는 깨끗한 프롬프트 데이터가 JSON으로 {filename}에 저장되었습니다.")
        return filename

# 대량 생성 함수 수정 (CSV 저장)
def generate_massive_clean_prompts(num_prompts: int = 1000):
    """대량 괄호 없는 깨끗한 프롬프트 생성 (CSV 저장)"""
    print(f"=== {num_prompts}개 괄호 없는 깨끗한 프롬프트 생성 시작 ===")
    
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
            result["sample_id"] = f"clean_prompt_{i+1:04d}"
            result["query"] = query
            prompts.append(result)
        except Exception as e:
            print(f"오류 발생 (인덱스 {i}): {str(e)}")
            continue
    
    # ✅ CSV 파일로 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"dongrae_clean_massive_{timestamp}.csv"
    
    # CSV 저장 함수 호출
    system.export_to_csv(prompts, csv_filename)
    
    print(f"\n=== 총 {len(prompts)}개 괄호 없는 깨끗한 프롬프트 생성 완료 ===")
    print(f"📁 CSV 파일 저장: {csv_filename}")
    
    # 샘플 출력
    print(f"\n=== 샘플 결과 (상위 5개) ===")
    for i, prompt in enumerate(prompts[:5], 1):
        print(f"{i}. 입력: {prompt['query']}")
        print(f"   출력: {prompt['prompt']}")
        print(f"   원본 템플릿: {prompt['template_used']}")
        print()
    
    return prompts

# 테스트 실행
if __name__ == "__main__":
    print("=== 법무법인 동래 괄호 없는 깨끗한 질의 생성 시스템 ===")
    
    dongrae_system = DongrageLawIntegratedSystem()
    
    # 단일 테스트
    test_query = "부산에서 교통사고 변호사 비용이 얼마나 하나요?"
    result = dongrae_system.generate_dongrae_prompt(test_query)
    
    print(f"입력 질의: {test_query}")
    print(f"생성된 프롬프트: {result['prompt']}")
    print(f"원본 템플릿: {result['template_used']}")
    print(f"추출된 키워드: {result['extracted_keywords']}")
    
    # 선택 메뉴
    print(f"\n선택하세요:")
    print("1. 기본 샘플 생성 (10개)")
    print("2. 중복 제거 모드 🔄")
    print("3. 대량 생성 (1000개)")
    print("4. 사용자 지정 개수")
    
    choice = input("번호를 입력하세요 (1-4): ").strip()
    
    if choice == "1":
        samples = dongrae_system.batch_generate_samples(10)
        dongrae_system.export_to_csv(samples)  # ✅ CSV로 저장
        
        print("\n✅ 생성된 괄호 없는 깨끗한 프롬프트들:")
        for i, sample in enumerate(samples, 1):
            print(f"{i}. {sample['prompt']}")
    
    elif choice == "2":
        print("\n🔄 === 중복 제거 모드 ===")
        print("기존 프롬프트 파일을 업로드하여 중복되지 않는 프롬프트를 생성합니다.")
        
        # 기존 프롬프트 파일 업로드
        existing_file = input("기존 프롬프트 파일 경로 (CSV 또는 JSON): ").strip()
        
        if existing_file:
            loaded_count = dongrae_system.load_existing_prompts(existing_file)
            if loaded_count > 0:
                try:
                    count = int(input("생성할 프롬프트 개수 (기본 100): ") or "100")
                    max_attempts = int(input("프롬프트당 최대 시도 횟수 (기본 50): ") or "50")
                except ValueError:
                    count = 100
                    max_attempts = 50
                    print("잘못된 입력입니다. 기본값을 사용합니다.")
                
                print(f"\n🔄 중복되지 않는 {count}개 프롬프트 생성 중...")
                samples = dongrae_system.generate_non_duplicate_batch(count, max_attempts)
                
                # CSV 저장
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"dongrae_non_duplicate_{timestamp}.csv"
                dongrae_system.export_to_csv(samples, filename)
                
                print(f"\n🎉 === 중복 제거 모드 완료 ===")
                print(f"📁 저장 파일: {filename}")
                print(f"✨ 총 생성: {len(samples)}개 (중복 없음)")
                
                # 샘플 출력
                print(f"\n📋 === 샘플 프롬프트 (상위 5개) ===")
                for i, sample in enumerate(samples[:5], 1):
                    print(f"{i}. {sample['prompt']}")
            else:
                print("❌ 파일 로드에 실패했습니다.")
        else:
            print("❌ 파일 경로를 입력해주세요.")
            
    elif choice == "3":
        generate_massive_clean_prompts(1000)  # ✅ 자동으로 CSV 저장
        
    elif choice == "4":
        try:
            num = int(input("생성할 개수를 입력하세요: "))
            generate_massive_clean_prompts(num)  # ✅ 자동으로 CSV 저장
        except ValueError:
            print("잘못된 숫자입니다.")
            
    else:
        print("기본 샘플 생성을 실행합니다.")
        samples = dongrae_system.batch_generate_samples(10)
        dongrae_system.export_to_csv(samples)  # ✅ CSV로 저장
