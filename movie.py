import streamlit as st

# Set the title and description of your app
st.title("Simple Square Calculator")
st.write("Enter a number below and click the button to calculate its square.")

# Create an input field for the user to enter a number
user_input = st.number_input("Enter a number")

# Create a button to trigger the calculation
if st.button("Calculate Square"):
    # Calculate the square of the user's input
    result = user_input ** 2
    # Display the result
    st.write(f"The square of {user_input} is {result}")

# Add a footer to your app
st.text("Built with Streamlit")
