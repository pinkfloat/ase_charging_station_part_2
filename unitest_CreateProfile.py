class CreateProfileTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    def test_create_profile_success(self):
        # Simulate form data
        form_data = {

            "firstname": "Danny",
            "lastname": "Mart",
            "emailaddress": "Danny.Mart@gmail.com",
            "username": "DanyMart1610",
            "password": "Dany@123",
            "month": "01",
            "day": "15",
            "year": "1990",
            "contactinformation": "9876543211",
            "Gender": "01",
            "street": "36T Main St",
            "state": "Berlin",
            "city": "Berlin",
            "zipcode": "99401"
        
        }

        # Send POST request to create profile
        response = self.app.post('/create-profile', data=form_data)
        
        # Check response status code
        self.assertEqual(response.status_code, 201)
        
        # Check response data
        response_data = json.loads(response.data)
        self.assertEqual(response_data["message"], "Profile created successfully")
        self.assertEqual(response_data["profile"]["firstname"], form_data["firstname"])
        self.assertEqual(response_data["profile"]["lastname"], form_data["lastname"])
        self.assertEqual(response_data["profile"]["emailaddress"], form_data["emailaddress"])
        self.assertEqual(response_data["profile"]["username"], form_data["username"])
        self.assertEqual(response_data["profile"]["birthday"], "1990-01-15")
        self.assertEqual(response_data["profile"]["contactinformation"], form_data["contactinformation"])
        self.assertEqual(response_data["profile"]["gender"], form_data["Gender"])
        self.assertEqual(response_data["profile"]["street"], form_data["street"])
        self.assertEqual(response_data["profile"]["state"], form_data["state"])
        self.assertEqual(response_data["profile"]["city"], form_data["city"])
        self.assertEqual(response_data["profile"]["zipcode"], form_data["zipcode"])

    def test_missing_firstname(self):
        form_data = {
            "lastname": "Mart",
            "emailaddress": "Danny.Mart@gmail.com",
            "username": "DanyMart1610",
            "password": "Dany@123",
            "month": "01",
            "day": "15",
            "year": "1990",
            "contactinformation": "9876543211",
            "Gender": "01",
            "street": "36T Main St",
            "state": "Berlin",
            "city": "Berlin",
            "zipcode": "99401"
        
        }
        response = self.app.post('/create-profile', data=form_data)
        self.assertNotEqual(response.status_code, 201)

    def test_missing_lastname(self):
        form_data = {
            "firstname": "John",
            "emailaddress": "Danny.Mart@gmail.com",
            "username": "DanyMart1610",
            "password": "Dany@123",
            "month": "01",
            "day": "15",
            "year": "1990",
            "contactinformation": "9876543211",
            "Gender": "01",
            "street": "36T Main St",
            "state": "Berlin",
            "city": "Berlin",
            "zipcode": "99401"
        
        }
        response = self.app.post('/create-profile', data=form_data)
        self.assertNotEqual(response.status_code, 201)

    def test_invalid_email(self):
        form_data = {
            "firstname": "John",
            "lastname": "Mart",
            "emailaddress": "DannyMart11@gmail.com", # Invalid email address
            "username": "DanyMart1610",
            "password": "Dany@123",
            "month": "01",
            "day": "15",
            "year": "1990",
            "contactinformation": "9876543211",
            "Gender": "01",
            "street": "36T Main St",
            "state": "Berlin",
            "city": "Berlin",
            "zipcode": "99401"
        
        }
        response = self.app.post('/create-profile', data=form_data)
        self.assertNotEqual(response.status_code, 201)

    def test_invalid_password(self):
        form_data = {
            "firstname": "Danny",
            "lastname": "Mart",
            "emailaddress": "Danny.Mart@gmail.com",
            "username": "DanyMart1610",
            "password": "Dany234", # invalid password
            "month": "01",
            "day": "15",
            "year": "1990",
            "contactinformation": "9876543211",
            "Gender": "01",
            "street": "36T Main St",
            "state": "Berlin",
            "city": "Berlin",
            "zipcode": "99401"
        }
        response = self.app.post('/create-profile', data=form_data)
        self.assertNotEqual(response.status_code, 201)

    def test_invalid_contact_number(self):
        form_data = {
            "firstname": "Danny",
            "lastname": "Mart",
            "emailaddress": "Danny.Mart@gmail.com",
            "username": "DanyMart1610",
            "password": "Dany@123",
            "month": "01",
            "day": "15",
            "year": "1990",
            "contactinformation": "1234abcd",
            "Gender": "01",
            "street": "36T Main St",
            "state": "Berlin",
            "city": "Berlin",
            "zipcode": "99401"
        }
        response = self.app.post('/create-profile', data=form_data)
        self.assertNotEqual(response.status_code, 201)

    def test_missing_gender(self):
        form_data = {
            "firstname": "Danny",
            "lastname": "Mart",
            "emailaddress": "Danny.Mart@gmail.com",
            "username": "DanyMart1610",
            "password": "Dany@123",
            "month": "01",
            "day": "15",
            "year": "1990",
            "contactinformation": "9876543211",
            "street": "36T Main St",
            "state": "Berlin",
            "city": "Berlin",
            "zipcode": "99401"
        }
        response = self.app.post('/create-profile', data=form_data)
        self.assertNotEqual(response.status_code, 201)

    def test_missing_address(self):
        form_data = {
            "firstname": "Danny",
            "lastname": "Mart",
            "emailaddress": "Danny.Mart@gmail.com",
            "username": "DanyMart1610",
            "password": "Dany@123",
            "month": "01",
            "day": "15",
            "year": "1990",
            "contactinformation": "9876543211",
            "Gender": "01",
            "state": "Berlin",
            "city": "Berlin",
            "zipcode": "99401"
        }
        response = self.app.post('/create-profile', data=form_data)
        self.assertNotEqual(response.status_code, 201)

    def test_invalid_zipcode(self):
        form_data = {
            "firstname": "Danny",
            "lastname": "Mart",
            "emailaddress": "Danny.Mart@gmail.com",
            "username": "DanyMart1610",
            "password": "Dany@123",
            "month": "01",
            "day": "15",
            "year": "1990",
            "contactinformation": "9876543211",
            "Gender": "01",
            "street": "36T Main St",
            "state": "Berlin",
            "city": "Berlin",
            "zipcode": "abcds"  # invalid zipcode
        }
        response = self.app.post('/create-profile', data=form_data)
        self.assertNotEqual(response.status_code, 201)
