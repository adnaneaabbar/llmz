import re
from typing import Any, Dict, List
from uuid import uuid4

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def chunk_documents(data: List[Dict[str, Any]], *args, **kwargs):
    documents = []
    
    for idx, item in enumerate(data):
        course = item['course']
        
        for info in item['documents']:
            section = info['section']
            question = info['question']
            answer = info['text']
            
            # Generate a unique document ID
            document_id = ':'.join([re.sub(r'\W', '_', part) 
	            for part in [course, section, question]]).lower()
            
            # Format the document string
            chunk = '\n'.join([
                f'course:\n{course}\n',
                f'section:\n{section}\n',
                f'question:\n{question}\n',
                f'answer:\n{answer}\n',
            ])
            
            documents.append(dict(
                chunk=chunk,
                document=info,
	            document_id=document_id,
            ))

    print(f'Documents:', len(documents))
            
    return [documents]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'