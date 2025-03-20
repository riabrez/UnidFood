from django.test import TestCase
# Create your tests here.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest

class UnidFoodTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://your-website-url.com"  
        self.driver.get(self.base_url)
    
    def test_homepage_loads(self):
        """Test if the homepage loads and displays essential elements."""
        driver = self.driver
        self.assertIn("UnidFood", driver.title)
        self.assertTrue(driver.find_element(By.ID, "homepage-map")) 
    
    def test_user_authentication(self):
        """Test if users can sign up, log in, and log out."""
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Sign Up").click()
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "submit").click()
        self.assertIn("Welcome, testuser", driver.page_source)
        
        driver.find_element(By.LINK_TEXT, "Log Out").click()
        self.assertIn("Log In", driver.page_source)
    
    def test_review_submission(self):
        """Test if a signed-in user can submit a review."""
        driver = self.driver
        self.login()
        driver.get(f"{self.base_url}/places/restaurants/restaurant")
        driver.find_element(By.NAME, "review_text").send_keys("Great place!")
        driver.find_element(By.NAME, "rating").send_keys("5")
        driver.find_element(By.NAME, "submit").click()
        self.assertIn("Great place!", driver.page_source)
    
    def test_edit_delete_review(self):
        """Test if users can edit and delete their own reviews."""
        driver = self.driver
        self.login()
        driver.get(f"{self.base_url}/myreviews")
        driver.find_element(By.LINK_TEXT, "Edit").click()
        driver.find_element(By.NAME, "review_text").clear()
        driver.find_element(By.NAME, "review_text").send_keys("Updated review!")
        driver.find_element(By.NAME, "submit").click()
        self.assertIn("Updated review!", driver.page_source)
        
        driver.find_element(By.LINK_TEXT, "Delete").click()
        self.assertNotIn("Updated review!", driver.page_source)
    
    def test_student_deals_visible(self):
        """Test if student deals are accessible."""
        driver = self.driver
        driver.get(f"{self.base_url}/places/studentdeals")
        self.assertTrue(driver.find_element(By.CLASS_NAME, "deal-item"))
    
    def test_meetup_invites(self):
        """Test if users can invite friends for meetups."""
        driver = self.driver
        self.login()
        driver.get(f"{self.base_url}/mymeetups")
        driver.find_element(By.NAME, "invite_friend").send_keys("friend@example.com")
        driver.find_element(By.NAME, "submit").click()
        self.assertIn("Invitation sent", driver.page_source)
    
    def test_notifications_for_meetups(self):
        """Test if users receive notifications for meetup invitations."""
        driver = self.driver
        self.login()
        driver.get(f"{self.base_url}/notifications")
        self.assertIn("Meetup Invitation", driver.page_source)
    
    def login(self):
        """Helper method to log in a test user."""
        driver = self.driver
        driver.get(f"{self.base_url}/login")
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "submit").click()
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()