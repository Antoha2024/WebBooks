from transformers import BertModel, BertTokenizerFast
import torch

model_name = "DeepPavlov/rubert-base-cased-conversational"
tokenizer = BertTokenizerFast.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

def extract_keywords(text):
    inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    # Получили векторное представление текста, но ключевое слово придется выбирать самим,
    # возможно, применяя кластеризацию или алгоритмы подбора семантически близких слов.

    # Простейший способ выбрать ключевые слова: берем топ-N наиболее важных слов
    top_n = 10
    most_important_words = sorted(inputs.input_ids.squeeze().tolist(), reverse=True)[:top_n]
    decoded_words = tokenizer.convert_ids_to_tokens(most_important_words)
    return decoded_words


input_text = "Пример текста"
print(input_text)
#input_text = input("Введите текст: ")
#keywords = extract_keywords(input_text)
#print(f"Ключевые слова: {keywords}")