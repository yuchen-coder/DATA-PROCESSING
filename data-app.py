import streamlit as st
import pandas as pd
import altair as alt

# =========================================================================
# 🛠️ 【核心相容補丁】跨版本環境相容性補丁 (預防環境 Pandas 衝突)
# =========================================================================
if not hasattr(pd.Series, 'iteritems'):
    pd.Series.iteritems = pd.Series.items
if not hasattr(pd.DataFrame, 'iteritems'):
    pd.DataFrame.iteritems = pd.DataFrame.items

# ==========================================
# 1. 網頁基礎系統設定 (必須放在最頂端)
# ==========================================
st.set_page_config(
    page_title="Global Market", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

# ==========================================
# 2. 🦄 結構安全零衝突：夢幻可愛紫色風暴 CSS 樣式表
# ==========================================
st.markdown(
    """
    <style>
    /* 🔒 【結構安全鎖】使用不影響排版尺寸的「透明隱形技術」 */
    [data-testid="stSidebarCollapseButton"], 
    [data-testid="stSidebarCollapseButton"] button, 
    [data-testid="stSidebarCollapseButton"] svg {
        opacity: 0 !important;               
        pointer-events: none !important;     
    }
    
    /* 🔮 側邊欄換上超可愛的「薰衣草馬卡龍淡紫色」 */
    [data-testid="stSidebar"] {
        background-color: #F3E8FF !important;
    }
    
    /* 🎯 側邊欄「目錄」標題樣式 */
    .custom-sidebar-title {
        font-size: 36px !important;
        font-weight: 900 !important;
        color: #4C1D95 !important; 
        margin-top: 2rem !important;  
        margin-bottom: 1rem !important;
        letter-spacing: 2px;
    }
    
    /* 側邊欄單選按鈕字體加深加粗 */
    .stRadio p {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #5B21B6 !important;
    }
    
    /* 🎈 讓橫向拉桿 (Slider) 變身夢幻粉紫色 */
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: #A855F7 !important;
        border: 3px solid #FFFFFF !important;
        box-shadow: 0px 3px 10px rgba(168, 85, 247, 0.4) !important;
        width: 24px !important;
        height: 24px !important;
    }
    div[data-testid="stSlider"] div[aria-valuemax] {
        background: linear-gradient(to right, #C084FC, #E9D5FF) !important;
    }
    
    /* 🎯 主頁面大標題風格化：4.5rem 巨幕大字體 */
    .main-title {
        color: #7C3AED !important; 
        font-weight: bold !important; 
        font-size: 4.5rem !important; 
        line-height: 1.2 !important;
        margin-top: 0.5rem !important;
        margin-bottom: 2rem !important;
        text-shadow: 3px 3px 8px rgba(124, 58, 237, 0.2) !important; 
    }
    
    /* 數據健康檢查小精靈的外框 */
    .health-check-box {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 12px;
        border: 2px dashed #D8B4FE;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 3. 使用 Pandas 載入並處理原始數據
# ==========================================
try:
    df = pd.read_csv('資料處理期末原始資料.csv')
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Year_Month'] = df['Order_Date'].dt.strftime('%Y-%m')
    total_missing_values = df.isnull().sum().sum()
    all_regions = sorted(df['Region'].unique())
except FileNotFoundError:
    st.error("❌ 找不到名為 '資料處理期末原始資料.csv' 的檔案，請確認已放入 Stlite 左側的檔案樹中喔！")
    st.stop()

# ==========================================
# 4. 初始化 Session State (原生安全隔離區)
# ==========================================
for r in all_regions:
    if f"thresh_{r}" not in st.session_state:
        st.session_state[f"thresh_{r}"] = 0  
if "global_sync_thresh" not in st.session_state:
    st.session_state["global_sync_thresh"] = 0

# ==========================================
# 5. 左側側邊欄：純目錄控制面板
# ==========================================
st.sidebar.markdown('<p class="custom-sidebar-title">🔮 目錄</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "請切換分析報表：",
    ["銷售表現分析", "KPI與目標達成率分析", "客戶行為分析", "時間趨勢分析", "銷售漏斗與勝率分析"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <div class="health-check-box">
        <p style='margin:0; font-weight:bold; color:#6D28D9;'>🧚‍♀️ 數據健康檢查小精靈</p>
        <p style='margin:5px 0 0 0; font-size:13px; color:#4B5563;'>本資料集欄位：<b>{len(df.columns)} 個</b></p>
        <p style='margin:3px 0 0 0; font-size:13px; color:#4B5563;'>總數據筆數：<b>{len(df):,} 筆</b></p>
        <p style='margin:3px 0 0 0; font-size:13px; color:#059669;'>全表遺漏值數量：<b>{total_missing_values} (極度完美!)</b></p>
    </div>
    """, 
    unsafe_allow_html=True
)

# ==========================================
# 6. 主頁面內容：大字體巨幕呈現
# ==========================================
st.markdown('<p class="main-title">🦄 Global Market 全球市場數據決策儀表板</p>', unsafe_allow_html=True)
st.markdown(f"💜 當前正在功能瀏覽：**{menu}**")
st.markdown("---")

# ---- 功能 1：銷售表現分析 ----
if menu == "銷售表現分析":
    st.header("📊 各地區銷售表現分析")
    region_revenue = df.groupby('Region')['Revenue'].sum().reset_index()
    
    st.write("### 🗺️ 各地區總營業額統計 (Bar Chart)")
    chart1 = alt.Chart(region_revenue).mark_bar(
        color='#A78BFA', cornerRadiusTopLeft=10, cornerRadiusTopRight=10
    ).encode(
        x=alt.X('Region:N', axis=alt.Axis(labelAngle=0, labelFontSize=13), title="地區 (Region)"),
        y=alt.Y('Revenue:Q', title="總營業額 (USD)")
    ).properties(height=400)
    
    st.altair_chart(chart1, use_container_width=True)
    
    st.write("### 📋 詳細地區銷售數據報表")
    region_summary = df.groupby('Region')[['Units_Sold', 'Revenue']].sum()
    region_summary.columns = ['總銷售數量', '總營業額 (USD)']
    st.dataframe(region_summary)

# ---- 功能 2：KPI與目標達成率分析 ----
elif menu == "KPI與目標達成率分析":
    st.header("🎯 KPI與目標達成率動態模擬")
    
    # —— 「哇嗚」組件 2：決策模式切換 ——
    st.write("### 🔮 決策水晶球：在地化精準調音台")
    strategy_mode = st.radio(
        "🛠️ **選擇戰略部署模式：**",
        ["🌍 全球統一門檻下達 (齊頭式策略)", "🎯 獨立海外區域微調 (四個拉桿同時現身)"],
        horizontal=True
    )
    
    st.markdown(" ")
    
    if strategy_mode == "🌍 全球統一門檻下達 (齊頭式策略)":
        st.slider(
            "🎚️ 請滑動調整「全球一刀切」准入金額 (USD)：",
            min_value=0, max_value=1999,
            step=1,
            key="global_sync_thresh"
        )
        for r in all_regions:
            st.session_state[f"thresh_{r}"] = st.session_state["global_sync_thresh"]
            
    else:
        st.info("💡 **高階數據調音台已啟動**：您可以同時拖動下方各海外區域的專屬拉桿，進行在地化的敏感度測試！")
        
        cols = st.columns(len(all_regions))
        for i, r in enumerate(all_regions):
            with cols[i]:
                st.slider(
                    f"🔮 {r} 核心門檻 (USD)",
                    min_value=0, max_value=1999,
                    step=1,
                    key=f"thresh_{r}"
                )

    # —— 「哇嗚」組件 3：智慧多區黃色預警 ——
    triggered_warnings = []
    for r in all_regions:
        r_val = st.session_state[f"thresh_{r}"]
        if r_val <= 400:
            triggered_warnings.append(f"<b>{r}區</b> (${r_val:,})")
            
    if triggered_warnings:
        warning_text = "、".join(triggered_warnings)
        st.warning(f"⚠️ **決策水晶球・風險預警**：當前系統偵測到 {warning_text} 的過濾門檻低於安全水位 (\$400)。這會導致該區報表混入大量瑣碎的低價值訂單，稀釋跨國集團的決策品質！建議將拉桿往右調高。")

    # —— 使用高階向量化篩選 (4區連動過濾數據) ——
    condition = pd.Series(True, index=df.index)
    for r in all_regions:
        current_thresh = st.session_state[f"thresh_{r}"]
        condition &= ~((df['Region'] == r) & (df['Revenue'] < current_thresh))
        
    filtered_df = df[condition]
    
    # 渲染結果
    if filtered_df.empty:
        st.error("🔮 警告：當前各區設定的門檻過高，導致全球商機數據遭到全數蒸發！請調低拉桿。")
    else:
        total_rev = filtered_df['Revenue'].sum()
        total_tar = filtered_df['Target'].sum()
        achievement_rate = round((total_rev / total_tar) * 100, 2) if total_tar > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("過濾後全球總營收 (Actual)", f"${total_rev:,.0f}")
        col2.metric("預設全球總目標 (Target)", f"${total_tar:,.0f}")
        col3.metric("整體目標達成率 (%)", f"{achievement_rate}%")
        st.markdown("---")
        
        st.write("### ⚖️ 在地化防線部署後：各地區實際營業額 vs 預期目標對比圖")
        kpi_data = filtered_df.groupby('Region')[['Revenue', 'Target']].sum().reset_index()
        kpi_melted = kpi_data.melt(id_vars='Region', value_vars=['Revenue', 'Target'], var_name='Metric', value_name='Amount')
        
        # 🌟 基礎子圖形狀與尺寸安全設定 (全英文底層，避免網頁前端不支援中文圖例編譯)
        base_chart = alt.Chart(kpi_melted).mark_bar(
            cornerRadiusTopLeft=6, cornerRadiusTopRight=6
        ).encode(
            x=alt.X('Metric:N', axis=alt.Axis(labelAngle=0), title=None),
            y=alt.Y('Amount:Q', title="金額 (USD)"),
            color=alt.Color('Metric:N', scale=alt.Scale(range=['#C084FC', '#E9D5FF']), title="數據指標")
        ).properties(
            width=130, 
            height=300
        )
        
        chart2 = base_chart.facet(
            column=alt.Column('Region:N', header=alt.Header(labelAngle=0, title="地區 (Region)", labelFontSize=13))
        )
        
        st.altair_chart(chart2)

# ---- 功能 3：客戶行為分析 ----
elif menu == "客戶行為分析":
    st.header("👥 客戶行為分析")
    segment_units = df.groupby('Customer_Segment')['Units_Sold'].sum().reset_index()
    
    st.write("### 🏢 各客戶客群總銷售量統計 (Bar Chart)")
    chart3 = alt.Chart(segment_units).mark_bar(
        color='#818CF8', cornerRadiusTopLeft=10, cornerRadiusTopRight=10  
    ).encode(
        x=alt.X('Customer_Segment:N', axis=alt.Axis(labelAngle=0, labelFontSize=13), title="客戶客群 (Segment)"),
        y=alt.Y('Units_Sold:Q', title="總銷售量 (Units)")
    ).properties(height=400)
    
    st.altair_chart(chart3, use_container_width=True)
    
    st.write("### 📋 產品類別 vs. 客戶客群 交叉銷量矩陣")
    cross_table = pd.crosstab(
        df['Product_Category'], 
        df['Customer_Segment'], 
        values=df['Units_Sold'], 
        aggfunc='sum'
    ).fillna(0)
    st.dataframe(cross_table)

# ---- 功能 4：時間趨勢分析 ----
elif menu == "時間趨勢分析":
    st.header("📈 時間趨勢分析")
    monthly_trend = df.sort_values('Year_Month').groupby('Year_Month')['Revenue'].sum().reset_index()
    
    st.write("### 📅 全球每月總營業額趨勢走勢 (Line Chart)")
    chart4 = alt.Chart(monthly_trend).mark_line(
        color='#7C3AED', strokeWidth=3, point=alt.OverlayMarkDef(color='#9333EA', size=60)
    ).encode(
        x=alt.X('Year_Month:N', axis=alt.Axis(labelAngle=0), title="月份 (Year-Month)"),
        y=alt.Y('Revenue:Q', title="總營業額 (USD)")
    ).properties(height=400)
    
    st.altair_chart(chart4, use_container_width=True)

# ---- 功能 5：銷售漏斗與勝率分析 ----
elif menu == "銷售漏斗與勝率分析":
    st.header("📈 全球銷售漏斗與勝率分析 (Sales Win Rate)")
    st.markdown(r"本模組專門剖析各產品與各地區之銷售轉換品質，計算公式：$\text{勝率 (\%)} = \frac{\text{Won 成功筆數}}{\text{總商機案量 (Won + Lost + Opportunity)}} \times 100$")
    
    tab1, tab2 = st.tabs(["📦 產品線轉換勝率", "🌍 跨國區域轉換勝率"])
    
    with tab1:
        st.write("### 🏆 各產品類別結案勝率比較 (Won Rate)")
        prod_stage = df.groupby(['Product_Category', 'Stage']).size().unstack(fill_value=0)
        for stage in ['Won', 'Lost', 'Opportunity']:
            if stage not in prod_stage.columns:
                prod_stage[stage] = 0
                
        prod_stage['Total_Deals'] = prod_stage['Won'] + prod_stage['Lost'] + prod_stage['Opportunity']
        prod_stage['Win_Rate'] = (prod_stage['Won'] / prod_stage['Total_Deals']) * 100
        prod_stage_res = prod_stage.reset_index()
        
        # 🔒【全英文核心隔離】重新命名欄位為乾淨英文，澈底摧毀特殊符號 (%) 引發的 JavaScript 網頁編譯錯誤！
        prod_stage_res.columns = ['Product_Category', 'Lost', 'Opportunity', 'Won', 'Total_Deals', 'Win_Rate']
        
        chart_p_win = alt.Chart(prod_stage_res).mark_bar(
            color='#7C3AED', cornerRadiusTopLeft=10, cornerRadiusTopRight=10
        ).encode(
            x=alt.X('Product_Category:N', axis=alt.Axis(labelAngle=0, labelFontSize=13), title="產品類別"),
            y=alt.Y('Win_Rate:Q', title="結案勝率 (%)"),
            tooltip=[
                alt.Tooltip('Product_Category:N', title='產品類別'),
                alt.Tooltip('Win_Rate:Q', title='勝率 (%)', format='.2f'),
                alt.Tooltip('Total_Deals:Q', title='總商機案量'),
                alt.Tooltip('Won:Q', title='成功筆數 (Won)')
            ]
        ).properties(height=350)
        
        st.altair_chart(chart_p_win, use_container_width=True)
        
        st.write("📋 **產品類別之銷售漏斗詳細數據表**")
        # 呈現給人類看的時候再轉成漂亮的中文字元，安全又漂亮
        prod_stage_display = prod_stage_res.rename(columns={
            'Product_Category': '產品類別',
            'Lost': '流失 (Lost)',
            'Opportunity': '洽談中 (Opportunity)',
            'Won': '成功 (Won)',
            'Total_Deals': '總商機案量',
            'Win_Rate': '勝率 (%)'
        })
        st.dataframe(prod_stage_display)
        
    with tab2:
        st.write("### 🗺️ 各地區結案勝率比較 (Won Rate)")
        reg_stage = df.groupby(['Region', 'Stage']).size().unstack(fill_value=0)
        for stage in ['Won', 'Lost', 'Opportunity']:
            if stage not in reg_stage.columns:
                reg_stage[stage] = 0
                
        reg_stage['Total_Deals'] = reg_stage['Won'] + reg_stage['Lost'] + reg_stage['Opportunity']
        reg_stage['Win_Rate'] = (reg_stage['Won'] / reg_stage['Total_Deals']) * 100
        reg_stage_res = reg_stage.reset_index()
        
        # 🔒【全英文核心隔離】重新命名欄位為乾淨英文，澈底摧毀特殊符號 (%) 引發的 JavaScript 網頁編譯錯誤！
        reg_stage_res.columns = ['Region', 'Lost', 'Opportunity', 'Won', 'Total_Deals', 'Win_Rate']
        
        chart_r_win = alt.Chart(reg_stage_res).mark_bar(
            color='#A78BFA', cornerRadiusTopLeft=10, cornerRadiusTopRight=10
        ).encode(
            x=alt.X('Region:N', axis=alt.Axis(labelAngle=0, labelFontSize=13), title="全球地區"),
            y=alt.Y('Win_Rate:Q', title="結案勝率 (%)"),
            tooltip=[
                alt.Tooltip('Region:N', title='地區'),
                alt.Tooltip('Win_Rate:Q', title='勝率 (%)', format='.2f'),
                alt.Tooltip('Total_Deals:Q', title='總商機案量'),
                alt.Tooltip('Won:Q', title='成功筆數 (Won)')
            ]
        ).properties(height=350)
        
        st.altair_chart(chart_r_win, use_container_width=True)
        
        st.write("📋 **全球地區之銷售漏斗詳細數據表**")
        # 呈現給人類看的時候再轉成漂亮的中文字元，安全又漂亮
        reg_stage_display = reg_stage_res.rename(columns={
            'Region': '地區',
            'Lost': '流失 (Lost)',
            'Opportunity': '洽談中 (Opportunity)',
            'Won': '成功 (Won)',
            'Total_Deals': '總商機案量',
            'Win_Rate': '勝率 (%)'
        })
        st.dataframe(reg_stage_display)
