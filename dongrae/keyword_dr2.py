"""
간단한 키워드 추출 도구
- LLM 없이 키워드 추출
- 터미널에서 결과 확인
- 법무법인 동래 사이트 전용
"""

import requests
import re
import time
from collections import Counter
from urllib.parse import quote
import csv

class SimpleKeywordExtractor:
    def __init__(self, website_url="https://www.dongraelaw.shop/"):
        self.website_url = website_url
        self.brand_name = "법무법인 동래"
        self.location = "부산 연제"
        self.all_keywords = []
        
    def extract_from_website(self):
        """웹사이트에서 직접 키워드 추출"""
        print("🔍 1단계: 웹사이트에서 키워드 추출 중...")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(self.website_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # HTML에서 텍스트 추출 (간단한 방법)
                html = response.text
                
                # 제목 추출
                title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
                title = title_match.group(1) if title_match else ""
                
                # 메타 설명 추출
                meta_desc = re.search(r'<meta name="description" content="(.*?)"', html, re.IGNORECASE)
                description = meta_desc.group(1) if meta_desc else ""
                
                # HTML 태그 제거하고 텍스트만 추출
                text = re.sub(r'<[^>]+>', ' ', html)
                text = re.sub(r'\s+', ' ', text)
                
                # 한글 키워드 추출
                korean_words = re.findall(r'[가-힣]{2,}', text)
                
                print(f"   📄 제목: {title}")
                print(f"   📝 설명: {description}")
                print(f"   📊 추출된 한글 단어: {len(korean_words)}개")
                
                # 빈도수 계산
                word_count = Counter(korean_words)
                
                # 불용어 제거
                stopwords = {
                    '이것', '그것', '저것', '여기', '거기', '저기', '이곳', '그곳', '저곳',
                    '때문', '경우', '시간', '정도', '상태', '방법', '이후', '다음',
                    '모든', '각각', '전체', '일부', '하나', '다른', '같은', '새로운'
                }
                
                # 상위 키워드 선별 (불용어 제외)
                website_keywords = []
                for word, count in word_count.most_common(20):
                    if word not in stopwords and len(word) >= 2:
                        website_keywords.append((word, count))
                
                print("   🔝 웹사이트 주요 키워드:")
                for i, (word, count) in enumerate(website_keywords[:10], 1):
                    print(f"      {i}. {word} ({count}회)")
                
                return [word for word, count in website_keywords]
                
            else:
                print(f"   ❌ 웹사이트 접근 실패: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ 오류 발생: {e}")
            return []
    
    def extract_base_keywords(self):
        """기본 키워드 생성"""
        print("\n🔧 2단계: 기본 키워드 생성 중...")
        
        base_keywords = [
            # 브랜드 관련
            "법무법인 동래",
            "동래 법무법인",
            "법무법인동래",
            
            # 지역 + 서비스
            "연제 변호사",
            "연제구 변호사", 
            "부산 연제 변호사",
            "거제역 변호사",
            "시청역 변호사",
            "연산역 변호사",
            
            # 서비스 키워드
            "연제 법률상담",
            "연제 법무법인",
            "부산 연제 법무법인",
            "연제구 법률상담",
            
            # 전문 분야
            "연제 민사소송",
            "연제 형사변호",
            "연제 이혼변호사",
            "연제 상속변호사",
            "연제 교통사고",
            "연제 기업법무",
            "연제 부동산",
            "연제 채권회수"
        ]
        
        print(f"   ✅ {len(base_keywords)}개 기본 키워드 생성")
        print("   📋 기본 키워드 목록:")
        for i, keyword in enumerate(base_keywords, 1):
            print(f"      {i}. {keyword}")
        
        return base_keywords
    
    def extract_naver_autocomplete(self, seed_keywords):
        """네이버 자동완성에서 키워드 추출"""
        print("\n🔍 3단계: 네이버 자동완성 키워드 수집 중...")
        
        all_suggestions = []
        
        # 주요 시드 키워드만 사용 (API 호출 최소화)
        main_seeds = [
            "연제 변호사",
            "법무법인 동래",
            "연제 법률상담",
            "부산 연제 변호사"
        ]
        
        for seed in main_seeds:
            print(f"   🔎 '{seed}' 자동완성 검색...")
            
            try:
                url = "https://ac.search.naver.com/nx/ac"
                params = {
                    'q': seed,
                    'con': '0',
                    'frm': 'nv',
                    'ans': '2'
                }
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                }
                
                response = requests.get(url, params=params, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    suggestions = []
                    
                    for item in data.get('items', []):
                        for suggestion in item:
                            if isinstance(suggestion, list) and len(suggestion) > 0:
                                keyword = suggestion[0]
                                if keyword and isinstance(keyword, str):
                                    suggestions.append(keyword.strip())
                    
                    unique_suggestions = list(set(suggestions))
                    all_suggestions.extend(unique_suggestions)
                    
                    print(f"      → {len(unique_suggestions)}개 키워드 발견")
                    for suggestion in unique_suggestions[:5]:
                        print(f"         • {suggestion}")
                
                time.sleep(1)  # API 호출 간격 조절
                
            except Exception as e:
                print(f"      ❌ {seed} 자동완성 실패: {e}")
        
        # 중복 제거
        unique_all = list(set(all_suggestions))
        print(f"   ✅ 총 {len(unique_all)}개 네이버 자동완성 키워드 수집")
        
        return unique_all
    
    def generate_pattern_keywords(self, base_keywords):
        """패턴 기반 키워드 확장"""
        print("\n🔧 4단계: 패턴 기반 키워드 확장 중...")
        
        # 법률 관련 용어
        law_terms = [
            "상담", "비용", "수임료", "추천", "후기", "평가", "순위",
            "민사", "형사", "이혼", "상속", "교통사고", "부동산", 
            "기업법무", "채권회수", "손해배상", "계약", "소송", "변호"
        ]
        
        # 지역 확장
        locations = [
            "부산", "연제구", "연제", "거제역", "시청역", "연산역",
            "토현동", "거제동", "연산동", "경남"
        ]
        
        # 의도 키워드
        intents = [
            "무료상담", "초기상담", "전화상담", "방문상담",
            "24시간", "주말상담", "야간상담", "온라인상담",
            "전문", "경험", "실력", "믿을만한", "유명한"
        ]
        
        pattern_keywords = []
        
        # 지역 + 법률 용어 조합
        for location in locations[:3]:  # 주요 지역만
            for law_term in law_terms:
                pattern_keywords.extend([
                    f"{location} {law_term}",
                    f"{location} 변호사 {law_term}",
                    f"{location} 법무법인 {law_term}"
                ])
        
        # 브랜드 + 의도 조합
        brand_terms = ["법무법인 동래", "동래", "연제"]
        for brand in brand_terms:
            for intent in intents:
                pattern_keywords.extend([
                    f"{brand} {intent}",
                    f"{intent} {brand}"
                ])
        
        # 중복 제거
        unique_pattern = list(set(pattern_keywords))
        
        print(f"   ✅ {len(unique_pattern)}개 패턴 키워드 생성")
        print("   📋 패턴 키워드 예시:")
        for i, keyword in enumerate(unique_pattern[:10], 1):
            print(f"      {i}. {keyword}")
        
        return unique_pattern
    
    def create_conversational_keywords(self, base_keywords):
        """대화형 키워드 생성 (AI 검색용)"""
        print("\n💬 5단계: 대화형 키워드 생성 중...")
        
        conversation_patterns = [
            "{}에 대해 알려줘",
            "{}를 추천해줘",
            "{}가 어때?",
            "{}의 장단점이 뭐야?",
            "{}를 선택해야 할까?",
            "{}에서 상담받고 싶어",
            "{}의 비용은 얼마야?",
            "{}는 믿을만해?",
            "{}의 평판은 어때?",
            "{}에서 소송하면 어떨까?"
        ]
        
        conversational_keywords = []
        
        # 주요 키워드만 사용
        main_keywords = [
            "법무법인 동래",
            "부산 변호사", 
            "부산 법무법인",
            "부산 동래 변호사"
        ]
        
        for keyword in main_keywords:
            for pattern in conversation_patterns:
                conversational_keywords.append(pattern.format(keyword))
        
        print(f"   ✅ {len(conversational_keywords)}개 대화형 키워드 생성")
        print("   📋 대화형 키워드 예시:")
        for i, keyword in enumerate(conversational_keywords[:8], 1):
            print(f"      {i}. {keyword}")
        
        return conversational_keywords
    
    def save_keywords_to_file(self, all_keywords, filename="extracted_keywords.csv"):
        """키워드를 파일로 저장"""
        print(f"\n💾 6단계: 키워드를 {filename}에 저장 중...")
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['번호', '키워드', '길이', '단어수', '유형'])
                
                for i, (keyword, keyword_type) in enumerate(all_keywords, 1):
                    word_count = len(keyword.split())
                    writer.writerow([i, keyword, len(keyword), word_count, keyword_type])
            
            print(f"   ✅ {len(all_keywords)}개 키워드가 {filename}에 저장됨")
            
        except Exception as e:
            print(f"   ❌ 파일 저장 오류: {e}")
    
    def run_extraction(self):
        """전체 키워드 추출 실행"""
        print("=" * 60)
        print("🚀 법무법인 동래 키워드 추출 시작!")
        print(f"🔗 대상 웹사이트: {self.website_url}")
        print("=" * 60)
        
        all_keywords = []
        
        # 1. 웹사이트에서 키워드 추출
        website_keywords = self.extract_from_website()
        for keyword in website_keywords:
            all_keywords.append((keyword, "웹사이트"))
        
        # 2. 기본 키워드 생성
        base_keywords = self.extract_base_keywords()
        for keyword in base_keywords:
            all_keywords.append((keyword, "기본"))
        
        # 3. 네이버 자동완성
        naver_keywords = self.extract_naver_autocomplete(base_keywords)
        for keyword in naver_keywords:
            all_keywords.append((keyword, "네이버"))
        
        # 4. 패턴 확장
        pattern_keywords = self.generate_pattern_keywords(base_keywords)
        for keyword in pattern_keywords:
            all_keywords.append((keyword, "패턴"))
        
        # 5. 대화형 키워드
        conversational_keywords = self.create_conversational_keywords(base_keywords)
        for keyword in conversational_keywords:
            all_keywords.append((keyword, "대화형"))
        
        # 중복 제거 (키워드만 기준으로)
        seen_keywords = set()
        unique_keywords = []
        for keyword, keyword_type in all_keywords:
            if keyword.lower() not in seen_keywords:
                seen_keywords.add(keyword.lower())
                unique_keywords.append((keyword, keyword_type))
        
        # 6. 결과 저장
        self.save_keywords_to_file(unique_keywords)
        
        # 7. 최종 결과 출력
        print("\n" + "=" * 60)
        print("🎉 키워드 추출 완료!")
        print("=" * 60)
        
        # 유형별 통계
        type_counts = {}
        for keyword, keyword_type in unique_keywords:
            type_counts[keyword_type] = type_counts.get(keyword_type, 0) + 1
        
        print("📊 추출 결과 통계:")
        for keyword_type, count in type_counts.items():
            print(f"   • {keyword_type}: {count}개")
        
        print(f"\n🔢 총 키워드 개수: {len(unique_keywords)}개")
        
        # 전체 키워드 출력
        print(f"\n📋 전체 추출된 키워드 목록:")
        print("-" * 60)
        
        current_type = ""
        for i, (keyword, keyword_type) in enumerate(unique_keywords, 1):
            if keyword_type != current_type:
                current_type = keyword_type
                print(f"\n[{keyword_type} 키워드]")
            print(f"{i:3d}. {keyword}")
        
        print("\n" + "=" * 60)
        print("✅ 모든 작업이 완료되었습니다!")
        print("📁 'extracted_keywords.csv' 파일을 확인하세요.")
        print("=" * 60)
        
        return unique_keywords

# 실행 함수
def main():
    """메인 실행 함수"""
    extractor = SimpleKeywordExtractor()
    keywords = extractor.run_extraction()
    return keywords

if __name__ == "__main__":
    print("🔥 법무법인 동래 키워드 추출을 시작합니다!")
    keywords = main()