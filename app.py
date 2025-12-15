import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
import db_manager
import constants

# --- Page Config ---
st.set_page_config(
    page_title="Mom’ｓココロ Diary",
    page_icon="🤍", # Changed to white heart as flower is unwanted
    layout="wide"
)

# --- CSS Styling ---
# --- CSS Styling ---
# --- CSS Styling ---
# --- CSS Styling ---
st.markdown("""
<style>
    /* Botanical Peppermint Theme Variables */
    :root {
        --primary-bg: #E8F5E9; /* Peppermint Green */
        --card-bg: rgba(255, 255, 255, 0.96); /* Higher Opacity White */
        --text-primary: #0B3D15; /* Much Darker Green for better readability */
        --text-header: #4E342E; /* Darker Brown */
        --text-secondary: #212121; /* Almost Black */
        --accent-gold: #C5A059;
        --accent-soft: #A5D6A7;
        --accent-pop: #F8BBD0;
        --accent-warm: #FF8A65; /* Warm Coral for title accent */
    }

    /* Global App Styling */
    .stApp {
        background-color: var(--primary-bg);
        background-image: url("app/static/background.png"); 
        color: var(--text-primary);
        font-family: "Helvetica Neue", "Arial", "Hiragino Kaku Gothic ProN", "Hiragino Sans", sans-serif;
    }
    
    /* Background Image Handling */
    /* We will inject the base64 background in Python code below this block to ensure it works */

    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 500 !important; /* Slightly bolder for readability */
        letter-spacing: 0.05em;
        font-family: 'Georgia', serif;
        text-shadow: 0 1px 2px rgba(255,255,255,0.8); /* Halo effect for text on bg */
    }

    /* Main Header */
    .main-header {
        font-size: 2.8rem; /* Slightly larger */
        color: var(--text-header); /* Hokkori Brown */
        text-align: center;
        margin-bottom: 2.5rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid var(--accent-soft); /* Peppermint Green */
        display: block;
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
        background-color: rgba(255,255,255,0.8);
        padding: 1rem 3rem;
        border-radius: 50px; /* Rounded for cuteness */
        font-family: "M PLUS Rounded 1c", "Hiragino Maru Gothic Pro", "Meiryo UI", "Arial Rounded MT Bold", sans-serif;
        font-weight: 800 !important;
    }

    /* Sub Header */
    .sub-header {
        font-size: 1.4rem;
        color: var(--text-primary);
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px dotted var(--text-primary);
        padding-bottom: 0.5rem;
        font-weight: 600;
        background-color: rgba(255,255,255,0.6);
        padding-left: 10px;
        border-radius: 5px;
    }

    /* Question Card */
    .question-card {
        background-color: var(--card-bg); /* Use the new high opacity var */
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 2px solid var(--accent-soft);
        border-left: 6px solid var(--accent-pop);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08); /* Darker shadow definition */
        backdrop-filter: blur(10px); /* Stronger blur */
    }
    .question-card b {
        color: var(--text-primary);
        font-weight: 700;
    }

    /* Customizing Streamlit Elements */
    .stRadio > label {
        font-weight: 500;
        color: var(--text-secondary);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: none;
        background-color: rgba(255,255,255,0.4);
        padding: 10px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.7);
        border-radius: 10px;
        border: 1px solid var(--accent-soft);
        color: var(--text-secondary);
        font-weight: 500;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF;
        color: var(--text-primary) !important;
        font-weight: 700;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* Buttons */
    div.stButton > button {
        background-color: var(--text-primary);
        color: white;
        border-radius: 30px;
        padding: 0.6rem 3rem;
        border: none;
        box-shadow: 0 4px 12px rgba(46, 93, 50, 0.3);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #1B5E20;
        transform: translateY(-2px);
        color: white;
    }
    
    /* Alerts/Toasts */
    .stToast {
        background-color: var(--card-bg);
        color: var(--text-primary);
        border-left: 4px solid var(--accent-pop);
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.8);
        border: 1px solid var(--accent-soft);
        color: var(--text-primary);
    }

</style>
""", unsafe_allow_html=True)

import base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    try:
        bin_str = get_base64_of_bin_file(png_file)
        page_bg_img = '''
        <style>
        .stApp {
            background-image: url("data:image/png;base64,%s");
            background-size: cover;
            background-attachment: fixed;
        }
        </style>
        ''' % bin_str
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError:
        pass # Fallback to solid color defined in CSS

