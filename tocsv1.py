import pandas as pd
import json
import os
from datetime import datetime

def debug_json_file(file_path):
    """JSON 파일의 구조와 문제점을 진단하는 함수"""
    print(f"🔍 JSON 파일 진단 시작: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ JSON 파일 로드 성공")
        
        if isinstance(data, list):
            print(f"📊 리스트 형태 - 총 {len(data)}개 항목")
            
            # 빈 항목이나 None 값 체크
            empty_count = 0
            none_count = 0
            error_items = []
            
            for i, item in enumerate(data):
                if item is None:
                    none_count += 1
                elif isinstance(item, dict) and len(item) == 0:
                    empty_count += 1
                elif not isinstance(item, dict):
                    error_items.append((i, type(item).__name__))
            
            print(f"📈 데이터 품질 분석:")
            print(f"  - None 항목: {none_count}개")
            print(f"  - 빈 dict 항목: {empty_count}개")
            print(f"  - dict가 아닌 항목: {len(error_items)}개")
            
            if error_items:
                print(f"  - dict가 아닌 항목들: {error_items[:5]}...")
            
            # 유효한 항목 수 계산
            valid_items = len(data) - none_count - empty_count - len(error_items)
            print(f"  - 유효한 항목: {valid_items}개")
            
            # 첫 번째 유효한 항목의 구조 분석
            first_valid = None
            for item in data:
                if isinstance(item, dict) and len(item) > 0:
                    first_valid = item
                    break
            
            if first_valid:
                print(f"🔍 첫 번째 유효 항목 구조:")
                print(f"  - 키 개수: {len(first_valid.keys())}")
                print(f"  - 키 목록: {list(first_valid.keys())}")
                
                # prompt 확인
                if 'prompt' in first_valid:
                    prompt = first_valid['prompt']
                    print(f"  - prompt 길이: {len(str(prompt))}")
                    print(f"  - prompt 미리보기: {str(prompt)[:100]}...")
            
            return data, valid_items
            
        else:
            print(f"📊 단일 객체 형태")
            return data, 1
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return None, 0

def safe_flatten_json(nested_json, parent_key='', sep='_'):
    """안전한 JSON 평면화 - 오류 처리 강화"""
    items = []
    try:
        if not isinstance(nested_json, dict):
            return {parent_key or 'value': str(nested_json)}
        
        for k, v in nested_json.items():
            try:
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                
                if isinstance(v, dict):
                    items.extend(safe_flatten_json(v, new_key, sep=sep).items())
                elif isinstance(v, list):
                    # 리스트 처리 개선
                    if v:  # 비어있지 않은 리스트
                        items.append((new_key, ', '.join(map(str, v))))
                    else:  # 빈 리스트
                        items.append((new_key, None))
                else:
                    items.append((new_key, v))
            except Exception as e:
                print(f"⚠️ 키 '{k}' 처리 중 오류: {e}")
                items.append((new_key if 'new_key' in locals() else k, str(v)))
                
    except Exception as e:
        print(f"❌ flatten_json 전체 오류: {e}")
        return {parent_key or 'error': str(nested_json)}
    
    return dict(items)

