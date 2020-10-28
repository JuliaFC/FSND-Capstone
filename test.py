AUTH0_LOGIN_URL = 'https://cowffeeshop.us.auth0.com/authorize?audience=capstone-api&response_type=token&client_id=9thObDYilxkxjY8cWvynTiF4hjH5vyxD&redirect_uri=https://127.0.0.1:5000'

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all, Crew, Base


SUPREME_LEADER_TOKEN = os.environ['SUPREME_LEADER_TOKEN']
CREW_TOKEN = os.environ['CREW_TOKEN']
DATABASE_PATH = os.environ['DATABASE_URL']

FIRST_BASE = 1
NON_EXISTENT_BASE = 10000

FIRST_CREW = 1
NON_EXISTENT_CREW = 10000
'''
This class represents the What To Eat test case.
'''


class FirstOrderTestCase(unittest.TestCase):

    def setUp(self):
        # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_fsnd_test"
        self.database_path = "postgres://{}/{}".format('postgres:1234@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # db_drop_and_create_all()

        # Binds the app to the current context.
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.new_base = {
                "name": "Starkiller Base",
                "planet": "Ilum",
            }
            
        self.new_base_422 = {
                "planet": "Sullust",
            }

        self.new_crew = {
                "name": "Kylo Ren",
                "rank": "Commander",
                "date_of_birth": "0005-12-17",
                "bio": "Commander of the First Order",
                "base_id": "1"
            }
        
        self.new_crew_422 = {
                "name": "Ben Solo",
            }

    def tearDown(self):
        pass

    '''
    TEST SUPREME_LEADER ROLE
    '''

    '''
    Test Supreme Leader post base
    '''
    def test_post_base_supreme_leader(self):
        res = self.client().post('/base', headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)},
            json=self.new_base)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        FIRST_BASE = data['base']['id']

    def test_422_post_base_supreme_leader(self):
        res = self.client().post('/base', headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)},
            json=self.new_base_422)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    '''
    Test Supreme Leader get base
    '''
    def test_get_base_supreme_leader(self):
        res = self.client().get("/base", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['base'])

    def test_404_get_base_supreme_leader(self):
        base_id = NON_EXISTENT_BASE
        res = self.client().get("/base/" + str(base_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    '''
    Test Supreme Leader patch base
    '''
    def test_patch_base_supreme_leader(self):
        base_id = FIRST_BASE
        res = self.client().patch('/base/' + str(
            base_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)},
            json={'name': 'Sith Eternal Base'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_base_supreme_leader(self):
        base_id = NON_EXISTENT_BASE
        res = self.client().patch('/base/' + str(
            base_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)},
            json={'name': 'Sith Eternal Base'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    '''
    Test Supreme Leader post crew
    '''
    def test_post_crew_supreme_leader(self):
        res = self.client().post('/crew', headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)},
            json=self.new_crew)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        FIRST_CREW = data['crew']['id']

    def test_422_post_crew_supreme_leader(self):
        res = self.client().post('/crew', headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)},
            json=self.new_crew_422)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    '''
    Test Supreme Leader get crew
    '''
    def test_get_crew_supreme_leader(self):
        res = self.client().get("/crew", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['crew'])

    def test_404_get_crew_supreme_leader(self):
        crew_id = NON_EXISTENT_BASE
        res = self.client().get("/crew/" + str(crew_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    '''
    Test Supreme Leader patch crew
    '''
    def test_patch_crew_supreme_leader(self):
        crew_id = FIRST_CREW
        res = self.client().patch('/crew/' + str(crew_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)},
            json={'name': 'Luke Skywalker'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_crew_supreme_leader(self):
        crew_id = NON_EXISTENT_CREW
        res = self.client().patch('/crew/' + str(crew_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)},
            json={'name': 'Luke Skywalker'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Test Supreme Leader delete crew
    '''
    def test_remove_crew_supreme_leader(self):
        res = self.client().post('/crew', headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)},
            json=self.new_crew)
        data = json.loads(res.data)
        crew_id = data['crew']['id']

        res = self.client().delete('/crew/' + str(crew_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_remove_crew_supreme_leader(self):
        crew_id = NON_EXISTENT_CREW
        res = self.client().delete('/crew/' + str(crew_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Test Supreme Leader delete base
    '''
    def test_remove_base_supreme_leader(self):
        res = self.client().post('/base', headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)},
            json=self.new_base)
        data = json.loads(res.data)
        base_id = data['base']['id']
        
        res = self.client().delete('/base/' + str(
            base_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_remove_base_supreme_leader(self):
        base_id = NON_EXISTENT_BASE
        res = self.client().delete('/base/' + str(
            base_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SUPREME_LEADER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    # '''
    # TEST CREW ROLE
    # '''

    '''
    Test Crew get crew
    '''
    def test_get_crew_crew(self):
        res = self.client().get("/crew", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CREW_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['crew'])

    '''
    Test Crew get crew which doesn't exist
    '''
    def test_404_get_crew_crew(self):
        crew_id = NON_EXISTENT_CREW
        res = self.client().get("/crew/" + str(crew_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CREW_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    '''
    Test Crew get base
    '''
    def test_get_base_crew(self):
        res = self.client().get("/base", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CREW_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_404_get_base_crew(self):
        base_id = NON_EXISTENT_BASE
        res = self.client().get("/base/" + str(base_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CREW_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    def test_403_post_base_crew(self):
        res = self.client().post('/base', headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CREW_TOKEN)},
            json=self.new_base)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_403_patch_base_crew(self):
        base_id = FIRST_BASE
        res = self.client().patch('/base/' + str(
            base_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CREW_TOKEN)},
            json={'name': 'Sith Eternal Base'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
    
    def test_403_remove_base_crew(self):
        base_id = FIRST_BASE
        
        res = self.client().delete('/base/' + str(
            base_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CREW_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


    def test_get_crew(self):
        res = self.client().get("/crew", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CREW_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_404_get_crew(self):
        crew_id = NON_EXISTENT_BASE
        res = self.client().get("/crew/" + str(crew_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CREW_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
    
    def test_403_post_crew(self):
        res = self.client().post('/crew', headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CREW_TOKEN)},
            json=self.new_crew)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
            
    def test_403_patch_crew(self):
        crew_id = FIRST_CREW
        res = self.client().patch('/crew/' + str(
            crew_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CREW_TOKEN)},
            json={'name': 'Sith Eternal Base'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
    
    def test_403_remove_crew(self):
        crew_id = FIRST_CREW
        
        res = self.client().delete('/crew/' + str(
            crew_id), headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CREW_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

'''
Make the tests conveniently executable
'''

if __name__ == "__main__":
    unittest.main()