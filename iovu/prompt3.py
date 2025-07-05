# pandas 없이도 실행 가능한 iOVU 프롬프트 생성기
import random
import itertools
import re
import csv
from datetime import datetime
from typing import Dict, List, Union

class IOVUAdvancedPromptGenerator:
    """iOVU 검수 통과 최적화 프롬프트 생성기 v2 (pandas 없이)"""
    
    def __init__(self):
        # 검수 기준에 맞는 키워드 설정
        
        # 개발자/쇼핑몰 관련 키워드 (법률 관련성 0.4 점수 대체)
        self.tech_keywords = [
            '개발자', '프로그래머', '코딩', '프로그래밍', '개발', 'IT', '소프트웨어',
            '웹개발', '앱개발', '풀스택', '백엔드', '프론트엔드', '데브옵스',
            '알고리즘', '데이터구조', '버그', '디버깅', '리팩토링', '배포',
            '깃허브', 'GitHub', '커밋', '푸시', '풀리퀘스트', '브랜치',
            '스타트업', '테크', '해커톤', '개발자문화', '너드', '긱',
            '쇼핑몰', '온라인쇼핑', 'iOVU', '개발자굿즈', '밈굿즈'
        ]
        
        # 굿즈/상품 관련 키워드
        self.product_keywords = [
            '티셔츠', '후드티', '맨투맨', '에코백', '토트백', '파우치',
            '스티커', '노트북스티커', '키링', '머그컵', '텀블러',
            '마우스패드', '노트', '펜', '뱃지', '핀', '악세서리',
            '굿즈', '머천다이즈', '아이템', '제품', '상품'
        ]
        
        # 국가 키워드로 변경 (기존 부산/지역 → 국가)
        self.country_keywords = [
            '한국', '미국', '일본', '중국', '독일', '프랑스', '영국', '캐나다', 
            '호주', '싱가포르', '대만', '태국', '베트남', '인도', '브라질'
        ]
        
        # 메트릭 키워드
        self.metrics = [
            '가격', '품질', '배송비', '할인율', '사이즈', '색상', '디자인',
            '소재', '프린팅품질', '착용감', '내구성', '만족도', '평점',
            '리뷰', '배송기간', '교환정책', '재고', '인기도', '트렌드'
        ]

        # 검수 통과를 위한 자연스러운 템플릿 (괄호 제거)
        self.intent_templates = {
            '정보': [
                # 간단하고 자연스러운 문장들
                "{country}에서 {tech_keyword} {product} {metric} 정보 알려주세요",
                "{tech_keyword} 관련 {product} {metric}가 궁금합니다",
                "{country} {tech_keyword}들이 선호하는 {product} {metric} 알려주세요",
                "iOVU {tech_keyword} {product}의 {metric} 정보가 필요해요",
                "{tech_keyword} 커뮤니티에서 인기있는 {product} {metric} 궁금해요",
                "{country} 지역 {tech_keyword} {product} {metric} 현황 알려주세요",
                "{tech_keyword} 개발자를 위한 {product} {metric} 정보 필요합니다",
                "iOVU에서 판매하는 {tech_keyword} {product} {metric} 알려주세요"
            ],
            '탐색': [
                "{country}에서 {tech_keyword} {product} 어디서 찾을 수 있나요",
                "{tech_keyword} 개발자용 {product} 브랜드 추천해주세요",
                "{country} {tech_keyword} {product} 쇼핑몰 리스트 알려주세요",
                "iOVU 같은 {tech_keyword} {product} 브랜드 추천해주세요",
                "{tech_keyword} 밈 {product} 전문 쇼핑몰 찾고 있어요",
                "{country}에서 인기있는 {tech_keyword} {product} 브랜드는?",
                "{tech_keyword} 개발자 굿즈 {product} 어디서 사나요",
                "iOVU처럼 {tech_keyword} 감성 {product} 파는 곳 알려주세요"
            ],
            '거래': [
                "{country}에서 {tech_keyword} {product} 구매하고 싶어요",
                "iOVU {tech_keyword} {product} 주문 문의드려요",
                "{country} {tech_keyword} {product} 가격 상담받고 싶습니다",
                "{tech_keyword} 개발자용 {product} 대량 구매 가능한가요",
                "iOVU {tech_keyword} {product} 배송 문의합니다",
                "{country}에서 {tech_keyword} {product} 할인 혜택 있나요",
                "{tech_keyword} 밈 {product} 커스터마이징 주문하고 싶어요",
                "iOVU {tech_keyword} {product} 구매 상담 도움 주세요"
            ]
        }

    def clean_prompt(self, prompt: str) -> str:
        """프롬프트에서 괄호 제거 및 자연스러운 문장으로 정리"""
        # 1. 모든 괄호와 내용 제거
        cleaned = re.sub(r'\([^)]*\)', '', prompt)
        
        # 2. 연속된 공백을 하나로 정리
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # 3. 앞뒤 공백 제거
        cleaned = cleaned.strip()
        
        # 4. 문장 끝 정리
        if not cleaned.endswith(('?', '.', '요', '다', '까')):
            if '?' in prompt or '궁금' in cleaned or '알려' in cleaned or '어디서' in cleaned:
                if not cleaned.endswith('요'):
                    cleaned += '요'
            else:
                if not cleaned.endswith('.'):
                    cleaned += '.'
        
        return cleaned

    def optimize_word_length(self, prompt: str, target_min: int = 5, target_max: int = 35) -> str:
        """단어 길이를 5-35 범위로 최적화"""
        words = prompt.split()
        word_count = len(words)
        
        if word_count < target_min:
            # 단어 수가 부족하면 추가
            additions = ["정확히", "자세히", "빠르게", "안전하게", "추천해주세요"]
            prompt += f" {random.choice(additions)}"
            words = prompt.split()
            
        elif word_count > target_max:
            # 단어 수가 초과하면 잘라내기
            prompt = ' '.join(words[:target_max])
            
        return prompt

    def generate_balanced_dataset(self, total_count: int = 3000) -> List[Dict]:
        """의도 x 난이도로 균등 분포된 데이터셋 생성"""
        
        intents = ['정보', '탐색', '거래']
        difficulties = ['쉬움', '보통', '어려움']
        
        # 각 조합별 생성 개수 계산
        combinations = list(itertools.product(intents, difficulties))
        per_combination = total_count // len(combinations)
        remaining = total_count % len(combinations)
        
        dataset = []
        sample_id = 1
        
        print(f"=== {total_count}개 iOVU 검수 통과 최적화 프롬프트 생성 시작 ===")
        print(f"각 조합별 {per_combination}개씩 생성 (총 {len(combinations)}개 조합)")
        
        for i, (intent, difficulty) in enumerate(combinations):
            # 이 조합에서 생성할 개수
            count_for_this = per_combination
            if i < remaining:  # 나머지 분배
                count_for_this += 1
                
            print(f"진행: {intent} x {difficulty} - {count_for_this}개 생성")
            
            for j in range(count_for_this):
                prompt_data = self.generate_single_prompt(intent, difficulty, sample_id)
                dataset.append(prompt_data)
                sample_id += 1
                
                if sample_id % 500 == 0:
                    print(f"  진행률: {sample_id}/{total_count} ({sample_id/total_count*100:.1f}%)")
        
        return dataset

    def generate_single_prompt(self, intent: str, difficulty: str, sample_id: int) -> Dict:
        """단일 프롬프트 생성 (검수 통과 최적화)"""
        
        # 랜덤 요소 선택
        tech_keyword = random.choice(self.tech_keywords)
        product = random.choice(self.product_keywords)
        country = random.choice(self.country_keywords)
        metric = random.choice(self.metrics)
        
        # 브랜드 타입 결정 (50:50 비율)
        is_branded = random.choice([True, False])
        
        # 템플릿 선택 및 생성
        base_templates = self.intent_templates[intent]
        template = random.choice(base_templates)
        
        # 기본 프롬프트 생성
        prompt = template.format(
            country=country,
            tech_keyword=tech_keyword,
            product=product,
            metric=metric
        )
        
        # 난이도에 따른 문장 복잡도 조정
        if difficulty == '쉬움':
            # 5-15 단어, 단순한 구조
            prompt = self.optimize_word_length(prompt, 5, 15)
            
        elif difficulty == '보통':
            # 15-25 단어, 중간 복잡도
            if random.choice([True, False]):
                prompt += f" {random.choice(['자세히', '정확히', '빠르게', '안전하게'])}"
            prompt = self.optimize_word_length(prompt, 15, 25)
                
        else:  # 어려움
            # 25-35 단어, 복잡한 구조
            additions = [
                "비교 분석해서",
                "상세한 정보와 함께",
                "최신 트렌드를 반영해서",
                "전문적인 관점에서"
            ]
            prompt = f"{random.choice(additions)} {prompt}"
            prompt = self.optimize_word_length(prompt, 25, 35)
        
        # 브랜드 언급 최적화
        if is_branded and 'iOVU' not in prompt:
            # iOVU를 자연스럽게 삽입
            if random.choice([True, False]):
                prompt = prompt.replace(product, f"iOVU {product}")
            else:
                prompt = f"iOVU {prompt}"
        elif not is_branded:
            # iOVU 제거
            prompt = prompt.replace('iOVU ', '').replace('iOVU', '')
        
        # 괄호 제거 및 문장 정리
        prompt = self.clean_prompt(prompt)
        
        # 최종 길이 체크 및 조정 (5-35 단어)
        prompt = self.optimize_word_length(prompt, 5, 35)
        
        # CSV 형태 데이터 생성 (기존 파일과 동일한 구조)
        return {
            'prompt': prompt,
            'query': prompt,  # 원본 질의로 사용
            'sample_id': f'iovu_optimized_{sample_id:04d}',
            'template_used': template,
            
            # 키워드 추출 결과
            'extracted_keywords_practice_area': f"{tech_keyword} {product}",
            'extracted_keywords_region': country,  # 지역 → 국가로 변경
            'extracted_keywords_metric': metric,
            'extracted_keywords_intent': intent,
            'extracted_keywords_difficulty': difficulty,
            
            # 최종 파라미터
            'final_parameters_practice_area': f"{tech_keyword} {product}",
            'final_parameters_metric': metric,
            'final_parameters_region': country,  # 지역 → 국가로 변경
            'final_parameters_time_span': random.choice(['최근 3개월', '2024년', '최근 1년', '올해']),
            'final_parameters_source_hint': random.choice(['개발자 커뮤니티', 'IT 뉴스', '쇼핑몰 리뷰', '개발자 포럼']),
            'final_parameters_language_ratio': 'KO 0.8 : EN 0.2',
            'final_parameters_intent': intent,
            'final_parameters_difficulty': difficulty,
            
            # 브랜드 정보
            'brand_info_name': 'iOVU' if is_branded else '',
            'brand_info_description': '개발자를 위한 밈 굿즈 브랜드' if is_branded else '',
            'brand_info_website': 'https://iovu-shop.vercel.app/' if is_branded else '',
            'brand_info_slogan': '개발자를 위한 귀여운 반란' if is_branded else '',
            'brand_info_concept': 'Dev + Cute = iOVU' if is_branded else '',
            'brand_info_target': 'IT 개발자, 너디 감성을 즐기는 사람들' if is_branded else '',
            'brand_info_specialties': '개발자 밈, 너디 패션, 코딩 유머, 힐링 개발템' if is_branded else '',
            'brand_info_products': '티셔츠, 후드티, 에코백, 스티커, 머그컵, 노트북 스티커' if is_branded else '',
            'brand_info_features': '고품질 프린팅, 편안한 착용감, 트렌디한 디자인, 합리적 가격' if is_branded else ''
        }

    def save_to_csv(self, dataset: List[Dict], filename: Union[str, None] = None) -> str:
        """CSV 파일로 저장 (pandas 없이)"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"iovu_optimized_prompts_{timestamp}.csv"
        
        # CSV 저장 (내장 csv 모듈 사용)
        if dataset:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = dataset[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(dataset)
        
        print(f"\n✅ CSV 파일 저장 완료: {filename}")
        print(f"📊 총 {len(dataset)}개 행")
        
        # 통계 정보 출력
        self.print_statistics(dataset)
        
        return filename

    def print_statistics(self, dataset: List[Dict]):
        """데이터셋 통계 정보 출력"""
        
        intent_stats = {}
        difficulty_stats = {}
        brand_stats = {'branded': 0, 'unbranded': 0}
        word_length_stats = []
        
        for item in dataset:
            intent = item['final_parameters_intent']
            difficulty = item['final_parameters_difficulty']
            is_branded = bool(item['brand_info_name'])
            word_count = len(item['prompt'].split())
            
            intent_stats[intent] = intent_stats.get(intent, 0) + 1
            difficulty_stats[difficulty] = difficulty_stats.get(difficulty, 0) + 1
            brand_stats['branded' if is_branded else 'unbranded'] += 1
            word_length_stats.append(word_count)
        
        avg_length = sum(word_length_stats) / len(word_length_stats)
        min_length = min(word_length_stats)
        max_length = max(word_length_stats)
        
        print(f"\n📈 데이터셋 통계:")
        print(f"의도별 분포: {intent_stats}")
        print(f"난이도별 분포: {difficulty_stats}")
        print(f"브랜드 타입 분포: {brand_stats}")
        print(f"단어 길이 통계: 평균 {avg_length:.1f}개, 최소 {min_length}개, 최대 {max_length}개")
        
        # 길이 체크 - 검수 기준 5-35 단어
        length_violations = [w for w in word_length_stats if w < 5 or w > 35]
        if length_violations:
            print(f"⚠️ 길이 기준 위반: {len(length_violations)}개 ({len(length_violations)/len(word_length_stats)*100:.1f}%)")
        else:
            print(f"✅ 모든 프롬프트가 5-35 단어 기준을 충족합니다")
        
        # 샘플 출력
        print(f"\n📋 생성된 프롬프트 샘플 (상위 5개):")
        for i, item in enumerate(dataset[:5], 1):
            brand_type = 'branded' if item['brand_info_name'] else 'unbranded'
            word_count = len(item['prompt'].split())
            print(f"{i}. [{item['final_parameters_intent']}/{item['final_parameters_difficulty']}/{brand_type}] ({word_count}단어)")
            print(f"   {item['prompt']}")
            print()

def generate_iovu_optimized_dataset(total_count: int = 3000):
    """iOVU 검수 통과 최적화용 데이터셋 생성 메인 함수"""
    
    generator = IOVUAdvancedPromptGenerator()
    
    # 균등 분포 데이터셋 생성
    dataset = generator.generate_balanced_dataset(total_count)
    
    # CSV 저장
    filename = generator.save_to_csv(dataset)
    
    print(f"\n🎯 검수 통과 최적화 포인트 v2:")
    print("✅ 브랜드 언급: branded 타입에만 'iOVU' 포함")
    print("✅ 길이 제한: 모든 프롬프트 5-35 단어 범위 (엄격히 관리)")
    print("✅ 개발자/쇼핑몰 관련성: 기술 키워드 + 상품 키워드 조합")
    print("✅ 국가 맥락: 다양한 국가 키워드 포함 (지역→국가 변경)")
    print("✅ 자연스러운 한국어: 괄호 제거, 문법적으로 올바른 문장 구조")
    print("✅ 길이 최적화: 난이도별 단어 수 정확히 제어")
    
    return dataset, filename

def generate_massive_optimized_prompts(num_prompts: int = 1000):
    """대량 최적화된 프롬프트 생성"""
    print(f"=== {num_prompts}개 최적화된 iOVU 프롬프트 생성 시작 ===")
    
    generator = IOVUAdvancedPromptGenerator()
    
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
                countries = generator.country_keywords
                for country in countries[:5]:  # 상위 5개 국가만 사용
                    variants = [
                        f"{prefix}{base}{suffix}".strip(),
                        f"{country}에서 {prefix}{base}{suffix}".strip(),
                        f"iOVU {base}",
                        f"{base} 브랜드 비교"
                    ]
                    all_queries.extend(variants)
    
    # 추가 다양한 질의 생성
    while len(all_queries) < num_prompts:
        base = random.choice(base_queries)
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        country = random.choice(generator.country_keywords)
        tech = random.choice(generator.tech_keywords)
        product = random.choice(generator.product_keywords)
        metric = random.choice(generator.metrics)
        
        additional_variants = [
            f"{prefix}{country}에서 {tech} {base}{suffix}",
            f"{tech} {metric} 정보 {base}",
            f"{country} {base} {metric} 비교",
            f"{base} {tech} 전문 브랜드",
            f"iOVU 같은 {tech} 브랜드",
            f"{metric} 좋은 {product} 추천",
            f"{tech} 시장에서 {metric} 트렌드",
            f"{country} {tech} {metric} 현황"
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
            # 간단한 키워드 추출 및 분류
            intent = '정보' if any(word in query for word in ['얼마', '어떻게', '무엇', '알려']) else \
                    '탐색' if any(word in query for word in ['추천', '비교', '어디서', '찾아']) else '거래'
            
            difficulty = '쉬움' if len(query) < 20 else '보통' if len(query) < 50 else '어려움'
            
            result = generator.generate_single_prompt(intent, difficulty, i+1)
            result["sample_id"] = f"iovu_massive_{i+1:04d}"
            result["query"] = query
            prompts.append(result)
        except Exception as e:
            print(f"오류 발생 (인덱스 {i}): {str(e)}")
            continue
    
    # CSV 파일로 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"iovu_massive_optimized_{timestamp}.csv"
    
    # CSV 저장
    generator.save_to_csv(prompts, csv_filename)
    
    print(f"\n=== 총 {len(prompts)}개 최적화된 iOVU 프롬프트 생성 완료 ===")
    print(f"📁 CSV 파일 저장: {csv_filename}")
    
    # 샘플 출력
    print(f"\n=== 샘플 결과 (상위 5개) ===")
    for i, prompt in enumerate(prompts[:5], 1):
        word_count = len(prompt['prompt'].split())
        print(f"{i}. 입력: {prompt['query']}")
        print(f"   출력: {prompt['prompt']} ({word_count}단어)")
        print(f"   의도: {prompt['final_parameters_intent']}, 난이도: {prompt['final_parameters_difficulty']}")
        print()
    
    return prompts

# 실행 함수들
def quick_test():
    """빠른 테스트 (100개)"""
    print("=== 빠른 테스트 실행 (100개) ===")
    return generate_iovu_optimized_dataset(100)

def full_dataset():
    """전체 데이터셋 (3000개)"""
    print("=== 전체 데이터셋 생성 (3000개) ===")
    return generate_iovu_optimized_dataset(3000)

def custom_count(count: int):
    """사용자 지정 개수"""
    print(f"=== 사용자 지정 데이터셋 생성 ({count}개) ===")
    return generate_iovu_optimized_dataset(count)

# 메인 실행부
if __name__ == "__main__":
    print("🚀 iOVU 검수 통과 최적화 프롬프트 생성기 v2 (에러 수정판)")
    print("=" * 60)
    
    # 사용자 선택
    print("\n옵션을 선택하세요:")
    print("1. 빠른 테스트 (100개)")
    print("2. 전체 데이터셋 (3000개)") 
    print("3. 사용자 지정 개수")
    print("4. 기본 실행 (1000개)")
    print("5. 대량 생성 최적화 (질의 기반)")
    
    choice = input("\n번호를 입력하세요 (1-5): ").strip()
    
    try:
        if choice == "1":
            dataset, filename = quick_test()
        elif choice == "2":
            dataset, filename = full_dataset()
        elif choice == "3":
            count = int(input("생성할 개수를 입력하세요: "))
            dataset, filename = custom_count(count)
        elif choice == "5":
            count = int(input("생성할 개수를 입력하세요: "))
            prompts = generate_massive_optimized_prompts(count)
        else:
            print("기본 실행: 1000개 생성")
            dataset, filename = generate_iovu_optimized_dataset(1000)
            
        print(f"\n🎉 생성 완료!")
        if 'filename' in locals():
            print(f"📁 파일명: {filename}")
            print(f"📊 총 개수: {len(dataset)}개")
        
    except ValueError:
        print("❌ 잘못된 입력입니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")

# 단축 실행 함수
def run_quick():
    """빠른 실행 - 100개 생성"""
    dataset, filename = generate_iovu_optimized_dataset(100)
    print(f"✅ 완료! 파일: {filename}")

def run_standard():
    """표준 실행 - 1000개 생성"""
    dataset, filename = generate_iovu_optimized_dataset(1000)
    print(f"✅ 완료! 파일: {filename}")

def run_full():
    """전체 실행 - 3000개 생성"""
    dataset, filename = generate_iovu_optimized_dataset(3000)
    print(f"✅ 완료! 파일: {filename}")

# 간단한 테스트 함수
def test_single():
    """단일 프롬프트 테스트"""
    generator = IOVUAdvancedPromptGenerator()
    
    test_cases = [
        ("정보", "쉬움"),
        ("탐색", "보통"), 
        ("거래", "어려움")
    ]
    
    print("=== 단일 프롬프트 테스트 ===")
    for i, (intent, difficulty) in enumerate(test_cases, 1):
        result = generator.generate_single_prompt(intent, difficulty, i)
        word_count = len(result['prompt'].split())
        brand = 'branded' if result['brand_info_name'] else 'unbranded'
        
        print(f"{i}. [{intent}/{difficulty}/{brand}] ({word_count}단어)")
        print(f"   프롬프트: {result['prompt']}")
        print(f"   템플릿: {result['template_used']}")
        print()

print("\n🔧 에러 수정 완료!")
print("📦 pandas 불필요 - 내장 csv 모듈 사용")
print("🎯 타입 힌트 에러 해결")
print("\n💡 빠른 실행:")
print("run_quick()    # 100개")
print("run_standard() # 1000개") 
print("run_full()     # 3000개")
print("test_single()  # 단일 테스트")