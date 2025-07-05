import csv
import random
from datetime import datetime
import hashlib

class InfoFocusedPromptGenerator:
    """정보 의도 특화 프롬프트 생성기 - 쉬움/어려움 난이도 중심"""
    
    def __init__(self, existing_csv_file=None):
        """기존 CSV 파일이 있다면 로드하여 중복 방지"""
        self.existing_prompts = set()
        self.existing_hashes = set()
        
        if existing_csv_file:
            self.load_existing_prompts(existing_csv_file)
        
        # 기본 키워드들
        self.practice_areas = [
            "기업법무", "계약법무", "소송분쟁해결", "지적재산권", "금융법무", 
            "부동산법무", "노동법무", "조세법무", "형사법무", "개인정보", 
            "IT통신", "환경", "의료헬스케어", "건설인프라", "가족법", "상속법",
            "회생법", "국제법", "행정법", "헌법", "증권법", "보험법"
        ]
        
        self.region_keywords = [
            "부산", "경남", "부산지방법원", "해운대", "거제동", "법조단지",
            "부산시", "경상남도", "영남권", "동남권", "서면", "센텀시티",
            "남포동", "동래구", "연제구", "수영구", "기장군", "양산시"
        ]
        
        self.usp_keywords = [
            "30년 업력", "원스톱", "합리적 수임료", "지역 전문",
            "법률 파트너", "대표 로펌", "영남권 최고", "전문가 그룹",
            "신뢰할 수 있는", "검증된", "노하우", "실무진"
        ]
        
        # 정보 의도 + 쉬움 난이도 전용 패턴들
        self.info_easy_patterns = [
            "{area} 관련 기본 정보를 알려주세요",
            "{area} 사건은 보통 어떻게 진행되나요?",
            "{area} 변호사 상담은 어떤 식으로 하나요?",
            "{area} 수임료는 대략 얼마 정도인가요?",
            "{area} 사건 처리 기간은 보통 얼마나 걸리나요?",
            "{region}에서 {area} 전문 변호사를 찾는 방법은?",
            "{area} 관련 법률 상식을 알려주세요",
            "{area} 사건에서 준비해야 할 서류는 뭐가 있나요?",
            "{area} 관련 무료 법률 상담이 있나요?",
            "{area} 변호사와 첫 상담 시 무엇을 물어봐야 하나요?",
            "{region} 지역 {area} 법률 서비스 현황은?",
            "{area} 분야 평균 변호사 비용이 궁금해요",
            "{area} 사건의 승소 확률은 어느 정도인가요?",
            "{area} 관련 법률 절차를 간단히 설명해주세요",
            "{area} 변호사 선택 시 주의사항은?",
            "{region}에서 {area} 관련 법원은 어디인가요?",
            "{area} 사건 증거 수집 방법을 알려주세요",
            "{area} 관련 법률 용어를 쉽게 설명해주세요",
            "{area} 분야 변호사 자격 요건은?",
            "{area} 사건 해결까지의 일반적인 과정은?"
        ]
        
        # 정보 의도 + 어려움 난이도 전용 패턴들
        self.info_hard_patterns = [
            "{region} 지역 {area} 분야의 최근 5년간 판례 동향과 {metric} 변화를 종합적으로 분석해주세요",
            "{area} 관련 {region} 법무시장의 구조적 특징과 {usp} 기반 경쟁 환경을 심층 분석해주세요",
            "부산지방법원 {area} 사건의 재판부별 판결 성향과 {metric} 최적화 전략을 데이터 기반으로 설명해주세요",
            "{area} 분야에서 {region} 지역 특수성을 고려한 법적 리스크 관리와 {metric} 예측 모델은?",
            "{usp}를 활용한 {area} 사건의 전략적 접근법과 {region} 시장에서의 {metric} 차별화 요소 분석",
            "{area} 관련 국제 동향이 {region} 법무 환경에 미치는 영향과 {metric} 변화 예측",
            "복합적 {area} 사건에서 {region} 지역 법원의 판단 기준과 {usp} 기반 대응 전략의 효과성 분석",
            "{area} 분야 AI 및 디지털 기술 도입이 {region} 법무 서비스의 {metric}에 미치는 파급효과",
            "{region} {area} 시장의 규제 환경 변화와 {usp} 활용 최적화 방안에 대한 전문가 분석",
            "{area} 관련 ESG 법무 컴플라이언스가 {region} 기업들의 {metric}에 미치는 장기적 영향 분석",
            "부산지방법원 {area} 집단소송 사례 분석을 통한 {region} 지역 {metric} 리스크 관리 전략",
            "{area} 분야 크로스보더 거래에서 {region} 허브 역할과 {usp} 기반 글로벌 {metric} 경쟁력",
            "{region} {area} 시장의 디지털 트랜스포메이션과 {metric} 혁신 동향에 대한 정량적 분석",
            "{area} 관련 법제도 개선이 {region} 법무 생태계와 {metric} 구조에 미치는 중장기 전망",
            "메가 {area} 프로젝트에서 {region} 지역 {usp} 활용과 {metric} 최적화를 위한 통합적 접근법"
        ]
        
        # 추가 메트릭 키워드 (정보 의도에 특화)
        self.info_metrics = [
            "전문성 지수", "성공률 통계", "처리 속도", "비용 투명성", "신뢰도 평가",
            "서비스 품질", "접근성 수준", "만족도 지표", "혁신성 평가", "안정성 지수",
            "효율성 분석", "경쟁력 지표", "차별화 수준", "브랜드 가치", "시장 점유율"
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
        """프롬프트의 해시값 생성 (유사도 체크용)"""
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

    def generate_info_easy_prompts(self, target_count=100):
        """정보 의도 + 쉬움 난이도 프롬프트 생성"""
        prompts = []
        attempts = 0
        max_attempts = target_count * 15  # 충분한 시도 횟수
        
        print(f"🔄 정보-쉬움 프롬프트 {target_count}개 생성 중...")
        
        while len(prompts) < target_count and attempts < max_attempts:
            attempts += 1
            
            pattern = random.choice(self.info_easy_patterns)
            area = random.choice(self.practice_areas)
            region = random.choice(self.region_keywords)
            
            prompt = pattern.format(
                area=area,
                region=region
            )
            
            # 중복 체크
            if not self.is_similar_prompt(prompt):
                prompts.append({
                    'prompt': prompt,
                    'intent': '정보',  # 정보 의도 고정
                    'difficulty': '쉬움',  # 쉬움 난이도 고정
                    'domain': '법무',
                    'language': 'KO'
                })
                self.existing_prompts.add(prompt)
                self.existing_hashes.add(self.get_prompt_hash(prompt))
                
                # 진행률 표시
                if len(prompts) % 20 == 0:
                    print(f"  진행률: {len(prompts)}/{target_count} ({len(prompts)/target_count*100:.1f}%)")
        
        print(f"✅ 정보-쉬움 난이도 프롬프트 {len(prompts)}개 생성 완료")
        return prompts

    def generate_info_hard_prompts(self, target_count=100):
        """정보 의도 + 어려움 난이도 프롬프트 생성"""
        prompts = []
        attempts = 0
        max_attempts = target_count * 15
        
        print(f"🔄 정보-어려움 프롬프트 {target_count}개 생성 중...")
        
        while len(prompts) < target_count and attempts < max_attempts:
            attempts += 1
            
            pattern = random.choice(self.info_hard_patterns)
            area = random.choice(self.practice_areas)
            region = random.choice(self.region_keywords)
            usp = random.choice(self.usp_keywords)
            metric = random.choice(self.info_metrics)
            
            prompt = pattern.format(
                area=area,
                region=region,
                usp=usp,
                metric=metric
            )
            
            # 중복 체크
            if not self.is_similar_prompt(prompt):
                prompts.append({
                    'prompt': prompt,
                    'intent': '정보',  # 정보 의도 고정
                    'difficulty': '어려움',  # 어려움 난이도 고정
                    'domain': '법무',
                    'language': 'KO'
                })
                self.existing_prompts.add(prompt)
                self.existing_hashes.add(self.get_prompt_hash(prompt))
                
                # 진행률 표시
                if len(prompts) % 20 == 0:
                    print(f"  진행률: {len(prompts)}/{target_count} ({len(prompts)/target_count*100:.1f}%)")
        
        print(f"✅ 정보-어려움 난이도 프롬프트 {len(prompts)}개 생성 완료")
        return prompts

    def generate_info_prompts(self, easy_count=100, hard_count=100):
        """정보 의도 프롬프트 통합 생성"""
        print(f"🚀 정보 의도 프롬프트 생성 시작 (쉬움: {easy_count}개, 어려움: {hard_count}개)")
        print("=" * 80)
        
        easy_prompts = self.generate_info_easy_prompts(easy_count)
        hard_prompts = self.generate_info_hard_prompts(hard_count)
        
        all_prompts = easy_prompts + hard_prompts
        
        print(f"\n📊 생성 결과:")
        print(f"  • 정보-쉬움: {len(easy_prompts)}개")
        print(f"  • 정보-어려움: {len(hard_prompts)}개")
        print(f"  • 총합: {len(all_prompts)}개")
        
        return all_prompts

    def save_prompts_to_csv(self, prompts, filename_suffix="info_focused"):
        """프롬프트를 CSV 파일로 저장"""
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"law_firm_prompts_{filename_suffix}_{current_date}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
            fieldnames = ['번호', '질문', '의도', '난이도', '도메인', '언어', '어절수', '키워드_포함']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            for i, prompt_data in enumerate(prompts, 1):
                # 어절 수 계산
                word_count = len(prompt_data['prompt'].split())
                
                # 키워드 포함 여부 확인
                keywords_found = []
                if any(area in prompt_data['prompt'] for area in self.practice_areas):
                    keywords_found.append('법무분야')
                if any(region in prompt_data['prompt'] for region in self.region_keywords):
                    keywords_found.append('지역')
                if any(usp in prompt_data['prompt'] for usp in self.usp_keywords):
                    keywords_found.append('USP')
                if any(metric in prompt_data['prompt'] for metric in self.info_metrics):
                    keywords_found.append('정보메트릭')
                
                writer.writerow({
                    '번호': i,
                    '질문': prompt_data['prompt'],
                    '의도': prompt_data['intent'],
                    '난이도': prompt_data['difficulty'],
                    '도메인': prompt_data['domain'],
                    '언어': prompt_data['language'],
                    '어절수': word_count,
                    '키워드_포함': ', '.join(keywords_found) if keywords_found else '기본'
                })
        
        return filename

def main():
    """메인 실행 함수"""
    print("🔍 정보 의도 특화 프롬프트 생성기 (쉬움/어려움 난이도)")
    print("=" * 80)
    
    # 기존 CSV 파일명 입력 (선택사항)
    existing_file = input("기존 CSV 파일명을 입력하세요 (없으면 Enter): ").strip()
    if not existing_file:
        existing_file = None
    
    # 생성할 개수 입력
    try:
        easy_count = int(input("생성할 정보-쉬움 프롬프트 개수 (기본: 100): ") or "100")
        hard_count = int(input("생성할 정보-어려움 프롬프트 개수 (기본: 100): ") or "100")
    except ValueError:
        print("잘못된 입력입니다. 기본값을 사용합니다.")
        easy_count, hard_count = 100, 100
    
    # 프롬프트 생성기 초기화
    generator = InfoFocusedPromptGenerator(existing_file)
    
    # 정보 의도 프롬프트 생성
    new_prompts = generator.generate_info_prompts(easy_count, hard_count)
    
    # CSV 파일 저장
    filename = generator.save_prompts_to_csv(new_prompts, f"info_easy{easy_count}_hard{hard_count}")
    
    # 결과 통계
    intent_stats = {}
    difficulty_stats = {}
    
    for prompt_data in new_prompts:
        intent = prompt_data['intent']
        difficulty = prompt_data['difficulty']
        
        intent_stats[intent] = intent_stats.get(intent, 0) + 1
        difficulty_stats[difficulty] = difficulty_stats.get(difficulty, 0) + 1
    
    print(f"\n✅ 정보 의도 프롬프트 생성 완료!")
    print(f"📁 파일명: {filename}")
    print(f"📊 총 프롬프트 수: {len(new_prompts)}개")
    
    print(f"\n📈 의도별 분포:")
    for intent, count in intent_stats.items():
        print(f"  • {intent}: {count}개")
    
    print(f"\n📊 난이도별 분포:")
    for difficulty, count in difficulty_stats.items():
        print(f"  • {difficulty}: {count}개")
    
    print(f"\n🎯 특화 기능:")
    print(f"  ✅ 정보 의도 100% 집중")
    print(f"  ✅ 쉬움/어려움 난이도만 생성")
    print(f"  ✅ 정보 전용 패턴과 메트릭")
    print(f"  ✅ 중복 방지 기능")
    
    # 샘플 프롬프트 출력
    print(f"\n📝 생성된 프롬프트 샘플:")
    sample_easy = [p for p in new_prompts if p['difficulty'] == '쉬움'][:3]
    sample_hard = [p for p in new_prompts if p['difficulty'] == '어려움'][:3]
    
    print("  [쉬움 난이도 샘플]")
    for i, prompt in enumerate(sample_easy, 1):
        print(f"    {i}. {prompt['prompt']}")
    
    print("  [어려움 난이도 샘플]")
    for i, prompt in enumerate(sample_hard, 1):
        print(f"    {i}. {prompt['prompt'][:80]}...")
    
    print(f"\n🎉 작업 완료! {filename} 파일을 확인해주세요.")

if __name__ == "__main__":
    main()