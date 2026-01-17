from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

try:
    print("Looking for your open Chrome profile...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    print("Connected to your profile!")

    input(">>> Press ENTER here to inject scripts and start...")

    # --- INJECTION SCRIPT (Includes Global Switch: window.botActive) ---
    setup_js = """
    window.botActive = true; 

    // 1. Big Cookie
    if (window.bigCookieLoop) clearInterval(window.bigCookieLoop);
    window.bigCookieLoop = setInterval(function() {
        if (window.botActive && typeof Game !== 'undefined' && Game.ready) Game.ClickCookie();
    }, 5);

    // 2. Golden Cookies
    if (window.goldenLoop) clearInterval(window.goldenLoop);
    window.goldenLoop = setInterval(function() {
        if (window.botActive && typeof Game !== 'undefined' && Game.ready) {
            var shimmers = document.getElementsByClassName('shimmer');
            for (var i = 0; i < shimmers.length; i++) {
                if (!shimmers[i].getAttribute('data-waiting')) {
                    shimmers[i].setAttribute('data-waiting', 'true');
                    let target = shimmers[i];
                    setTimeout(function() {
                        if (window.botActive && target) target.click();
                    }, 1000);
                }
            }
        }
    }, 500);

    // 3. Upgrades
    if (window.upgradeLoop) clearInterval(window.upgradeLoop);
    window.upgradeLoop = setInterval(function() {
        if (window.botActive && typeof Game !== 'undefined' && Game.ready) {
            // Filter list: only keep upgrades that aren't 'toggles' or 'tech' switches
            var realUpgrades = Game.UpgradesInStore.filter(function(u) {
                return u.pool !== 'toggle' && u.pool !== 'tech';
            });

            if (realUpgrades.length > 0) {
                var upgrade = realUpgrades[0];
                if (upgrade.getPrice() <= Game.cookies) {
                    upgrade.buy();
                    console.log("Bought real upgrade: " + upgrade.name);
                }
            }
        }
    }, 1000);

    // 4. Smart Buildings
    if (window.smartBuyLoop) clearInterval(window.smartBuyLoop);
    window.smartBuyLoop = setInterval(function() {
        if (window.botActive && typeof Game !== 'undefined' && Game.ready) {
            var bestObj = null; var bestScore = Infinity; var currentCps = Game.cookiesPs;
            Game.ObjectsById.forEach(function(obj) {
                var price = obj.bulkPrice;
                var cpsIncrease = obj.storedCps * Game.globalCpsMult;
                if (cpsIncrease > 0) {
                    var payoffLoad = price * (1 + (currentCps / cpsIncrease));
                    if (payoffLoad < bestScore) { bestScore = payoffLoad; bestObj = obj; }
                }
            });
            if (bestObj && Game.cookies >= bestObj.bulkPrice) bestObj.buy(1);
        }
    }, 100);

    // 5. Wrinkler Popper (Force Click Method)
    if (window.wrinklerLoop) clearInterval(window.wrinklerLoop);
    window.wrinklerLoop = setInterval(function() {
        if (window.botActive && typeof Game !== 'undefined' && Game.ready) {
            for (var i in Game.wrinklers) {
                var w = Game.wrinklers[i];
                // Phase 2 means they are attached and eating
                if (w.phase === 2) {
                    w.hp = 0; // Set health to 0
                    // Trigger the 'click' event on the wrinkler specifically
                    Game.wrinklers[i].type = 1; // Ensure it's not a shiny one if you want to keep those
                    w.die(); 
                }
            }
        }
    }, 5000); 
    """
    driver.execute_script(setup_js)
    print(">>> BOT INITIALIZED.")
    def loop_status(name):
        return driver.execute_script(f"return window.{name} ? 'WORKING' : 'STOPPED';")


    # --- PAUSE SYSTEM LOOP ---
    while True:
        print(f"""
        [MAIN]
        P = Pause all
        R = Resume all
        S = Stop & Save

        [LOOPS STATUS]
        1 = Big Cookie     [{loop_status('bigCookieLoop')}]
        2 = Golden Cookies [{loop_status('goldenLoop')}]
        3 = Upgrades       [{loop_status('upgradeLoop')}]
        4 = Buildings      [{loop_status('smartBuyLoop')}]
        5 = Wrinklers      [{loop_status('wrinklerLoop')}]
        """)


        cmd = input(">> ").lower()

        if cmd == 'p':
            driver.execute_script("window.botActive = false;")
            print("|| BOT PAUSED")

        elif cmd == 'r':
            driver.execute_script("window.botActive = true;")
            print(">> BOT RESUMED")

        elif cmd == '1':
            driver.execute_script("""
                if (window.bigCookieLoop) {
                    clearInterval(window.bigCookieLoop);
                    window.bigCookieLoop = null;
                } else {
                    window.bigCookieLoop = setInterval(function() {
                        if (window.botActive && Game.ready) Game.ClickCookie();
                    }, 5);
                }
            """)
            print("Toggled Big Cookie")

        elif cmd == '2':
            driver.execute_script("""
                if (window.goldenLoop) {
                    clearInterval(window.goldenLoop);
                    window.goldenLoop = null;
                } else {
                    window.goldenLoop = setInterval(function() {
                        if (window.botActive && Game.ready) {
                            var shimmers = document.getElementsByClassName('shimmer');
                            for (var i = 0; i < shimmers.length; i++) shimmers[i].click();
                        }
                    }, 500);
                }
            """)
            print("Toggled Golden Cookies")

        elif cmd == '3':
            driver.execute_script("""
                if (window.upgradeLoop) {
                    clearInterval(window.upgradeLoop);
                    window.upgradeLoop = null;
                } else {
                    window.upgradeLoop = setInterval(function() {
                        if (window.botActive && Game.ready) {
                            var u = Game.UpgradesInStore[0];
                            if (u && u.getPrice() <= Game.cookies) u.buy();
                        }
                    }, 1000);
                }
            """)
            print("Toggled Upgrades")

        elif cmd == '4':
            driver.execute_script("""
                if (window.smartBuyLoop) {
                    clearInterval(window.smartBuyLoop);
                    window.smartBuyLoop = null;
                } else {
                    window.smartBuyLoop = setInterval(function() {
                        if (window.botActive && Game.ready) {
                            var o = Game.ObjectsById[0];
                            if (o && Game.cookies >= o.bulkPrice) o.buy(1);
                        }
                    }, 100);
                }
            """)
            print("Toggled Buildings")

        elif cmd == '5':
            driver.execute_script("""
                if (window.wrinklerLoop) {
                    clearInterval(window.wrinklerLoop);
                    window.wrinklerLoop = null;
                } else {
                    window.wrinklerLoop = setInterval(function() {
                        if (window.botActive && Game.ready) {
                            Game.wrinklers.forEach(w => { if (w.phase === 2) w.hp = 0; });
                        }
                    }, 5000);
                }
            """)
            print("Toggled Wrinklers")

        elif cmd == 's':
            print("Stopping all loops and saving...")
            driver.execute_script("""
                window.botActive = false;
                clearInterval(window.bigCookieLoop);
                clearInterval(window.goldenLoop);
                clearInterval(window.upgradeLoop);
                clearInterval(window.smartBuyLoop);
                clearInterval(window.wrinklerLoop);
            """)
            break

        else:
            print("Invalid command.")


except Exception as e:
    print(f"\n[!] ERROR: {e}")

finally:
    if 'driver' in locals():
        driver.quit()