import csv
import os
from datetime import datetime

def merge_csv_files(file1_path, file2_path, output_filename=None):
    """
    두 CSV 파일을 하나로 합치는 함수
    
    Args:
        file1_path: 첫 번째 CSV 파일 경로 (1000행 검수결과 파일)
        file2_path: 두 번째 CSV 파일 경로 (100행 새 프롬프트 파일)
        output_filename: 출력 파일명 (None이면 자동 생성)
    """
    
    try:
        # 출력 파일명 생성
        if output_filename is None:
            current_date = datetime.now().strftime("%Y%m%d_%H%M")
            output_filename = f"dongrae_merged_complete_{current_date}.csv"
        
        # 첫 번째 파일 데이터 읽기
        print(f"📂 첫 번째 파일 읽는 중: {file1_path}")
        file1_data = []
        
        if os.path.exists(file1_path):
            with open(file1_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                file1_headers = reader.fieldnames
                print(f"   컬럼: {file1_headers}")
                
                for row in reader:
                    file1_data.append(row)
                print(f"   데이터: {len(file1_data)}행")
        else:
            print(f"❌ 파일을 찾을 수 없습니다: {file1_path}")
            return None
        
        # 두 번째 파일 데이터 읽기
        print(f"\n📂 두 번째 파일 읽는 중: {file2_path}")
        file2_data = []
        
        if os.path.exists(file2_path):
            with open(file2_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                file2_headers = reader.fieldnames
                print(f"   컬럼: {file2_headers}")
                
                for row in reader:
                    file2_data.append(row)
                print(f"   데이터: {len(file2_data)}행")
        else:
            print(f"❌ 파일을 찾을 수 없습니다: {file2_path}")
            return None
        
        # 통합된 컬럼 정의 (첫 번째 파일 기준으로 통일)
        merged_headers = [
            '원본_행', '질문', '추출된_의도', '추출된_난이도', '추출된_버킷타입',
            '검수_점수', '검수_통과', '검수_사유', '원본_의도', '원본_난이도'
        ]
        
        print(f"\n🔄 데이터 변환 및 통합 중...")
        
        # 통합된 데이터 생성
        merged_data = []
        
        # 첫 번째 파일 데이터 추가 (기존 1000개)
        for row in file1_data:
            merged_row = {}
            for header in merged_headers:
                merged_row[header] = row.get(header, '')
            merged_data.append(merged_row)
        
        # 두 번째 파일 데이터 변환 후 추가 (새로운 100개)
        start_row = len(file1_data) + 1
        for i, row in enumerate(file2_data):
            merged_row = {
                '원본_행': start_row + i,
                '질문': row.get('질문', ''),
                '추출된_의도': row.get('의도', ''),
                '추출된_난이도': row.get('난이도', ''),
                '추출된_버킷타입': row.get('도메인', '동래'),
                '검수_점수': 0.85,  # 새 프롬프트는 고품질로 기본 점수 부여
                '검수_통과': 'Y',    # 새 프롬프트는 통과로 설정
                '검수_사유': '신규_고품질_프롬프트',
                '원본_의도': row.get('의도', ''),
                '원본_난이도': row.get('난이도', '')
            }
            merged_data.append(merged_row)
        
        # 통합된 파일 저장
        print(f"\n💾 통합 파일 저장 중: {output_filename}")
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=merged_headers)
            writer.writeheader()
            writer.writerows(merged_data)
        
        # 결과 출력
        print("\n✅ 파일 통합 완료!")
        print(f"📁 출력 파일: {output_filename}")
        print("📊 통합 결과:")
        print(f"  • 기존 데이터: {len(file1_data)}행")
        print(f"  • 새 데이터: {len(file2_data)}행")
        print(f"  • 총 데이터: {len(merged_data)}행")
        
        # 의도별 통계
        intent_stats = {}
        difficulty_stats = {}
        
        for row in merged_data:
            intent = row.get('추출된_의도', '미분류')
            difficulty = row.get('추출된_난이도', '미분류')
            
            intent_stats[intent] = intent_stats.get(intent, 0) + 1
            difficulty_stats[difficulty] = difficulty_stats.get(difficulty, 0) + 1
        
        print("\n📈 의도별 분포:")
        for intent, count in intent_stats.items():
            print(f"  • {intent}: {count}개")
        
        print("\n📊 난이도별 분포:")
        for difficulty, count in difficulty_stats.items():
            print(f"  • {difficulty}: {count}개")
        
        return output_filename
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return None

def main():
    """메인 실행 함수"""
    print("🚀 CSV 파일 통합 프로그램 시작")
    print("=" * 50)
    
    # 파일 경로 설정 (실제 파일명으로 수정해주세요)
    file1_path = "dongrae_통과_질문_필터링결과.csv"
    file2_path = "dongrae_88.csv"
    
    # 파일 존재 여부 확인
    print("📋 파일 존재 여부 확인:")
    print(f"  파일 1: {os.path.exists(file1_path)} - {file1_path}")
    print(f"  파일 2: {os.path.exists(file2_path)} - {file2_path}")
    
    if not os.path.exists(file1_path):
        print(f"\n❌ 첫 번째 파일이 없습니다. 파일명을 확인해주세요: {file1_path}")
        return
    
    if not os.path.exists(file2_path):
        print(f"\n❌ 두 번째 파일이 없습니다. 파일명을 확인해주세요: {file2_path}")
        return
    
    # 파일 통합 실행
    result_file = merge_csv_files(file1_path, file2_path)
    
    if result_file:
        print(f"\n🎉 작업 완료! {result_file} 파일을 확인해주세요.")
        print("\n📝 통합된 파일 구조:")
        print("  • 원본_행: 행 번호 (1-1100)")
        print("  • 질문: 프롬프트 내용")
        print("  • 추출된_의도: 정보/탐색/거래")
        print("  • 추출된_난이도: 쉬움/보통/어려움")
        print("  • 추출된_버킷타입: 동래")
        print("  • 검수_점수: 품질 점수")
        print("  • 검수_통과: Y/N")
        print("  • 검수_사유: 통과/실패 사유")
        print("  • 원본_의도: 원본 의도")
        print("  • 원본_난이도: 원본 난이도")
    else:
        print("\n❌ 파일 통합 실패!")

if __name__ == "__main__":
    main()