def convert_json_to_csv_safe(json_file_name):
    """안전한 JSON → CSV 변환"""
    print(f"🚀 JSON → CSV 변환 시작")
    print(f"📁 작업 디렉토리: {os.getcwd()}")
    print(f"📄 대상 파일: {json_file_name}")
    
    # 1. 파일 존재 확인
    if not os.path.exists(json_file_name):
        print(f"❌ 파일을 찾을 수 없습니다: {json_file_name}")
        return False
    
    # 2. 파일 크기 확인
    file_size = os.path.getsize(json_file_name)
    print(f"📏 파일 크기: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
    
    # 3. JSON 파일 진단
    json_data, expected_count = debug_json_file(json_file_name)
    
    if json_data is None:
        print("❌ JSON 파일을 읽을 수 없습니다.")
        return False
    
    print(f"\n🔄 데이터 변환 시작 (예상 {expected_count}개 항목)")
    
    processed_data = []
    error_count = 0
    
    # 4. 각 항목을 안전하게 처리
    if isinstance(json_data, list):
        for i, item in enumerate(json_data):
            try:
                # 진행률 표시
                if i % 100 == 0:
                    print(f"진행률: {i}/{len(json_data)} ({i/len(json_data)*100:.1f}%)")
                
                # None이나 빈 항목 건너뛰기
                if item is None:
                    print(f"⚠️ 항목 {i}: None 값 건너뜀")
                    continue
                
                if not isinstance(item, dict):
                    print(f"⚠️ 항목 {i}: dict가 아님 ({type(item).__name__}) - 문자열로 변환")
                    processed_data.append({'item_index': i, 'raw_data': str(item)})
                    continue
                
                if len(item) == 0:
                    print(f"⚠️ 항목 {i}: 빈 dict 건너뜀")
                    continue
                
                # 정상 처리
                flattened = safe_flatten_json(item)
                flattened['item_index'] = i  # 원본 인덱스 추가
                processed_data.append(flattened)
                
            except Exception as e:
                error_count += 1
                print(f"❌ 항목 {i} 처리 오류: {e}")
                # 오류가 발생해도 기본 정보라도 저장
                try:
                    processed_data.append({
                        'item_index': i,
                        'error': str(e),
                        'raw_data': str(item)[:500]  # 처음 500자만
                    })
                except:
                    pass
                continue
    else:
        # 단일 객체 처리
        try:
            flattened = safe_flatten_json(json_data)
            processed_data.append(flattened)
        except Exception as e:
            print(f"❌ 단일 객체 처리 오류: {e}")
            return False
    
    print(f"\n📊 처리 결과:")
    print(f"  - 원본 항목 수: {len(json_data) if isinstance(json_data, list) else 1}")
    print(f"  - 성공적으로 처리된 항목: {len(processed_data)}")
    print(f"  - 오류 발생 항목: {error_count}")
    
    if len(processed_data) == 0:
        print("❌ 처리된 데이터가 없습니다.")
        return False
    
    # 5. DataFrame 생성
    try:
        df = pd.DataFrame(processed_data)
        print(f"✅ DataFrame 생성 성공 - {len(df)}행 × {len(df.columns)}열")
    except Exception as e:
        print(f"❌ DataFrame 생성 오류: {e}")
        return False
    
    # 6. CSV 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = json_file_name.replace('.json', '')
    output_filename = f"{base_name}_fixed_{timestamp}.csv"
    
    try:
        df.to_csv(output_filename, index=False, encoding='utf-8')
        print(f"✅ CSV 저장 성공: {output_filename}")
        
        # 저장된 파일 크기 확인
        output_size = os.path.getsize(output_filename)
        print(f"📏 출력 파일 크기: {output_size:,} bytes ({output_size/1024/1024:.2f} MB)")
        
    except Exception as e:
        print(f"❌ CSV 저장 오류: {e}")
        return False
    
    # 7. 결과 미리보기
    print(f"\n📋 결과 미리보기:")
    print(f"컬럼명 (총 {len(df.columns)}개): {list(df.columns)[:10]}...")
    
    # prompt 컬럼이 있으면 확인
    if 'prompt' in df.columns:
        print(f"\nPrompt 샘플 (처음 3개):")
        for i in range(min(3, len(df))):
            prompt = str(df.iloc[i]['prompt'])
            print(f"  {i+1}. {prompt[:100]}...")
    
    return True

# 실행 부분
if __name__ == "__main__":
    # ★★★ 여기에 실제 JSON 파일명을 입력하세요! ★★★
    JSON_FILE_NAME = 'iovu_gpt4o_massive_20250704_095609.json'
    
    print("=== JSON → CSV 안전 변환기 ===")
    print("문제점을 진단하고 안전하게 변환합니다.\n")
    
    success = convert_json_to_csv_safe(JSON_FILE_NAME)
    
    if success:
        print("\n🎉 변환 완료!")
        print("📝 만약 여전히 데이터가 부족하다면:")
        print("  1. 원본 JSON 파일에 실제로 2000개 항목이 있는지 확인")
        print("  2. JSON 파일이 손상되지 않았는지 확인")
        print("  3. 메모리 부족이나 다른 시스템 문제가 없는지 확인")
    else:
        print("\n❌ 변환 실패 - 위의 오류 메시지를 확인하세요.")
    
    print(f"\n🔧 추가 디버깅이 필요하면:")
    print(f"  1. JSON 파일을 텍스트 에디터로 열어 구조 확인")
    print("  2. 파일 끝부분이 제대로 닫혀있는지 확인 (']' 또는 '}')")
    print(f"  3. 파일 중간에 잘못된 형식이 없는지 확인")