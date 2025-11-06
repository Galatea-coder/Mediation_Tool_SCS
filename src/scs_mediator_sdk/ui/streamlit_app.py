from PIL import Image
import json, os
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="SCS Instructor Console", layout="wide")
st.title("SCS Instructor Console — SDK v4")

API_URL = os.environ.get("SCS_API_URL", "http://localhost:8000")

st.sidebar.header("Scenario")

# --- Map Overlay Configurator ---
st.sidebar.header("Map Overlay")
opt = st.sidebar.radio("Choose overlay source", ["Auto", "Pick PNG", "Render GeoJSON"])
selected_map = None

def preview_map(path):
    if os.path.exists(path):
        st.sidebar.image(path, caption="Map Preview", use_column_width=True)
        return path
    else:
        st.sidebar.warning(f"Map not found: {path}")

if opt == "Auto":
    # keep earlier auto-detect
    pass
elif opt == "Pick PNG":
    pngs = [os.path.join('assets/maps', p) for p in os.listdir('assets/maps') if p.lower().endswith(('.png','.jpg','.jpeg'))]
    choice = st.sidebar.selectbox("PNG", pngs if pngs else ["(none)"])
    if choice != "(none)":
        selected_map = preview_map(choice)
elif opt == "Render GeoJSON":
    geos = [os.path.join('assets/geo', g) for g in os.listdir('assets/geo')] if os.path.exists('assets/geo') else []
    gchoice = st.sidebar.selectbox("GeoJSON", geos if geos else ["(none)"])
    out_path = st.sidebar.text_input("Output PNG", "assets/maps/overlay.png")
    if st.sidebar.button("Render"):
        if gchoice != "(none)":
            # Call the renderer (assumes Python available in container)
            import subprocess
            try:
                subprocess.run(["python", "render_geo.py", gchoice, out_path], check=True)
                st.sidebar.success(f"Rendered to {out_path}")
                preview_map(out_path)
            except Exception as e:
                st.sidebar.error(f"Render failed: {e}")


case_dir = st.sidebar.text_input("Cases folder", "cases/scs")
scenario_files = [f for f in os.listdir(case_dir) if f.endswith(".json")] if os.path.exists(case_dir) else []
scenario = st.sidebar.selectbox("Scenario file", scenario_files if scenario_files else ["(none)"])

# Sidebar map preview
map_candidates = []
# per-scenario named maps
if scenario != "(none)":
    stem = os.path.splitext(scenario)[0].lower()
    if os.path.exists('assets/maps'):
        for fn in os.listdir('assets/maps'):
            if stem in fn.lower():
                map_candidates.append(os.path.join('assets/maps', fn))
# fallback overlay and generic
for fn in ['assets/maps/overlay.png', 'assets/maps/map_second_thomas.png', 'assets/maps/map_scarborough.png', 'assets/maps/map_kasawari.png', 'assets/maps/map_natuna.png']:
    if os.path.exists(fn):
        map_candidates.append(fn)
if map_candidates:
    st.sidebar.image(map_candidates[0], caption="Scenario Map Preview", use_column_width=True)

if scenario != "(none)":
    with open(os.path.join(case_dir, scenario), "r", encoding="utf-8") as f:
        case = json.load(f)
    st.subheader("Scenario Snapshot")
    st.json(case)
else:
    case = {"id":"demo_case","weather_state":"calm","media_visibility":2}

# Auto-load per-scenario calibration file if present
if scenario != "(none)":
    calib_path = os.path.join(case_dir, os.path.splitext(scenario)[0] + "_calibration.json")
    if os.path.exists(calib_path):
        with open(calib_path, "r", encoding="utf-8") as f:
            prev = json.load(f)
        st.sidebar.info(f"Found calibration: {calib_path}")
        if st.sidebar.button("Apply scenario calibration to /sim/params"):
            requests.put(f"{API_URL}/sim/params", json={"params":{"alpha": prev.get("alpha",1.0), "base_p": prev.get("base_p",0.25)}}, timeout=30)
            st.sidebar.success("Applied scenario calibration")


with st.sidebar.expander("Start Session"):
    case_id = case.get("id","demo_case")
    parties = st.multiselect("Parties", ["PH_GOV","PRC_MARITIME","VN_CG","MY_CG"], default=["PH_GOV","PRC_MARITIME"])
    mediator = st.text_input("Mediator", "NGO_Facilitator_A")
    issue_space = st.multiselect("Issues", ["resupply_SOP","hotline_cues","media_protocol","scarborough_fisheries_corridor","ais_transparency_cell"], default=["resupply_SOP","hotline_cues","media_protocol"])
    if st.button("Start Session"):
        payload = {"case_id": case_id, "parties": parties, "mediator": mediator, "issue_space": issue_space}
        r = requests.post(f"{API_URL}/bargain/sessions", json=payload, timeout=30)
        st.success(r.json())

