import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# List of FAQs and their answers
faqs = [
    ("What is your return policy?", "Our return policy allows customers to return items within 30 days of purchase."),
    ("How can I track my order?", "You can track your order by logging into your account or using the tracking number provided in the shipping confirmation email."),
    ("Do you offer international shipping?", "Yes, we offer international shipping to most countries. Please check our shipping page for more details."),
    # Add more FAQs and answers here
    ("What are the top Android phone brands available?", "Some of the top Android phone brands include Samsung, Google, OnePlus, Xiaomi, and Huawei."),
    ("Which brand offers the best camera quality in Android phones?", "Many brands like Samsung, Google, and Huawei are known for their excellent camera quality in Android phones."),
    ("What is the latest flagship phone from Samsung?", "The latest flagship phone from Samsung is the Samsung Galaxy S21."),
    ("Does OnePlus offer 5G connectivity in their Android phones?", "Yes, OnePlus offers 5G connectivity in their latest Android phone models."),
    ("Which brand provides stock Android experience in their phones?", "Google Pixel phones are known for providing a stock Android experience."),
    ("Are Xiaomi Android phones budget-friendly?", "Yes, Xiaomi offers a range of budget-friendly Android phone options."),
    #
    ("What are the key features to consider when buying an Android phone?", "Key features to consider when buying an Android phone include display size and quality, processor performance, camera capabilities, battery life, storage capacity, and software updates."),
    ("Does Huawei offer Google services on their Android phones?", "Recent Huawei phones may not have Google services pre-installed due to trade restrictions. However, they provide their own alternative app ecosystem."),
    ("Can I expand the storage on an Android phone?", "Many Android phones have a microSD card slot that allows you to expand the storage capacity. However, some models may not have this feature, so it's important to check the specifications."),
    ("Do Android phones support dual SIM cards?", "Yes, many Android phones offer dual SIM card support, allowing you to use two SIM cards simultaneously."),
    ("What is the warranty period for Android phones?", "The warranty period for Android phones varies by brand and model. Typically, it ranges from 1 to 2 years."),
    ("Which brand offers the best battery life in Android phones?", "Brands like Samsung, OnePlus, and Motorola are known for providing good battery life in their Android phones."),
    ("What are the available color options for Android phones?", "The available color options for Android phones vary by brand and model. It's best to check the specific product listings for the available color choices."),
    ("Can I use wireless charging with an Android phone?", "Many Android phones now support wireless charging. However, it's important to check the phone's specifications to confirm if it has wireless charging capabilities."),
    ("What is the difference between OLED and LCD displays on Android phones?", "OLED displays offer deeper blacks and better contrast compared to LCD displays. They also provide more vibrant colors and better energy efficiency."),
    # Add more FAQs and answers here
    ("What are the delivery options available?", "We offer various delivery options, including standard delivery, express delivery, and scheduled delivery. The available options will be displayed during the checkout process."),
    ("Can I return an item if it is damaged during delivery?", "Yes, you can return an item if it is damaged during delivery. Please initiate a return and provide details of the damage for a smooth process."),
    ("How can I pay for my order on your website?", "You can pay for your order using multiple payment options, including credit cards, debit cards, net banking, and UPI. The available payment methods will be displayed during the checkout process."),
    ("What is the estimated delivery time for my location?", "The estimated delivery time depends on your location and the availability of the product. You can enter your pin code on the product page or during the checkout process to get an estimated delivery date."),
    ("Do you offer cash on delivery (COD) as a payment option?", "Yes, we offer cash on delivery (COD) as a payment option for select products and locations. You can check the availability of COD during the checkout process."),
    ("Can I cancel my order after it has been placed?", "You can cancel your order if it hasn't been shipped yet. However, once the order is shipped, it cannot be canceled. Please contact our customer support for assistance."),
    ("Are there any additional charges for delivery?", "Additional charges for delivery may apply depending on the product, location, and delivery option chosen. Any applicable charges will be displayed during the checkout process."),
    ("What is the warranty period for electronic products?", "The warranty period for electronic products varies by brand and product. You can find the warranty details on the product page or refer to the manufacturer's warranty policy."),
    ("Do you offer EMI (Equated Monthly Installments) options?", "Yes, we offer EMI options on select products and for certain payment methods. You can check the availability of EMI options during the checkout process."),
    ("Can I track my order using a mobile app?", "Yes, you can track your order using our mobile app. Simply download our app from the App Store or Google Play Store and sign in to your account."),
    ("What should I do if I receive a wrong or defective item?", "If you receive a wrong or defective item, please contact our customer support within [number of days] of delivery. We will arrange for a return and replacement of the item."),
    ("Is there a loyalty program or rewards program for customers?", "Yes, we have a loyalty program for our valued customers. You can earn rewards points on eligible purchases and redeem them for discounts or other benefits."),
    ("What is your price match policy?", "We have a price match policy where we strive to offer competitive prices. If you find the same product at a lower price on another website, please contact our customer support with the details for possible price matching."),
    ("Are there any restrictions on using promotional codes?", "Some promotional codes may have restrictions, such as being valid for a limited time, applicable only to certain products, or eligible for specific customer segments. Please review the terms and conditions of the promotional code for more details."),
    ("Do you offer installation services for large appliances?", "Yes, we provide installation services for large appliances like refrigerators, washing machines, and televisions. You can select this option during the checkout process or contact our customer support for assistance."),
    ("Can I return a gift I received?", "Yes, you can return a gift you received. Please contact our customer support with the order details or gift receipt, and we will assist you with the return process."),
    ("What is your privacy policy?", "We take customer privacy seriously. You can find detailed information about our privacy policy on our website. We ensure that your personal information is securely handled and used only for relevant purposes."),
    ("Do you offer international shipping?", "Yes, we offer international shipping to select countries. The available countries and shipping rates will be displayed during the checkout process."),
    ("Can I change my shipping address after placing the order?", "Once an order is placed, the shipping address cannot be changed. Please ensure that the shipping address provided during checkout is accurate."),

    #clothing
    ("What are the available sizes for the merchandise/clothing?", "The available sizes for the merchandise/clothing may vary. It's best to check the size chart provided on the product page for accurate measurements."),
    ("What is the material used for the merchandise/clothing?", "The material used for the merchandise/clothing depends on the specific item. Common materials include cotton, polyester, silk, and blends. The product description or specifications will provide details about the material."),
    ("How do I choose the right size for the merchandise/clothing?", "To choose the right size, refer to the size chart provided on the product page. Measure yourself and compare the measurements with the size chart to find the best fit."),
    ("What is the return/exchange policy for merchandise/clothing?", "The return/exchange policy for merchandise/clothing may vary by store. It's important to review the specific store's policy regarding returns and exchanges."),
    ("Are there any discounts available for the merchandise/clothing?", "Discounts on merchandise/clothing may be available during sales events, promotions, or with the use of discount codes. Check the store's website or promotional materials for any ongoing discounts."),
    ("Can I track the shipment of the merchandise/clothing?", "Yes, you can track the shipment of the merchandise/clothing. A tracking number is usually provided, which you can use to track the package on the shipping carrier's website."),
    ("How do I care for the merchandise/clothing?", "The care instructions for merchandise/clothing will depend on the specific item and material. Generally, it is recommended to follow the care instructions provided on the product's label or packaging."),
    ("What payment methods are accepted for purchasing merchandise/clothing?", "Accepted payment methods for purchasing merchandise/clothing may include credit cards, debit cards, online payment platforms, and gift cards. The available payment options are usually displayed during the checkout process."),
    ("Can I cancel my order for merchandise/clothing?", "The ability to cancel an order for merchandise/clothing depends on various factors, such as the store's cancellation policy and the order status. It's best to contact customer support for assistance with order cancellations."),
    ("Are there any additional costs for international shipping of merchandise/clothing?", "Additional costs, such as customs duties or taxes, may apply for international shipping of merchandise/clothing. It's important to review the store's international shipping policy or contact customer support for more information."),
    # Add more FAQs and answers here

    
]

# Preprocess the FAQs and answers
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(lemmatized_tokens)

preprocessed_faqs = [(preprocess_text(question), answer) for question, answer in faqs]

# Vectorize the preprocessed FAQs
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform([question for question, answer in preprocessed_faqs])

# Function to find the best answer based on user input
def find_best_answer(user_input):
    preprocessed_input = preprocess_text(user_input)
    input_vector = vectorizer.transform([preprocessed_input])

    # Calculate cosine similarities between user input and FAQ vectors
    similarities = cosine_similarity(input_vector, faq_vectors).flatten()
    best_index = similarities.argmax()

    # Return the corresponding answer
    return preprocessed_faqs[best_index][1]
