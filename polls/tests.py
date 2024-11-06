from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

class MySeleniumTests(StaticLiveServerTestCase):
# no crearem una BD de test en aquesta ocasió (comentem la línia)
#fixtures = ['testdb.json',]
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		opts = Options()
		cls.selenium = WebDriver(options=opts)
		cls.selenium.implicitly_wait(5)
# creem superusuari
		user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
		user.is_superuser = True
		user.is_staff = True
		user.save()
	@classmethod
	def tearDownClass(cls):
		cls.selenium.quit()
		super().tearDownClass()
#acc
	def test_login(self):
		self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
		self.assertEqual( self.selenium.title , "Log in | Django site admin" )# comprovem que el títol de la pàgina és el que esperem
		username_input = self.selenium.find_element(By.NAME,"username") # introduïm dades de login i cliquem el botó "Log in" per entrar
		username_input.send_keys('isard')
		password_input = self.selenium.find_element(By.NAME,"password")
		password_input.send_keys('pirineus')
		self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()
		self.assertEqual( self.selenium.title , "Site administration | Django site admin" )# testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
		self.selenium.find_element(By.XPATH,'/html/body/div/div/main/div/div[1]/div[1]/table/tbody/tr[2]/td[1]/a').click()#fem click afegir nou usuari
		usuari_input = self.selenium.find_element(By.XPATH,'//*[@id="id_username"]')
		usuari_input.send_keys('staff')
		contrasenya_input = self.selenium.find_element(By.XPATH,'//*[@id="id_password1"]')
		contrasenya_input.send_keys('Staff080399')
		contrasenya1_input = self.selenium.find_element(By.XPATH,'//*[@id="id_password2"]')
		contrasenya1_input.send_keys('Staff080399')
		self.selenium.find_element(By.XPATH,'/html/body/div/div/main/div/div/form/div/div/input[1]').click()#fer guardar
		self.selenium.find_element(By.XPATH,'//*[@id="id_is_staff"]').click()#donar permisos
		self.selenium.find_element(By.XPATH,'/html/body/div[1]/div/main/div/div/form/div/div/input[1]').click()
		self.selenium.find_element(By.XPATH,'/html/body/div[1]/header/div[2]/form/button').click()
		self.selenium.find_element(By.XPATH,'/html/body/div/div/main/div/p[2]/a').click()
		usuari1 = self.selenium.find_element(By.NAME,"username") # introduïm dades de login i cliquem el botó "Log in" per entrar
		usuari1.send_keys('staff')
		contrasenya1 = self.selenium.find_element(By.NAME,"password")
		contrasenya1.send_keys('Staff080399')
		self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()
		self.assertEqual( self.selenium.title , "Site administration | Django site admin" )
		try:
			self.selenium.find_element(By.XPATH,'/html/body/div/div/main/div/div[1]/div[1]/table/tbody/tr[2]/td[1]/a')
			assert False, "Trobat element que NO hi ha de ser"
		except NoSuchElementException:
			pass
		try:
			self.selenium.find_element(By.XPATH,'/html/body/div/div/main/div/div[1]/div[2]/table/tbody/tr[2]/td[1]/a')
			assert False, "Trobat element que NO hi ha de ser"
		except NoSuchElementException:
			pass


# Create your tests here.
