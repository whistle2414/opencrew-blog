from anthropic import Anthropic

client = Anthropic()

models = client.models.list()

for model in models.data:
    print(model.id)