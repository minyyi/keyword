import pandas as pd
import json
import os
from datetime import datetime

def flatten_json(nested_json, parent_key='', sep='_'):
    """
    중첩된 JSON을 평면화하는 함수 - 모든 데이터를 보존
    """
    items = []
    for k, v in nested_json.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # 리스트는 문자열로 변환
            items.append((new_key, ', '.join(map(str, v)) if v else None))
        else:
            items.append((new_key, v))
    return dict(items)

def extract_key_info(data):
    """
    주요 정보만 추출하여 정리된 형태로 변환 (일부 데이터만)
    """
    extracted = {
        'prompt': data.get('prompt'),
        'template_used': data.get('template_used'),
        
        # extracted_keywords에서
        'extracted_region': data.get('extracted_keywords', {}).get('region'),
        'extracted_intent': data.get('extracted_keywords', {}).get('intent'),
        'extracted_difficulty': data.get('extracted_keywords', {}).get('difficulty'),
        'extracted_practice_area': data.get('extracted_keywords', {}).get('practice_area'),
        'extracted_metric': data.get('extracted_keywords', {}).get('metric'),
        
        # final_parameters에서
        'practice_area': data.get('final_parameters', {}).get('practice_area'),
        'metric': data.get('final_parameters', {}).get('metric'),
        'region': data.get('final_parameters', {}).get('region'),
        'time_span': data.get('final_parameters', {}).get('time_span'),
        'source_hint': data.get('final_parameters', {}).get('source_hint'),
        'language_ratio': data.get('final_parameters', {}).get('language_ratio'),
        'intent': data.get('final_parameters', {}).get('intent'),
        'difficulty': data.get('final_parameters', {}).get('difficulty'),
        
        # brand_info에서
        'firm_name': data.get('brand_info', {}).get('name'),
        'firm_english_name': data.get('brand_info', {}).get('english_name'),
        'firm_website': data.get('brand_info', {}).get('website'),
        'firm_location': data.get('brand_info', {}).get('location'),
        'firm_phone': data.get('brand_info', {}).get('phone'),
        'firm_established': data.get('brand_info', {}).get('established'),
        'firm_experience': data.get('brand_info', {}).get('experience'),
        'firm_specialties': ', '.join(data.get('brand_info', {}).get('specialties', []))
    }
    return extracted

# 파일에서 JSON 데이터를 읽어오는 경우
def load_json_from_file(file_path):
    """
    파일에서 JSON 데이터를 읽어오는 함수
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"파일 '{file_path}'을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        print(f"파일 '{file_path}'의 JSON 형식이 올바르지 않습니다.")
        return None

# ★★★ 여기에 실제 JSON 파일명을 입력하세요! ★★★
JSON_FILE_NAME = 'iovu_massive_20250704_100638.json'  # 이 부분만 실제 파일명으로 바꾸세요!

# =============================================================================
# 실제 JSON 파일을 CSV로 변환하는 메인 코드 
# =============================================================================
def extract_key_info(data):
    """
    주요 정보만 추출하여 정리된 형태로 변환
    """
    extracted = {
        'prompt': data.get('prompt'),
        'template_used': data.get('template_used'),
        
        # extracted_keywords에서
        'extracted_region': data.get('extracted_keywords', {}).get('region'),
        'extracted_intent': data.get('extracted_keywords', {}).get('intent'),
        'extracted_difficulty': data.get('extracted_keywords', {}).get('difficulty'),
        
        # final_parameters에서
        'practice_area': data.get('final_parameters', {}).get('practice_area'),
        'metric': data.get('final_parameters', {}).get('metric'),
        'region': data.get('final_parameters', {}).get('region'),
        'time_span': data.get('final_parameters', {}).get('time_span'),
        'source_hint': data.get('final_parameters', {}).get('source_hint'),
        'language_ratio': data.get('final_parameters', {}).get('language_ratio'),
        'intent': data.get('final_parameters', {}).get('intent'),
        'difficulty': data.get('final_parameters', {}).get('difficulty'),
        
        # brand_info에서
        'firm_name': data.get('brand_info', {}).get('name'),
        'firm_english_name': data.get('brand_info', {}).get('english_name'),
        'firm_website': data.get('brand_info', {}).get('website'),
        'firm_location': data.get('brand_info', {}).get('location'),
        'firm_phone': data.get('brand_info', {}).get('phone'),
        'firm_established': data.get('brand_info', {}).get('established'),
        'firm_experience': data.get('brand_info', {}).get('experience'),
        'firm_specialties': ', '.join(data.get('brand_info', {}).get('specialties', []))
    }
    return extracted



# 파일에서 JSON 데이터를 읽어오는 경우
def load_json_from_file(file_path):
    """
    파일에서 JSON 데이터를 읽어오는 함수
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"파일 '{file_path}'을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        print(f"파일 '{file_path}'의 JSON 형식이 올바르지 않습니다.")
        return None

# ★★★ 여기에 실제 JSON 파일명을 입력하세요! ★★★
JSON_FILE_NAME = 'iovu_massive_20250704_100638.json'  # 실제 파일명으로 변경됨

print(f"🔍 현재 작업 디렉토리: {os.getcwd()}")
print(f"🔍 읽으려는 파일: {JSON_FILE_NAME}")

# 실제 JSON 파일에서 데이터 읽어오기
print(f"'{JSON_FILE_NAME}' 파일을 읽는 중...")
json_data = load_json_from_file(JSON_FILE_NAME)

