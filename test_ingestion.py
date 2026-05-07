from ingestion.loaders import DocumentLoader


loader = DocumentLoader()


documents = loader.load_multiple(
    [
        "test_documents/Divya M K - Langchain.pdf",
        "test_documents/AI Agents path.txt",
    ]
)


print(f"\nLoaded documents: {len(documents)}\n")


if documents:

    print("FIRST DOCUMENT CONTENT:\n")

    print(documents[0].page_content[:1000])

    print("\nMETADATA:\n")

    print(documents[0].metadata)