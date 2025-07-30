# Masters_india_Task
This project is a task from masters india private limited
# 🧾 Invoice Extractor

## 📌 Introduction

**Invoice Extractor 2** is a Python-based tool that extracts structured data from invoices in PDF or image format using OCR and regex-powered pattern matching. It intelligently parses key invoice fields such as:

- Invoice Number  
- Invoice Date  
- GST Number  
- Line Items (from tables)

The tool is modular, configuration-driven, and supports various invoice formats by allowing easy pattern adjustments in `fields_config.json`.

---

## 🧠 What I Learned

- How to integrate OCR (Tesseract) with PDF parsing  
- Building a modular extractor class using regex and configs  
- Handling real-world invoice layouts with messy spacing or inconsistent formatting  
- Date parsing and field validation using `dateutil`  
- Creating a reusable pattern-driven extractor engine

---

## 💼 Use Cases

- Automating invoice processing in accounting or ERP systems  
- Extracting product/item data for analytics  
- Back-office automation for finance departments  
- Pre-processing step for machine learning pipelines (structured data extraction)

---

## 📁 File Structure

```
invoice_extractor_2/
├── invoices/
│   └── invoice.pdf              # Sample invoice
├── extractors.py                # Core extraction logic using regex and config
├── field_config.json            # Regex rules for each field (editable)
├── utils.py                     # OCR and PDF/image conversion
├── main.py                      # Entry point to run the pipeline
```

---

## ⚙️ Dependencies

Install all required libraries with:

```bash
pip install paddleocr
pip install pdf2image
pip install python-dateutil
pip install pytesseract
pip install pillow
```

### Additional Setup

- **Poppler for Windows** (required for `pdf2image`):  
  Download from: https://github.com/oschwartz10612/poppler-windows  
  Update the path in `main.py`:
  ```python
  poppler_path = r"C:\Users\ADMIN\Documents\poppler-24.08.0\Library\bin"
  ```

- **Tesseract OCR**:  
  Install from https://github.com/tesseract-ocr/tesseract  
  Ensure it's available in your system PATH.

---

## 🔍 Field Extraction Config (JSON)

The field definitions in `field_config.json` use regular expressions and support:

- Multiple patterns per field  
- Group index to extract from match  
- Date parsing via `parse_date: true`  
- Start/end boundaries for table parsing

Example:
```json
"invoice_date": {
  "patterns": [
    "(?is)date(?:\\s*of\\s*issue)?\\s*[:\\-–]?\\s*([\\d]{1,4}[\\-/\\.][\\d]{1,2}[\\-/\\.][\\d]{1,4})",
    "(?is)(\\d{1,2}[\\-/\\.][\\d]{1,2}[\\-/\\.][\\d]{2,4})"
  ],
  "group": 1,
  "parse_date": true
}
```

---

## 🧪 Sample Output

```
invoice_number: 27301261
invoice_date: 2012-09-10
gst_number: 07ABCDE1234F1Z5

line_items: [
  { "item_no": "1", "description": "Lilly Pulitzer dress Size 2", "quantity": "5,00" },
  { "item_no": "2", "description": "New ERIN Erin Fertherston", "quantity": "1,00" }
]

raw_text: Invoice no: 27301261 ...
```

---

## 🚧 Challenges I Faced

- **Irregular invoice layouts**: Date and invoice number often appeared far from their labels with unpredictable spacing or on the right side of the page.
- **Excessive whitespace**: Needed regex that spans multiple lines and tolerates irregular tabs/spaces.
- **Table parsing**: Line items were not always structured in single lines; some descriptions wrapped across lines.
- **OCR inaccuracies**: Minor text distortions affected extraction, requiring fallback handling (e.g., checking next line).
- **Scalability**: Ensuring the extractor supports new fields just by updating config without touching code.

---

## 🛠 How to Extend

To add a new field (e.g., "buyer_name"):

1. Open `field_config.json`
2. Add a new entry like:
   ```json
   "buyer_name": {
     "patterns": ["(?i)buyer[:\\s\\n]*([A-Za-z\\s]+)"],
     "group": 1
   }
   ```
3. Run `main.py` again — it will automatically include this new field in output.

---

## ▶️ How to Run

```bash
python main.py
```

Make sure `invoice.pdf` is placed inside the `invoices/` directory.

---

> 💡 Tip: This extractor is fully config-driven. You can adjust field behavior or add new ones just by editing `field_config.json`.

---
