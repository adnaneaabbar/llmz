import spacy
from typing import Dict, List


@transformer
def lemmatize_text(documents: List[Dict], *args, **kwargs):
    print('Documents', len(documents))
    sample = kwargs.get('sample', -1)

    nlp = spacy.load('en_core_web_sm')

    data = []

    for document in documents[:sample]:
        document_id = document['document_id']

        # Process the text chunk using spaCy
        chunk = document['chunk']
        doc = nlp(chunk)
        tokens = [token.lemma_ for token in doc]

        data.append(
            dict(
                chunk=chunk,
                document_id=document_id,
                tokens=tokens,
            )
        )

    print('\nData', len(data))

    return [data]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'