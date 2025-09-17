import fitz  # PyMuPDF
from PIL import Image
import io
import argparse
import google.generativeai as genai
import os
from markdown_it import MarkdownIt
from google.api_core import exceptions as google_exceptions
import re

def convert_pdf_to_images(pdf_path):
    """
    将 PDF 文件的每一页转换为图像。
    """
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        images.append(img)
    return images

def ocr_image_with_gemini(image):
    """
    使用 Google Gemini 2.5 Flash API 对图像进行 OCR。
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-1.5-flash')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format if image.format else 'PNG')
    img_byte_arr = img_byte_arr.getvalue()

    response = model.generate_content(["Extract all text from this image.", Image.open(io.BytesIO(img_byte_arr))])
    return response.text

def text_to_basic_markdown(text):
    """
    将纯文本转换为基本的 Markdown 格式，尝试识别标题和列表。
    """
    md = MarkdownIt()
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue

        # 尝试识别标题 (简单的启发式，例如全大写或以数字开头)
        if stripped_line.isupper() and len(stripped_line) > 3:
            formatted_lines.append(f"## {stripped_line}") # 假设二级标题
        elif re.match(r'^\d+\.\s', stripped_line) or re.match(r'^[-*+]\s', stripped_line):
            formatted_lines.append(stripped_line) # 保持列表格式
        else:
            formatted_lines.append(md.render(stripped_line).strip())
    
    # 移除 markdown-it 渲染时可能添加的 <p> 标签，并确保段落间有空行
    final_markdown = []
    for line in formatted_lines:
        if line.startswith('<p>') and line.endswith('</p>'):
            final_markdown.append(line[3:-4].strip())
        else:
            final_markdown.append(line.strip())
    
    return "\n\n".join(filter(None, final_markdown))

def postprocess_ocr_text(text):
    """
    对 OCR 提取的文本进行后处理，清理常见错误。
    """
    # 移除多余的空白字符，例如多个空格替换为单个空格
    text = re.sub(r'\s+', ' ', text).strip()
    # 尝试处理常见的 OCR 错误，例如单词合并或分割
    # 这部分可能需要更复杂的规则或机器学习模型
    # 示例：将“wordone”转换为“word one”
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown.")
    parser.add_argument("input_pdf", type=str, help="Path to the input PDF file.")
    parser.add_argument("output_md", type=str, help="Path to the output Markdown file.")

    args = parser.parse_args()

    pdf_file = args.input_pdf
    output_md_file = args.output_md

    print(f"Starting conversion of '{pdf_file}' to Markdown...")
    
    try:
        if not os.path.exists(pdf_file):
            raise FileNotFoundError(f"Input PDF file not found: {pdf_file}")

        print("Converting PDF pages to images...")
        images = convert_pdf_to_images(pdf_file)
        print(f"Successfully converted {len(images)} pages to images.")

        extracted_texts = []
        for i, img in enumerate(images):
            print(f"Performing OCR on page {i+1}/{len(images)}...")
            try:
                text = ocr_image_with_gemini(img)
                processed_text = postprocess_ocr_text(text)
                extracted_texts.append(processed_text)
                # print(f"Extracted text from page {i+1}: {processed_text[:200]}...") # Optional: print snippet for debugging
            except google_exceptions.GoogleAPIError as api_error:
                print(f"Google API Error during OCR on page {i+1}: {api_error}")
                extracted_texts.append(f"[OCR Error on page {i+1}: {api_error}]\n")
            except Exception as ocr_error:
                print(f"Error during OCR on page {i+1}: {ocr_error}")
                extracted_texts.append(f"[OCR Error on page {i+1}: {ocr_error}]\n")

        print("Converting extracted text to Markdown format...")
        markdown_content = []
        for text in extracted_texts:
            markdown_content.append(text_to_basic_markdown(text))

        print(f"Writing Markdown content to '{output_md_file}'...")
        with open(output_md_file, "w", encoding="utf-8") as f:
            for md_text in markdown_content:
                f.write(md_text + "\n\n")

        print(f"Conversion successful! Output saved to '{output_md_file}'.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the input PDF file exists and the path is correct.")
    except fitz.FileDataError as e:
        print(f"Error processing PDF file (PyMuPDF): {e}")
        print("Please ensure the input file is a valid and uncorrupted PDF document.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please check the error message and try again. Ensure your GOOGLE_API_KEY is set correctly.")