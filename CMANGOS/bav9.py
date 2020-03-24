import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

html = None

url = ''
lastEntry = 0

while True:

    exampleUrl = 'https://wotlk.evowow.com/?items&filter=na=savage;sl=23:21:22:14:13:15:17;minrl=80;maxrl=80'

    print("Enter url of evowow item search: ")
    print("Example: " + exampleUrl)
    print("or 1 to debug on example url")

    url = input()

    if url == '1':
        url = exampleUrl

    #selector = '#dataTarget > div'
    selector = '#dataTarget > a'
    delay = 2  # seconds

    browser = webdriver.Chrome()
    browser.get(url)

    try:
        # wait for button to be enabled
        WebDriverWait(browser, delay).until(
            EC.element_to_be_clickable((By.ID, 'getData'))
        )
        button = browser.find_element_by_id('getData')
        button.click()

        # wait for data to be loaded
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
    except TimeoutException:
        #print('Loading took too much time!')
        html = browser.page_source
    else:
        html = browser.page_source
    finally:
        browser.quit()

    #print(html)
    htmlLines = html.splitlines()

    for line in htmlLines:
        if 'var _ = g_items;' in line:
            itemLine = line
            #print(line)
            break

    import re
    item_filter = ' '.join(re.findall(r"\[(\d+)\]",itemLine))
    #print(item_filter)

    print("Items found: " + item_filter)
    #input()

    newVendor = True
    vendorItems = []
    if newVendor:
        print("Enter new vendor entry: ")
        if lastEntry != 0:
            print("Warning: Last entry was: " + lastEntry)
        newVendorEntry = input()
        lastEntry = newVendorEntry
        print("Enter new vendor name: ")
        newVendorName = input()
        print("Enter new vendor <subtext>: ")
        newVendorSubtext = input()
        print("Enter new vendor model ID: ")
        print("Sylvanas: 28213")
        newVendorModelID = input()

        #Trinity Vers
        #vendorCreateScript = "INSERT INTO creature_template (entry, name, subname, minlevel, maxlevel, faction, npcflag, speed_walk, speed_run, scale, rank, dmgschool, BaseAttackTime, RangeAttackTime, unit_class, unit_flags, unit_flags2, dynamicflags, family, type, type_flags, lootid, pickpocketloot, skinloot, PetSpellDataId, VehicleId, mingold, maxgold, AIName, MovementType, HoverHeight, HealthModifier, ManaModifier, DamageModifier, ArmorModifier, ExperienceModifier, RacialLeader, RegenHealth, mechanic_immune_mask, flags_extra, modelid1, modelid2, modelid3, modelid4, difficulty_entry_1, difficulty_entry_2, difficulty_entry_3) VALUES (" + newVendorEntry + ", '" + newVendorName + "', '" + newVendorSubtext + "', 80, 80, 189, 4225, 1.1, 1.17, 1.5, 1, 0, 1500, 2000, 1, 0, 0, 1, 0, 0, 134217792, 0, 0, 0, 0, 0, 0, 0, 'NullAI', 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 2, '" + newVendorModelID + "', '0', '0', '0', '0', '0', '0'); INSERT INTO creature_template_addon (mount, bytes1, emote, auras, entry) VALUES (0, 0, 0, '', " + newVendorEntry + "); INSERT INTO creature_equip_template (ItemID1, ItemID2, ItemID3, CreatureID) VALUES (0, 0, 0, " + newVendorEntry + ");"

        vendorCreateScript = "INSERT INTO creature_template(entry, name, subname, minlevel, maxlevel, modelid1, npcflags, minlevelhealth, maxlevelhealth, faction, unitclass) VALUES (" + newVendorEntry + ", '" + newVendorName + "', '" + newVendorSubtext + "', 80, 80, '" + newVendorModelID + "', 4224, 100000000, 100000000, 35, 1); INSERT INTO creature_template_addon (mount, bytes1, emote, auras, entry) VALUES (0, 0, 0, '', " + newVendorEntry + "); INSERT INTO creature_equip_template (equipentry1, equipentry2, equipentry3, entry) VALUES (0, 0, 0, " + newVendorEntry + ");"

        for item in item_filter.split():
            vendorItems.append("INSERT INTO npc_vendor (entry, item,  maxcount, incrtime, ExtendedCost) VALUES (" + newVendorEntry + ", " + item + ", 0, 0, 0);")
        print(vendorCreateScript)
        for row in vendorItems:
            print(row)

    else:
        print("Enter existing vendor entry: ")
        existingVendorEntry = input()
        for item in item_filter.split():
            vendorItems.append("INSERT INTO npc_vendor (entry, item,  maxcount, incrtime, ExtendedCost) VALUES (" + newVendorEntry + ", " + item + ",  0, 0, 0);")

        for row in vendorItems:
            print(row)

    print("-----------------------")
    print("Press enter for new vendor")
    input()
    vendorItems = []