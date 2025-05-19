from flask import Flask, render_template, request,redirect, url_for, session
from transformers import pipeline
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Required for session to work

# SQLAlchemy Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql1234_@localhost/feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(50), nullable=False)



def analyze_sentiment(text):
    sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    sentiment = sentiment_pipeline(text)

    # blob = TextBlob(text)                     # Uses TextBlob to analyze the text’s sentiment.
    # sentiment = blob.sentiment
    # polarity = sentiment.polarity             # polarity is extracted, ranging from -1 (negative) to 1 (positive).

    if sentiment[0]['label'] == '1 star':
        sentiment_category = "Very Negative"
    elif sentiment[0]['label'] == '2 stars':
        sentiment_category = "Negative"
    elif sentiment[0]['label'] == '3 stars':
        sentiment_category = "Neutral"
    elif sentiment[0]['label'] == '4 stars':
        sentiment_category = "Positive"
    else:
        sentiment_category = "Very Positive"

    return sentiment_category

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')

        if name and phone:
            session['name'] = name
            session['phone'] = phone
            return redirect(url_for('home'))
        else:
            return "Missing name or phone number", 400  # Optional error message

    return render_template('login.html')


@app.route('/', methods=["GET", "POST"])
def home():
    # Redirect if user is not logged in
    if 'name' not in session or 'phone' not in session:
        return redirect(url_for('login'))

    sentiment = None
    category = None
    feedback = None

    if request.method == 'POST':
        category = request.form.get('category')  # Get selected category
        feedback = request.form.get('text')      # Get feedback text
        sentiment = analyze_sentiment(feedback) if feedback else None  # Analyze only if feedback exists

        if category and feedback and sentiment:
            new_feedback = Feedback(
                name=session.get('name'),
                phone=session.get('phone'),
                category=category,
                feedback_text=feedback,
                sentiment=sentiment
            )
            db.session.add(new_feedback)
            db.session.commit()

    return render_template('index.html',
                           sentiment=sentiment,
                           category=category,
                           feedback=feedback,
                           name=session.get('name'))  # Optional: Pass user's name to template


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return (render_template('about.html'))


@app.route('/contact')
def contact():
    return (render_template('contact.html'))


if __name__ == '__main__':
    app.run(debug=True)
