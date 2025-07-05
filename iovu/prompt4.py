"""
iOVU 개발자 밈 굿즈 브랜드 프롬프트 생성기 (단순화 버전)
실행 방법: python iovu_simple_generator.py
"""

import pandas as pd
import numpy as np
import random
import csv
import os
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class IOVUParameters:
    """iOVU 브랜드 파라미터 정의"""
    
    def __init__(self):
        # 1. practice_area (서비스 분야) - 14개
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
            "2024년", "2025년", "최근 3개월", "최근 5개월", "2019-2023년", 
            "팬데믹(2020-2022년)", "10년 추세(2015-2024년)"
        ]
        
        # 5. source_hint (정보 출처) - 4개
        self.source_hints = [
            "개발자 커뮤니티", "깃허브 트렌드", "IT 뉴스", "밈 사이트"
        ]
        
        # 6. language_ratio
        self.language_ratio = "KO 0.8 : EN 0.2"
        
        # 7. intent (의도) - 3개
        self.intents = ["정보", "탐색", "거래"]
        
        # 8. difficulty (난이도) - 3개  
        self.difficulties = ["쉬움", "보통", "어려움"]

class IOVUKeywordBank:
    """iOVU 브랜드 키워드 뱅크"""
    
    def __init__(self):
        # 핵심 제품 속성
        self.core_attributes = [
            "티셔츠", "후드티", "후드집업", "에코백", "머그컵", "노트북스티커", 
            "키링", "마우스패드", "파우치", "볼펜", "스마트톡", "폰케이스",
            "M사이즈", "L사이즈", "XL사이즈", "블랙", "화이트", "네이비", "그레이",
            "코튼", "폴리에스터", "캔버스", "아크릴"
        ]
        
        # 프린팅 기술
        self.printing_tech = [
            "DTG 프린팅", "실크스크린", "다중색 프린팅", "승화전사", 
            "비닐 커팅", "자수", "UV 프린팅", "열전사"
        ]
        
        # 브랜드 슬로건
        self.slogans = [
            "IN OUR VIVID UNIVERSE", "Nerdy is the new cool", 
            "Dev + Cute = iOVU", "밈도 입는 시대", "코드를 입다",
            "Debug & Chill", "개발자를 위한 귀여운 반란", 
            "Code with Love", "힐링하는 코더", "Meme Lover"
        ]
        
        # 밈 & 무드 키워드
        self.meme_mood = [
            "개발자 밈", "코딩 유머", "동물×코딩", "너디 감성", "힐링템",
            "위트 있는", "개발자 고민", "코드 리뷰", "버그 수정", "스택오버플로우",
            "깃허브", "커밋", "푸시", "풀리퀘스트", "머지", "브랜치", 
            "리팩토링", "디버깅", "테스트", "배포", "404 에러", "NullPointer",
            "Hello World", "변수명 고민", "주석 없는 코드", "야근", "카페인"
        ]
        
        # 커뮤니티 키워드  
        self.community = [
            "GitHub 스타", "오픈소스 기여", "해커톤 참가", "스터디 모임",
            "Slack 워크스페이스", "Discord 서버", "개발자 컨퍼런스", 
            "코딩 부트캠프", "테크 밋업", "백엔드 개발자", "프론트엔드 개발자",
            "풀스택 개발자", "데브옵스", "AI/ML 엔지니어", "데이터 사이언티스트",
            "스타트업", "대기업", "IT 업계", "개발팀", "CTO", "테크리드"
        ]
        


