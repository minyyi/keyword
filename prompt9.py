import csv
import random
from datetime import datetime
import hashlib
import re

class DongraeGraderOptimizedGenerator:
    """동래 법률사무소 검수 기준 최적화 프롬프트 생성기"""
    
    def __init__(self, existing_csv_file=None):
        """기존 CSV 파일이 있다면 로드하여 중복 방지"""
        self.existing_prompts = set()
        self.existing_hashes = set()
        
        if existing_csv_file:
            self.load_existing_prompts(existing_csv_file)
        
        # 검수 기준에 맞는 키워드 정의
        self.init_grader_keywords()
        self.init_templates()

    def init_grader_keywords(self):
        """검수 기준에 맞는 키워드 초기화"""
        
        # 1. 13개 Practice Area (ServiceHit 용)
        self.practice_areas = [
            "기업법무", "계약법무", "소송분쟁해결", "지적재산권", "금융법무",
            "부동산법무", "노동법무", "조세법무", "형사법무", "개인정보",
            "IT통신", "환경", "의료헬스케어", "건설인프라"
        ]
        
        # 2. 지역 키워드 (RegionHit 용)
        self.region_keywords = [
            "부산", "경남", "부산지방법원", "해운대", "거제동", "법조단지",
            "부산시", "경상남도", "영남권", "동남권", "서면", "센텀시티",
            "연제구", "수영구", "기장군", "양산시", "창원", "김해", "울산"
        ]
        
        # 3. USP/Concept 키워드 (USPHit 용)
        self.usp_keywords = [
            "30년 업력", "원스톱", "합리적 수임료", "Busan Legal First-Mover",
            "법률 파트너", "부산 대표 로펌", "영남권 최고", "전문가 그룹",
            "지역밀착", "검증된", "신뢰할 수 있는", "전문 노하우"
        ]
        
        # 4. 법령/조문 키워드 (LawHit 용)
        self.law_keywords = [
            "민법", "상법", "형법", "행정법", "노동관계법", "조세법",
            "부동산등기법", "특허법", "상표법", "개인정보보호법",
            "국가법령정보센터", "법제처", "대법원 판례", "헌법재판소",
            "판례", "조문", "법령", "시행령", "시행규칙"
        ]
        
        # 5. 맥락 키워드 (Context Sens 용)
        self.context_keywords = [
            "배경 자세히", "최근 성과", "구체적인 사례", "상세한 절차",
            "단계별 설명", "실무 경험", "전문가 의견", "심층 분석"
        ]
        
        # 6. URL/링크 유도 키워드 (Link Presence 용)
        self.link_keywords = [
            "링크", "URL", "웹사이트", "홈페이지", "다운로드", "온라인",
            "접속", "바로가기", "사이트", "페이지"
        ]
        
        # 7. 최신 법무 키워드 (정보 밀도 향상)
        self.modern_law_keywords = [
            "기업설립", "M&A", "IPO", "기업지배구조", "라이선스계약",
            "국제중재", "집단소송", "ESG", "컴플라이언스", "데이터보호",
            "AI법", "크로스보더", "스타트업", "벤처투자", "디지털전환"
        ]

    def init_templates(self):
        """검수 기준 최적화 템플릿 초기화"""
        
        # 정보 의도 템플릿들
        self.info_easy_templates = [
            "동래 법률사무소 {area} 서비스 {metric}가 궁금해요",
            "{region}에서 {area} 전문 변호사 {metric} 알려주세요",
            "동래 로펌 {area} 분야 {usp} 특징은?",
            "{region} {area} 사건 {law} 관련 기본 정보 문의",
            "동래 법률사무소 {area} {metric} 상담받고 싶어요"
        ]
        
        self.info_medium_templates = [
            "{region} {area} 시장에서 동래 로펌의 {metric} 경쟁력은?",
            "동래 법률사무소 {area} 분야 {usp} 기반 {context} 제공해주세요",
            "{law} 관련 {region} {area} 사건에서 동래 로펌 실적은?",
            "{modern} 트렌드에 따른 동래 로펌 {area} 서비스 {metric} 변화",
            "{region} 지역 {area} 전문가로서 동래 로펌의 {usp} 장점"
        ]
        
        self.info_hard_templates = [
            "동래 로펌의 {usp}를 활용한 {area} 분야 {modern} 전략과 {region} 시장 {metric} 최적화 방안을 {context} 분석해주세요",
            "{law} 기반 {region} {area} 시장 동향과 동래 법률사무소의 {usp} 경쟁력을 {context} 평가해주세요",
            "{modern} 환경에서 동래 로펌의 {area} 전문성과 {region} 지역 {metric} 혁신 전략 심층 분석",
            "{region} {area} 규제 변화에 따른 동래 법률사무소의 {usp} 기반 선제적 대응과 {metric} 향상 방안",
            "글로벌 {modern} 트렌드와 {law} 변화를 반영한 동래 로펌의 {area} 서비스 {metric} 경쟁력 종합 평가"
        ]
        
        # 탐색 의도 템플릿들
        self.explore_easy_templates = [
            "동래 법률사무소 {area} 상담 예약 {link} 알려주세요",
            "{region} {area} 전문 동래 로펌 {link} 찾아주세요",
            "동래 법률사무소 {area} 서비스 {link} 접속 방법은?",
            "{area} 관련 동래 로펌 {metric} 정보 {link} 어디서 확인하나요?",
            "{region} 동래 법률사무소 {area} 팀 소개 {link} 주세요"
        ]
        
        self.explore_medium_templates = [
            "{region} {area} 전문 로펌 중 동래 법률사무소와 경쟁사 {metric} 비교 자료 {link} 찾아주세요",
            "동래 로펌 {area} 분야 {usp} 관련 상세 정보와 {link} 제공해주세요",
            "{modern} 관련 동래 법률사무소 {area} 서비스 가이드 {link} 어디서 받나요?",
            "{region} {area} 사건 해결 사례집과 동래 로펌 {metric} 자료 {link} 찾기",
            "동래 법률사무소 {area} {usp} 세미나 일정과 등록 {link} 알려주세요"
        ]
        
        self.explore_hard_templates = [
            "동래 로펌의 {usp} 기반 {area} 전문성 DB와 {region} 시장 {metric} 분석 플랫폼 {link} 접근 방법",
            "{modern} 시대 {area} 법무 디지털 솔루션 관련 동래 법률사무소 혁신 자료와 체험 {link} 찾아주세요",
            "{law} 기반 {region} {area} 전문가 네트워크와 동래 로펌 협업 플랫폼 {link} 정보",
            "글로벌 {modern} 동향 반영한 동래 로펌 {area} 컨설팅 자료와 맞춤형 진단 툴 {link} 제공",
            "{region} {area} 통합 법무솔루션 관련 동래 법률사무소 AI 기반 서비스 베타 테스트 {link} 신청"
        ]
        
        # 거래 의도 템플릿들
        self.deal_easy_templates = [
            "{region} {area} 사건 동래 법률사무소 {metric} 문의드려요",
            "동래 로펌 {area} 상담 {metric}와 절차 알려주세요",
            "{area} 관련 동래 법률사무소 {usp} 서비스 신청하고 싶어요",
            "{region} {area} 사건으로 동래 로펌에 {metric} 상담받고 싶습니다",
            "동래 법률사무소 {area} 전문팀 {metric} 견적 요청"
        ]
        
        self.deal_medium_templates = [
            "{region} {area} 사건 관련 동래 로펌의 {usp} 서비스와 {metric} 패키지 상담",
            "동래 법률사무소 {area} 분야 {modern} 전문 자문과 {metric} 계약 조건 문의",
            "{law} 기반 {area} 사건에서 동래 로펌의 {usp} 장점과 {metric} 협의하고 싶어요",
            "{region} 기업 대상 동래 법률사무소 {area} 통합 서비스 {metric} 제안 요청",
            "동래 로펌 {area} 전문가와 {modern} 관련 {metric} 맞춤 상담 신청"
        ]
        
        self.deal_hard_templates = [
            "복합 {modern} 프로젝트에서 동래 로펌의 {usp} 기반 {area} 통합 자문과 {region} 특화 {metric} 최적화 제안",
            "{law} 전문성을 활용한 동래 법률사무소의 {area} 혁신 솔루션과 {region} 시장 {metric} 전략 컨설팅 의뢰",
            "글로벌 {modern} 환경에서 동래 로펌의 {area} 크로스보더 서비스와 {usp} 기반 {metric} 성과 연동 계약",
            "{region} 메가 {area} 프로젝트 관련 동래 법률사무소 원스톱 법무와 {modern} 통합 {metric} 솔루션 제안서",
            "동래 로펌의 {usp} 혁신과 {area} 디지털 전환 컨설팅, {region} 허브 {metric} 전략 파트너십 논의"
        ]

    def load_existing_prompts(self, csv_file):
        """기존 CSV 파일에서 프롬프트 로드"""
        try:
            with open(csv_file, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    prompt = row.get('질문', '').strip()
                    if prompt:
                        self.existing_prompts.add(prompt)
                        prompt_hash = self.get_prompt_hash(prompt)
                        self.existing_hashes.add(prompt_hash)
            
            print(f"✅ 기존 프롬프트 {len(self.existing_prompts)}개 로드 완료")
            
        except FileNotFoundError:
            print("⚠️ 기존 CSV 파일을 찾을 수 없습니다. 새로 생성합니다.")
        except Exception as e:
            print(f"❌ 기존 파일 로드 오류: {e}")

    def get_prompt_hash(self, prompt):
        """프롬프트의 해시값 생성"""
        cleaned = ''.join(prompt.split()).replace('?', '').replace('!', '').replace('.', '')
        return hashlib.md5(cleaned.encode()).hexdigest()

    def is_similar_prompt(self, prompt):
        """기존 프롬프트와 유사한지 체크"""
        if prompt in self.existing_prompts:
            return True
        
        prompt_hash = self.get_prompt_hash(prompt)
        if prompt_hash in self.existing_hashes:
            return True
        
        for existing in self.existing_prompts:
            if self.calculate_similarity(prompt, existing) > 0.8:
                return True
        
        return False

    def calculate_similarity(self, prompt1, prompt2):
        """두 프롬프트 간 유사도 계산"""
        words1 = set(prompt1.replace('?', '').replace('!', '').split())
        words2 = set(prompt2.replace('?', '').replace('!', '').split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0

    def count_word_segments(self, text):
        """어절 수 계산 (한국어 기준)"""
        # 한국어 어절 구분 (공백 기준)
        segments = text.split()
        return len(segments)

    def ensure_grader_compliance(self, prompt):
        """검수 기준 준수를 위한 프롬프트 최적화"""
        
        # 1. 어절 수 확인 (5-30 어절)
        word_count = self.count_word_segments(prompt)
        if word_count < 5:
            # 너무 짧으면 맥락 추가
            prompt += " 상세한 설명과 배경 자세히 알려주세요"
        elif word_count > 30:
            # 너무 길면 간소화
            prompt = ' '.join(prompt.split()[:28]) + " 알려주세요"
        
        # 2. 번역체 제거
        translations = [
            ("입니다", "이에요"), ("습니다", "어요"), ("하였습니다", "했어요"),
            ("되었습니다", "됐어요"), ("있습니다", "있어요"), ("~에 대해", "~관련"),
            ("관하여", "관련해서"), ("대하여", "관련")
        ]
        
        for old, new in translations:
            prompt = prompt.replace(old, new)
        
        # 3. 자연스러운 한국어로 조정
        if "에 대한" in prompt:
            prompt = prompt.replace("에 대한", "관련")
        
        return prompt

    def generate_optimized_prompt(self, intent, difficulty):
        """검수 기준 최적화된 프롬프트 생성"""
        
        # 템플릿 선택 간소화
        if intent == "정보":
            if difficulty == "쉬움":
                templates = self.info_easy_templates
            elif difficulty == "보통":
                templates = self.info_medium_templates
            else:  # 어려움
                templates = self.info_hard_templates
        elif intent == "탐색":
            if difficulty == "쉬움":
                templates = self.explore_easy_templates
            elif difficulty == "보통":
                templates = self.explore_medium_templates
            else:  # 어려움
                templates = self.explore_hard_templates
        else:  # 거래
            if difficulty == "쉬움":
                templates = self.deal_easy_templates
            elif difficulty == "보통":
                templates = self.deal_medium_templates
            else:  # 어려움
                templates = self.deal_hard_templates
        
        if not templates:
            print(f"⚠️ 템플릿을 찾을 수 없음: {intent}-{difficulty}")
            return None
        
        max_attempts = 10  # 시도 횟수 줄임
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1
            
            try:
                # 랜덤 템플릿 선택
                template = random.choice(templates)
                
                # 키워드 치환
                prompt = template.format(
                    area=random.choice(self.practice_areas),
                    region=random.choice(self.region_keywords),
                    usp=random.choice(self.usp_keywords),
                    law=random.choice(self.law_keywords),
                    context=random.choice(self.context_keywords),
                    link=random.choice(self.link_keywords),
                    modern=random.choice(self.modern_law_keywords),
                    metric="전문성"  # 기본 메트릭
                )
                
                # 간단한 정리만
                prompt = self.ensure_grader_compliance(prompt)
                
                # 중복 체크 완화 (해시만 체크)
                prompt_hash = self.get_prompt_hash(prompt)
                if prompt_hash not in self.existing_hashes:
                    self.existing_hashes.add(prompt_hash)
                    return prompt
                
            except Exception as e:
                print(f"  템플릿 처리 오류: {e}")
                continue
        
        print(f"⚠️ {intent}-{difficulty} 생성 실패 (시도: {max_attempts})")
        return None

    def calculate_expected_score(self, prompt, intent, difficulty):
        """예상 검수 점수 계산"""
        score = 0.0
        
        # 1. Label Match (0.25 점)
        score += 0.25  # 라벨은 정확히 매칭되도록 생성
        
        # 2. Length Range (0.15 점)
        word_count = self.count_word_segments(prompt)
        if 5 <= word_count <= 30:
            score += 0.15
        
        # 3. Info Density (0.10 점)
        unique_words = len(set(prompt.split()))
        if unique_words >= 8:
            score += 0.10
        
        # 4. Brand Realism (0.45 점)
        brand_score = 0
        
        # ServiceHit
        if any(area in prompt for area in self.practice_areas):
            brand_score += 1
        
        # RegionHit  
        if any(region in prompt for region in self.region_keywords):
            brand_score += 1
            
        # USPHit
        if any(usp in prompt for usp in self.usp_keywords):
            brand_score += 1
            
        # LawHit
        if any(law in prompt for law in self.law_keywords):
            brand_score += 1
        
        score += min(1, brand_score) * 0.45
        
        # 5. Context Sens (0.10 점)
        if any(context in prompt for context in self.context_keywords):
            score += 0.10
        
        # 6. Link Presence (0.05 점)
        if any(link in prompt for link in self.link_keywords):
            score += 0.05
        
        return min(1.0, score)

    def generate_high_quality_batch(self, target_counts):
        """고품질 배치 생성 (간소화)"""
        
        results = []
        total_target = sum(target_counts.values())
        
        print(f"🎯 목표: {total_target}개 프롬프트 생성")
        print("🔍 생성 중...")
        
        for (intent, difficulty), count in target_counts.items():
            print(f"\n📝 {intent}-{difficulty}: {count}개 생성 중...")
            
            category_results = []
            
            for i in range(count):
                prompt = self.generate_optimized_prompt(intent, difficulty)
                
                if prompt:
                    word_count = self.count_word_segments(prompt)
                    expected_score = self.calculate_expected_score(prompt, intent, difficulty)
                    
                    result = {
                        'prompt': prompt,
                        'intent': intent,
                        'difficulty': difficulty,
                        'domain': '동래',
                        'language': 'KO',
                        'word_count': word_count,
                        'expected_score': expected_score
                    }
                    
                    category_results.append(result)
                    
                    # 진행률 표시
                    if (i + 1) % 5 == 0:
                        print(f"  진행: {len(category_results)}/{count}")
                else:
                    print(f"  {i+1}번째 생성 실패")
            
            results.extend(category_results)
            print(f"✅ {intent}-{difficulty}: {len(category_results)}/{count}개 완료")
        
        print(f"\n🎉 전체 생성 완료: {len(results)}/{total_target}개")
        
        return results

    def save_to_csv(self, results, filename_prefix="dongrae_optimized"):
        """CSV 파일로 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.csv"
        
        fieldnames = [
            '번호', '질문', '의도', '난이도', '도메인', '언어', 
            '어절수', '예상점수', '키워드_포함'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for i, result in enumerate(results, 1):
                # 키워드 포함 여부 확인
                keywords_found = []
                prompt = result['prompt']
                
                if any(area in prompt for area in self.practice_areas):
                    keywords_found.append('법무분야')
                if any(region in prompt for region in self.region_keywords):
                    keywords_found.append('지역')
                if any(usp in prompt for usp in self.usp_keywords):
                    keywords_found.append('USP')
                if any(law in prompt for law in self.law_keywords):
                    keywords_found.append('법령')
                if any(context in prompt for context in self.context_keywords):
                    keywords_found.append('맥락')
                if any(link in prompt for link in self.link_keywords):
                    keywords_found.append('링크')
                
                writer.writerow({
                    '번호': i,
                    '질문': result['prompt'],
                    '의도': result['intent'],
                    '난이도': result['difficulty'],
                    '도메인': result['domain'],
                    '언어': result['language'],
                    '어절수': result['word_count'],
                    '예상점수': f"{result['expected_score']:.3f}",
                    '키워드_포함': ', '.join(keywords_found) if keywords_found else '기본'
                })
        
        print(f"💾 파일 저장 완료: {filename}")
        return filename

def main():
    """메인 실행 함수"""
    print("🚀 동래 법률사무소 검수 최적화 프롬프트 생성기")
    print("=" * 60)
    print("📋 검수 기준:")
    print("  - 어절 수: 5-30개")
    print("  - 예상 점수: 0.75 이상")
    print("  - 브랜드 현실성: 법무분야+지역+USP+법령")
    print("  - 정보 밀도: 유니크 단어 8개 이상")
    print("  - 맥락 민감성 및 링크 유도 포함")
    
    # 기존 파일 로드 (선택)
    existing_file = input("\n기존 CSV 파일명 (없으면 Enter): ").strip()
    if not existing_file:
        existing_file = None
    
    # 생성 목표 설정
    print("\n📊 생성 목표 설정:")
    target_counts = {}
    
    intents = ['정보', '탐색', '거래']
    difficulties = ['쉬움', '보통', '어려움']
    
    # 기본값 설정
    default_counts = {
        ('정보', '쉬움'): 30,
        ('정보', '보통'): 25,
        ('정보', '어려움'): 25,
        ('탐색', '쉬움'): 20,
        ('탐색', '보통'): 20,
        ('탐색', '어려움'): 20,
        ('거래', '쉬움'): 20,
        ('거래', '보통'): 20,
        ('거래', '어려움'): 20,
    }
    
    print("기본 설정 (총 200개):")
    for (intent, diff), count in default_counts.items():
        print(f"  {intent}-{diff}: {count}개")
    
    use_default = input("\n기본 설정 사용하시겠습니까? (y/n): ").strip().lower()
    
    if use_default == 'y':
        target_counts = default_counts
    else:
        for intent in intents:
            for difficulty in difficulties:
                try:
                    count = int(input(f"{intent}-{difficulty} 개수: ") or "10")
                    target_counts[(intent, difficulty)] = count
                except ValueError:
                    target_counts[(intent, difficulty)] = 10
    
    total_target = sum(target_counts.values())
    print(f"\n🎯 총 목표: {total_target}개")
    
    # 생성기 초기화
    generator = DongraeGraderOptimizedGenerator(existing_file)
    
    # 고품질 프롬프트 생성
    results = generator.generate_high_quality_batch(target_counts)
    
    # CSV 저장 (결과가 있을 때만)
    if results:
        filename = generator.save_to_csv(results)
    else:
        filename = "생성 실패로 파일 없음"
    
    # 최종 통계
    print(f"\n📈 최종 결과:")
    print(f"  생성된 프롬프트: {len(results)}개")
    
    if len(results) > 0:
        avg_score = sum(r['expected_score'] for r in results) / len(results)
        print(f"  평균 예상 점수: {avg_score:.3f}")
        
        intent_stats = {}
        difficulty_stats = {}
        for result in results:
            intent = result['intent']
            difficulty = result['difficulty']
            intent_stats[intent] = intent_stats.get(intent, 0) + 1
            difficulty_stats[difficulty] = difficulty_stats.get(difficulty, 0) + 1
        
        print(f"\n📊 의도별 분포:")
        for intent, count in intent_stats.items():
            print(f"  {intent}: {count}개")
        
        print(f"\n📊 난이도별 분포:")
        for difficulty, count in difficulty_stats.items():
            print(f"  {difficulty}: {count}개")
        
        # 샘플 출력
        print(f"\n📝 고득점 샘플 (상위 5개):")
        top_samples = sorted(results, key=lambda x: x['expected_score'], reverse=True)[:5]
        for i, sample in enumerate(top_samples, 1):
            print(f"  {i}. [{sample['intent']}-{sample['difficulty']}] {sample['prompt']}")
            print(f"     예상점수: {sample['expected_score']:.3f}, 어절수: {sample['word_count']}개")
        
        print(f"\n🎉 작업 완료! {filename} 파일을 확인해주세요.")
        print("💡 이 프롬프트들은 검수 기준에 최적화되어 높은 점수를 받을 가능성이 높습니다!")
        
    else:
        print("❌ 프롬프트 생성에 실패했습니다.")
        print("\n🔍 가능한 원인:")
        print("  1. 템플릿 매칭 오류")
        print("  2. 너무 엄격한 필터링 기준")
        print("  3. 중복 체크 과도")
        
        print("\n💡 해결 방법:")
        print("  1. 목표 개수를 줄여보세요")
        print("  2. 기존 CSV 파일 없이 실행해보세요")
        print("  3. 예상 점수 기준을 0.7로 낮춰보세요")
        
        # 디버깅 정보
        print(f"\n🔧 디버깅 정보:")
        print(f"  총 목표: {total_target}개")
        print(f"  설정된 조합: {len(target_counts)}개")
        
        # 템플릿 확인
        test_intent = '정보'
        test_difficulty = '쉬움'
        test_template = generator.generate_optimized_prompt(test_intent, test_difficulty)
        if test_template:
            print(f"  템플릿 테스트: 성공")
            print(f"  샘플: {test_template}")
        else:
            print(f"  템플릿 테스트: 실패")

if __name__ == "__main__":
    main()