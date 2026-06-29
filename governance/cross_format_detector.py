from difflib import SequenceMatcher


class CrossFormatDuplicateDetector:
    """
    Detect cross-format duplicate documents
    based on normalized text similarity.
    """

    def __init__(self, threshold: float = 0.98):
        self.threshold = threshold

    def detect(self, documents):
        results = []

        n = len(documents)

        for i in range(n):
            for j in range(i + 1, n):

                doc1 = documents[i]
                doc2 = documents[j]

                # 同一种格式不比较
                if doc1.file_type == doc2.file_type:
                    continue

                similarity = self._similarity(
                    doc1.cleaned_text,
                    doc2.cleaned_text
                )

                if similarity >= self.threshold:
                    results.append(
                        {
                            "doc1": doc1.file_name,
                            "doc2": doc2.file_name,
                            "type": "cross_format_duplicate",
                            "similarity": round(similarity, 4)
                        }
                    )

        return results

    def _similarity(self, text1, text2):
        return SequenceMatcher(
            None,
            self._normalize(text1),
            self._normalize(text2)
        ).ratio()

    def _normalize(self, text):
        return (
            text.replace("\r\n", "\n")
                .replace("\r", "\n")
                .replace(" ", "")
                .replace("\n", "")
        )
 