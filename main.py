from transformers import pipeline

# Load the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Test the model
text = ("material quality is good and really loved the softness ")
result = sentiment_pipeline(text)

# print(result)
print(result[0]['label'], "->", result[0]['score'])
if result[0]['label'] == '1 star':
    print("Very Negative")
elif result[0]['label'] == '2 stars':
    print("Negative")
elif result[0]['label'] == '3 stars':
    print("Neutral")
elif result[0]['label'] == '4 stars':
    print("Positive")
else:
    print("Very Positive")



# 1 star → Very negative
# 2 stars → Negative
# 3 stars → Neutral
# 4 stars → Positive
# 5 stars → Very positive