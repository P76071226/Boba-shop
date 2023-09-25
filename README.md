# AI Order System for Boba Tea House

## Project Description

The AI Order System for Boba Tea House is a project that utilizes the OpenAI API to create an AI agent capable of handling customer orders. The goal is to reduce labor costs and streamline the ordering process for the Boba tea house. The AI agent responds to customer requests, collects order information, and provides concise answers while maintaining a friendly and helpful tone.

## Installation

To use the AI Order System, follow these installation steps:

1. Clone the repository to your local machine.
2. Create a virtual environment and activate it.
3. Install the required dependencies by running the following command:

   ```bash
   pip install -r requirements.txt
   ```

4. Modify a `.env` file in the project directory and set your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

5. Run the application using the provided script.

## Usage

The AI Order System follows these steps to collect and format customer orders:

1. Greet the customer and ask what they would like to order.
2. Collect the drink order from the customer.
3. Ask if the customer wants their drink cold or hot (if hot option is available).
4. Collect additional order details, including quantity, ice level, sweetness level, and drink size.
5. Repeat the customer's order for confirmation.
6. Inform the customer of the total order amount and display the product order formatting.

You can also recommend drinks such as Honey Green Tea and Brown Sugar Milk Tea if the customer requests recommendations.

## Files

### `utils.py`

This file contains utility functions used in the AI Order System, including the system message and the steps for processing customer orders.

### `app.py`

The main application file that interacts with the OpenAI API to process user messages, collect order information, and generate responses. It includes functions for moderation, message processing, and more.

## Contact Information

For questions or support related to the AI Order System, please contact:

- [Your Name](mailto:your_email@example.com)

We hope you enjoy using the AI Order System for Boba Tea House!