class IOVUPromptGenerator:
    """iOVU 프롬프트 생성기"""
    
    def __init__(self):
        self.params = IOVUParameters()
        self.keywords = IOVUKeywordBank()
        self.generated_prompts = []
        
    def _create_prompt_template(self, intent: str, difficulty: str) -> str:
        """의도와 난이도에 따른 프롬프트 템플릿 생성"""
        
        templates = {
            # 정보 의도
            ("정보", "쉬움"): [
                "iOVU {slogan} 슬로건 의미가 뭐야?",
                "iOVU {product} {tech} 프린팅 방식 설명해줘.",
                "{meme} iOVU 굿즈 종류 뭐가 있어?",
                "iOVU {product} {size} 사이즈 특징이 뭐야?",
                "{community} 개발자들이 선호하는 iOVU 제품은?"
            ],
            ("정보", "보통"): [
                "iOVU {product} {tech} 제작 시 품질 관리 방법은?",
                "{community} 개발자들의 iOVU {product} 선호 스타일 비교해줘.",
                "iOVU {meme} 컨셉과 다른 브랜드의 차이점은?",
                "iOVU {slogan} 메시지가 {target}에게 주는 의미는?",
                "{tech} 프린팅의 iOVU 제품 품질 차이 설명해줘."
            ],
            ("정보", "어려움"): [
                "iOVU {meme} 전략의 브랜딩 효과를 정량적으로 분석해줘.",
                "{community} 트렌드가 iOVU 제품 기획에 미치는 영향을 데이터로 검증해줘.",
                "iOVU {slogan} 메시지의 {target} 타겟 가치 전달을 비판적으로 평가해줘.",
                "iOVU {meme} 마케팅의 개발자 커뮤니티 브랜딩 장기 효과를 모델링해줘.",
                "{metric} 기준 iOVU 브랜드 시장 포지셔닝을 전략적으로 분석해줘."
            ],
            
            # 탐색 의도  
            ("탐색", "쉬움"): [
                "iOVU {product} 구매 페이지 주소 알려줘.",
                "iOVU 공식 GitHub 리포지토리 링크는?",
                "{community} iOVU 커뮤니티 초대 링크 있어?",
                "iOVU {meme} 시리즈 제품 카탈로그 어디서 봐?",
                "iOVU 고객센터 연락처 알려줘."
            ],
            ("탐색", "보통"): [
                "iOVU {meme} 시리즈 제품 카탈로그 페이지 찾아줘.",
                "{community} 이벤트 관련 iOVU 공지사항 링크는?",
                "iOVU 커스텀 제작 견적 요청 폼 위치는?",
                "iOVU {tech} 프린팅 옵션별 제품 포트폴리오 페이지는?",
                "{target} 대상 iOVU 제품 추천 가이드 찾아줘."
            ],
            ("탐색", "어려움"): [
                "iOVU {community} 프로젝트 오픈소스 기여 가이드 문서 위치는?",
                "{tech} 프린팅 기술별 iOVU 제품 포트폴리오 문서 찾아줘.",
                "iOVU API 연동 {community} 자동화 솔루션 개발 가이드는?",
                "iOVU 브랜드 파트너십 {community} 협업 제안서 템플릿 위치는?",
                "{metric} 성과 측정용 iOVU 마케팅 대시보드 접근 방법은?"
            ],
            
            # 거래 의도
            ("거래", "쉬움"): [
                "iOVU {product} {size} 사이즈 지금 주문 가능해?",
                "{meme} 디자인 {product} 배송비 포함 총 가격은?",
                "iOVU {community} 이벤트 할인 코드 적용 방법은?",
                "iOVU {product} 반품 정책과 교환 절차는?",
                "{tech} 프린팅 iOVU {product} 주문 시 추가 비용은?"
            ],
            ("거래", "보통"): [
                "iOVU 팀티 대량 주문과 소량 주문 단가 비교해줘.",
                "{community} 단체용 {product} 커스터마이징 옵션과 비용은?",
                "iOVU {tech} 프린팅 옵션별 가격 차이와 배송 기간은?",
                "iOVU {meme} 시리즈와 일반 제품의 가격 정책 차이는?",
                "{target} 대상 iOVU 제품 구독 서비스 요금제 비교해줘."
            ],
            ("거래", "어려움"): [
                "{community} 기념 {product} 100장 주문 시 가격-마진 모델 만들어줘.",
                "iOVU 연간 구독과 단발 구매의 ROI를 {metric} 기준으로 계산해줘.",
                "{target} 세그먼트 iOVU 마케팅 캠페인 예산 배분과 전환율 모델링해줘.",
                "iOVU {tech} 프린팅 대량 주문 시 원가 구조와 최적 발주량 분석해줘.",
                "{community} 파트너십 iOVU 제품 유통 채널별 수익성 시뮬레이션해줘."
            ]
        }
        
        template_list = templates.get((intent, difficulty), templates[("정보", "쉬움")])
        return random.choice(template_list)
    
    def _fill_template(self, template: str, context: Dict[str, Any]) -> str:
        """템플릿에 키워드를 채워넣어 완성된 프롬프트 생성"""
        
        # 키워드 선택
        keywords = {
            'product': random.choice(self.keywords.core_attributes),
            'tech': random.choice(self.keywords.printing_tech),
            'slogan': random.choice(self.keywords.slogans),
            'meme': random.choice(self.keywords.meme_mood),
            'community': random.choice(self.keywords.community),
            'size': random.choice(['M', 'L', 'XL']),
            'target': random.choice(['개발자', '20-30대', '스타트업 직원', 'IT 업계 종사자']),
            'metric': random.choice([m for metrics in self.params.metrics.values() for m in metrics])
        }
        
        # 템플릿 치환
        try:
            filled_prompt = template.format(**keywords)
            return filled_prompt
        except KeyError as e:
            # 템플릿에 없는 키워드가 있으면 기본 프롬프트 반환
            return f"iOVU {keywords['product']}에 대해 알려줘."
    
    def generate_single_prompt(self, intent: str = None, difficulty: str = None) -> Dict[str, Any]:
        """단일 프롬프트 생성"""
        
        # 랜덤 선택 (파라미터가 없는 경우)
        if not intent:
            intent = random.choice(self.params.intents)
        if not difficulty:
            difficulty = random.choice(self.params.difficulties)
            
        # 템플릿 선택 및 프롬프트 생성
        template = self._create_prompt_template(intent, difficulty)
        context = {
            'intent': intent,
            'difficulty': difficulty,
            'practice_area': random.choice(self.params.practice_areas),
            'country': random.choice(self.params.countries),
            'time_span': random.choice(self.params.time_spans),
            'source_hint': random.choice(self.params.source_hints)
        }
        
        prompt_text = self._fill_template(template, context)
        
        # 언어 결정 (KO 80%, EN 20%)
        language = "KO" if random.random() < 0.8 else "EN"
        
        # 영어 번역 (간단한 예시)
        if language == "EN":
            prompt_text = self._translate_to_english(prompt_text)
        
        prompt_data = {
            'id': f"iovu_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000,9999)}",
            'prompt': prompt_text,
            'intent': intent,
            'difficulty': difficulty,
            'language': language,
            'domain': 'iOVU',
            'practice_area': context['practice_area'],
            'country': context['country'],
            'time_span': context['time_span'],
            'source_hint': context['source_hint'],
            'created_at': datetime.now().isoformat()
        }
        
        return prompt_data
    
    def _translate_to_english(self, korean_text: str) -> str:
        """간단한 영어 번역"""
        simple_translations = {
            "iOVU": "iOVU",
            "티셔츠": "t-shirt",
            "후드티": "hoodie", 
            "에코백": "eco bag",
            "머그컵": "mug",
            "스티커": "sticker",
            "주문": "order",
            "배송": "shipping",
            "가격": "price",
            "할인": "discount",
            "알려줘": "tell me about",
            "설명해줘": "explain",
            "비교해줘": "compare",
            "분석해줘": "analyze"
        }
        
        # 간단한 치환
        for ko, en in simple_translations.items():
            korean_text = korean_text.replace(ko, en)
            
        return korean_text
    
    def generate_batch_prompts(self, count: int = 100) -> List[Dict[str, Any]]:
        """배치 프롬프트 생성"""
        
        prompts = []
        
        # 의도별, 난이도별 분포 (3x3 = 9개 조합)
        combinations = [
            (intent, difficulty) 
            for intent in self.params.intents 
            for difficulty in self.params.difficulties
        ]
        
        # 각 조합별로 고르게 분배
        prompts_per_combo = count // len(combinations)
        remaining = count % len(combinations)
        
        for i, (intent, difficulty) in enumerate(combinations):
            # 기본 개수 + 나머지 분배
            combo_count = prompts_per_combo + (1 if i < remaining else 0)
            
            for _ in range(combo_count):
                prompt_data = self.generate_single_prompt(intent, difficulty)
                prompts.append(prompt_data)
        
        self.generated_prompts.extend(prompts)
        return prompts
    
    def save_to_csv(self, prompts: List[Dict[str, Any]], filename: str = None) -> str:
        """CSV 파일로 저장"""
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'iovu_prompts_{timestamp}.csv'
        
        # CSV 헤더
        fieldnames = [
            'id', 'prompt', 'intent', 'difficulty', 'language', 'domain',
            'practice_area', 'country', 'time_span', 'source_hint', 'created_at'
        ]
        
        # CSV 저장
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for prompt in prompts:
                writer.writerow(prompt)
        
        print(f"✅ {len(prompts)}개 프롬프트가 '{filename}' 파일로 저장되었습니다.")
        return filename
    
    def get_generation_stats(self, prompts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """생성 통계 반환"""
        
        stats = {
            'total_count': len(prompts),
            'by_intent': {},
            'by_difficulty': {},
            'by_language': {},
            'by_practice_area': {}
        }
        
        for prompt in prompts:
            # 의도별 통계
            intent = prompt['intent']
            stats['by_intent'][intent] = stats['by_intent'].get(intent, 0) + 1
            
            # 난이도별 통계  
            difficulty = prompt['difficulty']
            stats['by_difficulty'][difficulty] = stats['by_difficulty'].get(difficulty, 0) + 1
            
            # 언어별 통계
            language = prompt['language'] 
            stats['by_language'][language] = stats['by_language'].get(language, 0) + 1
            
            # 실무분야별 통계
            practice_area = prompt['practice_area']
            stats['by_practice_area'][practice_area] = stats['by_practice_area'].get(practice_area, 0) + 1
        
        return stats

def batch_production_mode():
    """대량생산 모드"""
    
    print("🏭 === iOVU 프롬프트 대량생산 모드 ===")
    print("대량으로 프롬프트를 생성하여 여러 파일로 저장합니다.")
    print("=" * 50)
    
    generator = IOVUPromptGenerator()
    
    # 1. 생산 설정 입력
    print("\n📋 대량생산 설정")
    try:
        total_count = int(input("총 생성할 프롬프트 개수 (기본 1000): ") or "1000")
        batch_size = int(input("배치당 개수 (기본 100): ") or "100")
        file_prefix = input("파일명 접두사 (기본 iovu_batch): ").strip() or "iovu_batch"
    except ValueError:
        print("잘못된 입력입니다. 기본값을 사용합니다.")
        total_count = 1000
        batch_size = 100
        file_prefix = "iovu_batch"
    
    # 2. 배치 개수 계산
    num_batches = (total_count + batch_size - 1) // batch_size
    
    print(f"\n🎯 생산 계획:")
    print(f"   총 생성 개수: {total_count:,}개")
    print(f"   배치 크기: {batch_size}개")
    print(f"   배치 수: {num_batches}개")
    print(f"   파일 접두사: {file_prefix}")
    
    # 확인
    confirm = input(f"\n계속 진행하시겠습니까? (y/n): ").lower()
    if confirm != 'y':
        print("대량생산을 취소했습니다.")
        return
    
    # 3. 대량생산 실행
    print(f"\n🏭 대량생산 시작!")
    overall_start = datetime.now()
    all_generated_prompts = []
    generated_files = []
    
    for batch_num in range(num_batches):
        print(f"\n--- 배치 {batch_num + 1}/{num_batches} ---")
        
        # 현재 배치 크기 계산 (마지막 배치는 크기가 다를 수 있음)
        current_batch_size = min(batch_size, total_count - len(all_generated_prompts))
        
        # 배치 생성
        batch_start = datetime.now()
        batch_prompts = generator.generate_batch_prompts(current_batch_size)
        batch_end = datetime.now()
        batch_time = (batch_end - batch_start).total_seconds()
        
        # 파일 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{file_prefix}_batch{batch_num+1:03d}_{timestamp}.csv"
        generator.save_to_csv(batch_prompts, filename)
        generated_files.append(filename)
        
        # 전체 누적
        all_generated_prompts.extend(batch_prompts)
        
        # 진행 상황 출력
        progress = len(all_generated_prompts) / total_count * 100
        speed = current_batch_size / batch_time if batch_time > 0 else 0
        
        print(f"   ✅ {current_batch_size}개 생성 완료")
        print(f"   📁 저장: {filename}")
        print(f"   ⏱️ 배치 시간: {batch_time:.2f}초 ({speed:.1f}개/초)")
        print(f"   📊 전체 진행률: {progress:.1f}% ({len(all_generated_prompts):,}/{total_count:,})")
    
    overall_end = datetime.now()
    total_time = (overall_end - overall_start).total_seconds()
    
    # 4. 전체 통합 파일 생성
    print(f"\n📦 통합 파일 생성 중...")
    integrated_filename = f"{file_prefix}_integrated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    generator.save_to_csv(all_generated_prompts, integrated_filename)
    
    # 5. 최종 통계
    stats = generator.get_generation_stats(all_generated_prompts)
    
    print(f"\n🎉 === 대량생산 완료 ===")
    print(f"✨ 총 생성: {len(all_generated_prompts):,}개")
    print(f"📦 생성 배치: {num_batches}개")
    print(f"⏱️ 총 소요 시간: {total_time:.2f}초 ({total_time/60:.1f}분)")
    print(f"🚀 평균 생산 속도: {len(all_generated_prompts)/total_time:.1f}개/초")
    
    print(f"\n📊 생산 통계:")
    print(f"   의도별: {stats['by_intent']}")
    print(f"   난이도별: {stats['by_difficulty']}")
    print(f"   언어별: {stats['by_language']}")
    
    print(f"\n📁 생성된 파일들:")
    print(f"   🔗 통합 파일: {integrated_filename}")
    print(f"   📦 배치 파일들:")
    for i, file in enumerate(generated_files):
        print(f"      {i+1:3d}. {file}")
    
    return all_generated_prompts, generated_files

def speed_test_mode():
    """속도 테스트 모드"""
    
    print("⚡ === iOVU 프롬프트 생성 속도 테스트 ===")
    
    generator = IOVUPromptGenerator()
    test_sizes = [10, 50, 100, 500, 1000]
    
    print(f"\n🔬 다양한 크기별 속도 테스트:")
    
    for size in test_sizes:
        print(f"\n📊 {size}개 프롬프트 생성 테스트:")
        
        # 3회 반복 테스트
        times = []
        for attempt in range(3):
            start_time = datetime.now()
            prompts = generator.generate_batch_prompts(size)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            times.append(duration)
            
            speed = size / duration if duration > 0 else 0
            print(f"   시도 {attempt+1}: {duration:.3f}초 ({speed:.1f}개/초)")
        
        # 평균 계산
        avg_time = sum(times) / len(times)
        avg_speed = size / avg_time if avg_time > 0 else 0
        print(f"   📈 평균: {avg_time:.3f}초 ({avg_speed:.1f}개/초)")
    
    print(f"\n✅ 속도 테스트 완료!")

def continuous_production_mode():
    """연속 생산 모드"""
    
    print("🔄 === iOVU 프롬프트 연속 생산 모드 ===")
    print("설정한 간격으로 계속해서 프롬프트를 생성합니다.")
    print("Ctrl+C로 중단할 수 있습니다.")
    print("=" * 50)
    
    generator = IOVUPromptGenerator()
    
    # 설정 입력
    try:
        batch_size = int(input("배치당 생성 개수 (기본 50): ") or "50")
        interval = int(input("생성 간격(초) (기본 10): ") or "10")
        max_batches = int(input("최대 배치 수 (0=무제한, 기본 10): ") or "10")
    except ValueError:
        batch_size = 50
        interval = 10
        max_batches = 10
    
    print(f"\n🔄 연속 생산 설정:")
    print(f"   배치 크기: {batch_size}개")
    print(f"   생성 간격: {interval}초")
    print(f"   최대 배치: {max_batches}개 ({'무제한' if max_batches == 0 else str(max_batches)})")
    
    # 연속 생산 실행
    batch_count = 0
    total_generated = 0
    all_files = []
    
    try:
        import time
        
        print(f"\n🚀 연속 생산 시작! (Ctrl+C로 중단)")
        
        while max_batches == 0 or batch_count < max_batches:
            batch_count += 1
            
            print(f"\n⚡ 배치 {batch_count} 생성 중...")
            start_time = datetime.now()
            
            # 프롬프트 생성
            prompts = generator.generate_batch_prompts(batch_size)
            
            # 파일 저장
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"iovu_continuous_batch{batch_count:03d}_{timestamp}.csv"
            generator.save_to_csv(prompts, filename)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            total_generated += len(prompts)
            all_files.append(filename)
            
            print(f"   ✅ {len(prompts)}개 생성 완료 ({duration:.2f}초)")
            print(f"   📁 저장: {filename}")
            print(f"   📊 총 누적: {total_generated:,}개")
            
            # 다음 배치까지 대기
            if max_batches == 0 or batch_count < max_batches:
                print(f"   ⏸️ {interval}초 대기 중...")
                time.sleep(interval)
    
    except KeyboardInterrupt:
        print(f"\n\n👋 사용자에 의해 중단되었습니다.")
    
    # 최종 요약
    print(f"\n🎉 === 연속 생산 완료 ===")
    print(f"✨ 총 배치: {batch_count}개")
    print(f"📊 총 생성: {total_generated:,}개")
    print(f"📁 생성 파일: {len(all_files)}개")
    
    return all_files

def advanced_menu():
    """고급 메뉴"""
    
    print("🎛️ === iOVU 프롬프트 생성기 고급 메뉴 ===")
    print("1. 일반 생성 모드")
    print("2. 대량생산 모드 🏭")
    print("3. 속도 테스트 모드 ⚡")
    print("4. 연속 생산 모드 🔄")
    print("0. 종료")
    
    while True:
        try:
            choice = input("\n선택하세요 (0-4): ").strip()
            
            if choice == "0":
                print("👋 프로그램을 종료합니다.")
                break
                
            elif choice == "1":
                print("\n🔄 일반 생성 모드 실행")
                main()
                
            elif choice == "2":
                print("\n🏭 대량생산 모드 실행")
                batch_production_mode()
                
            elif choice == "3":
                print("\n⚡ 속도 테스트 모드 실행")
                speed_test_mode()
                
            elif choice == "4":
                print("\n🔄 연속 생산 모드 실행")
                continuous_production_mode()
                
            else:
                print("❌ 잘못된 선택입니다. 0-4 중에서 선택하세요.")
                
        except KeyboardInterrupt:
            print("\n\n👋 사용자 중단으로 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")

def main():
    """메인 실행 함수"""
    
    print("🚀 === iOVU 프롬프트 생성기 (단순화 버전) ===")
    print(f"📅 실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 시스템 초기화
    generator = IOVUPromptGenerator()
    
    # 1. 파라미터 정보 출력
    print("\n1️⃣ iOVU 브랜드 파라미터")
    print(f"   - practice_area: {len(generator.params.practice_areas)}개")
    print(f"   - metrics: 4개 그룹 {sum(len(v) for v in generator.params.metrics.values())}개")
    print(f"   - countries: {len(generator.params.countries)}개")
    print(f"   - time_spans: {len(generator.params.time_spans)}개")
    print(f"   - source_hints: {len(generator.params.source_hints)}개")
    print(f"   - intents: {len(generator.params.intents)}개")
    print(f"   - difficulties: {len(generator.params.difficulties)}개")
    
    # 2. 키워드 뱅크 정보
    print(f"\n2️⃣ 키워드 뱅크 현황")
    print(f"   - 핵심 제품: {len(generator.keywords.core_attributes)}개")
    print(f"   - 프린팅 기술: {len(generator.keywords.printing_tech)}개") 
    print(f"   - 브랜드 슬로건: {len(generator.keywords.slogans)}개")
    print(f"   - 밈/무드: {len(generator.keywords.meme_mood)}개")
    print(f"   - 커뮤니티: {len(generator.keywords.community)}개")
    
    # 3. 사용자 입력
    try:
        count = int(input(f"\n생성할 프롬프트 개수를 입력하세요 (기본 50): ") or "50")
    except ValueError:
        count = 50
        print("잘못된 입력입니다. 기본값 50개로 설정합니다.")
    
    # 4. 프롬프트 생성
    print(f"\n3️⃣ {count}개 프롬프트 생성 중...")
    start_time = datetime.now()
    prompts = generator.generate_batch_prompts(count)
    end_time = datetime.now()
    generation_time = (end_time - start_time).total_seconds()
    
    # 5. 생성 통계 출력
    stats = generator.get_generation_stats(prompts)
    print(f"\n📊 === 생성 통계 ===")
    print(f"총 생성 개수: {stats['total_count']}개")
    print(f"생성 시간: {generation_time:.2f}초")
    print(f"의도별: {stats['by_intent']}")
    print(f"난이도별: {stats['by_difficulty']}")
    print(f"언어별: {stats['by_language']}")
    
    # 6. 샘플 프롬프트 출력
    print(f"\n📋 === 샘플 프롬프트 (상위 10개) ===")
    for i, prompt in enumerate(prompts[:10]):
        print(f"{i+1:2d}. [{prompt['intent']}·{prompt['difficulty']}·{prompt['language']}] {prompt['prompt']}")
    
    # 7. CSV 저장
    print(f"\n💾 === 결과 저장 중... ===")
    csv_filename = generator.save_to_csv(prompts)
    
    # 8. 최종 요약
    print(f"\n🎉 === 생성 완료 ===")
    print(f"✨ 총 생성: {len(prompts)}개")
    print(f"⏱️ 소요 시간: {generation_time:.2f}초")
    print(f"📁 저장 파일: {csv_filename}")
    print(f"📊 평균 생성 속도: {len(prompts)/generation_time:.1f}개/초" if generation_time > 0 else "📊 평균 생성 속도: 계산 불가 (너무 빠름)")
    
    return prompts

if __name__ == "__main__":
    try:
        # 명령줄 인수 확인
        import sys
        
        if len(sys.argv) > 1:
            if sys.argv[1] == "--batch":
                batch_production_mode()
            elif sys.argv[1] == "--speed":
                speed_test_mode()
            elif sys.argv[1] == "--continuous":
                continuous_production_mode()
            elif sys.argv[1] == "--menu":
                advanced_menu()
            else:
                main()
        else:
            # 사용자 선택
            print("🚀 === iOVU 프롬프트 생성기 ===")
            print("실행 모드를 선택하세요:")
            print("1. 일반 모드 (기본)")
            print("2. 고급 메뉴")
            
            choice = input("선택 (1-2, 기본 1): ").strip()
            
            if choice == "2":
                advanced_menu()
            else:
                result = main()
        
        print(f"\n🎉 프로그램이 성공적으로 완료되었습니다!")
        
    except KeyboardInterrupt:
        print(f"\n\n👋 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류가 발생했습니다: {str(e)}")
        import traceback
        traceback.print_exc()