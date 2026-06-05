import re

from validators.base_validator import BaseValidator
from schema.document import Document


class OCRNoiseValidator(BaseValidator):
    '''
    第一版仅检测OCR乱码 
    '''

    def __init__(self, max_noise_ratio: float = 0.05):
        self.max_noise_ratio = max_noise_ratio

    def validate(self, document: Document) -> Document:

        text = document.cleaned_text.strip()

        total_chars = len(text)

        # =========================
        # 空文档
        # =========================

        if total_chars == 0:

            document.validation_results["ocr_noise"] = {
                "rule": "ocr_noise_detection",  
                "status": "FAIL",
                "noise_chars": 0,
                "total_chars": 0,
                "noise_ratio": 1.0,
                "warnings": [],
                "message": "Empty document."
            }

            return document

        # =========================
        # OCR乱码统计
        # =========================
        noise_pattern = r"[■□◆◇▲△▼▽★☆●○�]"

        noise_chars = len(
            re.findall(noise_pattern, text)
        )

        noise_ratio = noise_chars / total_chars

        # =========================
        # 状态判断
        # =========================

        status = "PASS"

        warnings = []

        # FAIL
        if noise_ratio > self.max_noise_ratio:

            status = "FAIL"

        # WARNING
        elif noise_ratio > 0.01:

            warnings.append(
                f"OCR noise ratio is relatively high: {noise_ratio:.2%}"
            )

        # =========================
        # 保存结果
        # =========================

        document.validation_results["ocr_noise"] = {
            "rule": "ocr_noise_detection",
            "status": status,
            "noise_chars": noise_chars,
            "total_chars": total_chars,
            "noise_ratio": round(noise_ratio, 4),
            "warnings": warnings
        }


        return document