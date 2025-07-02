"""
키워드 추출 코드 - 초보자용 단계별 실행 가이드
법무법인 동래를 위한 키워드 자동 수집
"""

# 1단계: 필요한 라이브러리 설치 및 임포트
import requests
import json
import time
import csv
from typing import List, Dict
from urllib.parse import quote

class SimpleKeywordExtractor:
    """간단한 키워드 추출기 - 초보자용"""
    
    def __init__(self):
        self.brand_name = "법무법인 동래"
        self.location = "연제구"
        self.keywords = []
        
    def get_naver_autocomplete(self, query: str) -> List[str]:
        """네이버 자동완성 키워드 가져오기"""
        print(f"🔍 네이버에서 '{query}' 자동완성 검색 중...")
        
        try:
            # 네이버 자동완성 API 호출
            url = "https://ac.search.naver.com/nx/ac"
            params = {
                'q': query,
                'con': '0',
                'frm': 'nv',
                'ans': '2'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                suggestions = []
                
                # JSON 응답에서 키워드 추출
                for item in data.get('items', []):
                    for suggestion in item:
                        if isinstance(suggestion, list) and len(suggestion) > 0:
                            keyword = suggestion[0]
                            if keyword and isinstance(keyword, str) and len(keyword.strip()) > 0:
                                suggestions.append(keyword.strip())
                
                # 중복 제거 및 정리
                unique_suggestions = list(set(suggestions))
                print(f"   ✅ {len(unique_suggestions)}개 키워드 발견")
                
                # 결과 출력
                for i, keyword in enumerate(unique_suggestions[:10], 1):
                    print(f"   {i}. {keyword}")
                
                return unique_suggestions
            else:
                print(f"   ❌ 오류: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ 네이버 자동완성 오류: {e}")
            return []
    
    def generate_pattern_keywords(self, base_keywords: List[str]) -> List[str]:
        """패턴 기반 키워드 생성"""
        print("🔧 패턴 기반 키워드 생성 중...")
        
        # 법률 관련 키워드 패턴
        law_terms = [
            "상담", "비용", "추천", "후기", "순위", "전문",
            "민사", "형사", "이혼", "상속", "교통사고", "부동산",
            "소송", "변호", "자문", "의뢰", "선임", "수임료"
        ]
        
        location_terms = [
            "부산", "연제구", "연제", "거제역", "시청역", "연산역", 
            "토현동", "거제동", "연산동", "거제해법"
        ]
        
        service_terms = [
            "무료상담", "초기상담", "전화상담", "방문상담",
            "24시간", "주말상담", "야간상담", "온라인상담"
        ]
        
        generated = []
        
        for base in base_keywords:
            # 법률 용어 조합
            for term in law_terms:
                generated.extend([
                    f"{base} {term}",
                    f"{term} {base}",
                ])
            
            # 지역 용어 조합
            for location in location_terms:
                generated.extend([
                    f"{location} 변호사",
                    f"{location} 법무법인",
                    f"{location} 법률상담"
                ])
            
            # 서비스 용어 조합
            for service in service_terms:
                generated.extend([
                    f"{base} {service}",
                    f"동래 {service}"
                ])
        
        # 중복 제거
        unique_generated = list(set(generated))
        print(f"   ✅ {len(unique_generated)}개 패턴 키워드 생성")
        
        return unique_generated
    
    def create_conversational_keywords(self, base_keywords: List[str]) -> List[str]:
        """대화형 키워드 생성 (ChatGPT/Claude 용)"""
        print("💬 대화형 키워드 생성 중...")
        
        conversational_patterns = [
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
        
        for base in base_keywords[:5]:  # 처음 5개만 사용
            for pattern in conversational_patterns:
                conversational_keywords.append(pattern.format(base))
        
        print(f"   ✅ {len(conversational_keywords)}개 대화형 키워드 생성")
        
        return conversational_keywords
    
    def save_keywords_to_csv(self, keywords: List[str], filename: str = "keywords.csv"):
        """키워드를 CSV 파일로 저장"""
        print(f"💾 키워드를 {filename} 파일로 저장 중...")
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['번호', '키워드', '길이', '단어수'])
                
                for i, keyword in enumerate(keywords, 1):
                    word_count = len(keyword.split())
                    writer.writerow([i, keyword, len(keyword), word_count])
            
            print(f"   ✅ {len(keywords)}개 키워드가 {filename}에 저장됨")
            
        except Exception as e:
            print(f"   ❌ 파일 저장 오류: {e}")
    
    def extract_keywords_step_by_step(self):
        """단계별 키워드 추출 실행"""
        print("=" * 50)
        print("🚀 법무법인 동래 키워드 추출 시작!")
        print("=" * 50)
        
        all_keywords = []
        
        # 1단계: 기본 시드 키워드
        print("\n📋 1단계: 기본 시드 키워드 설정")
        seed_keywords = [
            "연제 변호사",
            "법무법인 동래", 
            "연제 법률상담",
            "연제구 법무법인",
            "부산 연제 변호사",
            "거제역 변호사"
        ]
        
        for keyword in seed_keywords:
            print(f"   • {keyword}")
        
        all_keywords.extend(seed_keywords)
        
        # 2단계: 네이버 자동완성
        print("\n🔍 2단계: 네이버 자동완성 키워드 수집")
        naver_keywords = []
        
        for seed in seed_keywords:
            time.sleep(1)  # API 호출 간격 조절
            suggestions = self.get_naver_autocomplete(seed)
            naver_keywords.extend(suggestions)
        
        # 중복 제거
        naver_keywords = list(set(naver_keywords))
        all_keywords.extend(naver_keywords)
        
        print(f"   📊 네이버에서 총 {len(naver_keywords)}개 키워드 수집")
        
        # 3단계: 패턴 기반 확장
        print("\n🔧 3단계: 패턴 기반 키워드 확장")
        pattern_keywords = self.generate_pattern_keywords(seed_keywords)
        all_keywords.extend(pattern_keywords)
        
        # 4단계: 대화형 키워드 생성
        print("\n💬 4단계: 대화형 키워드 생성")
        conversational_keywords = self.create_conversational_keywords(seed_keywords)
        all_keywords.extend(conversational_keywords)
        
        # 5단계: 중복 제거 및 정리
        print("\n🧹 5단계: 중복 제거 및 정리")
        unique_keywords = list(set(all_keywords))
        
        # 너무 짧거나 긴 키워드 제거
        filtered_keywords = [
            kw for kw in unique_keywords 
            if 2 <= len(kw) <= 50 and kw.strip()
        ]
        
        print(f"   📊 전체 수집: {len(all_keywords)}개")
        print(f"   📊 중복 제거: {len(unique_keywords)}개") 
        print(f"   📊 필터링 후: {len(filtered_keywords)}개")
        
        # 6단계: 결과 저장
        print("\n💾 6단계: 결과 저장")
        self.save_keywords_to_csv(filtered_keywords, "yeonje_keywords.csv")
        
        # 7단계: 결과 요약
        print("\n📊 7단계: 결과 요약")
        print("=" * 50)
        print(f"🎉 총 {len(filtered_keywords)}개 키워드 추출 완료!")
        print("\n🔝 상위 20개 키워드:")
        
        for i, keyword in enumerate(filtered_keywords[:20], 1):
            print(f"   {i:2d}. {keyword}")
        
        print(f"\n💾 모든 키워드가 'yeonje_keywords.csv' 파일에 저장되었습니다.")
        print("   엑셀에서 열어서 확인할 수 있습니다.")
        
        return filtered_keywords

# 간단한 ChatGPT API 활용 (선택사항)
class ChatGPTKeywordGenerator:
    """ChatGPT를 활용한 키워드 생성"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        
    def generate_keywords_with_chatgpt(self, prompt: str) -> List[str]:
        """ChatGPT API로 키워드 생성"""
        if not self.api_key:
            print("❌ OpenAI API 키가 없습니다. 수동 입력으로 진행하세요.")
            return []
        
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            # 응답에서 키워드 추출
            content = response.choices[0].message.content
            keywords = [line.strip() for line in content.split('\n') if line.strip()]
            
            return keywords
            
        except Exception as e:
            print(f"❌ ChatGPT API 오류: {e}")
            return []

# 실행 함수들
def run_basic_extraction():
    """기본 키워드 추출 실행"""
    extractor = SimpleKeywordExtractor()
    keywords = extractor.extract_keywords_step_by_step()
    return keywords

def run_with_chatgpt(api_key: str):
    """ChatGPT를 포함한 키워드 추출"""
    
    # 기본 추출 먼저 실행
    basic_keywords = run_basic_extraction()
    
    # ChatGPT 추가 생성
    print("\n🤖 ChatGPT로 추가 키워드 생성 중...")
    
    chatgpt = ChatGPTKeywordGenerator(api_key)
    
    prompt = f"""
    부산 연제구에 있는 '법무법인 동래'의 온라인 마케팅을 위한 키워드를 생성해주세요.
    
    현재까지 수집한 키워드: {', '.join(basic_keywords[:10])}
    
    위 키워드들을 참고해서 실제 사용자들이 검색할 만한 자연스러운 키워드 30개를 추가로 생성해주세요.
    각 키워드를 한 줄씩 작성해주세요.
    """
    
    chatgpt_keywords = chatgpt.generate_keywords_with_chatgpt(prompt)
    
    if chatgpt_keywords:
        print(f"   ✅ ChatGPT에서 {len(chatgpt_keywords)}개 추가 생성")
        
        # 전체 키워드 합치기
        all_keywords = basic_keywords + chatgpt_keywords
        unique_all = list(set(all_keywords))
        
        # 다시 저장
        extractor = SimpleKeywordExtractor()
        extractor.save_keywords_to_csv(unique_all, "yeonje_keywords_with_ai.csv")
        
        print(f"🎉 총 {len(unique_all)}개 키워드를 'yeonje_keywords_with_ai.csv'에 저장!")
        
        return unique_all
    else:
        return basic_keywords

# 메인 실행 함수
if __name__ == "__main__":
    print("🔥 키워드 추출 시작!")
    print("\n선택하세요:")
    print("1. 기본 추출 (무료, API 키 불필요)")
    print("2. ChatGPT 포함 추출 (유료, OpenAI API 키 필요)")
    
    choice = input("\n선택 (1 또는 2): ").strip()
    
    if choice == "1":
        print("\n🚀 기본 키워드 추출을 시작합니다...")
        keywords = run_basic_extraction()
        
    elif choice == "2":
        api_key = input("\nOpenAI API 키를 입력하세요: ").strip()
        if api_key:
            print("\n🚀 ChatGPT 포함 키워드 추출을 시작합니다...")
            keywords = run_with_chatgpt(api_key)
        else:
            print("❌ API 키가 없어서 기본 추출로 진행합니다.")
            keywords = run_basic_extraction()
    else:
        print("❌ 잘못된 선택입니다. 기본 추출로 진행합니다.")
        keywords = run_basic_extraction()
    
    print("\n✅ 모든 작업이 완료되었습니다!")
    print("📁 생성된 파일을 엑셀에서 열어서 확인하세요.")