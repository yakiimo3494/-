
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="📍 streamlit-js-eval テスト", layout="centered")
st.title("📡 streamlit-js-eval 動作確認")

if 'gps_refresh' not in st.session_state:
    st.session_state.gps_refresh = 0

if st.button("🔄 GPS再取得テスト"):
    st.session_state.gps_refresh += 1

gps_result = streamlit_js_eval(
    js_expressions="""
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const coords = pos.coords.latitude + ',' + pos.coords.longitude;
                Streamlit.setComponentValue('SUCCESS:' + coords);
            },
            (err) => {
                Streamlit.setComponentValue('ERROR:' + err.code + ':' + err.message);
            }
        );
    """,
    key=f"gps_test_{st.session_state.gps_refresh}"
)

if gps_result:
    if gps_result.startswith("SUCCESS:"):
        gps = gps_result.replace("SUCCESS:", "")
        st.success(f"✅ 取得成功: {gps}")
    elif gps_result.startswith("ERROR:"):
        parts = gps_result.split(':')
        code = parts[1] if len(parts) > 1 else 'N/A'
        msg = parts[2] if len(parts) > 2 else '詳細不明'
        st.error(f"❌ GPS取得失敗: {msg}（コード: {code}）")
    else:
        st.warning("⚠️ 予期しないレスポンス")
else:
    st.info("🕒 まだ取得していません。ボタンを押してください。")
