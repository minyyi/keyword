import csv
import random
from datetime import datetime
import hashlib

class DongraePromptExpander:
    """동래 법률사무소 프롬프트 확장 생성기 - 중복 방지 및 난이도 조절"""
    
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
            "30년 업력", "원스톱", "합리적 수임료", "Busan Legal First-Mover",
            "법률 파트너", "부산 대표 로펌", "영남권 최고", "전문가 그룹",
            "신뢰할 수 있는", "검증된", "노하우", "실무진"
        ]
        
        # 쉬움 난이도용 간단한 패턴들
        self.easy_patterns = [
            "{area} 관련 동래 법률사무소 상담 가능한가요?",
            "부산 {region}에서 {area} 전문 변호사 찾고 있어요",
            "동래 로펌 {area} 수임료는 어느 정도인가요?",
            "{area} 사건으로 동래 법률사무소 방문 예약하고 싶어요",
            "부산지방법원 {area} 소송 동래 로펌 도움받을 수 있나요?",
            "동래 법률사무소 {area} 변호사 경력이 궁금해요",
            "{region} 거주자인데 동래 로펌 {area} 상담 받고 싶어요",
            "동래 법률사무소 {area} 관련 무료상담 있나요?",
            "부산 {area} 전문 동래 로펌 평판은 어떤가요?",
            "{area} 초기 대응 동래 법률사무소 도움받고 싶어요"
        ]
        
        # 어려움 난이도용 복잡한 패턴들
        self.hard_patterns = [
            "동래 법률사무소의 {area} 전문성을 {region} 지역 {metric}와 연계하여 종합적으로 분석해주세요",
            "부산지방법원 {area} 관련 최근 5년간 판례 동향을 동래 로펌의 {usp} 관점에서 평가해주세요",
            "{region} 기반 글로벌 {area} 프로젝트에서 동래 법률사무소의 경쟁력과 {metric} 최적화 전략은?",
            "동래 로펌의 {usp}를 활용한 {area} 분야 디지털 혁신이 {region} 법무시장에 미치는 파급효과 분석",
            "부산지방법원 복합 {area} 사건에서 동래 법률사무소의 다학제적 접근법과 {metric} 효율성 평가",
            "{region} 지역 {area} 규제 변화에 따른 동래 로펌의 선제적 대응 전략과 클라이언트 {metric} 향상 방안",
            "동래 법률사무소의 AI 기반 {area} 솔루션이 {region} 기업들의 {metric} 혁신에 미치는 영향 분석",
            "부산 {region} 메가프로젝트 관련 {area} 통합 자문에서 동래 로펌의 {usp} 활용 극대화 전략",
            "{area} 분야 ESG 컴플라이언스 구축 시 동래 법률사무소의 {region} 특화 솔루션과 {metric} ROI 분석",
            "동래 로펌의 {usp} 기반 {area} 크로스보더 거래에서 {region} 허브 역할과 글로컬 {metric} 최적화"
        ]
        
        # 추가 메트릭 키워드
        self.metrics = [
            "비용 효율성", "시간 단축", "성공률", "만족도", "신뢰도", "전문성",
            "접근성", "편의성", "투명성", "안정성", "혁신성", "차별화"
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
                        # 해시값도 저장하여 유사한 문장 체크
                        prompt_hash = self.get_prompt_hash(prompt)
                        self.existing_hashes.add(prompt_hash)
            
            print(f"✅ 기존 프롬프트 {len(self.existing_prompts)}개 로드 완료")
            
        except FileNotFoundError:
            print("⚠️ 기존 CSV 파일을 찾을 수 없습니다. 새로 생성합니다.")
        except Exception as e:
            print(f"❌ 기존 파일 로드 오류: {e}")

    def get_prompt_hash(self, prompt):
        """프롬프트의 해시값 생성 (유사도 체크용)"""
        # 공백과 특수문자 제거 후 해시 생성
        cleaned = ''.join(prompt.split()).replace('?', '').replace('!', '').replace('.', '')
        return hashlib.md5(cleaned.encode()).hexdigest()

    def is_similar_prompt(self, prompt):
        """기존 프롬프트와 유사한지 체크"""
        # 완전 일치 체크
        if prompt in self.existing_prompts:
            return True
        
        # 해시 유사도 체크
        prompt_hash = self.get_prompt_hash(prompt)
        if prompt_hash in self.existing_hashes:
            return True
        
        # 핵심 키워드 기반 유사도 체크
        for existing in self.existing_prompts:
            if self.calculate_similarity(prompt, existing) > 0.8:
                return True
        
        return False

    def calculate_similarity(self, prompt1, prompt2):
        """두 프롬프트 간 유사도 계산 (간단한 자카드 유사도)"""
        words1 = set(prompt1.replace('?', '').replace('!', '').split())
        words2 = set(prompt2.replace('?', '').replace('!', '').split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0

    def generate_easy_prompts(self, target_count=50):
        """쉬움 난이도 프롬프트 생성"""
        prompts = []
        attempts = 0
        max_attempts = target_count * 10
        
        while len(prompts) < target_count and attempts < max_attempts:
            attempts += 1
            
            pattern = random.choice(self.easy_patterns)
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
                    'intent': random.choice(['정보', '탐색', '거래']),
                    'difficulty': '쉬움',
                    'domain': '동래',
                    'language': 'KO'
                })
                self.existing_prompts.add(prompt)
                self.existing_hashes.add(self.get_prompt_hash(prompt))
        
        print(f"✅ 쉬움 난이도 프롬프트 {len(prompts)}개 생성 완료")
        return prompts

    def generate_hard_prompts(self, target_count=50):
        """어려움 난이도 프롬프트 생성"""
        prompts = []
        attempts = 0
        max_attempts = target_count * 10
        
        while len(prompts) < target_count and attempts < max_attempts:
            attempts += 1
            
            pattern = random.choice(self.hard_patterns)
            area = random.choice(self.practice_areas)
            region = random.choice(self.region_keywords)
            usp = random.choice(self.usp_keywords)
            metric = random.choice(self.metrics)
            
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
                    'intent': random.choice(['정보', '탐색', '거래']),
                    'difficulty': '어려움',
                    'domain': '동래',
                    'language': 'KO'
                })
                self.existing_prompts.add(prompt)
                self.existing_hashes.add(self.get_prompt_hash(prompt))
        
        print(f"✅ 어려움 난이도 프롬프트 {len(prompts)}개 생성 완료")
        return prompts

    def generate_additional_prompts(self, easy_count=50, hard_count=50):
        """추가 프롬프트 생성 (중복 방지)"""
        print(f"🚀 추가 프롬프트 생성 시작 (쉬움: {easy_count}개, 어려움: {hard_count}개)")
        print("=" * 60)
        
        easy_prompts = self.generate_easy_prompts(easy_count)
        hard_prompts = self.generate_hard_prompts(hard_count)
        
        all_prompts = easy_prompts + hard_prompts
        
        print(f"\n📊 생성 결과:")
        print(f"  • 쉬움: {len(easy_prompts)}개")
        print(f"  • 어려움: {len(hard_prompts)}개")
        print(f"  • 총합: {len(all_prompts)}개")
        
        return all_prompts

    def save_prompts_to_csv(self, prompts, filename_suffix="additional"):
        """프롬프트를 CSV 파일로 저장"""
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dongrae_makeup_200{filename_suffix}_{current_date}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
            fieldnames = ['번호', '질문', '의도', '난이도', '도메인', '언어', '어절수', '키워드_포함']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            for i, prompt_data in enumerate(prompts, 1):
                # 어절 수 계산
                word_count = len(prompt_data['prompt'].split())
                
                # 키워드 포함 여부 확인
                keywords_found = []
                if '동래' in prompt_data['prompt']:
                    keywords_found.append('동래')
                if any(area in prompt_data['prompt'] for area in self.practice_areas):
                    keywords_found.append('법무분야')
                if any(region in prompt_data['prompt'] for region in self.region_keywords):
                    keywords_found.append('지역')
                if any(usp in prompt_data['prompt'] for usp in self.usp_keywords):
                    keywords_found.append('USP')
                
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
    print("🔄 동래 법률사무소 프롬프트 확장 생성기")
    print("=" * 60)
    
    # 기존 CSV 파일명 입력 (선택사항)
    existing_file = input("dongrae_88.csv").strip()
    if not existing_file:
        existing_file = None
    
    # 생성할 개수 입력
    try:
        easy_count = int(input("생성할 쉬움 난이도 프롬프트 개수 (기본: 50): ") or "50")
        hard_count = int(input("생성할 어려움 난이도 프롬프트 개수 (기본: 50): ") or "50")
    except ValueError:
        print("잘못된 입력입니다. 기본값을 사용합니다.")
        easy_count, hard_count = 50, 50
    
    # 프롬프트 생성기 초기화
    expander = DongraePromptExpander(existing_file)
    
    # 추가 프롬프트 생성
    new_prompts = expander.generate_additional_prompts(easy_count, hard_count)
    
    # CSV 파일 저장
    filename = expander.save_prompts_to_csv(new_prompts, f"easy{easy_count}_hard{hard_count}")
    
    # 결과 통계
    intent_stats = {}
    difficulty_stats = {}
    
    for prompt_data in new_prompts:
        intent = prompt_data['intent']
        difficulty = prompt_data['difficulty']
        
        intent_stats[intent] = intent_stats.get(intent, 0) + 1
        difficulty_stats[difficulty] = difficulty_stats.get(difficulty, 0) + 1
    
    print(f"\n✅ 추가 프롬프트 생성 완료!")
    print(f"📁 파일명: {filename}")
    print(f"📊 총 프롬프트 수: {len(new_prompts)}개")
    
    print(f"\n📈 의도별 분포:")
    for intent, count in intent_stats.items():
        print(f"  • {intent}: {count}개")
    
    print(f"\n📊 난이도별 분포:")
    for difficulty, count in difficulty_stats.items():
        print(f"  • {difficulty}: {count}개")
    
    print(f"\n🔍 중복 방지 기능:")
    print(f"  ✅ 기존 프롬프트와 중복 체크")
    print(f"  ✅ 유사도 기반 중복 제거")
    print(f"  ✅ 해시값 기반 중복 방지")
    
    # 샘플 프롬프트 출력
    print(f"\n📝 생성된 프롬프트 샘플:")
    for i, prompt in enumerate(new_prompts[:5], 1):
        print(f"  {i}. [{prompt['difficulty']}] {prompt['prompt']}")
    
    print(f"\n🎉 작업 완료! {filename} 파일을 확인해주세요.")

if __name__ == "__main__":
    main()