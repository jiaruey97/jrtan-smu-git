// <<<<<<< HEAD

sample_data = [{
  'course_id': '1',
  'course_name': 'Circuit Theory',
  'course_details': 'In this course, students are required to understand the underlying infrastructure of a circuit board and how each nodes are connected to each other.',
  'duration': '',
  'prerequisite': '',
  'start_time': '2021-12-01 00:00:00',
  'end_time': '2021-12-29 00:00:00',
  'lesson_materials': [{'section 1': [{
    'material_name': "Lecture 1",
    'material_location': 'somelocation...'
  }, {
    'material_name': "Lecture 2",
    'material_location': 'somelocation'
  }]}],
}]

const course_page = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data:{
      course_details: sample_data
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
<<<<<<< Updated upstream
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
=======

>>>>>>> Stashed changes
