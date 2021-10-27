// <<<<<<< HEAD
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
    },
    
    methods: {
        greet: function (event){
          //alert("hi")
          axios({
            url: 'http://localhost/jrtan-smu-git/testing.txt',
            method: 'GET',
            responseType: 'blob'
          }).then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'material');
            document.body.appendChild(link);
            link.click();
            });
        }

      }
})
// =======
// const course_leaner_app = new Vue({
//     el: '#app',
//     vuetify: new Vuetify(),
//     data: {
//       course: [{
//           'course_no': 1,
//           'session': [{
//               'session_no': [1, 2, 3],
//               'lesson': [{
//                   'lesson_no': [1, 2, 3],
//                   'quiz': 'Quiz 1',
//                   'material':[{
//                       'material_list': [1, 2, 3]
//                   }]
//                   }]
//               }]
//           },
//           {
//             'course_no': 2,
//             'session': [{
//                 'session_no': [1, 2, 3],
//                 'lesson': [{
//                     'lesson_no': [1, 2, 3],
//                     'quiz': 'Quiz 2',
//                     'material':[{
//                         'material_list': [1, 2, 3]
//                     }]
//                     }]
//                 }]
//             },
//             {
//                 'course_no': 3,
//                 'session': [{
//                     'session_no': [1, 2, 3],
//                     'lesson': [{
//                         'lesson_no': [1, 2, 3],
//                         'quiz': 'Quiz 3',
//                         'material':[{
//                             'material_list': [1, 2, 3]
//                         }]
//                         }]
//                     }]
//                 }]
//     }
// })
        
// >>>>>>> a25e2d26abd8522f5feb4e5ac5185dc59d5bbc63
