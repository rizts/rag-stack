from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str, chunk_size: int = 512, chunk_overlap: int = 50):
    """
    Split input text into overlapping chunks using LangChain's RecursiveCharacterTextSplitter.
    This version is modular and lightweight.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""],
    )
    return text_splitter.split_text(text)
