from playwright.sync_api import sync_playwright
# this file is for login in tensojapan.com as part of tensoparse
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) #slowmo=50

    context = browser.new_context()
    
    #context = browser.new_context(storage_state="default.json")
    #with open("default.json", "r") as json_state_file:
    #    storage_state = json.load(json_state_file)
    page = context.new_page()

    emairu=input("email ")
    paasuworudo= input("passw ")

    page.goto('https://www.tensojapan.com/en/login?ReturnUrl=%2Fen%2Fpackage%2Flist')
    print(page.content())
# <input class="form-control input-lg" id="UserName" name="UserName" type="text" value="">
# <input class="form-control input-lg" id="Password" maxlength="20" name="Password" type="password">
# page.get_by_role("button", name="Save").nth(1).click()
# page.get_by_placeholder("Enter your security key PIN").click()
#    page.wait_for_timeout(5000)
    page.wait_for_selector('text=Login')
    
    page.get_by_label('Registered Email Address').fill(emairu)
    page.get_by_label('Password').fill(paasuworudo)
    
    page.click('text=Login')
    
    page.wait_for_timeout(5000)
    #print(page.content())
    page_post = page.content()

    # Save the HTML content to a file
    with open("tensojapan_dashboard.html", "w", encoding="utf-8") as file:
        file.write(page_post)

    
    # Check if login was successful
    if "list" in page.url:
        print("Login successful!")

    else:
        print("Login failed!")

    # Close the browser
    browser.close()


