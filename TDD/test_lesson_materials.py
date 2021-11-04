import unittest
import requests
import json

test_lesson_materials = {
            'Course_ID': 5,
            'Lesson_Materials': [
                {
                    "section_no": "1",
                    "materials": [
                        {
                            "material_title": "History of Cliva",
                            "material_path": "upload/Clivian_files.pdf"
                        },
                        {
                            "material_title": "The Axiom Group",
                            "material_path": "upload/Clivian_files.pdf"
                        },
                        {
                            "material_title": "The Grid Palistia",
                            "material_path": "upload/Clivian_files.pdf"
                        },
                    ]
                },
                {
                    "section_no": "2",
                    "materials": [
                        {
                            "material_title": "The History of Void",
                            "material_path": "upload/Session_10_Market_Basket_Analysis.pdf"
                        },
                        {
                            "material_title": "The Perculiarities of Corrupt Magic",
                            "material_path": "upload/Session_10_Market_Basket_Analysis.pdf"
                        },
                        {
                            "material_title": "Idol vs Self",
                            "material_path": "upload/Session_10_Market_Basket_Analysis.pdf"
                        }
                    ]
                },
                {
                    "section_no": "3",
                    "materials": [
                        {
                            "material_title": "Introduction to Espers",
                            "material_path": "upload/Session_10_Market_Basket_Analysis.pdf"
                        },
                        {
                            "material_title": "The Gauntlet",
                            "material_path": "upload/Session_10_Market_Basket_Analysis.pdf"
                        },
                        {
                            "material_title": "Mana",
                            "material_path": "upload/Session_10_Market_Basket_Analysis.pdf"
                        }
                    ]
                }
            ],
            'Lesson_Materials_ID': 5,
        }

class test_retrieve_materials(unittest.TestCase):
    def test_update_class_materials(self):
        response = requests.post("http://3.131.65.207:5344/update_materials/5", json=test_lesson_materials)
        self.assertEqual(response.status_code, 200)
    
    def test_retrieve_class_materials(self):
        response = requests.get("http://3.131.65.207:5344/spm/materials/5")
        result = response.json()
        result['data']['Lesson_Materials'] = json.loads(result['data']['Lesson_Materials'])
        
        self.assertEqual(response.status_code, 300)
        self.assertDictEqual(test_lesson_materials, result['data'])


#{'Course_ID': 5, 'Lesson_Materials': [{'section_no': '1', 'materials': [{'material_title': 'History of Cliva', 'material_path': 'upload/Clivian_files.pdf'}, {'material_title': 'The Axiom Group', 'material_path': 'upload/Clivian_files.pdf'}, {'material_title': 'The Grid Palistia', 'material_path': 'upload/Clivian_files.pdf'}]}, {'section_no': '2', 'materials': [{'material_title': 'The History of Void', 'material_path': 'upload/Session_10_Market_Basket_Analysis.pdf'}, {'material_title': 'The Perculiarities of Corrupt Magic', 'material_path': 'upload/Session_10_Market_Basket_Analysis.pdf'}, {'material_title': 'Idol vs Self', 'material_path': 'upload/Session_10_Market_Basket_Analysis.pdf'}]}, {'section_no': '3', 'materials': [{'material_title': 'Introduction to Espers', 'material_path': 'upload/Session_10_Market_Basket_Analysis.pdf'}, {'material_title': 'The Gauntlet', 'material_path': 'upload/Session_10_Market_Basket_Analysis.pdf'}, {'material_title': 'Mana', 'material_path': 'upload/Session_10_Market_Basket_Analysis.pdf'}]}], 'Lesson_Materials_ID': 5}
#{'Course_ID': 5, 'Lesson_Materials': [{'section_no': '1', 'materials': [{'material_title': 'History of Cliva', 'material_path': 'upload/Clivian_files.pdf'}, {'material_title': 'The Axiom Group', 'material_path': 'upload/Clivian_files.pdf'}, {'material_title': 'The Grid Palistia', 'material_path': 'upload/Clivian_files.pdf'}]}, {'section_no': '2', 'materials': [{'material_title': 'The History of Void', 'material_path': 'upload/Session_10_Market_Basket_Analysis.pdf'}, {'material_title': 'The Perculiarities of Corrupt Magic', 'material_path': 'upload/Session_10_Market_Basket_Analysis.pdf'}, {'material_title': 'Idol vs Self', 'material_path': 'upload/Session_10_Market_Basket_Analysis.pdf'}]}, {'section_no': '3', 'materials': [{'material_title': 'Introduction to Espers', 'material_path': 'upload/Session_10_Market_Basket_Analysis.pdf'}, {'material_title': 'The Gauntlet', 'material_path': 'upload/Session_10_Market_Basket_Analysis.pdf'}, {'material_title': 'Mana', 'material_path': 'upload/Session_10_Market_Basket_Analysis.pdf'}]}], 'Lesson_Materials_ID': 5}