if json_data:
    print("JSON 파일을 성공적으로 읽었습니다!")
    
    # 🔍 디버깅: JSON 데이터의 첫 번째 항목 확인
    if isinstance(json_data, list):
        print(f"✅ 리스트 형태의 JSON 데이터입니다. 총 {len(json_data)}개의 항목이 있습니다.")
        
        # 첫 번째 항목의 일부 내용 확인
        if len(json_data) > 0:
            first_item = json_data[0]
            print(f"\n🔍 첫 번째 항목의 키들: {list(first_item.keys()) if isinstance(first_item, dict) else 'dict가 아님'}")
            if isinstance(first_item, dict):
                # prompt 내용 확인 (처음 100자만)
                prompt = first_item.get('prompt', 'prompt 키 없음')
                print(f"🔍 첫 번째 항목의 prompt: {str(prompt)[:100]}...")
                
                # brand_info의 name 확인
                brand_name = first_item.get('brand_info', {}).get('name', 'brand_info 없음')
                print(f"🔍 첫 번째 항목의 brand_name: {brand_name}")
        
        # ✅ 모든 데이터를 평면화해서 처리 (추천!)
        processed_data_list = []
        for i, item in enumerate(json_data):
            try:
                # flatten_json 사용 - 모든 데이터 보존
                flattened_item = flatten_json(item)
                processed_data_list.append(flattened_item)
                
                # 처음 몇 개의 처리 결과 확인
                if i < 3:
                    print(f"항목 {i+1} 처리 완료 - 총 {len(flattened_item)}개 컬럼 생성")
                    print(f"  -> prompt: {str(flattened_item.get('prompt', ''))[:50]}...")
                    
            except Exception as e:
                print(f"항목 {i+1} 처리 중 오류: {e}")
                continue
        
        # DataFrame 생성
        df_from_file = pd.DataFrame(processed_data_list)
        print(f"✅ 총 {len(df_from_file)}개의 레코드가 처리되었습니다.")
        
        # 🔍 디버깅: DataFrame의 일부 내용 확인
        if len(df_from_file) > 0:
            print(f"\n🔍 DataFrame 정보:")
            print(f"  - 총 컬럼 수: {len(df_from_file.columns)}")
            print(f"  - 총 행 수: {len(df_from_file)}")
            print(f"  - 첫 번째 행의 prompt: {str(df_from_file.iloc[0]['prompt'] if 'prompt' in df_from_file.columns else 'N/A')[:50]}...")
            
            # 컬럼명 일부 표시
            print(f"  - 컬럼명 예시 (처음 10개): {list(df_from_file.columns)[:10]}")
            
            # 데이터가 모두 같은지 확인
            if len(df_from_file) > 1:
                first_prompt = df_from_file.iloc[0]['prompt'] if 'prompt' in df_from_file.columns else ''
                second_prompt = df_from_file.iloc[1]['prompt'] if 'prompt' in df_from_file.columns else ''
                if first_prompt == second_prompt:
                    print("⚠️  경고: 첫 번째와 두 번째 행의 prompt가 동일합니다!")
                else:
                    print("✅ 첫 번째와 두 번째 행의 prompt가 다릅니다.")
        
    else:
        print("✅ 단일 객체 형태의 JSON 데이터입니다.")
        # 단일 객체도 모든 데이터 평면화
        flattened_data = flatten_json(json_data)
        df_from_file = pd.DataFrame([flattened_data])
        print(f"단일 객체에서 {len(flattened_data)}개 컬럼 생성됨")
    
    # 타임스탬프가 포함된 파일명 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = JSON_FILE_NAME.replace('.json', '').replace(' copy', '').replace(' ', '_')
    output_filename = f"{base_filename}_cnvrtd_{timestamp}.csv"
    
    df_from_file.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"✅ '{output_filename}' 파일로 저장 완료!")
    
    # 결과 미리보기
    print(f"\n📋 변환된 데이터 미리보기:")
    # 모든 컬럼이 많을 수 있으니 중요한 컬럼들만 먼저 보여주기
    key_columns = ['prompt', 'brand_info_name', 'final_parameters_region', 'final_parameters_practice_area']
    available_key_cols = [col for col in key_columns if col in df_from_file.columns]
    
    if available_key_cols:
        print("주요 컬럼 미리보기:")
        print(df_from_file[available_key_cols].head(3))
    else:
        print("전체 데이터 미리보기 (처음 5개 컬럼):")
        print(df_from_file.iloc[:3, :5])
    
    print(f"\n📊 최종 DataFrame 정보:")
    print(f"- 열 수: {len(df_from_file.columns)}")
    print(f"- 모든 컬럼명: {list(df_from_file.columns)}")
    
else:
    print("❌ JSON 파일을 읽을 수 없습니다. 파일명과 경로를 확인해주세요.")

print("\n=== 사용 방법 ===")
print("✅ 이제 JSON 파일의 **모든 데이터**가 CSV로 변환됩니다!")
print("1. 위의 JSON_FILE_NAME 변수에 실제 JSON 파일명을 입력하세요")
print("2. 코드를 실행하면 모든 필드가 평면화되어 CSV로 저장됩니다")
print("3. 중첩된 JSON 구조는 'parent_child' 형태의 컬럼명으로 변환됩니다")
print("4. 타임스탬프가 포함된 파일명으로 저장되어 파일이 겹치지 않습니다")