import re
from ocr import perform_ocr

def classify_text(text):
    regexS1 = r'\bS-?1\b'
    regexW2 = r'\bW-?2\b'
    USApassportRegex = r'\bPASSPORT\b'
    collegeIDRegex = r'\bStudent\b'

    print("About to run tests")
    print("Text type:", type(text))
    
    if re.search(regexS1, text, re.IGNORECASE):
        print('Found S-1')
        return 'S1'
    elif re.search(regexW2, text, re.IGNORECASE):
        print('Found W-2')
        return 'W2'
    elif re.search(USApassportRegex, text, re.IGNORECASE):
        print('Found PASSPORT')
        return 'USA passport'
    elif re.search(collegeIDRegex, text, re.IGNORECASE):
        print('Found Student')
        return 'college ID'
    else:
        print('Unknown')
        return 'unknown'

def run_classification(image_path):
    ocr_result = perform_ocr(image_path)

    if ocr_result:
        print("OCR Result:")
        print(ocr_result)
        
        classification_result = classify_text(str(ocr_result))
        print("Classification Result:")
        print(classification_result)
        
        return classification_result
    else:
        print("OCR failed or unsupported image format.")
        return ""
    
