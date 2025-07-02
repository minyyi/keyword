# 법무법인 동래 완전 통합 AI 서비스 시스템 (오류 해결)
import json
import random
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass
from collections import defaultdict
import re

# ==================== 기본 파라미터 클래스 ====================
class DongraeLawParameters:
    """법무법인 동래 특화 파라미터 클래스"""
    
    def __init__(self):
        # 1. 법무 전문분야 (practice_area)
        self.practice_areas = [
            "기업법무", "계약법무", "소송및분쟁해결", "지적재산권", "금융법무",
            "부동산법무", "노동법무", "조세법무", "형사법무", 
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
            "KISDI", "대법원", "부산지법", "부산법원"
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

# ==================== 템플릿 설정 클래스 ====================
@dataclass
class TemplateConfig:
    """템플릿 설정 클래스"""
    brand_name: str = "법무법인 동래"
    website: str = "dongraelaw.shop"
    location: str = "부산 연제구 거제동"
    experience: str = "29년 업력"
    specialty: str = "부산·경남 지역밀착"

# ==================== 템플릿 생성기 클래스 ====================
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
                "({source_hint}) 자료에 따르면, ({time_span}) ({region}) ({practice_area}) 로펌의 ({metric})와 성장 전망을 설명해 주세요.",
                "({practice_area}) 로펌이 제시하는 ({metric}) + ({source_hint})와 함께 비교해 주세요.",
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

# ==================== 고급 키워드 추출기 ====================
class AdvancedKeywordExtractor:
    """법무법인 동래 특화 고급 키워드 추출기"""
    
    def __init__(self):
        # 법무 분야별 세부 키워드 사전
        self.detailed_keywords = {
            "기업법무": {
                "primary": ["기업", "회사", "법인", "사업", "경영"],
                "secondary": ["설립", "M&A", "합병", "인수", "투자", "주식", "IPO", "상장"],
            },
            "계약법무": {
                "primary": ["계약", "계약서", "협정", "약정"],
                "secondary": ["작성", "검토", "협상", "체결", "해지", "갱신"],
            },
            "소송및분쟁해결": {
                "primary": ["소송", "분쟁", "재판", "법원", "판결"],
                "secondary": ["민사", "상사", "행정", "중재", "조정", "화해"],
            },
            "부동산법무": {
                "primary": ["부동산", "아파트", "주택", "건물", "토지"],
                "secondary": ["매매", "임대차", "전세", "월세", "분양", "개발"],
            },
            "노동법무": {
                "primary": ["노동", "근로", "고용", "직장", "회사"],
                "secondary": ["해고", "퇴직", "임금", "급여", "연장근무", "휴가"],
            },
            "형사법무": {
                "primary": ["형사", "범죄", "경찰", "검찰", "수사"],
                "secondary": ["고소", "고발", "조사", "구속", "기소", "재판"],
            }
        }
        
        # 지역별 세부 키워드
        self.region_keywords = {
            "부산": ["부산", "부산시", "부산광역시", "동래", "해운대", "서면", "남포동"],
            "부산연제구": ["연제구", "거제동", "법원남로", "부산법원"],
            "경남": ["경남", "경상남도", "창원", "김해", "양산", "진주", "통영"],
            "울산": ["울산", "울산시", "울산광역시", "남구", "동구", "북구"]
        }
        
        # 의도 분류 키워드
        self.intent_keywords = {
            "정보조회": {
                "question_words": ["얼마", "어떻게", "무엇", "언제", "어디서", "왜"],
                "info_seeking": ["알려주세요", "궁금해요", "알고싶어요", "정보", "설명"]
            },
            "탐색비교": {
                "comparison": ["비교", "추천", "어디가", "어느곳", "리스트", "순위"],
                "exploration": ["찾아주세요", "알아봐주세요", "검색", "찾기"]
            },
            "거래상담": {
                "consultation": ["상담", "문의", "도움", "도와주세요", "조언"],
                "transaction": ["의뢰", "부탁", "신청", "예약", "계약"]
            }
        }

    def extract_comprehensive_keywords(self, user_query: str) -> Dict:
        """종합적 키워드 추출"""
        query_lower = user_query.lower()
        results = {
            "practice_areas": self._extract_practice_areas(query_lower),
            "regions": self._extract_regions(query_lower),
            "intent": self._classify_intent(query_lower),
            "urgency": self._classify_urgency(query_lower),
            "confidence_scores": {}
        }
        
        # 신뢰도 점수 계산
        results["confidence_scores"] = self._calculate_confidence(query_lower, results)
        
        return results

    def _extract_practice_areas(self, query: str) -> List[Tuple[str, float]]:
        """법무 분야 추출 및 신뢰도 계산"""
        area_scores = defaultdict(float)
        
        for area, keywords in self.detailed_keywords.items():
            score = 0
            
            # Primary 키워드 매칭 (가중치 3.0)
            for keyword in keywords["primary"]:
                if keyword in query:
                    score += 3.0
            
            # Secondary 키워드 매칭 (가중치 2.0)
            for keyword in keywords["secondary"]:
                if keyword in query:
                    score += 2.0
            
            if score > 0:
                area_scores[area] = score
        
        # 점수순 정렬
        sorted_areas = sorted(area_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_areas[:3]  # 상위 3개만 반환

    def _extract_regions(self, query: str) -> List[Tuple[str, float]]:
        """지역 추출 및 신뢰도 계산"""
        region_scores = defaultdict(float)
        
        for region, keywords in self.region_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in query:
                    score += 1.0
            
            if score > 0:
                region_scores[region] = score
        
        sorted_regions = sorted(region_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_regions

    def _classify_intent(self, query: str) -> Tuple[str, float]:
        """의도 분류"""
        intent_scores = defaultdict(float)
        
        for intent, keyword_groups in self.intent_keywords.items():
            score = 0
            for group_name, keywords in keyword_groups.items():
                for keyword in keywords:
                    if keyword in query:
                        score += 1.0
            
            intent_scores[intent] = score
        
        if not intent_scores:
            return ("정보조회", 0.5)  # 기본값
        
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        return best_intent

    def _classify_urgency(self, query: str) -> Tuple[str, float]:
        """긴급도 분류"""
        urgency_keywords = {
            "high": ["긴급", "응급", "즉시", "빨리", "급해", "오늘", "지금", "당장"],
            "medium": ["빠른", "신속", "조속", "이번주", "며칠"],
            "low": ["천천히", "여유있게", "나중에", "계획", "준비"]
        }
        
        urgency_scores = {"high": 0, "medium": 0, "low": 0}
        
        for urgency, keywords in urgency_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    urgency_scores[urgency] += 1.0
        
        # 문장 길이도 고려
        if len(query) < 20:
            urgency_scores["high"] += 0.5
        elif len(query) > 100:
            urgency_scores["low"] += 0.5
        
        best_urgency = max(urgency_scores.items(), key=lambda x: x[1])
        
        # 매핑
        urgency_map = {"high": "어려움", "medium": "보통", "low": "쉬움"}
        return (urgency_map[best_urgency[0]], best_urgency[1])

    def _calculate_confidence(self, query: str, results: Dict) -> Dict:
        """신뢰도 점수 계산"""
        confidence = {}
        
        # 법무분야 신뢰도
        if results["practice_areas"]:
            max_score = max([score for _, score in results["practice_areas"]])
            confidence["practice_area"] = min(max_score / 3.0, 1.0)  # 정규화
        else:
            confidence["practice_area"] = 0.1
        
        # 지역 신뢰도
        if results["regions"]:
            confidence["region"] = 0.9  # 지역 키워드는 명확함
        else:
            confidence["region"] = 0.5  # 기본값 (부산)
        
        # 의도 신뢰도
        confidence["intent"] = min(results["intent"][1] / 2.0, 1.0)
        
        # 전체 신뢰도
        confidence["overall"] = sum(confidence.values()) / len(confidence)
        
        return confidence

# ==================== 통합 시스템 클래스 ====================
class DongrageLawIntegratedSystem:
    """법무법인 동래 통합 AI 서비스 시스템"""
    
    def __init__(self):
        # 앞서 정의한 클래스들 통합
        self.params = DongraeLawParameters()
        self.template_gen = DongraeTemplateGenerator()
        self.advanced_extractor = AdvancedKeywordExtractor()
        
        # 법무법인 동래 특화 브랜딩 정보
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
        """사용자 질의에서 키워드 추출"""
        # 고급 키워드 추출 사용
        advanced_results = self.advanced_extractor.extract_comprehensive_keywords(user_query)
        
        extracted = {
            "practice_area": None,
            "region": None,
            "metric": None,
            "intent": None,
            "difficulty": None
        }
        
        # 추출된 결과 매핑
        if advanced_results["practice_areas"]:
            extracted["practice_area"] = advanced_results["practice_areas"][0][0]
        
        if advanced_results["regions"]:
            extracted["region"] = advanced_results["regions"][0][0]
        
        extracted["intent"] = advanced_results["intent"][0]
        extracted["difficulty"] = advanced_results["urgency"][0]
        
        # 메트릭 키워드 매칭 (기본 방식)
        for metric_category, metrics in self.params.metrics.items():
            for metric in metrics:
                if metric in user_query:
                    extracted["metric"] = metric
                    break
            if extracted["metric"]:
                break
        
        return extracted

    def generate_dongrae_prompt(self, user_query: str) -> Dict:
        """사용자 질의를 바탕으로 법무법인 동래 특화 프롬프트 생성"""
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
        
        # 4. 법무법인 동래 특화 프롬프트 생성
        dongrae_prompt = f"""
당신은 {self.brand_info['name']}의 AI 법률상담 어시스턴트입니다.

**법무법인 정보:**
- 상호: {self.brand_info['name']} ({self.brand_info['english_name']})
- 위치: {self.brand_info['location']}
- 연락처: {self.brand_info['phone']}
- 설립: {self.brand_info['established']} ({self.brand_info['experience']} 경력)
- 웹사이트: {self.brand_info['website']}

**특화 분야:** {params.get('practice_area', '종합법무')}
**서비스 지역:** {', '.join(self.brand_info['target_regions'])}
**핵심 가치:** {', '.join(self.brand_info['specialties'])}

**사용자 질의:** {user_query}
**추출된 정보:** 
- 법무분야: {params.get('practice_area', '미분류')}
- 지역: {params.get('region', '부산')}
- 관심사항: {params.get('metric', '일반상담')}
- 상담의도: {intent}
- 복잡도: {difficulty}

**응답 가이드라인:**
1. 부산·경남 지역 특성을 반영한 실무적 조언 제공
2. {self.brand_info['experience']} 경험을 바탕으로 한 전문성 어필
3. 친근하면서도 신뢰할 수 있는 톤앤매너 유지
4. 필요시 직접 상담 연결 안내: {self.brand_info['phone']}
5. 법무법인 동래만의 차별화된 서비스 강점 언급

이제 사용자의 질의에 대해 법무법인 동래의 전문성을 살려 도움이 되는 답변을 제공해주세요.
"""
        
        return {
            "prompt": dongrae_prompt,
            "extracted_keywords": extracted_keywords,
            "final_parameters": params,
            "template_used": base_template,
            "brand_info": self.brand_info
        }

    def batch_generate_samples(self, num_samples: int = 10) -> List[Dict]:
        """샘플 데이터 배치 생성"""
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
        """결과를 JSON 파일로 내보내기"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dongrae_law_samples_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(samples, f, ensure_ascii=False, indent=2)
        
        print(f"샘플 데이터가 {filename}에 저장되었습니다.")
        return filename

    def generate_template_matrix(self) -> pd.DataFrame:
        """난이도 × 의도 매트릭스 테이블 생성"""
        difficulties = ["쉬움", "보통", "어려움"]
        intents = ["정보조회", "탐색비교", "거래상담"]
        
        # 샘플 파라미터
        sample_params = {
            'practice_area': '부동산법무',
            'metric': '승소율', 
            'region': '부산',
            'time_span': '최근3년',
            'source_hint': '부산변협'
        }
        
        matrix_data = []
        for difficulty in difficulties:
            row_data = {}
            row_data['난이도'] = difficulty
            
            for intent in intents:
                template = self.template_gen.generate_template(difficulty, intent, sample_params)
                row_data[intent] = template
            
            matrix_data.append(row_data)
        
        df = pd.DataFrame(matrix_data)
        return df

    def analyze_keyword_distribution(self, queries: List[str]) -> Dict:
        """키워드 분포 분석"""
        analysis = {
            "practice_area_dist": defaultdict(int),
            "region_dist": defaultdict(int),
            "intent_dist": defaultdict(int),
            "difficulty_dist": defaultdict(int)
        }
        
        for query in queries:
            extracted = self.extract_keywords_from_query(query)
            
            if extracted["practice_area"]:
                analysis["practice_area_dist"][extracted["practice_area"]] += 1
            if extracted["region"]:
                analysis["region_dist"][extracted["region"]] += 1
            if extracted["intent"]:
                analysis["intent_dist"][extracted["intent"]] += 1
            if extracted["difficulty"]:
                analysis["difficulty_dist"][extracted["difficulty"]] += 1
        
        return analysis

# ==================== 메인 실행 부분 ====================
if __name__ == "__main__":
    print("=== 법무법인 동래 통합 AI 서비스 시스템 ===")
    
    # 시스템 초기화
    dongrae_system = DongrageLawIntegratedSystem()
    
    # 1. 파라미터 테이블 출력
    print("\n1. 파라미터 정보:")
    print(f"   - 법무 분야: {len(dongrae_system.params.practice_areas)}개")
    print(f"   - 지역: {len(dongrae_system.params.regions)}개") 
    print(f"   - 의도: {len(dongrae_system.params.intents)}개")
    print(f"   - 난이도: {len(dongrae_system.params.difficulties)}개")
    
    # 2. 템플릿 매트릭스 생성 및 출력
    print("\n2. 난이도 × 의도 템플릿 매트릭스:")
    template_matrix = dongrae_system.generate_template_matrix()
    print(template_matrix.to_string(index=False))
    
    # 3. 단일 질의 테스트
    test_query = "부산에서 교통사고 변호사 비용이 얼마나 하나요?"
    print(f"\n3. 단일 질의 테스트:")
    print(f"   질의: {test_query}")
    
    result = dongrae_system.generate_dongrae_prompt(test_query)
    print(f"   추출된 키워드: {result['extracted_keywords']}")
    print(f"   최종 파라미터: {result['final_parameters']}")
    print(f"   생성된 템플릿: {result['template_used']}")
    
    # 4. 배치 샘플 생성
    print(f"\n4. 배치 샘플 생성:")
    samples = dongrae_system.batch_generate_samples(5)
    
    print(f"   총 {len(samples)}개 샘플 생성 완료")
    for i, sample in enumerate(samples, 1):
        print(f"   [{i}] {sample['query']}")
        print(f"       -> 분야: {sample['final_parameters']['practice_area']}")
        print(f"       -> 의도: {sample['final_parameters']['intent']}")
        print(f"       -> 난이도: {sample['final_parameters']['difficulty']}")
    
    # 5. 키워드 분포 분석
    test_queries = [
        "부산에서 이혼 변호사 추천해주세요",
        "교통사고 합의금이 적정한지 궁금해요", 
        "회사 설립 절차가 복잡해서 도움이 필요합니다",
        "부동산 계약서 검토받고 싶어요",
        "노동법 위반으로 신고하고 싶습니다"
    ]
    
    print(f"\n5. 키워드 분포 분석:")
    analysis = dongrae_system.analyze_keyword_distribution(test_queries)
    
    print("   법무분야 분포:")
    for area, count in analysis["practice_area_dist"].items():
        print(f"     - {area}: {count}회")
    
    print("   의도 분포:")
    for intent, count in analysis["intent_dist"].items():
        print(f"     - {intent}: {count}회")
    
    print("   난이도 분포:")
    for difficulty, count in analysis["difficulty_dist"].items():
        print(f"     - {difficulty}: {count}회")
    
    # 6. JSON 파일 저장
    print(f"\n6. 결과 저장:")
    filename = dongrae_system.export_to_json(samples)
    
    # 7. 템플릿 매트릭스 CSV 저장
    csv_filename = f"dongrae_template_matrix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    template_matrix.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"템플릿 매트릭스가 {csv_filename}에 저장되었습니다.")
    
    print(f"\n=== 시스템 실행 완료 ===")
    print(f"생성된 파일:")
    print(f"- JSON: {filename}")
    print(f"- CSV: {csv_filename}")
    
    # 8. 사용법 안내
    print(f"\n=== 사용법 안내 ===")
    print("1. 새로운 질의 테스트:")
    print("   result = dongrae_system.generate_dongrae_prompt('새로운 질문')")
    print("\n2. 더 많은 샘플 생성:")
    print("   samples = dongrae_system.batch_generate_samples(20)")
    print("\n3. 템플릿 매트릭스 확인:")
    print("   matrix = dongrae_system.generate_template_matrix()")
    print("   print(matrix)")
    print("\n4. 키워드 분석:")
    print("   analysis = dongrae_system.analyze_keyword_distribution(queries)")
    print("   print(analysis)")
    
    # 9. 개별 기능 테스트
    print(f"\n=== 개별 기능 테스트 ===")
    
    # 파라미터 생성 테스트
    print("9-1. 랜덤 파라미터 생성:")
    for i in range(3):
        params = dongrae_system.params.get_random_parameters()
        print(f"     파라미터 세트 {i+1}: {params}")
    
    # 템플릿 조합 테스트
    print("\n9-2. 모든 템플릿 조합 생성:")
    sample_params = {
        'practice_area': '형사법무',
        'metric': '승소율',
        'region': '부산',
        'time_span': '최근3년',
        'source_hint': '부산변협'
    }
    
    all_templates = dongrae_system.template_gen.generate_all_combinations(sample_params)
    for key, template in all_templates.items():
        difficulty, intent = key.split('.')
        print(f"     [{difficulty} × {intent}] {template}")
    
    # 고급 키워드 추출 테스트
    print("\n9-3. 고급 키워드 추출 테스트:")
    test_queries_advanced = [
        "부산에서 급하게 형사변호사 필요해요",
        "계약서 검토하고 싶은데 비용이 궁금합니다",
        "노동법 관련해서 전문가 추천해주세요"
    ]
    
    for query in test_queries_advanced:
        extracted = dongrae_system.advanced_extractor.extract_comprehensive_keywords(query)
        print(f"     질의: {query}")
        print(f"     추출: {extracted}")
        print()
    
    print("=== 모든 테스트 완료 ===")
    print("\n이제 시스템이 정상적으로 작동합니다!")
    print("추가 질문이나 커스터마이징이 필요하면 언제든지 말씀하세요.")