import pandas as pd
import re

# CSV 파일 로드
file_path = "dongrae_balanced_filterd_250_1.csv"  # 실제 파일명으로 바꾸세요
df = pd.read_csv(file_path)

print("📊 원본 데이터 정보:")
print(f"총 행 수: {len(df)}")
print(f"컬럼명: {list(df.columns)}")

# 🔧 검수_점수 컬럼 데이터 정리
print("\n🔧 검수_점수 컬럼 정리 중...")
print(f"검수_점수 데이터 타입: {df['검수_점수'].dtype}")
print(f"검수_점수 샘플 값 (처음 3개):")
for i in range(min(3, len(df))):
    print(f"  {i+1}. '{df['검수_점수'].iloc[i]}'")

# 문자열에서 첫 번째 숫자 추출
def extract_first_score(score_str):
    """문자열에서 첫 번째 점수 추출"""
    if pd.isna(score_str):
        return 1.0  # 기본값
    
    # 문자열로 변환
    score_str = str(score_str)
    
    # 첫 번째 숫자 패턴 찾기 (소수점 포함)
    match = re.search(r'(\d+\.?\d*)', score_str)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 1.0
    else:
        return 1.0

# 검수_점수 정리
df['검수_점수_원본'] = df['검수_점수'].copy()  # 원본 백업
df['검수_점수'] = df['검수_점수'].apply(extract_first_score)

print(f"\n✅ 검수_점수 정리 완료!")
print(f"정리 후 데이터 타입: {df['검수_점수'].dtype}")
print(f"정리 후 샘플 값: {df['검수_점수'].head().tolist()}")
print(f"점수 범위: {df['검수_점수'].min():.2f} ~ {df['검수_점수'].max():.2f}")

# 원본 분포 확인
print("\n📊 원본 데이터 분포:")
distribution = df.groupby(['추출된_의도', '추출된_난이도']).size()
print(distribution)
print(f"총 원본 데이터: {len(df)}개\n")

# 250개 기준으로 조정된 목표 개수
keep_counts = {
    # 정보 의도 (500개 기준 400개 → 250개 기준 200개)
    ("정보", "쉬움"): 67,    # 134 → 67
    ("정보", "보통"): 67,    # 133 → 67  
    ("정보", "어려움"): 66,  # 133 → 66
    
    # 탐색 의도 (500개 기준 50개 → 250개 기준 25개)
    ("탐색", "쉬움"): 8,     # 16 → 8
    ("탐색", "보통"): 9,     # 17 → 9
    ("탐색", "어려움"): 8,   # 17 → 8
    
    # 거래 의도 (500개 기준 50개 → 250개 기준 25개)
    ("거래", "쉬움"): 8,     # 16 → 8
    ("거래", "보통"): 9,     # 17 → 9
    ("거래", "어려움"): 8,   # 17 → 8
}

print("🎯 목표 분포 (250개 기준):")
for (intent, level), count in keep_counts.items():
    print(f"  {intent} - {level}: {count}개")

total_target = sum(keep_counts.values())
print(f"목표 총합: {total_target}개\n")

# 결과 누적
filtered_parts = []
actual_counts = {}

# 조합별로 필터링해서 추출 (검수 점수 높은 순)
print("🔄 필터링 진행 (검수 점수 높은 순):")
for (intent, level), target_count in keep_counts.items():
    subset = df[(df["추출된_의도"] == intent) & (df["추출된_난이도"] == level)]
    available_count = len(subset)
    
    # 사용 가능한 데이터가 목표보다 적은 경우 모두 사용
    actual_count = min(target_count, available_count)
    
    if available_count > 0:
        # 검수 점수 높은 순으로 정렬 후 상위 n개 선택
        sorted_subset = subset.sort_values('검수_점수', ascending=False)
        sampled = sorted_subset.head(actual_count)
        
        filtered_parts.append(sampled)
        actual_counts[(intent, level)] = actual_count
        
        avg_score = sampled['검수_점수'].mean()
        min_score = sampled['검수_점수'].min()
        max_score = sampled['검수_점수'].max()
        print(f"  {intent} - {level}: {actual_count}개 추출 (목표: {target_count}, 가용: {available_count})")
        print(f"    점수 범위: {min_score:.2f} ~ {max_score:.2f} (평균: {avg_score:.2f})")
    else:
        actual_counts[(intent, level)] = 0
        print(f"  {intent} - {level}: 0개 추출 (데이터 없음)")

