from pathlib import Path

from langchain_community.document_loaders import (
    UnstructuredPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader,
)
from langchain_community.document_loaders.excel import UnstructuredExcelLoader


def get_access_roles(file_path: Path):
    folder_name = file_path.parent.name.lower()

    if folder_name == "public":
        return ["public", "hr", "employee", "admin"]
    elif folder_name == "hr":
        return ["hr", "admin"]
    elif folder_name =="company":
        return ["employee", "admin"]
    else:
        return ["public"]


def enrich_metadata(docs, file_path: Path):
    access_roles = get_access_roles(file_path)

    for doc in docs:
        doc.metadata.update({
            "access_roles": access_roles,
            "source": str(file_path.name)
        })

    return docs


def load_all_documents(data_dir: str):
    data_path = Path(data_dir).resolve()
    documents = []

    # PDF files
    for pdf_file in data_path.glob('**/*.pdf'):
        try:
            loader = UnstructuredPDFLoader(str(pdf_file))
            loaded = loader.load()
            enriched_docs = enrich_metadata(loaded, pdf_file)
            documents.extend(enriched_docs)
            print(f"Loaded PDF: {pdf_file.name} | Chunks: {len(enriched_docs)}")
        except Exception as e:
            print(f"Error loading {pdf_file}: {e}") 

    # TXT files
    for txt_file in data_path.glob('**/*.txt'):
        try:
            loader = TextLoader(str(txt_file))
            loaded = loader.load()
            documents.extend(enrich_metadata(loaded, txt_file))
        except Exception as e:
            print(f"Error loading {txt_file}: {e}") 

    # CSV files
    for csv_file in data_path.glob('**/*.csv'):
        try:
            loader = CSVLoader(str(csv_file))
            loaded = loader.load()
            documents.extend(enrich_metadata(loaded, csv_file))
        except Exception as e:
            print(f"Error loading {csv_file}: {e}") 

    # Excel files
    for xlsx_file in data_path.glob('**/*.xlsx'):
        try:
            loader = UnstructuredExcelLoader(str(xlsx_file))
            loaded = loader.load()
            documents.extend(enrich_metadata(loaded, xlsx_file))
        except Exception as e:
            print(f"Error loading {xlsx_file}: {e}") 

    # Word files
    for docx_file in data_path.glob('**/*.docx'):
        try:
            loader = Docx2txtLoader(str(docx_file))
            loaded = loader.load()
            documents.extend(enrich_metadata(loaded, docx_file))
        except Exception as e:
            print(f"Error loading {docx_file}: {e}") 

    return documents


# Example usage
if __name__ == "__main__":
    docs = load_all_documents("data")
    print(f"Loaded {len(docs)} documents.")
    print("Example document:", docs[0] if docs else None)
