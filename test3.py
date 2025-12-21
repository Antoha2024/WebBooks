import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pymorphy3

def main():
    # Загрузка токенайзера и модели
    tokenizer = AutoTokenizer.from_pretrained('DeepPavlov/rubert-base-cased', num_proc=1)
    model = AutoModelForSequenceClassification.from_pretrained('DeepPavlov/rubert-base-cased', num_labels=2)

    # Текст для обработки
    text = '''
    Повесть о зимних чудесах
    В одной далёкой стороне,
    В обычной и простой семье,
    Живёт с любящей роднёй
    Младший сынишка озорной.
    ...
    Насмотревшись всех чудес,
    Гости покидали лес!
    '''

    # Токенизация текста
    tokens = tokenizer.tokenize(text)

    # Преобразование токенов в числовые индексы
    token_ids = tokenizer.convert_tokens_to_ids(tokens)

    # Печать токенов с индексами
    for idx, token in enumerate(token_ids):
        decoded_token = tokenizer.decode([token])
        print(f"{idx}: {decoded_token.strip()} ({token})")

    # Подготовка входа для модели
    inputs = tokenizer(text, return_tensors="pt")
    inputs["input_ids"] = inputs["input_ids"].to(model.device)
    inputs["attention_mask"] = inputs["attention_mask"].to(model.device)

    # Прогонка через модель
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_id = logits.argmax(dim=1).item()

    # Вывод результата
    print("\nОбработанный текст:")
    print(text)
    print(f"Прогнозируемый класс: {predicted_class_id}")

if __name__ == "__main__":
    main()