# 합치기
if filtered_parts:
    filtered_df = pd.concat(filtered_parts, ignore_index=True)
else:
    filtered_df = pd.DataFrame()

current_count = len(filtered_df)
print(f"\n1차 추출 완료: {current_count}개")

# 목표 개수에 부족한 경우 추가 확보 (검수 점수 높은 순)
if current_count < total_target:
    remaining = total_target - current_count
    print(f"🔄 부족분 {remaining}개 추가 확보 중 (검수 점수 높은 순)...")
    
    # 이미 뽑힌 인덱스 제외
    remaining_df = df[~df.index.isin(filtered_df.index)]
    
    if len(remaining_df) >= remaining:
        # 정보 의도 우선으로 부족분 보충 (검수 점수 높은 순)
        info_pool = remaining_df[remaining_df["추출된_의도"] == "정보"]
        
        if len(info_pool) >= remaining:
            # 검수 점수 높은 순으로 정렬 후 상위 n개 선택
            info_sorted = info_pool.sort_values('검수_점수', ascending=False)
            extra = info_sorted.head(remaining)
        else:
            # 정보 의도만으로 부족하면 전체에서 검수 점수 높은 순 선택
            remaining_sorted = remaining_df.sort_values('검수_점수', ascending=False)
            extra = remaining_sorted.head(remaining)
        
        filtered_df = pd.concat([filtered_df, extra], ignore_index=True)
        avg_extra_score = extra['검수_점수'].mean()
        print(f"✅ 추가 {len(extra)}개 확보 (평균점수: {avg_extra_score:.2f})")
    else:
        print(f"⚠️ 추가 확보 불가 (남은 데이터: {len(remaining_df)}개)")

# 최종 결과
final_count = len(filtered_df)
print(f"\n📈 최종 결과:")
print(f"목표: {total_target}개 → 실제: {final_count}개")

# 최종 분포 확인
print(f"\n📊 최종 분포:")
final_distribution = filtered_df.groupby(['추출된_의도', '추출된_난이도']).size()
print(final_distribution)

# 목표 vs 실제 비교
print(f"\n📋 목표 vs 실제 비교:")
for (intent, level), target in keep_counts.items():
    try:
        actual = final_distribution.loc[(intent, level)]
    except KeyError:
        actual = 0
    print(f"  {intent} - {level}: 목표 {target}개 → 실제 {actual}개")

# 250개 정확히 맞추기 (초과인 경우 검수 점수 낮은 것부터 제거)
if final_count > 250:
    print(f"\n🔄 250개 정확히 맞추기 위해 {final_count - 250}개 제거 (검수 점수 낮은 순)")
    # 검수 점수 높은 순으로 정렬하여 상위 250개만 유지
    filtered_df = filtered_df.sort_values('검수_점수', ascending=False).head(250).reset_index(drop=True)
    final_count = 250

# 최종 저장
output_file = "balanced_250_Dongrae_2.csv"
filtered_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n✅ 필터링 완료!")
print(f"📁 파일 저장: {output_file}")
print(f"📊 최종 데이터: {final_count}개")

# 최종 검증
print(f"\n🔍 최종 검증:")
verify_distribution = filtered_df.groupby(['추출된_의도', '추출된_난이도']).size()
print(verify_distribution)
print(f"총합: {verify_distribution.sum()}개")

# 검수 점수 통계
print(f"\n⭐ 검수 점수 통계:")
print(f"평균 점수: {filtered_df['검수_점수'].mean():.2f}")
print(f"최고 점수: {filtered_df['검수_점수'].max():.2f}")
print(f"최저 점수: {filtered_df['검수_점수'].min():.2f}")
print(f"점수 분포:")
print(filtered_df['검수_점수'].value_counts().sort_index(ascending=False))

print(f"\n🔧 데이터 정리 정보:")
print(f"원본 검수_점수는 '검수_점수_원본' 컬럼에 백업되었습니다.")
print(f"정리된 검수_점수로 필터링이 완료되었습니다.")