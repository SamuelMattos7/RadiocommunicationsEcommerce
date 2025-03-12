# My Project

![REIDIOSOLUTIONS Logo](Proyecto/static/img/reidiosolutionszz.jpg)

## 📌 Description
Through an eCommerce platform specialized in radiocommunications, organizations and businesses will have access to a unified platform where they can obtain not only the required equipment but also all related components and services. This will include the option to manage necessary licenses, purchase compatible accessories, and receive centralized technical support. By consolidating all these needs in a single site, operational complexities will be reduced, hardware management efficiency will be enhanced, and redundancies will be minimized.

![REIDIOSOLUTIONS Home](Proyecto/static/img/HomeScreenshot.jpg)

## 🚀 Features
- User Authentication & Management: Secure sign up system with email verification.
- Product Catalog Management: Allows easy addition, modification, and categorization of radio communication products.
- Shopping Cart & Checkout: Streamlined checkout process with order summary and secure transactions.
- Stock & Inventory Tracking: Track and manage existing inventory as well as the posibility of adding new products to the catalogue.
- Order management: ability to visualize users orders and their shipment information.

## 🛠️ Tech Stack

* **Backend:**
    * Django (Python)
    * MySQL
    * PayPal REST SDK
* **Frontend:**
    * HTML
    * CSS
    * JavaScript

## 📦 Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SamuelMattos7/RadiocommunicationsEcommerce.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd RadiocommunicationsEcommerce
    cd ProjectFinal
    ```

3.  **Activate the virtual environment:**
* **On Windows (Command Prompt or PowerShell):**
    ```
    venv\Scripts\activate
    ```

4.  **Navigate to proyecto folder and install the dependencies:**
    - this step installation requirements are only necessary if the venv activation failed, otherwise skip pip install command
    ```
    cd Proyecto
    pip install -r requirements.txt
    py manage.py runserver
    ```