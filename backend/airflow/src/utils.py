import random
import re
from typing import List

import tiktoken
from rank_bm25 import BM25Okapi
from nltk.tokenize import sent_tokenize


def token_count(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Estimate the number of tokens in a text.

    Args:
        text (str): The text to estimate the number of tokens.
        model (str, optional): The model to use. Defaults to "gpt-3.5-turbo". 
        Valid values are "gpt-3.5-turbo", "gpt-4", "text-davinci-003".
    """
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    n_tokens = len(tokens)
    return n_tokens


def word_tokenizer(text: str) -> List[str]:
    tokens = re.split(r"([.,!?]+)?\s+", text)
    return tokens


def get_top_pages(pages, question, n_char: int = 500):

    bodies = [
        page["body"][int(len(page["body"])*0.10): int(len(page["body"])*0.10) + n_char]
        for page in pages
    ]

    tokenized_bodies = map(word_tokenizer, bodies)

    bm25 = BM25Okapi(tokenized_bodies)

    tokenized_question = word_tokenizer(question)

    best_bodies = bm25.get_top_n(tokenized_question, bodies, n=5)  # TODO: check if this is rigth

    # Enforce randomness to avoid ChatGPT to learn the order of the pages
    random.shuffle(best_bodies)

    best_pages = []
    for best_body in best_bodies:
        for page in pages:
            # Offset to avoid the first 10% of the text. HTML is usually a mess in the beginning
            schar = int(len(page["body"]) * 0.10)
            body = page["body"][schar: schar + n_char]
            if best_body == body:
                best_pages.append({
                    "url": page["url"],
                    "title": page["title"],
                    "body": body,
                })

    return best_pages


def groupby(iterable, key):
    """Group items in an iterable by a key."""
    groups = {}
    for item in iterable:
        groups.setdefault(key(item), []).append(item)
    return groups.values()


def add_references(text: str, pages: dict):
    """Add references to a text."""

    page_idxs, pages_sentences = list(zip(*[
        (idx, sent)
        for idx, page in enumerate(pages)
        for sent in sent_tokenize(page["body"])
        if len(sent) > 70  # drop very short sentences
    ]))

    bm25 = BM25Okapi([word_tokenizer(sent) for sent in pages_sentences])

    # Compute the BM25 score for each sentence in the answer with each sentence on the pages.
    sent_refs = []  # (sent_idx, page_idx, score)
    sentences = sent_tokenize(text)
    for sent_idx, sentence in enumerate(sentences):
        tokens = word_tokenizer(sentence)
        docs_scores = list(bm25.get_scores(tokens))
        sent_ref = list(zip([sent_idx] * len(page_idxs), page_idxs, docs_scores))
        sent_refs += sent_ref

    # Get top references for each sentence.
    sent_refs.sort(key=lambda x: x[2], reverse=True)
    top_refs = sent_refs[:len(sentences)]
    top_refs.sort(key=lambda x: x[1])  # to make references sorted on the final answer.
    refs = [[] for _ in range(len(sentences))]
    for sent_idx, page_idx, _ in top_refs:
        refs[sent_idx].append(page_idx + 1)
    refs = [list(set(ref)) for ref in refs]

    ref_pages_idxs = set([page_idx for _, page_idx, _ in top_refs])
    ref_pages = [pages[idx] for idx in ref_pages_idxs]
    idx_map = {}
    for new_idx, (prev_idx, page) in enumerate(zip(ref_pages_idxs, ref_pages)):
        page.pop("body")
        page["id"] = new_idx + 1
        idx_map[prev_idx] = new_idx + 1

    # Build answer.
    answer = " ".join([
        f"{sent[:-1]} {[idx_map[r-1] for r in ref]}{sent[-1:]}" if ref else sent
        for sent, ref in zip(sentences, refs)
    ])

    return answer, ref_pages
