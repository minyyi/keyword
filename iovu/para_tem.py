"""
iOVU 브랜드 파라미터 테이블 & 난이도×의도 템플릿 생성기
실행 방법: python iovu_final_system.py
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random

class IOVUParameters:
    """iOVU 브랜드 파라미터 클래스"""
    
    def __init__(self):
        # 1. practice_area (서비스 분야) - 15개
        self.practice_areas = [
            "개발자 밈 굿즈", "너디 패션", "코딩 유머 아이템", "프로그래머 라이프스타일",
            "IT 굿즈", "개발자 커뮤니티", "밈 컬렉션", "개발자 선물", "힐링 개발템",
            "깃허브 문화", "오픈소스 굿즈", "해커톤 굿즈", "스타트업 문화", "개발자 정체성 표현"
        ]
        
        # 2. metrics (4개 그룹, 총 16개)
        self.metrics = {
            "Cost": ["제품 가격", "배송비", "할인율", "멤버십 혜택"],
            "Market": ["브랜드 인지도", "개발자 커뮤니티 반응", "밈 트렌드 반영도", "바이럴 지수"],
            "Quality": ["프린팅 품질", "원단 퀄리티", "디자인 완성도", "내구성"],
            "Resource": ["재고 관리", "배송 속도", "고객 응답", "커뮤니티 참여도"]
        }
        
        # 3. countries (국가) - 9개
        self.countries = [
            "한국", "미국", "일본", "중국", "독일", "프랑스", "영국", "캐나다", "호주"
        ]
        
        # 4. time_span (기간) - 7개
        self.time_spans = [
            "2024년", "2025년", "최근 3개월", "최근 5개월", "2019-2023년", "팬데믹(2020-2022년)", "10년 추세(2015-2024년)"
        ]
        
        # 5. source_hint (정보 출처) - 4개
        self.source_hints = [
            "개발자 커뮤니티", "깃허브 트렌드", "IT 뉴스", "밈 사이트"
        ]
        
        # 6. language_ratio
        self.language_ratio = "KO 0.8 : EN 0.2"
        
        # 7. intent (의도)
        self.intents = ["정보", "탐색", "거래"]
        
        # 8. difficulty (난이도)
        self.difficulties = ["쉬움", "보통", "어려움"]

class IOVUSystemGenerator:
    """iOVU 시스템 생성기"""
    
    def __init__(self):
        self.params = IOVUParameters()
        
    def create_parameter_table(self):
        """1. 파라미터 정의 테이블 생성"""
        
        # 모든 메트릭을 하나의 리스트로 합치기
        all_metrics = []
        for category, metrics in self.params.metrics.items():
            all_metrics.extend(metrics)
        
        data = {
            '파라미터': [
                'practice_area',
                'metric',
                'country', 
                'time_span',
                'source_hint',
                'language_ratio',
                'intent',
                'difficulty'
            ],
            '값': [
                f"({len(self.params.practice_areas)})",
                f"(4개 그룹 {len(all_metrics)}개)",
                f"({len(self.params.countries)})",
                f"({len(self.params.time_spans)})",
                f"({len(self.params.source_hints)})",
                "",
                "",
                ""
            ],
            '예시 내용': [
                " · ".join(self.params.practice_areas[:5]) + " · " + 
                " · ".join(self.params.practice_areas[5:10]) + " · " + 
                " · ".join(self.params.practice_areas[10:]),
                
                f"Cost: {' · '.join(self.params.metrics['Cost'])} " +
                f"Market: {' · '.join(self.params.metrics['Market'])} " +
                f"Quality: {' · '.join(self.params.metrics['Quality'])} " +
                f"Resource: {' · '.join(self.params.metrics['Resource'])}",
                
                " · ".join(self.params.countries) + " · Global",
                " · ".join(self.params.time_spans),
                " · ".join(self.params.source_hints),
                self.params.language_ratio,
                " · ".join(self.params.intents),
                " · ".join(self.params.difficulties)
            ]
        }
        
        return pd.DataFrame(data)
    
    def generate_keyword_counts(self):
        """키워드 수 생성 (실제 분석 시뮬레이션)"""
        np.random.seed(42)  # 재현 가능한 결과
        
        # 의도별 기본 키워드 수 (현실적인 분포)
        base_counts = {
            '정보': {'쉬움': 122, '보통': 120, '어려움': 122},
            '탐색': {'쉬움': 14, '보통': 15, '어려움': 16}, 
            '거래': {'쉬움': 14, '보통': 15, '어려움': 16}
        }
        
        keyword_data = {}
        for intent, difficulties in base_counts.items():
            for difficulty, base_count in difficulties.items():
                # 약간의 변동 추가
                if intent == '정보':
                    main_count = base_count
                    sub_count = 12 if difficulty == '쉬움' else (13 if difficulty == '보통' else 11)
                else:
                    main_count = base_count
                    sub_count = 2 if difficulty == '쉬움' else (2 if difficulty == '보통' else 1)
                
                total_count = main_count + sub_count
                
                keyword_data[(intent, difficulty)] = {
                    'main': main_count,
                    'sub': sub_count,
                    'total': total_count
                }
        
        return keyword_data
    
    def create_difficulty_intent_table(self):
        """2. 난이도 × 의도 테이블 생성 (첨부 이미지 형태)"""
        
        keyword_data = self.generate_keyword_counts()
        
        data = []
        intents = ["정보", "탐색", "거래"]
        difficulties = ["쉬움", "보통", "어려움"]
        
        for intent in intents:
            for i, difficulty in enumerate(difficulties):
                kw_info = keyword_data.get((intent, difficulty), {'main': 0, 'sub': 0, 'total': 0})
                
                data.append({
                    'iOVU': 'iOVU' if i == 0 else '',
                    '정보': intent if i == 0 else '',
                    '쉬움': difficulty,
                    '122': kw_info['main'],
                    '12': kw_info['sub'],
                    '134': kw_info['total']
                })
        
        # 도메인 소계 추가
        total_main = sum(kw['main'] for kw in keyword_data.values())
        total_sub = sum(kw['sub'] for kw in keyword_data.values())
        total_sum = sum(kw['total'] for kw in keyword_data.values())
        
        data.append({
            'iOVU': '',
            '정보': '도메인 소계',
            '쉬움': '—',
            '122': total_main,
            '12': total_sub,
            '134': total_sum
        })
        
        return pd.DataFrame(data)
    
    def save_results(self):
        """결과 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. 파라미터 테이블 생성 및 저장
        param_table = self.create_parameter_table()
        param_filename = f'iovu_parameters_{timestamp}.csv'
        param_table.to_csv(param_filename, index=False, encoding='utf-8-sig')
        
        # 2. 난이도×의도 테이블 생성 및 저장  
        difficulty_table = self.create_difficulty_intent_table()
        difficulty_filename = f'iovu_difficulty_intent_{timestamp}.csv'
        difficulty_table.to_csv(difficulty_filename, index=False, encoding='utf-8-sig')
        
        return param_table, difficulty_table, param_filename, difficulty_filename

