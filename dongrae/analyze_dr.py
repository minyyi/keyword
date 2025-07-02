"""
웹사이트 키워드 추출 및 검색가능성 분석 도구
- 특정 웹사이트에서 키워드 추출
- 검색엔진에서 해당 사이트가 검색되는지 확인
- SEO/GEO 최적화를 위한 키워드 분석
"""

import requests
from bs4 import BeautifulSoup
import re
import csv
from collections import Counter
from urllib.parse import urljoin, urlparse
import time
import json
from typing import List, Dict, Set

class WebsiteKeywordExtractor:
    """웹사이트에서 키워드 추출 및 검색가능성 분석"""
    
    def __init__(self, website_url: str):
        self.website_url = website_url
        self.domain = urlparse(website_url).netloc
        self.extracted_keywords = {}
        self.search_results = {}
        
    def fetch_website_content(self) -> Dict:
        """웹사이트 콘텐츠 가져오기"""
        print(f"🔍 웹사이트 분석 중: {self.website_url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(self.website_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 메타 정보 추출
                title = soup.find('title').get_text() if soup.find('title') else ""
                meta_description = ""
                meta_keywords = ""
                
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc:
                    meta_description = meta_desc.get('content', '')
                
                meta_kw = soup.find('meta', attrs={'name': 'keywords'})
                if meta_kw:
                    meta_keywords = meta_kw.get('content', '')
                
                # 본문 텍스트 추출
                # 스크립트, 스타일 태그 제거
                for script in soup(["script", "style"]):
                    script.decompose()
                
                body_text = soup.get_text()
                
                # 헤딩 태그 추출
                headings = {}
                for i in range(1, 7):
                    h_tags = soup.find_all(f'h{i}')
                    headings[f'h{i}'] = [tag.get_text().strip() for tag in h_tags]
                
                # 링크 텍스트 추출
                links = soup.find_all('a')
                link_texts = [link.get_text().strip() for link in links if link.get_text().strip()]
                
                result = {
                    'status': 'success',
                    'title': title.strip(),
                    'meta_description': meta_description.strip(),
                    'meta_keywords': meta_keywords.strip(),
                    'body_text': body_text.strip(),
                    'headings': headings,
                    'link_texts': link_texts,
                    'url': self.website_url
                }
                
                print(f"   ✅ 웹사이트 분석 완료")
                print(f"   📄 제목: {title[:50]}...")
                print(f"   📝 메타 설명: {meta_description[:50]}...")
                
                return result
                
            else:
                print(f"   ❌ HTTP 오류: {response.status_code}")
                return {'status': 'error', 'message': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"   ❌ 웹사이트 접근 오류: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def extract_keywords_from_content(self, content: Dict) -> List[str]:
        """웹사이트 콘텐츠에서 키워드 추출"""
        print("🔤 키워드 추출 중...")
        
        if content['status'] != 'success':
            return []
        
        all_text = ""
        keywords = []
        
        # 제목에서 키워드 (가중치 높음)
        title_keywords = self.extract_keywords_from_text(content['title'])
        keywords.extend(title_keywords * 3)  # 제목 키워드에 3배 가중치
        
        # 메타 키워드
        if content['meta_keywords']:
            meta_kw = [kw.strip() for kw in content['meta_keywords'].split(',')]
            keywords.extend(meta_kw)
        
        # 메타 설명에서 키워드
        desc_keywords = self.extract_keywords_from_text(content['meta_description'])
        keywords.extend(desc_keywords * 2)  # 메타 설명에 2배 가중치
        
        # 헤딩에서 키워드 (가중치 높음)
        for heading_level, headings in content['headings'].items():
            for heading in headings:
                heading_keywords = self.extract_keywords_from_text(heading)
                weight = 3 if heading_level in ['h1', 'h2'] else 2
                keywords.extend(heading_keywords * weight)
        
        # 본문에서 키워드
        body_keywords = self.extract_keywords_from_text(content['body_text'])
        keywords.extend(body_keywords)
        
        # 링크 텍스트에서 키워드
        for link_text in content['link_texts']:
            link_keywords = self.extract_keywords_from_text(link_text)
            keywords.extend(link_keywords)
        
        # 빈도수 계산
        keyword_counter = Counter(keywords)
        
        # 상위 키워드 반환
        top_keywords = [kw for kw, count in keyword_counter.most_common(100)]
        
        print(f"   ✅ {len(top_keywords)}개 키워드 추출 완료")
        print("   🔝 상위 10개 키워드:")
        for i, (keyword, count) in enumerate(keyword_counter.most_common(10), 1):
            print(f"      {i}. {keyword} ({count}회)")
        
        return top_keywords
    
    def extract_keywords_from_text(self, text: str) -> List[str]:
        """텍스트에서 의미있는 키워드 추출"""
        if not text:
            return []
        
        # 텍스트 정제
        text = re.sub(r'[^\w\s가-힣]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 단어 분리
        words = text.split()
        
        # 불용어 제거
        stopwords = {
            '이', '그', '저', '것', '수', '있', '있는', '없는', '의', '가', '을', '를', '에', '와', '과',
            '도', '만', '은', '는', '이다', '하다', '되다', '있다', '없다', '같다', '다른', '이런', '그런',
            '저런', '어떤', '무엇', '누구', '언제', '어디', '어떻게', '왜', '그리고', '그러나', '하지만',
            '또는', '또', '및', '등', '것들', '모든', '각', '여러', '다양한', '많은', '적은', '크다', '작다'
        }
        
        # 유효한 키워드 필터링
        keywords = []
        for word in words:
            # 길이 조건 (2글자 이상 10글자 이하)
            if 2 <= len(word) <= 10:
                # 불용어가 아님
                if word.lower() not in stopwords:
                    # 숫자만으로 이루어지지 않음
                    if not word.isdigit():
                        keywords.append(word)
        
        return keywords
    
    def check_search_visibility(self) -> Dict:
        """검색엔진에서 웹사이트 검색 가능성 확인"""
        print("🔍 검색 가능성 분석 중...")
        
        search_queries = [
            self.domain,
            f'site:{self.domain}',
            '법무법인 동래',
            '동래 법무법인',
            '연제 법무법인',
            'dongraelaw'
        ]
        
        visibility_results = {}
        
        for query in search_queries:
            print(f"   🔎 테스트 쿼리: {query}")
            
            # 실제 검색 API 호출은 복잡하므로, 시뮬레이션
            # 실제로는 Google Custom Search API나 다른 검색 API 사용
            visibility_results[query] = {
                'query': query,
                'found': '시뮬레이션', # 실제로는 True/False
                'position': '테스트 필요',
                'snippet': '실제 검색 결과 필요'
            }
        
        print("   ⚠️  실제 검색 결과 확인은 수동으로 해야 합니다:")
        print("   1. Google에서 직접 검색")
        print("   2. Naver에서 직접 검색")
        print("   3. 검색 결과에서 사이트 확인")
        
        return visibility_results
    
    def generate_seo_keywords(self, existing_keywords: List[str]) -> List[str]:
        """SEO 최적화를 위한 추가 키워드 생성"""
        print("🚀 SEO 최적화 키워드 생성 중...")
        
        # 기본 키워드 패턴
        base_patterns = [
            "법무법인", "변호사", "법률상담", "소송", "변호", "법무"
        ]
        
        # 지역 키워드
        location_patterns = [
            "부산", "연제", "연제구", "거제역", "시청역", "동래"
        ]
        
        # 서비스 키워드  
        service_patterns = [
            "상담", "비용", "수임료", "추천", "후기", "평가", "순위",
            "민사", "형사", "이혼", "상속", "교통사고", "부동산", "기업법무"
        ]
        
        # 의도 키워드
        intent_patterns = [
            "방법", "절차", "과정", "준비", "신청", "의뢰", "선임", "문의"
        ]
        
        generated_keywords = []
        
        # 패턴 조합으로 키워드 생성
        for base in base_patterns:
            for location in location_patterns:
                generated_keywords.extend([
                    f"{location} {base}",
                    f"{base} {location}",
                ])
        
        for service in service_patterns:
            for location in location_patterns:
                generated_keywords.extend([
                    f"{location} {service}",
                    f"{location} 변호사 {service}",
                    f"{location} 법무법인 {service}"
                ])
        
        # 기존 키워드와 조합
        for existing in existing_keywords[:10]:  # 상위 10개만 사용
            for intent in intent_patterns:
                generated_keywords.extend([
                    f"{existing} {intent}",
                    f"{intent} {existing}"
                ])
        
        # 중복 제거
        unique_generated = list(set(generated_keywords))
        
        print(f"   ✅ {len(unique_generated)}개 SEO 키워드 생성")
        
        return unique_generated
    
    def save_analysis_results(self, content: Dict, keywords: List[str], 
                            seo_keywords: List[str], visibility: Dict, 
                            filename: str = "website_analysis.csv"):
        """분석 결과를 CSV 파일로 저장"""
        print(f"💾 분석 결과를 {filename}에 저장 중...")
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                
                # 웹사이트 기본 정보
                writer.writerow(['=== 웹사이트 기본 정보 ==='])
                writer.writerow(['항목', '내용'])
                writer.writerow(['URL', self.website_url])
                writer.writerow(['제목', content.get('title', '')])
                writer.writerow(['메타 설명', content.get('meta_description', '')])
                writer.writerow(['메타 키워드', content.get('meta_keywords', '')])
                writer.writerow([])
                
                # 추출된 키워드
                writer.writerow(['=== 추출된 키워드 ==='])
                writer.writerow(['순번', '키워드', '유형'])
                
                for i, keyword in enumerate(keywords, 1):
                    writer.writerow([i, keyword, '웹사이트 추출'])
                
                writer.writerow([])
                
                # SEO 키워드
                writer.writerow(['=== SEO 최적화 키워드 ==='])
                writer.writerow(['순번', '키워드', '유형'])
                
                for i, keyword in enumerate(seo_keywords, 1):
                    writer.writerow([i, keyword, 'SEO 생성'])
                
                writer.writerow([])
                
                # 검색 가능성
                writer.writerow(['=== 검색 가능성 분석 ==='])
                writer.writerow(['검색어', '결과', '비고'])
                
                for query, result in visibility.items():
                    writer.writerow([query, result['found'], '수동 확인 필요'])
            
            print(f"   ✅ 분석 결과가 {filename}에 저장됨")
            
        except Exception as e:
            print(f"   ❌ 파일 저장 오류: {e}")
    
    def run_full_analysis(self):
        """전체 분석 실행"""
        print("=" * 60)
        print(f"🚀 웹사이트 키워드 분석 시작: {self.website_url}")
        print("=" * 60)
        
        # 1. 웹사이트 콘텐츠 가져오기
        print("\n1️⃣ 웹사이트 콘텐츠 분석")
        content = self.fetch_website_content()
        
        if content['status'] != 'success':
            print(f"❌ 웹사이트 분석 실패: {content.get('message', '알 수 없는 오류')}")
            return
        
        # 2. 키워드 추출
        print("\n2️⃣ 웹사이트에서 키워드 추출")
        extracted_keywords = self.extract_keywords_from_content(content)
        
        # 3. SEO 키워드 생성
        print("\n3️⃣ SEO 최적화 키워드 생성")
        seo_keywords = self.generate_seo_keywords(extracted_keywords)
        
        # 4. 검색 가능성 확인
        print("\n4️⃣ 검색 가능성 분석")
        visibility_results = self.check_search_visibility()
        
        # 5. 결과 저장
        print("\n5️⃣ 결과 저장")
        filename = f"{self.domain.replace('.', '_')}_analysis.csv"
        self.save_analysis_results(content, extracted_keywords, seo_keywords, 
                                 visibility_results, filename)
        
        # 6. 결과 요약
        print("\n6️⃣ 분석 결과 요약")
        print("=" * 60)
        print(f"🎉 분석 완료!")
        print(f"📊 추출된 키워드: {len(extracted_keywords)}개")
        print(f"🚀 SEO 키워드: {len(seo_keywords)}개")
        print(f"💾 결과 파일: {filename}")
        
        print(f"\n📋 추천 다음 단계:")
        print("1. CSV 파일을 엑셀에서 열어서 키워드 검토")
        print("2. Google/Naver에서 직접 검색해서 사이트 노출 확인")
        print("3. 효과적인 키워드로 콘텐츠 최적화")
        print("4. AI 검색(ChatGPT/Claude)에서 브랜드 언급도 테스트")
        
        return {
            'content': content,
            'extracted_keywords': extracted_keywords,
            'seo_keywords': seo_keywords,
            'visibility': visibility_results,
            'filename': filename
        }

# 실행 함수
def analyze_dongraelaw_website():
    """법무법인 동래 웹사이트 분석 실행"""
    
    website_url = "https://www.dongraelaw.shop/"
    
    analyzer = WebsiteKeywordExtractor(website_url)
    results = analyzer.run_full_analysis()
    
    return results

# 수동 검색 가이드 함수
def manual_search_guide():
    """수동 검색 확인 가이드"""
    print("\n" + "="*50)
    print("🔍 수동 검색 확인 가이드")
    print("="*50)
    
    search_tests = [
        ("Google", "dongraelaw.shop", "https://www.google.com/search?q=dongraelaw.shop"),
        ("Google", "법무법인 동래", "https://www.google.com/search?q=법무법인+동래"),
        ("Naver", "법무법인 동래", "https://search.naver.com/search.naver?query=법무법인+동래"),
        ("Google", "연제 법무법인", "https://www.google.com/search?q=연제+법무법인"),
        ("Google", "site:dongraelaw.shop", "https://www.google.com/search?q=site:dongraelaw.shop")
    ]
    
    print("다음 검색들을 직접 해보세요:")
    print()
    
    for i, (engine, query, url) in enumerate(search_tests, 1):
        print(f"{i}. {engine}에서 '{query}' 검색")
        print(f"   URL: {url}")
        print(f"   확인사항: dongraelaw.shop 사이트가 결과에 나오는지")
        print()
    
    print("✅ 체크리스트:")
    print("□ 브랜드명으로 검색 시 1페이지에 나오는가?")
    print("□ 지역명으로 검색 시 경쟁사들과 함께 나오는가?") 
    print("□ site: 검색으로 페이지들이 색인되어 있는가?")
    print("□ 회사명 정확히 입력 시 최상단에 나오는가?")

if __name__ == "__main__":
    print("🚀 법무법인 동래 웹사이트 분석을 시작합니다!")
    
    # 웹사이트 분석 실행
    results = analyze_dongraelaw_website()
    
    # 수동 검색 가이드 출력
    manual_search_guide()