tabs = st.tabs(["Offer", "Simulate", "Calibrate"])
with tabs[0]:
    st.header("Offer Builder")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Resupply SOP")
        standoff = st.slider("standoff_nm", 0, 6, 3)
        escort = st.slider("escort_count", 0, 3, 1)
        prenotify = st.slider("pre_notification_hours", 0, 24, 12)
    with col2:
        st.subheader("Hotline & CUES")
        hotline = st.selectbox("hotline_status", ["ad_hoc","24_7"], index=1)
        cues = ["distance","AIS_on","video_record"]
    with col3:
        st.subheader("Media Protocol")
        embargo = st.slider("embargo_hours", 0, 24, 6)

    offer = {
        "resupply_SOP":{"standoff_nm":standoff,"escort_count":escort,"pre_notification_hours":prenotify},
        "hotline_cues":{"hotline_status":hotline,"cues_checklist":cues},
        "media_protocol":{"embargo_hours":embargo}
    }
    st.code(json.dumps(offer, indent=2))

    if st.button("Evaluate Offer"):
        payload = {"proposer_party_id": parties[0] if parties else "PH_GOV", "agreement_vector": offer}
        r = requests.post(f"{API_URL}/bargain/{case_id}/offer", json=payload, timeout=60)
        st.write(r.json())

with tabs[1]:
    st.header("Run Mesa ABM")
    steps = st.slider("Steps", 50, 1000, 300, 50)
    env = {"weather_state": case.get("weather_state","calm"), "media_visibility": case.get("media_visibility",2)}
    if st.button("Run Simulation"):
        sim_payload = {"steps": steps, "environment": env, "agreement_vector": offer}
        sr = requests.post(f"{API_URL}/sim/run", json=sim_payload, timeout=120)
        res = sr.json()
        st.subheader("Summary")
        st.json(res.get("summary",{}))
        st.subheader("Events")
        if len(res.get("events",[]))>0:
            df = pd.DataFrame(res["events"])
            st.dataframe(df)

            # Plot: incidents per 20 steps (time-series)
            df['bucket'] = (df['step']//20)*20
            ts = df.groupby('bucket').size().reset_index(name='incidents')
            import matplotlib.pyplot as plt
            import io
            st.subheader("Incidents over time (per 20 steps)")
            fig1 = plt.figure()
            plt.plot(ts['bucket'], ts['incidents'], marker='o')
            plt.xlabel('Step'); plt.ylabel('Incidents per 20 steps'); plt.title('Time-series of incidents')
            st.pyplot(fig1)

            # Plot: severity histogram
            st.subheader("Severity histogram")
            fig2 = plt.figure()
            plt.hist(df['severity'], bins=10)
            plt.xlabel('Severity'); plt.ylabel('Frequency'); plt.title('Distribution of incident severity')
            st.pyplot(fig2)


st.sidebar.header("Simulation Parameters")
# Load current params
if st.sidebar.button("Load Server Params"):
    pr = requests.get(f"{API_URL}/sim/params", timeout=30)
    st.sidebar.json(pr.json())

with st.sidebar.expander("Set Server Params"):
    alpha = st.number_input("alpha (risk scale)", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
    base_p = st.number_input("base_p (incident pressure)", min_value=0.01, max_value=0.95, value=0.25, step=0.01)
    if st.button("Update Server Params"):
        ur = requests.put(f"{API_URL}/sim/params", json={"params":{"alpha":alpha, "base_p":base_p}}, timeout=30)
        st.sidebar.success(ur.json())

st.sidebar.header("Calibration Persistence")
if scenario != "(none)":
    if st.sidebar.button("Save last calibration to cases"):
        # Expect last calibration stored in session_state
        best = st.session_state.get("last_calibration_best")
        if best:
            calib_path = os.path.join(case_dir, os.path.splitext(scenario)[0] + "_calibration.json")
            with open(calib_path, "w", encoding="utf-8") as f:
                json.dump(best, f, indent=2)
            st.sidebar.success(f"Saved calibration to {calib_path}")
        else:
            st.sidebar.warning("No calibration results in session. Run /sim/calibrate first (via external tool or an extension).")

with tabs[2]:
    st.header("Calibrate Model")
    st.write("Fit ABM params to historical incident counts (per bucket).")
    c_steps = st.slider("Steps (calibration run length)", 100, 1000, 300, 50)
    c_bucket = st.number_input("Bucket size (steps)", min_value=10, max_value=100, value=20, step=5)
    c_env_weather = st.selectbox("Weather", ["calm","rough"], index=0)
    c_env_media = st.slider("Media visibility", 0, 3, 2, 1)
    c_hist = st.text_area('Historical counts JSON (e.g. {"0":4,"20":3,"40":5})', value='{"0":4,"20":2,"40":3,"60":5,"80":2}')
    c_seeds = st.text_input("Seeds (comma-separated)", value="42,1337,7")
    apply_after = st.checkbox("Apply best params to server (/sim/params) after calibration", value=True)

    if st.button("Run Calibration"):
        try:
            hist = json.loads(c_hist)
            hist = {int(k): int(v) for k,v in hist.items()}
            payload = {
                "steps": int(c_steps),
                "environment": {"weather_state": c_env_weather, "media_visibility": int(c_env_media)},
                "agreement_vector": offer,
                "historical": hist,
                "bucket": int(c_bucket),
                "seeds": [int(x) for x in c_seeds.split(",") if x.strip().isdigit()]
            }
            r = requests.post(f"{API_URL}/sim/calibrate", json=payload, timeout=120)
            best = r.json().get("best_params", {})
            st.session_state["last_calibration_best"] = best
            st.success(best)
            if apply_after and best:
                requests.put(f"{API_URL}/sim/params", json={"params":{"alpha": best.get("alpha",1.0), "base_p": best.get("base_p",0.25)}}, timeout=30)
                st.info("Applied best params to /sim/params")
        except Exception as e:
            st.error(f"Calibration failed: {e}")
