from collections import defaultdict


class DuplicateDetector:

    def detect(self, documents):

        hash_groups = defaultdict(list)

        for document in documents:

            document_hash = (
                document.metadata.common.get(
                    "document_hash"
                )
            )

            hash_groups[
                document_hash
            ].append(document)

        duplicates = {
            h: docs
            for h, docs in hash_groups.items()
            if len(docs) > 1
        }

        return duplicates