def main():
    # Initialize DB
    db_manager.init_db()
    
    # Apply Background
    set_png_as_page_bg('background.png')

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="main-header">Mom’ｓココロ Diary</div>', unsafe_allow_html=True)

    # --- Sidebar: Date Selection ---
    with st.sidebar:
        st.header("📅 日付選択")
        today = datetime.date.today()
        # Custom styling for standard widgets is limited, but we rely on theme variables where possible
        selected_date = st.date_input("記録する日付", today)
        
        # History
        st.divider()
        st.write("📝 記録済みの日付:")
        history_dates = db_manager.get_all_entry_dates()
        for d_str in history_dates:
            st.text(f"- {d_str}")

    # --- Tabs ---
    tab1, tab2 = st.tabs(["📝 記録・編集", "📖 過去の日記一覧"])

    with tab1:
        show_record_page(selected_date)
    
    with tab2:
        show_history_page()

def show_record_page(selected_date):
    # --- Load Data for Selected Date ---
    entry_data = db_manager.get_entry(selected_date)
    
    default_comment = ""
    default_answers = {q['id']: 3 for q in constants.QUESTIONS} # Default to 3
    
    if entry_data:
        st.success(f"📅 {selected_date} の記録を読み込みました")
        default_comment = entry_data.get('comment', "")
        # Merge saved answers with defaults (safe for schema changes)
        saved_answers = entry_data.get('answers', {})
        for k, v in saved_answers.items():
            default_answers[k] = v
    else:
        st.info(f"🆕 {selected_date} の新しい記録を作成します")

    # --- Main Form ---
    with st.form("diary_form"):
        st.subheader("今日のひとこと")
        comment_input = st.text_input("今の気持ちや出来事を一言で...", value=default_comment, placeholder="例: 今日は子供と一緒に公園に行けて楽しかった！")
        
        st.subheader("今日の私の気持ちを確認してみる！")
        st.write("今の気分に一番近いものを選んでください。")

        # Questions
        current_answers = {}
        for q in constants.QUESTIONS:
            st.markdown(f'<div class="question-card"><b>{q["id"]}</b>: {q["text"]}</div>', unsafe_allow_html=True)
            
            # Identify index for default value (1-5 mapped to 0-4)
            # stored value is 1..5
            default_val = default_answers.get(q['id'], 3)
            
            val = st.select_slider(
                f"回答 ({q['id']})",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: constants.CHOICES_POSITIVE[x],
                value=default_val, # select_slider takes value, not index
                key=f"{selected_date}_{q['id']}", # Unique key per date to force refresh if date changes
                label_visibility="collapsed"
            )
            current_answers[q['id']] = val

        # Submit Button
        st.markdown("<br>", unsafe_allow_html=True) # Spacer
        submitted = st.form_submit_button("💾 保存して診断する", use_container_width=True, type="primary")

    # --- Handling Submission ---
    if submitted:
        # Save to DB
        db_manager.save_entry(selected_date, comment_input, current_answers)
        st.toast("✅ 記録を保存しました！")
        
        # Display Results immediately
        calculate_and_display_results(current_answers, key_suffix="record_submitted")
    
    elif entry_data:
        # If not submitted but data exists (viewing past/current entry), show results
        calculate_and_display_results(default_answers, key_suffix="record_viewing")

