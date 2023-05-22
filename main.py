import streamlit as st
from st_pages import Page, add_page_title, show_pages

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide"
)

show_pages(
    [
        Page("main.py", "Home", "🏠"),
        # Can use :<icon-name>: or the actual icon
        Page("plotting.py", "Plotting", "📈")
    ]
)

# add_page_title()  # Optional method to add title and icon to current page

st.write("# Welcome to the S/R line plotter! 👋")

st.write("🎉 Hey there! Welcome to the Support/Resistance line plotter App. This app is designed to assist you in performing price action technical analysis by drawing support and resistance lines on the charts. It aims to provide you with visual insights and aid in identifying key levels in the market.")

st.write("🔧 To enhance your experience, it offers some settings that you can customize according to your preferences. Feel free to experiment with these settings to find the best fit for your analysis style.")

st.write("💡 A helpful tip: If you're using a mobile device, we recommend switching to landscape mode for optimal viewing and ease of analysis. Give it a try and explore the features!")

st.write("📈 Start plotting support and resistance lines to gain a deeper understanding of price movements and make more informed trading decisions. Enjoy using the S/R line plotter app!")

st.info("For updates and more, follow me on 🐦 Twitter: [@jptsantossilva](https://twitter.com/jptsantossilva). Check out the code on 💻[GitHub](https://github.com/jptsantossilva)")