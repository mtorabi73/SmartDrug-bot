from gradio_client import Client

client = Client("https://mohammadreza73-ag-predictor.hf.space/")
result = client.predict("CC(=O)OC1=CC=CC=C1C(=O)O")
print(result)
