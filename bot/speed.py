# bot/speed.py

import speedtest

def test():
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download() / 1024 / 1024  # Convert to Mbps
    upload = st.upload() / 1024 / 1024
    ping = st.results.ping
    return f"📶 Speed Test Results:\n\n🔽 Download: {download:.2f} Mbps\n🔼 Upload: {upload:.2f} Mbps\n⏱ Ping: {ping:.2f} ms"
