const course_leaner_app = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
      course: [{
          'course_no': 1,
          'session': [{
              'session_no': [1, 2, 3],
              'lesson': [{
                  'lesson_no': [1, 2, 3],
                  'quiz': 'Quiz 1',
                  'material':[{
                      'material_list': [1, 2, 3]
                  }]
                  }]
              }]
          },
          {
            'course_no': 2,
            'session': [{
                'session_no': [1, 2, 3],
                'lesson': [{
                    'lesson_no': [1, 2, 3],
                    'quiz': 'Quiz 2',
                    'material':[{
                        'material_list': [1, 2, 3]
                    }]
                    }]
                }]
            },
            {
                'course_no': 3,
                'session': [{
                    'session_no': [1, 2, 3],
                    'lesson': [{
                        'lesson_no': [1, 2, 3],
                        'quiz': 'Quiz 3',
                        'material':[{
                            'material_list': [1, 2, 3]
                        }]
                        }]
                    }]
                }]
    }
})
        