# crypto-deathrow 🤖💸  
A Telegram bot that helps you optimize your funds across multiple platforms on a daily basis for maximum returns. 🚀✨  

## Features
- 📊 Analyze potential returns based on your balances, APRs, and transfer fees.  
- 📥 Accepts data in a simple JSON format for seamless input.  
- 🎨 Generates fancy visualizations to show the best platform to consolidate your funds.  
- ⚡ Provides instant results, saving you time and effort.  

---

## How It Works
1. Start the bot by sending `/start`.  
2. Provide your data in JSON format:  
   ```json
   {
     "platforms": ["Platform1", "Platform2", "Platform3"],
     "balances": [1000.00, 2000.00, 1500.00],
     "APRs": [0.05, 0.10, 0.07],
     "transfer_fee_matrix": [
       [0, 1.0, 1.5],
       [1.0, 0, 2.0],
       [1.5, 2.0, 0]
     ]
   }
   ```
 
3. Receive an optimized breakdown of potential returns and a barplot visualization.  

---

## Example Output
💬 **Bot Response**:  
```
✨ Fund Optimization Results ✨  
💼 Status Quo Return: $X,XXX.XX  
💰 Highest Potential Return: $Y,YYY.YY  
🏆 Best Platform: Platform3  
```  
📊 A barplot image showing potential returns for each platform.  

---

## Installation
1. Clone the repo:  
   ```bash
   git clone https://github.com/yourusername/crypto-deathrow.git
   cd crypto-deathrow
   ```  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Set up your Telegram bot token by adding it to the `.env` file:  
   ```env
   BOT_TOKEN=your_telegram_bot_token
   ```  
4. Run the bot:  
   ```bash
   python bot.py
   ```  

---

## Contribution
I love contributions! Create a fork, make your changes, and submit a PR.  

---

## License
MIT License  

---

Made with ❤️ and Python for smarter financial decisions. 🌟