def show_history_page():
    st.markdown('<div class="sub-header">📖 過去の日記一覧</div>', unsafe_allow_html=True)
    entries = db_manager.get_all_entries()
    
    if not entries:
        st.info("まだ記録がありません。")
        return

    # Prepare data for dataframe
    df_data = []
    for e in entries:
        df_data.append({
            "日付": e['date'],
            "ひとこと": e['comment']
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(
        df, 
        use_container_width=True,
        hide_index=True,
        column_config={
            "日付": st.column_config.TextColumn("日付", width="medium"),
            "ひとこと": st.column_config.TextColumn("ひとこと", width="large"),
        }
    )
    
    st.divider()
    st.subheader("🔍 過去の私の心バランスを見る")
    
    # Date selection
    # Create option list (Date + Comment snippet)
    date_options = [e['date'] for e in entries]
    selected_date_str = st.selectbox("詳しく見たい日付を選択してください", date_options)
    
    if selected_date_str:
        # Find the entry
        selected_entry = next((e for e in entries if e['date'] == selected_date_str), None)
        
        if selected_entry:
            st.markdown(f"### 📅 {selected_entry['date']} の記録")
            st.info(f"**ひとこと**: {selected_entry['comment']}")
            
            # Display the visualization and advice
            calculate_and_display_results(selected_entry['answers'], key_suffix=f"history_{selected_date_str}")

def calculate_and_display_results(answers, key_suffix=""):
    # ... (omitted) ...
    # This function is used by both the main record page and the history page.
    # To avoid duplicate element IDs when calling this multiple times in one session (or in loops),
    # we need to ensure unique keys for Streamlit widgets.

    # --- 1. VARY Positive Domains (I-VII) ---
    domains = {
        "I. 愛着・喜び": [],
        "II. 効力感": [],
        "III. 自己受容": [],
        "IV. パートナーシップ": [],
        "V. アンガーマネジメント": [],
        "VI. リカバリー": [],
        "VII. 自律性": []
    }
    
    # Process Questions
    for q in constants.QUESTIONS:
        score = answers.get(q['id'], 0)
        domain = q['domain']
        if domain in domains:
            domains[domain].append(score)

    # Calculate VARY Averages
    radar_data = {}
    for d, scores in domains.items():
        if scores:
            avg = sum(scores) / len(scores)
            radar_data[d] = avg
        else:
            radar_data[d] = 0

    # Display VARY Radar
    st.markdown('<div class="sub-header">📊 診断結果: ペアレンティング・バランス</div>', unsafe_allow_html=True)
    
    categories = list(radar_data.keys())
    values = list(radar_data.values())
    
    # Close the loop
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='あなた',
        line_color='#A8C3A4' # Changed to Sage Green
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=20, b=20)
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True, key=f"radar_chart_{key_suffix}")
    
    with col2:
         # Sort strong and weak points
        sorted_domains = sorted(radar_data.items(), key=lambda x: x[1], reverse=True)
        if sorted_domains:
            best_domain_name, best_score = sorted_domains[0]
            # Load Character Image
            try:
                # Using the character image provided by user
                char_img_base64 = get_base64_of_bin_file("IMG_8931.PNG")
                char_img_html = f'<img src="data:image/png;base64,{char_img_base64}" class="character-img">'
            except Exception:
                char_img_html = "" # Fallback if image not found

            st.info(f"✨ **今日の強み**: {best_domain_name}")
            
            if best_domain_name in constants.DIAGNOSTIC_FEEDBACK:
                 content = constants.DIAGNOSTIC_FEEDBACK[best_domain_name]
                 
                 # Styled Text for Speech Bubble
                 bubble_html = f"""
                 <style>
                 .character-container {{
                     display: flex;
                     align_items: flex-start;
                     gap: 20px;
                     margin-top: 15px;
                     margin-bottom: 25px;
                 }}
                 .character-img {{
                     width: 120px; /* Adjust size as needed */
                     height: auto;
                     object-fit: contain;
                     filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
                 }}
                 .speech-bubble {{
                     position: relative;
                     background: #FFF;
                     border-radius: 15px;
                     padding: 20px;
                     color: #4E342E;
                     box-shadow: 0 4px 10px rgba(0,0,0,0.05);
                     border: 2px solid #A5D6A7; /* Peppermint Green */
                     flex: 1;
                 }}
                 .speech-bubble:after {{
                     content: '';
                     position: absolute;
                     left: 0;
                     top: 30px;
                     width: 0;
                     height: 0;
                     border: 12px solid transparent;
                     border-right-color: #A5D6A7;
                     border-left: 0;
                     margin-left: -12px;
                 }}
                 .bubble-title {{
                     font-weight: bold;
                     color: #C5A059;
                     font-size: 1.1em;
                     margin-bottom: 8px;
                     display: block;
                 }}
                 </style>
                 
                 <div class="character-container">
                    {char_img_html}
                    <div class="speech-bubble">
                        <span class="bubble-title">{content['high_title']}</span>
                        {content['high_text']}
                    </div>
                 </div>
                 """
                 st.markdown(bubble_html, unsafe_allow_html=True)

    # --- Analysis & Advice (SOS Signs) ---
    st.markdown('<div class="sub-header">💡 詳細分析 & メッセージ</div>', unsafe_allow_html=True)
    
    # 2. Check for Low Scores (<= 3.0)
    low_domains = [d for d, s in radar_data.items() if s <= 3.0]

    if low_domains:
        st.warning("🆘 **心からのSOSサイン**")
        st.markdown("""
        > スコアが低い領域は、あなたが悪いわけではありません。
        > その部分が「疲れ」や「ストレス」でSOSを出しているサインです。
        """)
        
        for d_name in low_domains:
            if d_name in constants.DIAGNOSTIC_FEEDBACK:
                content = constants.DIAGNOSTIC_FEEDBACK[d_name]
                with st.expander(f"**{d_name}** (スコア: {radar_data[d_name]:.1f}) - {content['low_title']}", expanded=True):
                    st.markdown(f"""
                    {content['low_text']}
                    
                    **🍀 アドバイス**  
                    {content['advice']}
                    """)
    else:
        st.success("全ての領域でバランスが取れています！心の状態は非常に安定しています。この調子で自分を大切にしてください。")


if __name__ == "__main__":
    main()
