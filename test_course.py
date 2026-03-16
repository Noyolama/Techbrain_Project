import pytest
from playwright.sync_api import Page, expect
import re

BASE_URL = "https://techbrain.ai"


# 1️ Verify that home page displays courses
def test_home(page: Page):
    page.goto(BASE_URL)
    courses_heading = page.locator("//h1[contains(text(),'Courses')]")
    expect(courses_heading).to_be_visible()


# 2️ Verify signin with valid credentials
def test_signinbutton(page: Page):
    page.goto(BASE_URL)
    page.locator("//nav//a[span[text()='Sign in']]").click()
  
    page.fill("#user_email", "maya0102@gmail.com")
    page.fill("#user_password", "test123")
    page.locator("input[name='commit']").click()
    expect(page).to_have_url(re.compile("sign_in"))


# 3️ Verify signup with valid credentials
def test_signup(page: Page):
    page.goto(BASE_URL)
    page.locator("//nav//a[span[text()='Sign in']]").click()
    page.locator("//div/a[text()='Sign up']").click()
    page.fill("#user_email", "test0102@gmail.com")
    page.fill("#user_password", "test123")
    page.fill("#user_password_confirmation", "test123")
    page.locator("input[name='commit']").click()
    expect(page).to_have_url(re.compile("sign_up"))


# 4️ Verify quiz functionality
def test_quiz(page):
    page.goto(BASE_URL)

    page.locator("//a[contains(@href,'goals-of-the-intro-course')]").click()

    for _ in range(4):
        current_url = page.url
        page.locator("//form//button[@type='submit']").click()
        page.wait_for_url(lambda url: url != current_url)

    page.locator("//a[contains(@href,'quiz')]").click()
    page.wait_for_url(lambda url: "quiz" in url)


# 5️  Verify lists of courses have lessons
def test_lists(page: Page):
    page.goto(BASE_URL)
    page.locator("(//span[text()='Lists'])[1]").click()
    first_topic = page.locator("//a[contains(@href,'goals')]")
    first_topic.click()
    page.wait_for_url('https://techbrain.ai/introduction-to-ruby-and-object-oriented-programming/lessons/goals-of-the-intro-course')
    expect(page).to_have_url("goals")


# 6️ Verify that lesson list is viewable after starting course
def test_lessonlist(page: Page):
    page.goto(BASE_URL)
    page.locator("(//a/span[text()='Start'])[1]").click()
 
    lesson_list = page.locator("//div/a/span[@class='pr-1']")
    lesson_list.click()

    lesson_topic = page.locator("//a[contains(@href,'goals')]")
    

# 7️ Verify GitHub link opens
def test_github(page: Page):
    page.goto(BASE_URL)
    page.locator("//a[contains(@href,'ideator-an-idea-sharing-app/lessons/setting-up-the-environment')]/span").click()
    page.locator("//form//button[@type='submit']").click()

    increment = 300
    while True:
        github_links = page.locator("//a[contains(@href,'github')]")
        if github_links.count() > 0 and github_links.first.is_visible():
            github_links.first.click()
            break
        page.evaluate(f"window.scrollBy(0, {increment})")
        page.wait_for_timeout(500)

    page.wait_for_timeout(1000)
    page_contexts = page.context.pages
    page.context.pages[-1].bring_to_front()


# 8 Verify assignment's link opens
def test_assignment(page: Page):
    page.goto(BASE_URL)
    page.locator("(//span[text()='Lists'])[3]").click()
    topic = page.locator("//h3/a[contains(text(),' 1. Practice, Practice, Practice')]")
    topic.click()

    assignment_problem = page.locator("//p/a[contains(text(),'Remove Duplicates')]")
    assignment_problem.scroll_into_view_if_needed()
    assignment_problem.click()

    # Switch to new tab
    page.context.pages[-1].bring_to_front()
    


# 9 Verify that click on finish button navigates to home page
def test_finish(page: Page):
    page.goto(BASE_URL)
    
    # Click on intro course link
    page.locator("(//span[@class='text-blue-700' and text()='Lists'])[1]").click()

    lessons = page.locator("//h3/a")
    lesson_count = lessons.count()

    lesson_locator = "//h3/a[contains(text(),' 5. Challenge: Building a Deck of Cards')]"
    max_scrolls = 20
    for i in range(max_scrolls):
        lesson = page.locator(lesson_locator)
        if lesson.is_visible():
            lesson.scroll_into_view_if_needed()
            lesson.click()
            print(f"Clicked lesson on scroll attempt {i+1}")
            break
        page.evaluate("window.scrollBy(0, 400)")  # scroll down
        page.wait_for_timeout(500)  # small pause to see scrolling
    else:
        raise Exception("Lesson not found after scrolling")
    
    next_button = page.locator("//form/button/span[contains(text(), 'Finish')]")
    next_button.wait_for(state="visible", timeout=5000)
    next_button.scroll_into_view_if_needed()
    next_button.click()
    expect(page).to_have_url(re.compile("techbrain"))


def test_image(page: Page):
    page.goto(BASE_URL)
    # Locate the image
    Start = page.locator("//a[contains(@href,'ideator-an-idea-sharing-app/lessons/setting-up-the-environment')]/span")
    Start.click()

    image_locator = "(//img[@alt='image.png'])[1]"
    max_scrolls = 20
    for i in range(max_scrolls):
        image = page.locator(image_locator)
        if image.is_visible():
            image.scroll_into_view_if_needed()
            print(f"Clicked lesson on scroll attempt {i+1}")
            break
        page.evaluate("window.scrollBy(0, 400)")  # scroll down
        page.wait_for_timeout(500)  # small pause to see scrolling
    else:
        raise Exception("Lesson not found after scrolling")   
        

   

    

#10 Verify closing a lesson tab
def test_close(page: Page):
    page.goto(BASE_URL)
    page.locator("(//a/span[text()='Start'])[1]").click()

    lesson_list = page.locator("//div/a/span[@class='pr-1']")
    lesson_list.click()

    close_tab = page.locator("//button/span[@class ='text-gray-500']")
    close_tab.click()

    page_back = page.locator("//div/a/span[@class='pr-1']")
    expect(page_back).to_have_text("Lesson list")
