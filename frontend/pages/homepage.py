import streamlit as st
import os
import base64

# Get the path to the images folder
images_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
illustration_path = os.path.join(images_path, "Illustration.png")
logo_path = os.path.join(images_path, "logo.png")

# Convert images to base64
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

illustration_base64 = get_image_base64(illustration_path)
logo_base64 = get_image_base64(logo_path)

# Build HTML with base64 images
left_img_html = f'<img src="data:image/png;base64,{illustration_base64}" class="illustration-img" />' if illustration_base64 else ""
logo_img_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-img" />' if logo_base64 else ""

def show():
    st.markdown("""
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            html, body {
                height: 100%;
            }

            /* Container full-screen fixed */
            .fullscreen-layout {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                display: flex;
            }

            .left-section {
                background-color: #0F3D5E;
                color: white;
                padding: 60px 40px;
                flex: 0 0 45%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: flex-start;
                position: relative;
                overflow: hidden;
            }

            .right-section {
                background-color: white;
                padding: 60px 40px;
                flex: 0 0 55%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                position: relative;
            }

            .action-section {
                text-align: center;
                display: flex;
                flex-direction: column;
                gap: 20px;
                align-items: center;
                width: 100%;
                max-width: 350px;
            }

            .logo-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-bottom: 30px;
                gap: 10px;
            }

            .divider {
                text-align: center;
                color: #999;
                margin: 10px 0;
                font-size: 12px;
            }

            .button-container {
                width: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .button-custom {
                background-color: #835AFD;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                width: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: opacity 0.3s ease;
            }

            .button-custom:hover {
                opacity: 0.9;
            }

            .button-dark {
                background-color: #0F3D5E;
            }

            .input-code {
                width: 100%;
                padding: 10px 16px;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                color: #A8A8B3;
            }

            .input-code::placeholder {
                color: #A8A8B3;
            }

            .title-left {
                font-size: 56px;
                font-weight: bold;
                margin-bottom: 30px;
                color: white;
                line-height: 1.2;
                position: relative;
                z-index: 2;
            }

            .subtitle-left {
                font-size: 16px;
                color: rgba(255, 255, 255, 0.8);
                line-height: 1.6;
                max-width: 500px;
                position: relative;
                z-index: 2;
            }

            .illustration-img {
                max-width: 313px;
                max-height: 403px;
            }

            .logo-img {
                max-width: 200px;
                max-height: 200px;
            }

            h2 {
                margin: 0;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="fullscreen-layout">
            <div class="left-section">
                {left_img_html}
                <div class="title-left">Search. Summarize.<br>Understand.</div>
                <div class="subtitle-left">
                    Make your investigations more robust,<br> and never lose information again.
                </div>
            </div>
            <div class="right-section">
                <div class="action-section">
                    <div class="logo-container">
                        {logo_img_html}
                    </div>
                    <button class="button-custom" onclick="alert('Create account with Google')">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white" style="margin-right: 8px;"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M12 2a9.96 9.96 0 0 1 6.29 2.226a1 1 0 0 1 .04 1.52l-1.51 1.362a1 1 0 0 1 -1.265 .06a6 6 0 1 0 2.103 6.836l.001 -.004h-3.66a1 1 0 0 1 -.992 -.883l-.007 -.117v-2a1 1 0 0 1 1 -1h6.945a1 1 0 0 1 .994 .89c.04 .367 .061 .737 .061 1.11c0 5.523 -4.477 10 -10 10s-10 -4.477 -10 -10s4.477 -10 10 -10z" /></svg>
                        Create account with Google
                    </button>
                    <div class="divider">or enter a room</div>
                    <input type="text" class="input-code" placeholder="Enter the room code" />
                    <button class="button-custom button-dark" onclick="alert('Enter the room')">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 8v-2a2 2 0 0 1 2 -2h7a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-7a2 2 0 0 1 -2 -2v-2" /><path d="M3 12h13l-3 -3" /><path d="M13 15l3 -3" /></svg>
                        Enter the room
                    </button>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)