from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # --- THE CALCULATION SCRIPT ---
    calc_js = """
    let totalCostToBuy = 0;
    let totalGainFromSell = 0;
    let currentBank = Game.cookies;

    Game.ObjectsById.forEach(function(obj) {
        // Calculate cost to reach 200
        if (obj.amount < 200) {
            let needed = 200 - obj.amount;
            totalCostToBuy += obj.getSumPrice(needed);
        }
        // Calculate gain from selling down to 200
        else if (obj.amount > 200) {
            let extra = obj.amount - 200;
            // Game formula for sell return
            totalGainFromSell += obj.getReverseSumPrice(extra);
        }
    });

    return {
        cost: totalCostToBuy,
        gain: totalGainFromSell,
        bank: currentBank,
        possible: (currentBank + totalGainFromSell) >= totalCostToBuy
    };
    """

    result = driver.execute_script(calc_js)
    
    cost = result['cost']
    gain = result['gain']
    bank = result['bank']
    can_afford = result['possible']

    print("--- STRATEGY AUDIT ---")
    print(f"Current Cookies:   {bank:,.0f}")
    print(f"Gain from Selling: +{gain:,.0f}")
    print(f"Cost to reach 200: -{cost:,.0f}")
    print("----------------------")
    
    net_total = (bank + gain) - cost
    
    if can_afford:
        print(f"PROJECTION: SUCCESS. You will have {net_total:,.0f} cookies left.")
    else:
        print(f"PROJECTION: FAILURE. You are short by {abs(net_total):,.0f} cookies.")

    # --- THE USER PROMPT ---
    confirm = input("\nDo you want to run the Equalize-to-200 strategy? (yes/no): ").lower()

    if confirm == 'yes' and can_afford:
        print("Executing Strategy...")
        execute_js = """
        Game.ObjectsById.forEach(function(obj) {
            if (obj.amount > 200) {
                obj.sell(obj.amount - 200);
            }
            if (obj.amount < 200) {
                obj.buy(200 - obj.amount);
            }
        });
        """
        driver.execute_script(execute_js)
        print("Done! All buildings are now at 200.")
    elif confirm == 'yes' and not can_afford:
        print("Strategy aborted: You don't have enough cookies even after selling.")
    else:
        print("Strategy cancelled by user.")

except Exception as e:
    print(f"Error: {e}")