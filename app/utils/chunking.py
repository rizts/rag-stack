from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text: str, chunk_size: int = 512, chunk_overlap: int = 50):
    """
    Split input text into overlapping chunks using LangChain's RecursiveCharacterTextSplitter.
    This approach is more intelligent than simple slicing because it respects sentence and paragraph boundaries.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""],
    )
    return text_splitter.split_text(text)
