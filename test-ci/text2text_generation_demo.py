from mindnlp.transformers import pipeline

generator = pipeline("text2text-generation", model="t5-base")
import mindspore
outputs = generator("My name is Wolfgang and I live in Berlin")
print(outputs)
# [{'generated_text': 'Wolfgang and I live in Berlin. My name is Wolfgang and I am from Berlin.'}]
