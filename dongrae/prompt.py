# 법무법인 동래 대량 프롬프트 생성기
import json
import random
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple
from itertools import product, combinations
from collections import defaultdict
import os

# 기존 시스템 클래스들 import (앞서 만든 코드가 있다고 가정)
# 여기서는 필요한 부분만 재정의

class MassivePromptGenerator:
    """법무법인 동래 대량 프롬프트 생성기"""
    
    def __init__(self):
        # 기본 시스템 초기화
        from para_tem import DongrageLawIntegratedSystem
        self.dongrae_system = DongrageLawIntegratedSystem()
        
        # 확장된 질의 템플릿들
        self.expanded_query_templates = {
            "기업법무": [
                "{region}에서 {action} 기업 설립 {detail} {urgency}",
                "스타트업 {action} {detail} 법무 서비스 {metric} {urgency}",
                "M&A {action} {detail} 전문 변호사 {metric} {region}",
                "주식회사 {action} {detail} 절차 {metric} {urgency}",
                "투자계약서 {action} {detail} 검토 {metric} {region}",
                "법인세 {action} {detail} 자문 {metric} {urgency}",
                "컴플라이언스 {action} {detail} 구축 {metric} {region}",
                "주주총회 {action} {detail} 운영 {metric} {urgency}",
                "기업분쟁 {action} {detail} 해결 {metric} {region}",
                "상장준비 {action} {detail} 법무 {metric} {urgency}"
            ],
            
            "계약법무": [
                "계약서 {action} {detail} 작성 {metric} {region}",
                "공급계약 {action} {detail} 검토 {metric} {urgency}",
                "유통계약 {action} {detail} 협상 {metric} {region}",
                "라이선스 {action} {detail} 계약 {metric} {urgency}",
                "프랜차이즈 {action} {detail} 계약 {metric} {region}",
                "고용계약 {action} {detail} 작성 {metric} {urgency}",
                "비밀유지 {action} {detail} 계약 {metric} {region}",
                "계약분쟁 {action} {detail} 해결 {metric} {urgency}",
                "국제계약 {action} {detail} 검토 {metric} {region}",
                "건설계약 {action} {detail} 자문 {metric} {urgency}"
            ],
            
            "소송및분쟁해결": [
                "민사소송 {action} {detail} 대리 {metric} {region}",
                "상사분쟁 {action} {detail} 해결 {metric} {urgency}",
                "손해배상 {action} {detail} 청구 {metric} {region}",
                "채권회수 {action} {detail} 소송 {metric} {urgency}",
                "중재절차 {action} {detail} 대리 {metric} {region}",
                "조정신청 {action} {detail} 대리 {metric} {urgency}",
                "집단소송 {action} {detail} 참여 {metric} {region}",
                "행정소송 {action} {detail} 대리 {metric} {urgency}",
                "국제중재 {action} {detail} 대리 {metric} {region}",
                "부동산분쟁 {action} {detail} 해결 {metric} {urgency}"
            ],
            
            "부동산법무": [
                "부동산 {action} {detail} 매매 {metric} {region}",
                "임대차 {action} {detail} 분쟁 {metric} {urgency}",
                "전세계약 {action} {detail} 검토 {metric} {region}",
                "건축허가 {action} {detail} 신청 {metric} {urgency}",
                "재개발 {action} {detail} 법무 {metric} {region}",
                "부동산투자 {action} {detail} 자문 {metric} {urgency}",
                "등기업무 {action} {detail} 대행 {metric} {region}",
                "소유권분쟁 {action} {detail} 해결 {metric} {urgency}",
                "부동산개발 {action} {detail} 법무 {metric} {region}",
                "상가임대 {action} {detail} 계약 {metric} {urgency}"
            ],
            
            "노동법무": [
                "부당해고 {action} {detail} 구제 {metric} {region}",
                "임금체불 {action} {detail} 해결 {metric} {urgency}",
                "근로계약 {action} {detail} 작성 {metric} {region}",
                "성희롱 {action} {detail} 대응 {metric} {urgency}",
                "산업재해 {action} {detail} 보상 {metric} {region}",
                "노동조합 {action} {detail} 교섭 {metric} {urgency}",
                "퇴직금 {action} {detail} 분쟁 {metric} {region}",
                "직장내괴롭힘 {action} {detail} 신고 {metric} {urgency}",
                "연장근무 {action} {detail} 수당 {metric} {region}",
                "4대보험 {action} {detail} 자문 {metric} {urgency}"
            ],
            
            "형사법무": [
                "교통사고 {action} {detail} 변호 {metric} {region}",
                "음주운전 {action} {detail} 변호 {metric} {urgency}",
                "폭행사건 {action} {detail} 변호 {metric} {region}",
                "사기사건 {action} {detail} 변호 {metric} {urgency}",
                "횡령사건 {action} {detail} 변호 {metric} {region}",
                "성범죄 {action} {detail} 변호 {metric} {urgency}",
                "경제범죄 {action} {detail} 변호 {metric} {region}",
                "고소고발 {action} {detail} 대리 {metric} {urgency}",
                "수사동행 {action} {detail} 서비스 {metric} {region}",
                "형사합의 {action} {detail} 중재 {metric} {urgency}"
            ],
            
            "조세법무": [
                "세무조사 {action} {detail} 대응 {metric} {region}",
                "조세불복 {action} {detail} 신청 {metric} {urgency}",
                "상속세 {action} {detail} 신고 {metric} {region}",
                "증여세 {action} {detail} 절세 {metric} {urgency}",
                "부가가치세 {action} {detail} 환급 {metric} {region}",
                "법인세 {action} {detail} 신고 {metric} {urgency}",
                "종합소득세 {action} {detail} 신고 {metric} {region}",
                "국세청협의 {action} {detail} 대리 {metric} {urgency}",
                "이전가격 {action} {detail} 자문 {metric} {region}",
                "국제조세 {action} {detail} 자문 {metric} {urgency}"
            ],
            
            "지적재산권": [
                "특허출원 {action} {detail} 대리 {metric} {region}",
                "상표등록 {action} {detail} 신청 {metric} {urgency}",
                "저작권 {action} {detail} 보호 {metric} {region}",
                "디자인등록 {action} {detail} 신청 {metric} {urgency}",
                "특허침해 {action} {detail} 소송 {metric} {region}",
                "라이선스 {action} {detail} 계약 {metric} {urgency}",
                "기술이전 {action} {detail} 계약 {metric} {region}",
                "영업비밀 {action} {detail} 보호 {metric} {urgency}",
                "브랜드보호 {action} {detail} 전략 {metric} {region}",
                "지재권분쟁 {action} {detail} 해결 {metric} {urgency}"
            ]
        }
        
        # 변수 값들
        self.template_variables = {
            "action": [
                "관련해서", "때문에", "하려고 하는데", "문제로", "필요해서",
                "하고 싶은데", "도움이 필요한", "상담받고 싶은", "의뢰하고 싶은",
                "알아보고 있는", "준비하는", "진행하는", "계획중인", "검토하는"
            ],
            "detail": [
                "전문적인", "합리적인", "신속한", "정확한", "체계적인",
                "경험있는", "믿을만한", "실무적인", "효과적인", "안전한",
                "투명한", "친절한", "꼼꼼한", "세밀한", "종합적인"
            ],
            "metric": [
                "비용이 궁금해요", "절차를 알고 싶어요", "기간이 얼마나 걸리나요",
                "성공률이 어떻게 되나요", "준비서류가 뭐가 있나요", "주의사항이 있나요",
                "장단점을 알려주세요", "경험담을 들려주세요", "추천해주세요",
                "상담받고 싶어요", "견적을 받고 싶어요", "문의드려요"
            ],
            "urgency": [
                "급해요", "빨리 해결해야 해요", "시간이 없어요", "오늘 중에 상담받고 싶어요",
                "응급상황이에요", "내일까지 필요해요", "이번 주 안에 해결해야 해요",
                "천천히 상담받고 싶어요", "계획적으로 준비하고 싶어요", "여유있게 진행하고 싶어요"
            ],
            "region": [
                "부산에서", "부산 연제구에서", "부산 해운대에서", "부산 서면에서",
                "창원에서", "김해에서", "양산에서", "울산에서", "경남에서", "부울경에서"
            ]
        }
        
        # 시나리오별 질의 패턴
        self.scenario_patterns = {
            "개인_일반": [
                "개인적으로 {practice_area} 문제가 생겼는데 도움받을 수 있나요?",
                "{practice_area} 관련해서 처음 겪는 일이라 어떻게 해야 할지 모르겠어요",
                "친구가 {practice_area} 문제를 겪고 있는데 추천해주고 싶어요",
                "가족이 {practice_area} 상황에 처했는데 상담받고 싶어요"
            ],
            "기업_임원": [
                "저희 회사에서 {practice_area} 이슈가 발생했습니다",
                "{practice_area} 관련 기업 법무 서비스가 필요합니다",
                "임원진 차원에서 {practice_area} 전략을 수립하고 있습니다",
                "회사 정책으로 {practice_area} 컴플라이언스를 강화하려고 합니다"
            ],
            "소상공인": [
                "작은 사업을 하는데 {practice_area} 문제가 생겼어요",
                "개인사업자로서 {practice_area} 관련 궁금한 점이 있어요",
                "자영업 하면서 {practice_area} 이슈를 겪고 있어요",
                "소규모 사업체에서 {practice_area} 자문이 필요해요"
            ],
            "긴급상황": [
                "지금 당장 {practice_area} 관련 응급상황이에요!",
                "오늘 중으로 {practice_area} 문제를 해결해야 해요",
                "긴급하게 {practice_area} 전문가가 필요합니다",
                "급한 {practice_area} 사안으로 즉시 상담이 필요해요"
            ],
            "비교검토": [
                "다른 로펌과 {practice_area} 서비스를 비교해보고 싶어요",
                "{practice_area} 전문 변호사들 중에서 추천해주세요",
                "여러 법무법인의 {practice_area} 비용을 알아보고 있어요",
                "{practice_area} 분야에서 평판 좋은 곳을 찾고 있어요"
            ]
        }

    def generate_comprehensive_queries(self) -> List[str]:
        """종합적인 질의 생성"""
        all_queries = []
        
        # 1. 템플릿 기반 질의 생성
        for practice_area, templates in self.expanded_query_templates.items():
            for template in templates:
                # 각 템플릿마다 3가지 변형 생성
                for _ in range(3):
                    query = template.format(
                        action=random.choice(self.template_variables["action"]),
                        detail=random.choice(self.template_variables["detail"]),
                        metric=random.choice(self.template_variables["metric"]),
                        urgency=random.choice(self.template_variables["urgency"]),
                        region=random.choice(self.template_variables["region"])
                    )
                    all_queries.append(query)
        
        # 2. 시나리오 기반 질의 생성
        for scenario, patterns in self.scenario_patterns.items():
            for pattern in patterns:
                for practice_area in self.dongrae_system.params.practice_areas:
                    query = pattern.format(practice_area=practice_area)
                    all_queries.append(query)
        
        # 3. 실제 상황 기반 질의 생성
        realistic_queries = [
            "부산에서 교통사고 났는데 상대방이 합의를 거부해요",
            "이혼하려는데 재산분할과 양육권이 걱정돼요",
            "회사에서 갑자기 해고통보를 받았어요",
            "임대인이 보증금을 돌려주지 않아요",
            "사업파트너가 돈을 가지고 잠적했어요",
            "세무서에서 조사하겠다고 연락이 왔어요",
            "특허 침해로 소송을 당했어요",
            "건축업체가 공사를 제대로 하지 않아요",
            "직장에서 성희롱을 당했어요",
            "상속받은 부동산 때문에 형제들과 분쟁이 생겼어요",
            "회사 설립하려는데 절차가 복잡해요",
            "개인정보가 유출되어서 피해를 봤어요",
            "음주운전으로 단속되었는데 면허정지가 걱정돼요",
            "온라인 쇼핑몰 창업하려는데 약관 작성이 필요해요",
            "근로자가 산업재해를 당했어요",
            "상표를 등록하려는데 기존 상표와 유사해요",
            "계약서를 작성했는데 불리한 조항이 있는 것 같아요",
            "부동산 투자하려는데 법적 검토가 필요해요",
            "직원이 회사 기밀을 유출했어요",
            "프랜차이즈 계약을 체결하려는데 조건을 검토해주세요",
            # 부산 지역 특화 질의들
            "해운대 아파트 매매계약 체결 전에 검토받고 싶어요",
            "부산항 물류업체와 계약 분쟁이 생겼어요",
            "서면 상가임대 계약 갱신을 거부당했어요",
            "동래온천 관광업 관련 허가 문제가 있어요",
            "광안리 펜션 운영 중 민원이 발생했어요",
            "부산 조선업체에서 근무하다가 해고됐어요",
            "기장군 농지 전용허가를 받고 싶어요",
            "사하구 공장 설립 관련 환경평가가 필요해요",
            "영도구 재개발 관련 보상 문제가 있어요",
            "연제구 병원 개설 허가를 받고 싶어요"
        ]
        
        all_queries.extend(realistic_queries)
        
        # 4. 난이도별 전문 질의 생성
        expert_queries = [
            # 고난이도 질의들
            "복합적인 M&A 거래에서 실사(Due Diligence) 과정의 법적 리스크를 평가해주세요",
            "국제계약에서 CISG 적용 배제 조항과 준거법 선택의 유효성을 검토해주세요",
            "스톡옵션 부여 시 세무상 이슈와 노동법상 제약사항을 종합 분석해주세요",
            "GDPR과 개인정보보호법의 충돌 시 해결방안을 제시해주세요",
            "크로스보더 중재절차에서 한국법원의 관할권 문제를 검토해주세요",
            # 중간 난이도 질의들
            "부동산 매매계약의 특약사항이 법적으로 유효한지 확인해주세요",
            "근로계약서의 경업금지 조항이 과도한지 판단해주세요",
            "스타트업 투자계약서의 희석방지 조항을 설명해주세요",
            "상표권 침해 여부를 판단하는 기준을 알려주세요",
            "세무조사 시 납세자의 권리와 의무를 설명해주세요"
        ]
        
        all_queries.extend(expert_queries)
        
        return list(set(all_queries))  # 중복 제거

    def generate_massive_prompts(self, num_prompts: int = 1000) -> List[Dict]:
        """대량 프롬프트 생성"""
        print(f"=== {num_prompts}개 프롬프트 대량 생성 시작 ===")
        
        # 모든 질의 생성
        all_queries = self.generate_comprehensive_queries()
        print(f"기본 질의 {len(all_queries)}개 생성 완료")
        
        # 추가 질의 생성 (목표 개수까지)
        additional_needed = max(0, num_prompts - len(all_queries))
        if additional_needed > 0:
            print(f"추가 질의 {additional_needed}개 생성 중...")
            
            # 기존 질의를 변형해서 추가 생성
            for _ in range(additional_needed):
                base_query = random.choice(all_queries)
                
                # 랜덤하게 변형 요소 추가
                variations = [
                    f"급하게 {base_query}",
                    f"비용을 최소화해서 {base_query}",
                    f"전문적으로 {base_query}",
                    f"신속하게 {base_query}",
                    f"정확하게 {base_query}",
                    f"안전하게 {base_query}",
                    f"체계적으로 {base_query}",
                    f"경험 많은 변호사에게 {base_query}",
                    f"부산 지역 전문가에게 {base_query}",
                    f"법무법인 동래에서 {base_query}"
                ]
                
                variation = random.choice(variations)
                all_queries.append(variation)
        
        # 프롬프트 생성
        prompts = []
        selected_queries = all_queries[:num_prompts]
        
        print(f"선택된 {len(selected_queries)}개 질의로 프롬프트 생성 중...")
        
        for i, query in enumerate(selected_queries):
            if i % 100 == 0:
                print(f"진행률: {i}/{len(selected_queries)} ({i/len(selected_queries)*100:.1f}%)")
            
            try:
                result = self.dongrae_system.generate_dongrae_prompt(query)
                result["sample_id"] = f"dongrae_massive_{i+1:04d}"
                result["query"] = query
                result["generation_timestamp"] = datetime.now().isoformat()
                prompts.append(result)
            except Exception as e:
                print(f"질의 처리 오류 (인덱스 {i}): {str(e)}")
                continue
        
        print(f"=== 총 {len(prompts)}개 프롬프트 생성 완료 ===")
        return prompts

    def analyze_massive_results(self, prompts: List[Dict]) -> Dict:
        """대량 생성 결과 분석"""
        analysis = {
            "total_count": len(prompts),
            "practice_area_distribution": defaultdict(int),
            "region_distribution": defaultdict(int),
            "intent_distribution": defaultdict(int),
            "difficulty_distribution": defaultdict(int),
            "metric_distribution": defaultdict(int),
            "query_length_stats": {
                "min": float('inf'),
                "max": 0,
                "avg": 0,
                "lengths": []
            },
            "template_diversity": defaultdict(int)
        }
        
        for prompt in prompts:
            params = prompt["final_parameters"]
            query = prompt["query"]
            
            # 분포 분석
            analysis["practice_area_distribution"][params.get("practice_area", "미분류")] += 1
            analysis["region_distribution"][params.get("region", "미분류")] += 1
            analysis["intent_distribution"][params.get("intent", "미분류")] += 1
            analysis["difficulty_distribution"][params.get("difficulty", "미분류")] += 1
            analysis["metric_distribution"][params.get("metric", "미분류")] += 1
            
            # 길이 통계
            query_len = len(query)
            analysis["query_length_stats"]["lengths"].append(query_len)
            analysis["query_length_stats"]["min"] = min(analysis["query_length_stats"]["min"], query_len)
            analysis["query_length_stats"]["max"] = max(analysis["query_length_stats"]["max"], query_len)
            
            # 템플릿 다양성
            template = prompt["template_used"][:50] + "..."  # 앞 50자만
            analysis["template_diversity"][template] += 1
        
        # 평균 길이 계산
        if analysis["query_length_stats"]["lengths"]:
            analysis["query_length_stats"]["avg"] = sum(analysis["query_length_stats"]["lengths"]) / len(analysis["query_length_stats"]["lengths"])
        
        return analysis

    def export_massive_results(self, prompts: List[Dict], analysis: Dict) -> Dict:
        """대량 생성 결과 내보내기"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. 전체 프롬프트 JSON 저장
        json_filename = f"dongrae_massive_prompts_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, ensure_ascii=False, indent=2)
        
        # 2. 분석 결과 JSON 저장
        analysis_filename = f"dongrae_analysis_{timestamp}.json"
        with open(analysis_filename, 'w', encoding='utf-8') as f:
            # defaultdict을 일반 dict으로 변환
            analysis_dict = {}
            for key, value in analysis.items():
                if isinstance(value, defaultdict):
                    analysis_dict[key] = dict(value)
                else:
                    analysis_dict[key] = value
            json.dump(analysis_dict, f, ensure_ascii=False, indent=2)
        
        # 3. 질의만 추출해서 텍스트 파일로 저장
        queries_filename = f"dongrae_queries_{timestamp}.txt"
        with open(queries_filename, 'w', encoding='utf-8') as f:
            for i, prompt in enumerate(prompts, 1):
                f.write(f"{i:04d}. {prompt['query']}\n")
        
        # 4. 프롬프트만 추출해서 텍스트 파일로 저장
        prompts_filename = f"dongrae_prompts_only_{timestamp}.txt"
        with open(prompts_filename, 'w', encoding='utf-8') as f:
            for i, prompt in enumerate(prompts, 1):
                f.write(f"=== 프롬프트 {i:04d} ===\n")
                f.write(f"질의: {prompt['query']}\n")
                f.write(f"프롬프트:\n{prompt['prompt']}\n")
                f.write("\n" + "="*50 + "\n\n")
        
        # 5. 분석 결과 요약 CSV 저장
        summary_data = []
        
        # 법무분야별 통계
        for area, count in analysis["practice_area_distribution"].items():
            summary_data.append({
                "카테고리": "법무분야",
                "항목": area,
                "개수": count,
                "비율": f"{count/analysis['total_count']*100:.1f}%"
            })
        
        # 지역별 통계
        for region, count in analysis["region_distribution"].items():
            summary_data.append({
                "카테고리": "지역",
                "항목": region,
                "개수": count,
                "비율": f"{count/analysis['total_count']*100:.1f}%"
            })
        
        # 의도별 통계
        for intent, count in analysis["intent_distribution"].items():
            summary_data.append({
                "카테고리": "의도",
                "항목": intent,
                "개수": count,
                "비율": f"{count/analysis['total_count']*100:.1f}%"
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_csv = f"dongrae_summary_{timestamp}.csv"
        summary_df.to_csv(summary_csv, index=False, encoding='utf-8-sig')
        
        print(f"\n=== 파일 저장 완료 ===")
        print(f"1. 전체 프롬프트: {json_filename}")
        print(f"2. 분석 결과: {analysis_filename}")
        print(f"3. 질의 목록: {queries_filename}")
        print(f"4. 프롬프트 모음: {prompts_filename}")
        print(f"5. 요약 통계: {summary_csv}")
        
        return {
            "json_file": json_filename,
            "analysis_file": analysis_filename,
            "queries_file": queries_filename,
            "prompts_file": prompts_filename,
            "summary_file": summary_csv
        }

# 실행 함수
# 실행 함수
def run_massive_generation(num_prompts: int = 1000):
    """대량 프롬프트 생성 실행"""
    print("=" * 60)
    print("법무법인 동래 대량 프롬프트 생성기 시작")
    print("=" * 60)
    
    # 생성기 초기화
    generator = MassivePromptGenerator()
    
    # 대량 프롬프트 생성
    prompts = generator.generate_massive_prompts(num_prompts)
    
    # 결과 분석
    print("\n분석 중...")
    analysis = generator.analyze_massive_results(prompts)
    
    # 분석 결과 출력
    print(f"\n=== 생성 결과 분석 ===")
    print(f"총 생성 개수: {analysis['total_count']:,}개")
    print(f"질의 길이: 최소 {analysis['query_length_stats']['min']}자, 최대 {analysis['query_length_stats']['max']}자, 평균 {analysis['query_length_stats']['avg']:.1f}자")
    
    print(f"\n📊 법무분야 분포:")
    for area, count in sorted(analysis["practice_area_distribution"].items(), key=lambda x: x[1], reverse=True):
        percentage = count / analysis['total_count'] * 100
        print(f"  {area}: {count}개 ({percentage:.1f}%)")
    
    print(f"\n🗺️ 지역 분포:")
    for region, count in sorted(analysis["region_distribution"].items(), key=lambda x: x[1], reverse=True):
        percentage = count / analysis['total_count'] * 100
        print(f"  {region}: {count}개 ({percentage:.1f}%)")
    
    print(f"\n🎯 의도 분포:")
    for intent, count in sorted(analysis["intent_distribution"].items(), key=lambda x: x[1], reverse=True):
        percentage = count / analysis['total_count'] * 100
        print(f"  {intent}: {count}개 ({percentage:.1f}%)")
    
    print(f"\n⚡ 난이도 분포:")
    for difficulty, count in sorted(analysis["difficulty_distribution"].items(), key=lambda x: x[1], reverse=True):
        percentage = count / analysis['total_count'] * 100
        print(f"  {difficulty}: {count}개 ({percentage:.1f}%)")
    
    # 샘플 프롬프트 출력
    print(f"\n=== 샘플 프롬프트 (상위 5개) ===")
    for i, prompt in enumerate(prompts[:5], 1):
        print(f"\n[샘플 {i}]")
        print(f"질의: {prompt['query']}")
        print(f"분야: {prompt['final_parameters']['practice_area']}")
        print(f"지역: {prompt['final_parameters']['region']}")
        print(f"의도: {prompt['final_parameters']['intent']}")
        print(f"난이도: {prompt['final_parameters']['difficulty']}")
        print("-" * 40)
    
    # 파일 저장
    files = generator.export_massive_results(prompts, analysis)
    
    # 추가 통계 정보
    print(f"\n=== 품질 지표 ===")
    print(f"템플릿 다양성: {len(analysis['template_diversity'])}개 고유 템플릿")
    print(f"평균 프롬프트 길이: {sum(len(p['prompt']) for p in prompts) // len(prompts):,}자")
    
    # 지역별 법무분야 교차 분석
    print(f"\n=== 지역 × 법무분야 교차 분석 (상위 10개) ===")
    cross_analysis = defaultdict(int)
    for prompt in prompts:
        params = prompt['final_parameters']
        key = f"{params.get('region', '미분류')} × {params.get('practice_area', '미분류')}"
        cross_analysis[key] += 1
    
    for combo, count in sorted(cross_analysis.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {combo}: {count}개")
    
    print(f"\n=== 활용 가이드 ===")
    print("1. 🤖 AI 모델 훈련용:")
    print(f"   - {files['json_file']} 파일을 AI 훈련 데이터로 활용")
    print("   - 질의-응답 쌍으로 구성되어 fine-tuning 가능")
    
    print("\n2. 📊 서비스 기획용:")
    print(f"   - {files['summary_file']} 파일로 고객 니즈 분석")
    print("   - 지역별, 분야별 수요 예측 가능")
    
    print("\n3. 🔍 키워드 분석용:")
    print(f"   - {files['queries_file']} 파일로 검색 키워드 최적화")
    print("   - SEO 및 마케팅 전략 수립")
    
    print("\n4. ✍️ 콘텐츠 제작용:")
    print(f"   - {files['prompts_file']} 파일로 FAQ, 블로그 소재 확보")
    print("   - 고객 상담 매뉴얼 작성")
    
    return {
        "prompts": prompts,
        "analysis": analysis,
        "files": files
    }

# 추가 유틸리티 함수들
def generate_specific_category_prompts(category: str, num_prompts: int = 100):
    """특정 카테고리 프롬프트 집중 생성"""
    generator = MassivePromptGenerator()
    
    if category not in generator.dongrae_system.params.practice_areas:
        print(f"오류: '{category}'는 유효한 법무분야가 아닙니다.")
        print(f"사용 가능한 분야: {generator.dongrae_system.params.practice_areas}")
        return None
    
    print(f"=== {category} 특화 프롬프트 {num_prompts}개 생성 ===")
    
    # 해당 카테고리 템플릿만 사용
    category_templates = generator.expanded_query_templates.get(category, [])
    if not category_templates:
        print(f"'{category}' 카테고리의 템플릿이 없습니다.")
        return None
    
    category_queries = []
    
    # 템플릿 기반 생성
    for _ in range(num_prompts):
        template = random.choice(category_templates)
        query = template.format(
            action=random.choice(generator.template_variables["action"]),
            detail=random.choice(generator.template_variables["detail"]),
            metric=random.choice(generator.template_variables["metric"]),
            urgency=random.choice(generator.template_variables["urgency"]),
            region=random.choice(generator.template_variables["region"])
        )
        category_queries.append(query)
    
    # 프롬프트 생성
    prompts = []
    for i, query in enumerate(category_queries):
        result = generator.dongrae_system.generate_dongrae_prompt(query)
        result["sample_id"] = f"dongrae_{category}_{i+1:03d}"
        result["query"] = query
        prompts.append(result)
    
    # 파일 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dongrae_{category}_prompts_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)
    
    print(f"{category} 특화 프롬프트 {len(prompts)}개 생성 완료")
    print(f"파일 저장: {filename}")
    
    return prompts

def generate_difficulty_prompts(difficulty: str, num_prompts: int = 100):
    """특정 난이도 프롬프트 집중 생성"""
    generator = MassivePromptGenerator()
    
    if difficulty not in ["쉬움", "보통", "어려움"]:
        print("오류: 난이도는 '쉬움', '보통', '어려움' 중 하나여야 합니다.")
        return None
    
    print(f"=== '{difficulty}' 난이도 프롬프트 {num_prompts}개 생성 ===")
    
    # 난이도별 특화 질의 패턴
    difficulty_patterns = {
        "쉬움": [
            "{practice_area} 관련해서 {metric}",
            "{region}에서 {practice_area} {action}",
            "{practice_area} {detail} 서비스 {metric}"
        ],
        "보통": [
            "{time_span} 기준으로 {region} {practice_area} {metric} {source_hint} 자료",
            "{practice_area} 분야에서 {detail} {metric} 비교분석",
            "{region} 지역 {practice_area} 전문가 {metric} 검토"
        ],
        "어려움": [
            "{source_hint} 데이터 기반 {time_span} {region} {practice_area} 시장 {metric} 종합분석",
            "복합적 {practice_area} 사안의 {metric} 전략적 접근과 {source_hint} 연계 검토",
            "{time_span} 동안 {region} {practice_area} 분야 {metric} 경쟁력 진단 및 개선방안"
        ]
    }
    
    patterns = difficulty_patterns[difficulty]
    queries = []
    
    for _ in range(num_prompts):
        pattern = random.choice(patterns)
        
        # 파라미터 강제 설정
        params = generator.dongrae_system.params.get_random_parameters()
        params["difficulty"] = difficulty
        
        query = pattern.format(
            practice_area=params["practice_area"],
            region=params["region"],
            metric=params["metric"],
            time_span=params.get("time_span", "최근3년"),
            source_hint=params.get("source_hint", "대한변협"),
            action=random.choice(generator.template_variables["action"]),
            detail=random.choice(generator.template_variables["detail"])
        )
        queries.append(query)
    
    # 프롬프트 생성
    prompts = []
    for i, query in enumerate(queries):
        result = generator.dongrae_system.generate_dongrae_prompt(query)
        # 난이도 강제 설정
        result["final_parameters"]["difficulty"] = difficulty
        result["sample_id"] = f"dongrae_{difficulty}_{i+1:03d}"
        result["query"] = query
        prompts.append(result)
    
    # 파일 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dongrae_{difficulty}_difficulty_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)
    
    print(f"'{difficulty}' 난이도 프롬프트 {len(prompts)}개 생성 완료")
    print(f"파일 저장: {filename}")
    
    return prompts

# 메인 실행 코드
if __name__ == "__main__":
    print("🚀 법무법인 동래 대량 프롬프트 생성기를 시작합니다!")
    print("\n선택하세요:")
    print("1. 대량 프롬프트 생성 (기본 1000개)")
    print("2. 대량 프롬프트 생성 (사용자 지정 개수)")
    print("3. 특정 법무분야 집중 생성")
    print("4. 특정 난이도 집중 생성")
    print("5. 모든 옵션 자동 실행")
    
    choice = input("\n번호를 입력하세요 (1-5): ").strip()
    
    if choice == "1":
        # 기본 1000개 생성
        result = run_massive_generation(1000)
        
    elif choice == "2":
        # 사용자 지정 개수
        try:
            num = int(input("생성할 프롬프트 개수를 입력하세요: "))
            result = run_massive_generation(num)
        except ValueError:
            print("잘못된 숫자입니다. 기본값 1000개로 실행합니다.")
            result = run_massive_generation(1000)
            
    elif choice == "3":
        # 특정 분야 집중
        print("\n사용 가능한 법무분야:")
        generator = MassivePromptGenerator()
        for i, area in enumerate(generator.dongrae_system.params.practice_areas, 1):
            print(f"  {i}. {area}")
        
        try:
            area_idx = int(input("\n법무분야 번호를 선택하세요: ")) - 1
            area = generator.dongrae_system.params.practice_areas[area_idx]
            num = int(input("생성할 프롬프트 개수를 입력하세요: "))
            result = generate_specific_category_prompts(area, num)
        except (ValueError, IndexError):
            print("잘못된 입력입니다.")
            
    elif choice == "4":
        # 특정 난이도 집중
        print("\n사용 가능한 난이도:")
        print("  1. 쉬움")
        print("  2. 보통") 
        print("  3. 어려움")
        
        try:
            diff_choice = int(input("\n난이도 번호를 선택하세요: "))
            difficulties = ["쉬움", "보통", "어려움"]
            difficulty = difficulties[diff_choice - 1]
            num = int(input("생성할 프롬프트 개수를 입력하세요: "))
            result = generate_difficulty_prompts(difficulty, num)
        except (ValueError, IndexError):
            print("잘못된 입력입니다.")
            
    elif choice == "5":
        # 모든 옵션 자동 실행
        print("🎯 모든 옵션 자동 실행 시작!")
        
        # 1. 대량 생성 (500개)
        print("\n1️⃣ 대량 프롬프트 생성 (500개)")
        run_massive_generation(500)
        
        # 2. 주요 분야별 생성 (각 50개)
        major_areas = ["기업법무", "부동산법무", "형사법무", "노동법무", "계약법무"]
        for area in major_areas:
            print(f"\n2️⃣ {area} 특화 생성 (50개)")
            generate_specific_category_prompts(area, 50)
        
        # 3. 난이도별 생성 (각 30개)
        for difficulty in ["쉬움", "보통", "어려움"]:
            print(f"\n3️⃣ '{difficulty}' 난이도 생성 (30개)")
            generate_difficulty_prompts(difficulty, 30)
        
        print("\n🎉 모든 옵션 실행 완료!")
        print("총 생성량: 대량 500개 + 분야별 250개 + 난이도별 90개 = 840개")
        
    else:
        print("잘못된 선택입니다. 기본 실행합니다.")
        result = run_massive_generation(1000)
    
    print("\n✅ 프롬프트 생성이 완료되었습니다!")
    print("생성된 파일들을 확인해보세요.")
    print("\n📁 파일 활용법:")
    print("- JSON 파일: AI 훈련/API 연동용")
    print("- TXT 파일: 사람이 읽기 쉬운 형태")
    print("- CSV 파일: 엑셀에서 분석 가능")