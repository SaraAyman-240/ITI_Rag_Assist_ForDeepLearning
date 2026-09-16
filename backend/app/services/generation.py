import ollama

from app.core.config import OLLAMA_MODEL


class GenerationService:
    def build_prompt(self, question: str, results: dict) -> str:
        """
        Build a grounded prompt from retrieved ChromaDB chunks.
        """

        context_blocks = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        for document, metadata in zip(
            documents,
            metadatas,
        ):
            source = metadata.get(
                "source",
                "Unknown source",
            )

            context_blocks.append(
                f"[Source: {source}]\n{document}"
            )

        context = "\n\n".join(context_blocks)

        prompt = f"""
You are a helpful assistant answering questions using ONLY the provided context.

If the answer is not contained in the context, say you don't know based on the provided documents.

Do not use outside knowledge.

At the end of your answer, cite only the exact source filename(s)
provided in the context.

Do not invent page numbers, section numbers, lecture numbers,
or any citation details that are not explicitly provided in the context.

Context:
{context}

Question: {question}

Answer:
"""

        return prompt

    def generate(
        self,
        question: str,
        results: dict,
    ) -> str:
        """
        Send the grounded prompt to Ollama.
        """

        prompt = self.build_prompt(
            question,
            results,
        )

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]