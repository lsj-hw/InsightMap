import folium
import pandas as pd
import requests
import webbrowser
import os
import random
from datetime import datetime

# 1. 지역 리스트 정의
regions = ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시',
           '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원도',
           '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도']

# 2. 사용량 데이터 생성
data = {
    'region': regions,
    'usage': [random.randint(0, 200) for _ in regions]
}
df = pd.DataFrame(data)

# 3. GeoJSON 불러오기
geo_url = 'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_provinces_geo.json'
geo_json = requests.get(geo_url).json()

# 4. 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7, max_bounds=True)
m.fit_bounds([[33.0, 124.0], [39.5, 130.0]])  # 남한 중심에 포커스


# 5. 색상 기반 시각화 추가 (회색 ~ 초록)
folium.Choropleth(
    geo_data=geo_json,
    data=df,
    columns=['region', 'usage'],
    key_on='feature.properties.name',
    fill_color='Greens',
    fill_opacity=0.7,
    line_opacity=0.2,
    threshold_scale=[0, 50, 100, 150, 200],
    legend_name='지역별 샌드랩 사용량',
    highlight=True
).add_to(m)

# 6. 지역 이름 툴팁 추가
folium.GeoJson(
    geo_json,
    name="지역 경계",
    style_function=lambda x: {'fillColor': '#00000000', 'color': 'black', 'weight': 0.5},
    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['지역명:'])
).add_to(m)

# 7. 마커(팝업) 추가
region_coords = {
    '서울특별시': [37.5665, 126.9780],
    '부산광역시': [35.1796, 129.0756],
    '대구광역시': [35.8722, 128.6025],
    '인천광역시': [37.4563, 126.7052],
    '광주광역시': [35.1595, 126.8526],
    '대전광역시': [36.3504, 127.3845],
    '울산광역시': [35.5384, 129.3114],
    '세종특별자치시': [36.4800, 127.2890],
    '경기도': [37.4138, 127.5183],
    '강원도': [37.8228, 128.1555],
    '충청북도': [36.6357, 127.4917],
    '충청남도': [36.5184, 126.8000],
    '전라북도': [35.7167, 127.1442],
    '전라남도': [34.8161, 126.4630],
    '경상북도': [36.4919, 128.8889],
    '경상남도': [35.4606, 128.2132],
    '제주특별자치도': [33.4996, 126.5312]
}
# 7. 마커(정확 좌표 기반 팝업) 추가
for idx, row in df.iterrows():
    coords = region_coords[row['region']]
    folium.Marker(
        location=coords,
        popup=f"<b>{row['region']}</b><br>사용량: {row['usage']}회",
        icon=folium.Icon(color='green', icon='info-sign')
    ).add_to(m)


# 8. 날짜 타이틀 표시
title_html = f'''
    <h4 style="position:absolute; top:10px; left:10px; background:white;
    padding:10px; z-index:9999; font-size:16px;">
        샌드랩 지역별 사용량 지도<br>
        기준일: {datetime.today().strftime('%Y-%m-%d')}
    </h4>
'''
m.get_root().html.add_child(folium.Element(title_html))

# 9. HTML 저장 및 실행
file_path = os.path.abspath('sandlab_usage_map.html')
m.save(file_path)
webbrowser.open('file://' + file_path)
