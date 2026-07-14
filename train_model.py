import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

texts = [
    "Win a free iPhone now, click this link immediately",
    "Congratulations you have won a lottery prize claim now",
    "URGENT your account will be suspended verify now",
    "Limited time offer buy now and save 50 percent",
    "You have been selected for a free cash reward click here",
    "Claim your free gift card before it expires today",
    "Act now exclusive deal just for you limited stock",
    "Hot singles in your area waiting to chat now",
    "You are a winner claim your prize immediately",
    "Free money guaranteed no strings attached click now",
    "Hey are we still meeting for lunch tomorrow",
    "Can you send me the report before end of day",
    "Thanks for your help with the project yesterday",
    "Let's catch up over coffee this weekend",
    "The meeting has been moved to 3pm please confirm",
    "I attached the document you asked for",
    "Happy birthday hope you have a great day",
    "Can you review my code before I merge it",
    "Reminder your dentist appointment is tomorrow morning",
    "Great job on the presentation today well done",
]
labels = [
    "spam", "spam", "spam", "spam", "spam",
    "spam", "spam", "spam", "spam", "spam",
    "ham", "ham", "ham", "ham", "ham",
    "ham", "ham", "ham", "ham", "ham",
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

export = {
    "vocabulary": {word: int(idx) for word, idx in vectorizer.vocabulary_.items()},
    "classes": list(model.classes_),
    "class_log_prior": model.class_log_prior_.tolist(),
    "feature_log_prob": model.feature_log_prob_.tolist(),
}

with open("spam_model.json", "w") as f:
    json.dump(export, f)

print("Exported lightweight model to spam_model.json")
print(f"Vocabulary size: {len(export['vocabulary'])}")
print(f"Classes: {export['classes']}")

# ---- Verify: does the real scikit-learn model agree with our export? ----
test_texts = [
    "You have won a free prize click now",
    "Are you free for a call tomorrow",
]
test_vectors = vectorizer.transform(test_texts)
predictions = model.predict(test_vectors)
for text, pred in zip(test_texts, predictions):
    print(f"'{text}' -> {pred}")