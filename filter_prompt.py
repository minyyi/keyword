import pandas as pd

# CSV 파일 로드
file_path = "dongrae_balanced_250완.csv"  # 실제 파일명으로 바꾸세요
df = pd.read_csv(file_path)

# 유지할 조합별 최대 개수
keep_counts = {
    ("정보", "쉬움"): 134,
    ("정보", "보통"): 133,
    ("정보", "어려움"): 133,
    ("탐색", "쉬움"): 16,
    ("탐색", "보통"): 17,
    ("탐색", "어려움"): 17,
    ("거래", "쉬움"): 16,
    ("거래", "보통"): 17,
    ("거래", "어려움"): 17,
}

# 결과 누적
filtered_parts = []
total_target = 250

# 조합별로 필터링해서 최대한 추출
for (intent, level), count in keep_counts.items():
    subset = df[(df["추출된_의도"] == intent) & (df["추출된_난이도"] == level)]
    sampled = subset.sample(n=min(count, len(subset)), random_state=42)
    filtered_parts.append(sampled)

# 합치기
filtered_df = pd.concat(filtered_parts)

# 만약 250개보다 부족하다면 '정보' 의도에서 추가 확보
current_count = len(filtered_df)
if current_count < total_target:
    remaining = total_target - current_count
    info_pool = df[df["추출된_의도"] == "정보"]
    
    # 이미 뽑힌 건 제외
    info_pool = info_pool[~info_pool.index.isin(filtered_df.index)]
    
    extra = info_pool.sample(n=min(remaining, len(info_pool)), random_state=99)
    filtered_df = pd.concat([filtered_df, extra])

# 최종 저장
filtered_df.to_csv("dongrae_balanced_250찐완.csv", index=False, encoding='utf-8-sig')
print(f"✅ 필터링 완료: 최종 {len(filtered_df)}개 저장됨.")
