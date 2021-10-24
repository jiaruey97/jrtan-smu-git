const course_page = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data:{
        sections: [{
          'section_no': 1,
          'section_title': 'Section 1',

      },
      {
          'section_no': 2,
          'section_title': 'Section 2',

      },
      {
          'section_no': 3,
          'section_title': 'Section 3',
          
      },
    ],
        lessons: [{
        'lesson_no': 1,
        'lesson_title': 'Lesson 1',

    },
    {
        'lesson_no': 2,
        'lesson_title': 'Lesson 2',

    },
    {
        'lesson_no': 3,
        'lesson_title': 'Lesson 3',
        
    },
  ],
        course_section: true,
    }
})