import pandas as pd
from datetime import datetime

def remove_duplicate_questions(input_file, output_file=None):
    """CSV 파일에서 중복된 질문을 제거하는 함수"""
    
    # 파일 읽기
    print(f"📂 파일 읽는 중: {input_file}")
    df = pd.read_csv(input_file, encoding='utf-8')
    
    # 원본 정보
    original_count = len(df)
    print(f"\n📊 원본 데이터 정보:")
    print(f"  - 총 행 수: {original_count}")
    print(f"  - 총 컬럼 수: {len(df.columns)}")
    print(f"  - 컬럼명: {list(df.columns)}")
    
    # 중복 확인
    unique_count = df['질문'].nunique()
    duplicate_count = original_count - unique_count
    
    print(f"\n🔍 중복 분석:")
    print(f"  - 고유한 질문 개수: {unique_count}")
    print(f"  - 중복된 질문 개수: {duplicate_count}")
    
    # 중복된 질문들 출력 (처음 10개만)
    if duplicate_count > 0:
        duplicated = df[df['질문'].duplicated(keep=False)]
        print(f"\n📋 중복된 질문 목록 (처음 10개):")
        
        duplicate_questions = []
        for question in duplicated['질문'].unique()[:10]:
            count = (df['질문'] == question).sum()
            duplicate_questions.append((question, count))
            print(f"  - {count}번 중복: '{question[:70]}{'...' if len(question) > 70 else ''}'")
        
        if len(duplicated['질문'].unique()) > 10:
            print(f"  ... 그 외 {len(duplicated['질문'].unique()) - 10}개 더 있음")
    
    # 중복 제거 (첫 번째 항목만 유지)
    print(f"\n🧹 중복 제거 중...")
    df_clean = df.drop_duplicates(subset=['질문'], keep='first')
    final_count = len(df_clean)
    removed_count = original_count - final_count
    
    print(f"\n✅ 중복 제거 완료:")
    print(f"  - 남은 행 수: {final_count}")
    print(f"  - 제거된 행 수: {removed_count}")
    print(f"  - 제거율: {removed_count/original_count*100:.1f}%")
    
    # 출력 파일명 생성
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"remove_deduplicated_{timestamp}_without_3.csv"
    
    # 정리된 파일 저장
    df_clean.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n💾 중복 제거된 파일이 '{output_file}'로 저장되었습니다.")
    
    # 통계 요약
    print(f"\n📈 최종 결과 요약:")
    print(f"  원본: {original_count}개 → 정리 후: {final_count}개")
    print(f"  중복 제거: {removed_count}개 ({removed_count/original_count*100:.1f}%)")
    
    return df_clean, removed_count

# 실행
if __name__ == "__main__":
    input_filename = "remove_deduplicated_20250704_160833_without_2.csv"
    
    try:
        cleaned_df, removed_count = remove_duplicate_questions(input_filename)
        
        print(f"\n🎉 작업 완료!")
        print(f"최종 데이터: {len(cleaned_df)}개")
        
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {input_filename}")
        print("파일명을 확인해주세요.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")