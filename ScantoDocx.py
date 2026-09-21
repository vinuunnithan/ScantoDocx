import streamlit as st
import tempfile
import os
from google import genai
import pypandoc

# Setup Page Configuration
st.set_page_config(page_title="PNG to Word Converter", page_icon="📝", layout="centered")

# --- Sidebar Disclaimer & Signature Section ---
with st.sidebar:
    st.header("⚠️ Legal & Technical Disclaimer")
    st.markdown(
        """
        **Experimental Purpose:**  
        This application is developed strictly for experimental, proof-of-concept, and internal evaluation purposes. 
        
        **Accuracy & Liability:**  
        * Text generation and OCR outputs are processed using artificial intelligence (Gemini API). 
        * Outputs may contain **errors, hallucinations, omissions, or formatting discrepancies**. 
        * The user acknowledges and accepts all operational risks associated with using this software.
        * The developer offers **no warranties of any kind** (express or implied) and shall **not be held liable** for any direct, indirect, incidental, or consequential damages, data loss, or business interruptions arising out of the use or inability to use this tool.
        
        **Data Privacy Notice:**  
        Uploaded files are processed entirely in temporary memory buffers and are automatically destroyed when your session ends or closes. No data is permanently retained on this server.
        """
    )
    
    st.write("---")
    st.subheader("✍️ Digital Acknowledgement")
    # Interactive signature text entry
    user_signature = st.text_input(
        "Type your full name to accept these terms:", 
        placeholder="First and Last Name",
        help="Entering your name acts as a digital signature acknowledging the risks listed above."
    ).strip()

    # Track if the disclaimer has been signed
    is_signed = len(user_signature) > 0

st.title("📝 Scanned PNG to Markdown to Word Converter")
st.write("Upload your PNG images, convert them to crisp Markdown via Gemini AI, and download an editable Word Document.")

# Check signature status before displaying the core application tools
if not is_signed:
    st.warning("🔒 Please read and sign the **Legal & Technical Disclaimer** in the sidebar to unlock the application.")
else:
    st.success(f"✍️ Acknowledged by: **{user_signature}**")

    # --- API Key Section ---
    env_key = os.environ.get("GEMINI_API_KEY", "")

    if not env_key:
        api_key_input = st.text_input("Enter Gemini API Key:", type="password", help="Get a key from https://google.com")
        final_key = api_key_input.strip()
    else:
        final_key = env_key
        st.info("🤖 Gemini API Key loaded securely from Cloud Environment.")

    # --- File Upload Section ---
    uploaded_files = st.file_uploader(
        "Drag and drop or browse PNG files:", 
        type=["png"], 
        accept_multiple_files=True,
        help="Hold Ctrl/Cmd to select multiple files"
    )

    # Sort files alphabetically by name to preserve document flow order
    if uploaded_files:
        uploaded_files = sorted(uploaded_files, key=lambda x: x.name)
        st.info(f"📁 Loaded {len(uploaded_files)} file(s) for conversion.")

    # --- Filename Customization ---
    default_name = "converted_document"
    output_name = st.text_input("Output Document Name (without extension):", value=default_name)

    # --- Process Pipeline ---
    if st.button("🚀 Process and Convert", type="primary"):
        if not final_key:
            st.error("Please provide a valid Gemini API Key to proceed.")
        elif not uploaded_files:
            st.warning("Please upload at least one PNG file.")
        elif not output_name.strip():
            st.error("Please enter a valid output document name.")
        else:
            with st.spinner("Processing... calling Gemini AI and compiling Word document..."):
                try:
                    # 1. Initialize Gemini Client
                    client = genai.Client(api_key=final_key)
                    
                    contents = ["Please convert the content of these images into a single, cohesive, well-formatted Markdown document."]
                    
                    # Load image bytes directly from memory buffer
                    for uploaded_file in uploaded_files:
                        image_bytes = uploaded_file.read()
                        contents.append(
                            genai.types.Part.from_bytes(data=image_bytes, mime_type='image/png')
                        )

                    # 2. Generate Content via Gemini
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=contents
                    )
                    markdown_text = response.text

                    # 3. Handle Pandoc Conversion using secure temporary cloud directories
                    with tempfile.TemporaryDirectory() as tmpdir:
                        md_path = os.path.join(tmpdir, "temp.md")
                        docx_path = os.path.join(tmpdir, "temp.docx")
                        
                        # Write markdown to a temporary cloud file
                        with open(md_path, "w", encoding="utf-8") as md_file:
                            md_file.write(markdown_text)
                        
                        # Convert to docx via Pandoc
                        pypandoc.convert_file(md_path, 'docx', outputfile=docx_path)
                        
                        # Read the compiled docx file back into memory
                        with open(docx_path, "rb") as docx_file:
                            docx_bytes = docx_file.read()

                    # 4. Provide Downloads to the User
                    st.success("🎉 Conversion Complete!")
                    
                    # Format final filenames cleanly
                    clean_name = output_name.strip().replace(".docx", "").replace(".md", "")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📥 Download Word Document (.docx)",
                            data=docx_bytes,
                            file_name=f"{clean_name}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                    with col2:
                        st.download_button(
                            label="📄 Download Raw Markdown (.md)",
                            data=markdown_text,
                            file_name=f"{clean_name}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )

                except Exception as e:
                    st.error(f"An unexpected error occurred during processing:\n{e}")
