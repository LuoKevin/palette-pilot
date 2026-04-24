import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/colorize/upload"
PREVIEW_WIDTH = 420
DEBUG_IMAGE_WIDTH = 420


def rgb_to_hex(rgb: list[int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


st.set_page_config(page_title="Palette Pilot Upload Test", layout="wide")
st.title("Palette Pilot Backend Upload Test")
st.caption("This is a temporary test harness for the FastAPI upload endpoint.")

target_file = st.file_uploader("Target image", type=["png", "jpg", "jpeg"], key="target")
reference_file = st.file_uploader("Reference image", type=["png", "jpg", "jpeg"], key="reference")

if st.button("Send to backend", type="primary"):
    if target_file is None or reference_file is None:
        st.error("Upload both a target image and a reference image.")
    else:
        files = {
            "target_image": (target_file.name, target_file.getvalue(), target_file.type),
            "reference_image": (reference_file.name, reference_file.getvalue(), reference_file.type),
        }

        try:
            response = requests.post(API_URL, files=files, timeout=30)
            response.raise_for_status()
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")
        else:
            data = response.json()
            palette = data.get("palette", [])
            palette_counts = data.get("palette_counts", [])
            total_count = sum(palette_counts)
            target_luminance_base64 = data.get("target_luminance_png_base64")
            target_tone_buckets_base64 = data.get("target_tone_buckets_png_base64")
            target_recolored_base64 = data.get("recolored_image_png_base64")

            st.success("Backend responded successfully.")
            st.subheader("Extracted Palette")

            if palette:
                swatch_cols = st.columns(len(palette))
                for col, rgb, count in zip(swatch_cols, palette, palette_counts):
                    hex_color = rgb_to_hex(rgb)
                    percentage = (count / total_count * 100) if total_count else 0
                    with col:
                        st.markdown(
                            f"""
                            <div style="
                                height: 72px;
                                border-radius: 6px;
                                border: 1px solid #d0d0d0;
                                background: {hex_color};
                            "></div>
                            <div style="font-size: 12px; margin-top: 6px;">{rgb}</div>
                            <div style="font-size: 12px; color: #666;">{hex_color}</div>
                            <div style="font-size: 12px; color: #666;">{percentage:.1f}%</div>
                            <div style="font-size: 11px; color: #888;">{count} px</div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                st.info("No palette returned.")

            st.subheader("Target Preprocessing Debug")
            debug_col1, debug_col2, debug_col3 = st.columns(3)

            with debug_col1:
                if target_luminance_base64:
                    st.image(
                        f"data:image/png;base64,{target_luminance_base64}",
                        caption="Luminance",
                        width=DEBUG_IMAGE_WIDTH,
                    )
                else:
                    st.info("No luminance debug image returned.")

            with debug_col2:
                if target_tone_buckets_base64:
                    st.image(
                        f"data:image/png;base64,{target_tone_buckets_base64}",
                        caption="Tone buckets",
                        width=DEBUG_IMAGE_WIDTH,
                    )
                else:
                    st.info("No tone buckets debug image returned.")

            with debug_col3:
                if target_recolored_base64:
                    st.image(
                        f"data:image/png;base64,{target_recolored_base64}",
                        caption="Recolored",
                        width=DEBUG_IMAGE_WIDTH,
                    )
                else:
                    st.info("No recolored image returned.")

            st.subheader("Raw Response")
            st.json(data)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Target Preview")
    if target_file is not None:
        st.image(target_file, width=PREVIEW_WIDTH)

with col2:
    st.subheader("Reference Preview")
    if reference_file is not None:
        st.image(reference_file, width=PREVIEW_WIDTH)
