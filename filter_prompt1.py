import pandas as pd

# CSV 파일 로드
file_path = "dongrae_balanced_filtered_250plus.csv"  # 실제 파일명으로 바꾸세요
df = pd.read_csv(file_path)

print("📊 원본 데이터 분포:")
distribution = df.groupby(['추출된_의도', '추출된_난이도']).size()
print(distribution)
print(f"총 원본 데이터: {len(df)}개\n")

# 250개 기준으로 조정된 목표 개수
# 500개 기준 비율을 250개로 절반 조정
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

# 조합별로 필터링해서 추출
print("🔄 필터링 진행:")
for (intent, level), target_count in keep_counts.items():
    subset = df[(df["추출된_의도"] == intent) & (df["추출된_난이도"] == level)]
    available_count = len(subset)
    
    # 사용 가능한 데이터가 목표보다 적은 경우 모두 사용
    actual_count = min(target_count, available_count)
    
    if available_count > 0:
        sampled = subset.sample(n=actual_count, random_state=42)
        filtered_parts.append(sampled)
        actual_counts[(intent, level)] = actual_count
        
        print(f"  {intent} - {level}: {actual_count}개 추출 (목표: {target_count}, 가용: {available_count})")
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

# 목표 개수에 부족한 경우 추가 확보
if current_count < total_target:
    remaining = total_target - current_count
    print(f"🔄 부족분 {remaining}개 추가 확보 중...")
    
    # 이미 뽑힌 인덱스 제외
    remaining_df = df[~df.index.isin(filtered_df.index)]
    
    if len(remaining_df) >= remaining:
        # 정보 의도 우선으로 부족분 보충
        info_pool = remaining_df[remaining_df["추출된_의도"] == "정보"]
        
        if len(info_pool) >= remaining:
            extra = info_pool.sample(n=remaining, random_state=99)
        else:
            # 정보 의도만으로 부족하면 전체에서 랜덤 선택
            extra = remaining_df.sample(n=remaining, random_state=99)
        
        filtered_df = pd.concat([filtered_df, extra], ignore_index=True)
        print(f"✅ 추가 {len(extra)}개 확보")
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

# 250개 정확히 맞추기 (초과인 경우 랜덤 제거)
if final_count > 250:
    print(f"\n🔄 250개 정확히 맞추기 위해 {final_count - 250}개 제거")
    filtered_df = filtered_df.sample(n=250, random_state=123).reset_index(drop=True)
    final_count = 250

# 최종 저장
output_file = "dongrae_balanced_filterd_250_2.csv"
filtered_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n✅ 필터링 완료!")
print(f"📁 파일 저장: {output_file}")
print(f"📊 최종 데이터: {final_count}개")

# 최종 검증
print(f"\n🔍 최종 검증:")
verify_distribution = filtered_df.groupby(['추출된_의도', '추출된_난이도']).size()
print(verify_distribution)
print(f"총합: {verify_distribution.sum()}개")