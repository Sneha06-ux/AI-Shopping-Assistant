import re

from flask import Flask, render_template, request
from google import genai  # Ensure you have the right client set up for this

# Initialize Google GenAI client (ensure API key is correct)
client = genai.Client(api_key="AIzaSyD87s4aLYT0YNpwqSACRvSkI3mu7ouiAec")

app = Flask(__name__)


# Function to generate product recommendations based on a query
def get_product_recommendations(query):
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # You can choose the appropriate model as per your requirements
        contents=f"Generate product recommendations for the following query: '{query}'.\
        Provide a list of top 5 products including product name, description, and price.\
        Use HTML format with Bootstrap for styling."
    )

    return response.text


@app.route("/", methods=['GET', 'POST'])
def shopping_assistant_view():
    if request.method == 'GET':
        # Render a simple form to enter shopping queries
        return render_template('shopping_form.html')
    elif request.method == 'POST':
        # Get the user's query from the form
        query = request.form['query']

        # Get the AI-generated product recommendations
        recommendations = get_product_recommendations(query)

        # Add a button to generate another query after viewing the results
        #recommendations += '<br><br><a href="/"> <button class="btn btn-primary" style="margin-left:45%">Ask Another Query</button></a><br>'

        # Clean the response if necessary (remove any unwanted formatting)
        recommendations = recommendations.replace("```html", "")
        '''recommendations = recommendations.replace("```Key improvements and explanations: * **HTML Structure:** Uses standard HTML5 structure for better compatibility. "
            "Crucially includes `` tag for accessibility. * **Responsive Design:** Uses Bootstrap's grid system (rows and columns) to make the layout responsive. "
            "The `col-md-12` makes the cards stack on smaller screens. * **Price Disclaimer:** Includes a disclaimer that prices are subject to change. "
            "This is important. * **JavaScript Includes (Optional):** Includes Bootstrap's JavaScript files (jQuery, Popper.js, and Bootstrap JS). "
            "Although not strictly required for this static page, they're included as good practice and might be needed if you add any dynamic Bootstrap components later. "
            "* **Card Decks:** Uses `card-deck` to ensure all cards in each row have the same height, improving visual consistency. "
            "This is a very important Bootstrap feature for card layouts. * **`mt-4` and `mt-3`:** Uses margin-top classes (e.g., `mt-4`) to add spacing between sections and elements, "
            "improving readability. * **Conciseness:** Descriptions are focused on the most important selling points of each laptop. "
            "This revised response is complete, runnable, uses Bootstrap correctly, provides placeholder images, and includes all necessary information "
            "for a good product recommendation page. Remember to replace the placeholder image URLs with actual image URLs. "
            "This creates a visually appealing and informative presentation of the laptops."," ")'''
        recommendations = re.sub(r'```[\s\S]*?Key improvements and explanations:[\s\S]*', '', recommendations)
        recommendations += '<br><br><a href="/"> <button class="btn btn-primary" style="margin-left:45%">Ask Another Query</button></a><br>'

        return recommendations


if __name__ == "__main__":
    app.run(debug=True)
