import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
import datetime

# 1. 網頁基礎設定 (隱藏官方選單)
st.set_page_config(
    page_title="智慧跨航空機票比價系統", 
    layout="wide",
    menu_items={}
)

# 2. 🎯 【視覺終極完全體】注入 100% 雲端相容 CSS：三大指標、航班選項全部完美換裝深灰色卡片！
st.markdown("""
    <style>
    /* 全網頁底色大背景 */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }
    [data-testid="stHeader"] {
        background-color: #0f172a !important;
        background: #0f172a !important;
    }
    [data-testid="stSidebar"] {
        background-color: #111b31 !important;
    }
    h1, h2, h3, p, label, .stMarkdown {
        color: #f8fafc !important;
    }
    
    /* 三大指標區塊：強制改裝為深灰色卡片 */
    div[data-testid="metric-container"] {
        background-color: #1e293b !important;
        padding: 20px !important;
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* 第一分頁航班組合：強制改裝為與 Esme 面板一致的深灰色獨立卡片 */
    .stTabs [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1e293b !important;
        padding: 25px !important;
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        margin-bottom: 20px !important;
    }

    /* 下拉選單與搜尋按鈕美化 */
    div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border-color: #334155 !important;
    }
    div.stButton > button {
        color: #ffffff !important;
        background: linear-gradient(90deg, #1d4ed8 0%, #3b82f6 100%) !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%) !important;
        color: #ffffff !important;
    }
    
    /* 🎯 找回來的購買連結按鈕：定製為極具儀式感的商務亮藍色大按鈕 */
    div.stLinkButton > a {
        color: #ffffff !important;
        background-color: #2563eb !important;
        border: 1px solid #3b82f6 !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        width: 100% !important;
        text-align: center !important;
        padding: 8px 16px !important;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3) !important;
    }
    div.stLinkButton > a:hover {
        background-color: #1d4ed8 !important;
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.5) !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #3b82f6 !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 讀取最新 CSV 檔案
def load_data_by_index():
    try:
        try:
            df = pd.read_csv("my_premium_stable_flight_data.csv", encoding="utf-8")
        except:
            df = pd.read_csv("my_premium_stable_flight_data.csv", encoding="cp950")
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        cols = df.columns.tolist()
        rename_dict = {}
        if len(cols) >= 1: rename_dict[cols[0]] = 'Origin'
        if len(cols) >= 2: rename_dict[cols[1]] = 'Destination'
        if len(cols) >= 3: rename_dict[cols[2]] = 'Airline'
        if len(cols) >= 4: rename_dict[cols[3]] = 'FlightNo'
        if len(cols) >= 5: rename_dict[cols[4]] = 'DepTime'
        if len(cols) >= 6: rename_dict[cols[5]] = 'RetTime'
        if len(cols) >= 7: rename_dict[cols[6]] = 'Price'
        df = df.rename(columns=rename_dict)
        return df
    except Exception as e:
        return pd.DataFrame({
            'Origin': ['TPE', 'TPE', 'TPE'],
            'Destination': ['NRT', 'KIX', 'LAX'],
            'Airline': ['中華航空 to 長榮航空', '長榮航空 to 國泰航空', '星宇航空 to 台灣虎航'],
            'FlightNo': ['CI104 to BR197', 'BR178 to CX565', 'JX800 to IT211'],
            'DepTime': ['08:30 - 12:45', '07:00 - 11:10', '10:15 - 14:45'],
            'RetTime': ['18:30 - 21:00', '16:20 - 18:00', '14:00 - 16:30'],
            'Price': [15800, 14200, 13500]
        })

df_raw = load_data_by_index()
for col in ['Origin', 'Destination']:
    if col in df_raw.columns:
        df_raw[col] = df_raw[col].astype(str).str.strip()

# --- 側邊欄控制中心 ---
st.sidebar.header("Round-Trip Search Center")
available_origins = sorted(df_raw['Origin'].unique().tolist()) if 'Origin' in df_raw.columns else ['TPE']
available_dests = sorted(df_raw['Destination'].unique().tolist()) if 'Destination' in df_raw.columns else ['NRT']

user_name = st.sidebar.text_input("使用者姓名 User Name", value="Esme")
current_origin = st.sidebar.selectbox("出發地 Airport (Origin)", options=available_origins, index=0)
current_destination = st.sidebar.selectbox("目的地 Airport (Destination)", options=available_dests, index=0)

departure_date = st.sidebar.date_input("去程日期 Departure Date", value=datetime.date(2026, 6, 10))
return_date = st.sidebar.date_input("回程日期 Return Date", value=datetime.date(2026, 6, 17))
passengers = st.sidebar.number_input("搭乘人數 Passengers", min_value=1, max_value=10, value=1)

st.sidebar.subheader("附加服務成本換算")
tax_check = st.sidebar.checkbox("加計海外刷卡手續費 (1.5%)", value=True)
luggage_check = st.sidebar.checkbox("加購託運行李重量", value=False)
luggage_weight = 0
if luggage_check:
    luggage_weight = st.sidebar.slider("加購重量 (KG)", 0, 40, 20)

st.sidebar.write("") 
search_btn = st.sidebar.button("🔍 開始進行智慧比價", use_container_width=True)

if "lock_origin" not in st.session_state: st.session_state.lock_origin = current_origin
if "lock_dest" not in st.session_state: st.session_state.lock_dest = current_destination
if "app_click_lock" not in st.session_state: st.session_state.app_click_lock = False

if current_origin != st.session_state.lock_origin or current_destination != st.session_state.lock_dest:
    st.session_state.app_click_lock = False
    st.session_state.lock_origin = current_origin
    st.session_state.lock_dest = current_destination

if search_btn:
    st.session_state.app_click_lock = True

# --- 主畫面排版 ---
st.title("MY PLANE TICKETS")
st.caption("GDS-GRADE MULTI-FLIGHT AGGREGATOR ENGINE")

if st.session_state.app_click_lock:
    df_filtered = df_raw[(df_raw['Origin'] == current_origin) & (df_raw['Destination'] == current_destination)].copy()

    def calculate_final_price(row):
        try: base = float(row['Price'])
        except: base = 15000
        if tax_check: base = base * 1.015
        if luggage_check: base += (luggage_weight * 150)
        return int(base * passengers)

    if not df_filtered.empty:
        df_filtered['計算總價'] = df_filtered.apply(calculate_final_price, axis=1)
        df_filtered = df_filtered.sort_values(by='計算總價').reset_index(drop=True)
        no_data_flag = False
    else:
        df_filtered = df_raw.copy()
        df_filtered['計算總價'] = df_filtered.apply(calculate_final_price, axis=1)
        df_filtered = df_filtered.sort_values(by='計算總價').reset_index(drop=True)
        no_data_flag = True

    total_combos = len(df_filtered) if not no_data_flag else 0
    min_expense = int(df_filtered['計算總價'].min()) if total_combos > 0 else 0
    avg_expense = int(df_filtered['計算總價'].mean()) if total_combos > 0 else 0
    max_expense = int(df_filtered['計算總價'].max()) if total_combos > 0 else 0

    # 三大指標框框
    col1, col2, col3 = st.columns(3)
    with col1: st.metric(label="總機票組合數", value=f"{total_combos} 組")
    with col2: st.metric(label="全網平均總票價", value=f"${avg_expense:,} TWD")
    with col3: st.metric(label="全網最高總票價", value=f"${max_expense:,} TWD")

    st.write("")

    # 💡 Esme 智慧大數據走勢分析面板
    if total_combos > 0:
        st.markdown(f"""
            <div style="background-color: #1e293b; padding: 20px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 25px;">
                <h4 style="margin: 0 0 15px 0; color: #ffffff; font-family: sans-serif;">💡 {user_name} 智慧大數據走勢分析：</h4>
                <ul style="margin: 0; padding-left: 20px; color: #cbd5e1; font-size: 15px; line-height: 1.8;">
                    <li>當前航線 <span style="color: #3b82f6; font-weight: bold;">{current_origin}</span> to <span style="color: #3b82f6; font-weight: bold;">{current_destination}</span> 的歷史來回機票區間：最高 <span style="color: #f43f5e; font-weight: bold;">${max_expense:,} TWD</span>，最低 <span style="color: #10b981; font-weight: bold;">${min_expense:,} TWD</span>.</li>
                    <li><strong>智慧旅遊建議：</strong> 目前的比價結果已根據您左側的行李和手續費勾選進行了『跨航司公平權重換算』，最新全網低價屬於健康推薦區間，可安心前往平台開票！</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["智慧跨航空低價推薦", "市場數據統計圖表", "原始航班矩陣總表"])

    with tab1:
        st.subheader("智慧跨航空推薦組合：由低到高排序")
        if total_combos == 0:
            st.warning("當前航線無符合數據，請嘗試切換別的出發地 or 目的地。")
        else:
            for idx, row in df_filtered.iterrows():
                label_text = "自由行首選：全網最省跨航空組合" if idx == 0 else f"推薦方案 (選項 {idx+1})"
                
                with st.container(border=True):
                    st.markdown(f"### {label_text}")
                    c_left, c_mid, c_right = st.columns([3, 3, 2])
                    with c_left:
                        st.write(f"去程航班 - {departure_date}")
                        st.subheader(str(row.get('DepTime', '08:30 - 12:45')))
                        airline_str = str(row.get('Airline', 'N/A'))
                        flight_str = str(row.get('FlightNo', 'N/A'))
                        st.write(f"{airline_str.split(' to ')[0]} ({flight_str.split(' to ')[0]})")
                    with c_mid:
                        st.write(f"回程航班 - {return_date}")
                        st.subheader(str(row.get('RetTime', '18:30 - 21:00')))
                        airline_p = airline_str.split(' to ')
                        flight_p = flight_str.split(' to ')
                        air_back = airline_p[1] if len(airline_p) > 1 else airline_p[0]
                        flt_back = flight_p[1] if len(flight_p) > 1 else flight_p[0]
                        st.write(f"{air_back} ({flt_back})")
                    with c_right:
                        # 🎯 右側價格欄位：完美接回官網開票跳轉按鈕
                        st.write("來回總票價 (含稅)")
                        st.title(f"${row['計算總價']:,}")
                        st.caption(f"航線：{current_origin} to {current_destination}")
                        
                        # 🔗 購買按鈕核心代碼回歸！面試展示時點擊會直接跳轉航空公司（範例設為 Skyscanner 國際站）
                        st.link_button("✈️ 前往官網開票", url="https://www.skyscanner.com.tw", use_container_width=True)

    with tab2:
        st.subheader("各航司組合含稅總票價對比 (智慧聚焦領先方案)")
        if total_combos > 0:
            chart_data = df_filtered.head(15)
            categories = [f"{str(r.get('Airline', '航司')).split(' to ')[0]}\n({str(r.get('FlightNo', 'N/A')).split(' to ')[0]})" for _, r in chart_data.iterrows()]
            raw_values = chart_data['計算總價'].tolist()
            
            formatted_data = []
            for i, val in enumerate(raw_values):
                if i == 0:
                    formatted_data.append({"value": val, "itemStyle": {"color": "#10b981", "shadowBlur": 10, "shadowColor": "rgba(16, 185, 129, 0.5)"}})
                else:
                    formatted_data.append({"value": val, "itemStyle": {"color": "#475569"}})
            
            y_min = int(min(raw_values) * 0.95)
            options = {
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}, "formatter": "{b}<br/>來回總票價: <b>${c}</b> TWD"},
                "grid": {"top": "12%", "left": "8%", "right": "5%", "bottom": "18%"},
                "xAxis": {"type": "category", "data": categories, "axisLabel": {"rotate": 15, "color": "#94a3b8", "fontSize": 12, "interval": 0}},
                "yAxis": {"type": "value", "name": "價格 (TWD)", "min": y_min, "axisLabel": {"color": "#94a3b8"}, "splitLine": {"lineStyle": {"color": "#334155"}}},
                "series": [{"type": "bar", "data": formatted_data, "barWidth": "40%", "label": {"show": True, "position": "top", "color": "#ffffff", "fontWeight": "bold", "formatter": "${c}"}}],
                "backgroundColor": "#0f172a"
            }
            st_echarts(options=options, height="450px")
        else:
            st.info("暫無數據生成圖表。")

    with tab3:
        st.subheader("ALL SCHEDULED FLIGHT DETAILS")
        st.data_editor(
            df_filtered, use_container_width=True, disabled=True, hide_index=True,
            column_config={
                "Origin": st.column_config.TextColumn("Origin 🛫 出發機場"),
                "Destination": st.column_config.TextColumn("Destination 🛬 目的機場"),
                "Airline": st.column_config.TextColumn("Airline ✈️ 航空公司"),
                "FlightNo": st.column_config.TextColumn("FlightNo 🎫 航班代號"),
                "DepTime": st.column_config.TextColumn("DepTime 🕒 去程時間區間"),
                "RetTime": st.column_config.TextColumn("RetTime 🕒 回程時間區間"),
                "Price": st.column_config.NumberColumn("Price 💵 原始淨票價", format="$%d"),
                "計算總價": st.column_config.NumberColumn("Total Price 💰 試算總價 (含稅與行李)", format="$%d")
            }
        )
else:
    st.write("歡迎使用智慧跨航空機票比價系統！請在左側選擇您的出發地、目的地及附加服務，並點擊『開始進行智慧比價』解鎖大數據分析結果。")