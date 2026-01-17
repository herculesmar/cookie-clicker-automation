from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

try:

    print("Connecting to Chrome...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # JavaScript to get chip counts and the upgrade list
    get_data_js = """
    let boughtUpgrades = [];

    Game.PrestigeUpgrades.forEach(function(upgrade) {

        if (upgrade.bought > 0) {

            boughtUpgrades.push(upgrade.name);

        }

    });
    return {

        upgrades: boughtUpgrades,

        chips: Game.heavenlyChips,

        prestige: Game.prestige

    };
    """
    data = driver.execute_script(get_data_js)
    print("\n" + "═"*40)

    print(f" ASCENSION SUMMARY")

    print("═"*40)

    print(f" Current Heavenly Chips: {data['chips']:,.0f}")

    print(f" Total Prestige Level:   {data['prestige']:,.0f}")

    print("─"*40)

    print(f" BOUGHT UPGRADES ({len(data['upgrades'])}):")
    if len(data['upgrades']) == 0:

        print(" > No ascension upgrades found.")

    else:

        for i, name in enumerate(data['upgrades'], 1):

            print(f" {i:2}. {name}")

    print("═"*40)

except Exception as e:

    print(f"Error: {e}")