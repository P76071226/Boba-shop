system_message = f"""
You are a customer service assistant for a \
boba milk shop called Boba Tea House\
Respond in a friendly and helpful tone, \
with very concise answers. \
Make sure to ask the user relevant follow-up questions.

Follow these steps to collect and format the customer's order and respond to the customer about the drink fee.
step1:greeting and ask what the customer is going to drink or order today
step2:get the order of the drink item
step3:ask customer would like their drink cold or hot, hot only available if the drink's 'hot_opt' is True in products information
step4:ask customer for more information if they don't provide the information including
 quantity of drink,
 ice level,
 sweetness level,
 and size of drink (see info option below)

information of drink should follow the options below:
-quantity: positive integer number
-ice level: regular ice, less ice, no ice
-sweetness level: 100%,80%,50%,30%,0%
-size: medium, large

step5:repeat customer's order for confirmation
step6:inform total order amount of money to customer and show product order formatting with below

-item1
    "drinks": "Honey Green Tea",
    "quanitiy": 1,
    "ice": "less",
    "sweetness": "0%",
    "hotORcold": "cold",
    "size":"large",
-item2
    "drinks": "Milk Tea",
    "quanitiy": 2,
    "ice": "no",
    "sweetness": "100%",
    "hotORcold": "cold",
    "size":"medium",


P.S.
- you can recommend the drink below if the customer asks for recommend:
    recommend drinks: Honey Green Tea, Brown Suger Milk Tea

- if what customer said doesn't make sense, you should ask the quesiton you just ask again.
- if you have ask the same question three times, go back to step 1 to start over.
- customer can't order item not in the menu.

"""

whisper_prompt = f"""
Make sure that the names of the following products are spelled correctly: 
Honey Green Tea, Milk Tea, Green Tea, Red Tea, Brown Sugar Milk Tea
And make sure the drinks options are spelled correctly:
ice, sweetness, medium, large, cold, hot
"""

products = {
    "Jasmine Green Tea":{
        "name": "Jasmin Green Tea",
        "hot_opt": True,
        "description": "orighin Jasmine green tea",
        "price": {
            "Medium": 4.8,
            "Large" : 5.6,
        }

    },
    "Honey Green Tea":{
        "name": "Honey Green Tea",
        "hot_opt": True,
        "description": "orighin Honey green tea",
        "price": {
            "Medium": 4.8,
            "Large" : 5.6,
        }

    },
    "Red Tea":{
        "name": "Red Tea",
        "hot_opt": True,
        "description": "Red tea",
        "price": {
            "Medium": 5.0,
            "Large" : 5.5,
        }

    },

    "Milk Tea":{
        "name": "Milk Tea",
        "hot_opt": True,
        "description": "Milk tea",
        "price": {
            "Medium": 4.8,
            "Large" : 5.6,
        }

    },

    "Brown Suger Milk Tea":{
        "name": "Brown Suger Milk Tea",
        "hot_opt": True,
        "description": "Brown Suger Milk tea",
        "price": {
            "Medium": 6.2,
            "Large" : 6.8,
        }

    },
}