def main():
    """메인 실행 함수"""
    print("🚀 === iOVU 브랜드 분석 시스템 ===")
    print(f"📅 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 시스템 초기화
    generator = IOVUSystemGenerator()
    
    # 파라미터 정보 출력
    print("\n1️⃣ 파라미터 정의")
    print(f"   - practice_area: {len(generator.params.practice_areas)}개")
    print(f"   - metric: 4개 그룹 {sum(len(v) for v in generator.params.metrics.values())}개")
    print(f"   - country: {len(generator.params.countries)}개")
    print(f"   - time_span: {len(generator.params.time_spans)}개")
    print(f"   - source_hint: {len(generator.params.source_hints)}개")
    print(f"   - intent: {len(generator.params.intents)}개")
    print(f"   - difficulty: {len(generator.params.difficulties)}개")
    
    # 테이블 생성 및 저장
    print("\n2️⃣ 테이블 생성 및 저장 중...")
    param_table, difficulty_table, param_file, difficulty_file = generator.save_results()
    
    # 파라미터 테이블 출력
    print("\n📋 === 파라미터 정의 테이블 ===")
    print(param_table.to_string(index=False))
    
    # 난이도×의도 테이블 출력 (첨부 이미지 형태)
    print("\n📊 === 난이도 × 의도 테이블 ===")
    print(difficulty_table.to_string(index=False))
    
    # 결과 요약
    total_keywords = difficulty_table[difficulty_table['정보'] == '도메인 소계']['134'].iloc[0]
    
    print(f"\n✅ === 분석 결과 요약 ===")
    print(f"🏷️  브랜드명: iOVU")
    print(f"🎯 총 파라미터: {len(param_table)}개")
    print(f"📈 총 키워드 수: {total_keywords:,}개")
    print(f"🔄 의도별 분류: 3개 (정보, 탐색, 거래)")
    print(f"⚡ 난이도별 분류: 3개 (쉬움, 보통, 어려움)")
    
    # 의도별 키워드 분포
    print(f"\n📋 의도별 키워드 분포:")
    for intent in ["정보", "탐색", "거래"]:
        intent_total = difficulty_table[difficulty_table['정보'] == intent]['134'].sum()
        percentage = (intent_total / total_keywords) * 100
        print(f"   {intent}: {intent_total:,}개 ({percentage:.1f}%)")
    
    # 난이도별 키워드 분포
    print(f"\n⚡ 난이도별 키워드 분포:")
    for difficulty in ["쉬움", "보통", "어려움"]:
        diff_total = difficulty_table[difficulty_table['쉬움'] == difficulty]['134'].sum()
        percentage = (diff_total / total_keywords) * 100
        print(f"   {difficulty}: {diff_total:,}개 ({percentage:.1f}%)")
    
    # 저장된 파일 정보
    print(f"\n📁 === 저장된 파일 ===")
    print(f"   📄 {param_file}")
    print(f"   📄 {difficulty_file}")
    
    print(f"\n🎉 === 분석 완료 ===")
    print("iOVU 브랜드 파라미터 테이블과 난이도×의도 템플릿이 성공적으로 생성되었습니다!")

if __name__ == "__main__":
    main()