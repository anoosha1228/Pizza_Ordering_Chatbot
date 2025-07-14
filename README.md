# 🍕 Pizza Ordering Chatbot (Rasa + MongoDB)

This is a conversational AI chatbot for placing pizza orders, built using **Rasa** within a **Python virtual environment**. The bot understands different pizza types, crusts, and sizes, fetches their prices from MongoDB, validates user credentials using regex, confirms orders, and includes a **visual Rasa Graph** to map the chatbot’s conversation logic.

---

## 🧠 Workflow Overview

1. **Intent and Entity Creation**
   - Created intents such as ordering pizza, providing credentials, and confirming order.
   - Added examples with entities: `pizza_name`, `crust`, `size`.

2. **MongoDB Storage**
   - Stored pizza data (name, crust, size, price) in MongoDB.
   - Used MongoDB for fetching dynamic pricing via custom actions.

3. **Responses and Mapping**
   - Defined template responses for various intents.
   - Used **rules** and **stories** to control the conversation flow.

4. **Custom Actions**
   - Created Python functions to:
     - Access slot values.
     - Query MongoDB for pizza pricing.
     - Handle fallback scenarios when information is missing.
     - Validate credentials and calculate total order price.

5. **Slots and Entity Handling**
   - Entities like `pizza_name`, `crust`, and `size` were stored in **slots**.
   - Slot values were used by custom actions for logic and querying.

6. **Regex for Credential Extraction**
   - Used regex in NLU data to extract `phone_number` and `email` from user input.

7. **Order Confirmation**
   - Fetched individual pizza prices.
   - Summed up the total cost and confirmed the order.

8. **Lookup Tables**
   - Used lookup tables for diverse entity examples (pizza names, crusts, sizes, phone numbers, etc.)

9. **Rasa Graph**
   - Visualized the chatbot’s conversation logic using the **Rasa Graph**, which maps how intents, responses, rules, and stories are connected — improving debugging and understanding.

---

## 💬 Sample Queries
Try the following queries when interacting with the chatbot:

🍕 Ordering Pizza
"I want to order a large pepperoni pizza."

"Can I get a medium Margherita with thin crust?"

"I’d like two small chicken tikka pizzas."

🔁 Clarifications
"Do you have veggie pizza?"

"What crusts do you offer?"

"How much is a large BBQ chicken pizza?"

📩 Contact Info
"My phone number is 03001234567 and email is test@example.com"

"Here is my contact info: test123@gmail.com, 03111234567"

✅ Confirming Order
"Yes, please confirm the order."

"Go ahead and place the order."

---

## 📁 Project Structure

```
Pizza_Ordering_Chatbot/
├── actions/
│   └── actions.py            # Custom scraping & filtering logic
├── data/
│   ├── nlu.yml               # Intents, examples, and entities
│   ├── rules.yml             # Rules mapping
│   └── stories.yml           # Training stories
├── domain.yml                # Responses, slots, entities
├── config.yml                # Rasa pipeline configuration
├── endpoints.yml             # Action server and MongoDB configs
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```

---

## 📌 Features

✅ Rasa-based NLU with intent/entity extraction

✅ MongoDB integration for dynamic price lookup

✅ Custom actions for logic, fallback, and order confirmation

✅ Regex extraction of phone and email

✅ Lookup-based data augmentation

✅ Slot tracking for multi-turn conversation

✅ Rasa Graph visualization for mapping intent-response flows

---

## 🔧 Requirements

Python 3.8+
Rasa 3.x
pymongo
MongoDB

---

## 🛠️ Setup Instructions

Clone the repo
git clone <repo-url>
cd chatbot_project

Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Train the model
rasa train

# Start the action server (for custom scraping logic)
rasa run actions

# Start the chatbot
rasa shell
