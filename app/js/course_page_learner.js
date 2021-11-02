
const courseAddress = '3.131.65.207:5144'
const materialAddress = '3.131.65.207:5344'
const classAddress='3.131.65.207:5044'
const userAddress='3.131.65.207:5744'
// -> Section -> Lesson -> Materials

const vueApp = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: {
    selectedFile: null,
    student='chicken',
    all_courses: [],
    all_classes:[],
    lesson_materials: [],
    current_sections: 0, //Current number of sections
    new_old_section_choice: 'new',
    chosen_course: {}, //This one holds the course id chosen initially
    chosen_class:{},
    // chosen_course_name: 'Course',
    class_name="Class",
    class_id: 8,
    // chosen_course_id: 0, //This one locks the course id loaded
    chosen_section: 1, //Which section user choose if they want to update old sessions
    new_material: "",
    material_path: [],
    lock_upload_materials_interface: true, //Loock the Upload Material Interface, only unlock once user choose course!
    lock_course_update_button: true, //Unlock only after user has selected and loaded a course
  },
  created() {
    // this.current_sections = this.lesson_materials.length

    axios.get(`http://${classAddress}/spm/search_class/8`)
        .then(function (response) {
            // loaded_question = JSON.parse(response.data.data.Question_Object)
            // quiz_app.questions = loaded_question
            class_data = response.data.data
            vueApp.all_classes = class_data.class
            console.log(vueApp.all_classes)
      
        })
        .catch( function (error) {
            console.log(error)
        })
  },
  methods: {
    load_course_content: function () {

      //Display the course name:
      display_class_content()
      this.class_id=this.class_info
      // this.chosen_course_id = this.chosen_course
      axios.get(`http://${classAddress}/spm/class/${this.class_id}`)
        .then(function (response) {
          return_response = response.data.data

          //Need to parse the lesson materials, cos it's in JSON form.
          return_response.Lesson_Materials = JSON.parse(return_response.Lesson_Materials)
          vueApp.lesson_materials = return_response
          console.log(vueApp.lesson_materials)
          
          //Unlock!
          vueApp.lock_upload_materials_interface = false
          vueApp.lock_course_update_button = false
        })
        .catch(function (error) {
          console.log(error)
        })

    },
    // append_material: function () {
    //   if (this.new_old_section_choice == 'old') {
    //     const select_section = vueApp.lesson_materials.Lesson_Materials.find(section => section.section_no == this.chosen_section)
    //     const materials_arr = select_section.materials
    //     materials_arr.push({
    //       'material_title': this.new_material,
    //       'material_path': 'upload/' + this.material_path.name
    //     })
    //   } else {
    //     //Create a new section
    //     new_section = {
    //       'section_no': (this.current_sections + 1).toString(),
    //       'materials': [{
    //         'material_title': this.new_material,
    //         'material_path': 'upload/' + this.material_path.name
    //       }]
    //     }
    //     //Check if it's a new course
    //     if (this.lesson_materials.Lesson_Materials == '') {
    //       //If it's a new course
    //       this.lesson_materials.Lesson_Materials = [new_section]
    //     } else {
    //       //If it's an old course
    //       this.lesson_materials.Lesson_Materials.push(new_section)
    //     }
    //     this.current_sections += 1
    //   }
    // },
    // update_course_material: function () {
    //   lesson_material_id = this.lesson_materials.Lesson_Materials_ID
    //   axios.post(`http://${materialAddress}/update_materials/${lesson_material_id}`, this.lesson_materials)
    //   .then(function (response) {
    //     server_reply = response.data.message
    //     alert(server_reply)
    //   })
    //   .catch(function(error){
    //     alert(error)
    //   })

    // }
  },
})

//Find course name to display
function display_class_content(class_id){
    class_obj = vueApp.all_classes.find(class_item => class_item.Class_ID == vueApp.chosen_class)
    // vueApp.chosen_course_name = course_obj.Course_Name
    vueApp.class_id=class_obj.Class_ID
}

//We create a course prototype
function Course(course_id, course_name, course_details, duration, prerequisite, start_time, end_time) {
  this.course_info = {
    'course_id': course_id,
    'course_name': course_name,
    'course_details': course_details,
  }

  this.course_duration = duration
  this.course_prerequisite = prerequisite

  this.course_lesson_time = {
    'start_time': start_time,
    'end_time': end_time
  }
}

// function Lesson(section, lesson, materials) {
//   this.section = section
//   this.lesson = lesson
//   this.materials = materials
// }



// <<<<<<< HEAD

// sample_data = [{
//   'course_id': '1',
//   'course_name': 'Circuit Theory',
//   'course_details': 'In this course, students are required to understand the underlying infrastructure of a circuit board and how each nodes are connected to each other.',
//   'duration': '',
//   'prerequisite': '',
//   'start_time': '2021-12-01 00:00:00',
//   'end_time': '2021-12-29 00:00:00',
//   'lesson_materials': [{'section 1': [{
//     'material_name': "Lecture 1",
//     'material_location': 'somelocation...'
//   }, {
//     'material_name': "Lecture 2",
//     'material_location': 'somelocation'
//   }]}],
// }]

// const course_page = new Vue({
//     el: '#app',
//     vuetify: new Vuetify(),
//     data:{
//       course_details: sample_data
//     },
    
//     methods: {
//         greet: function (event){
//           //alert("hi")
//           axios({
//             url: 'http://localhost/jrtan-smu-git/testing.txt',
//             method: 'GET',
//             responseType: 'blob'
//           }).then((response) => {
//             const url = window.URL.createObjectURL(new Blob([response.data]));
//             const link = document.createElement('a');
//             link.href = url;
//             link.setAttribute('download', 'material');
//             document.body.appendChild(link);
//             link.click();
//             });
//         }

//     }
// })
// <<<<<<< Updated upstream
// // =======
// // const course_leaner_app = new Vue({
// //     el: '#app',
// //     vuetify: new Vuetify(),
// //     data: {
// //       course: [{
// //           'course_no': 1,
// //           'session': [{
// //               'session_no': [1, 2, 3],
// //               'lesson': [{
// //                   'lesson_no': [1, 2, 3],
// //                   'quiz': 'Quiz 1',
// //                   'material':[{
// //                       'material_list': [1, 2, 3]
// //                   }]
// //                   }]
// //               }]
// //           },
// //           {
// //             'course_no': 2,
// //             'session': [{
// //                 'session_no': [1, 2, 3],
// //                 'lesson': [{
// //                     'lesson_no': [1, 2, 3],
// //                     'quiz': 'Quiz 2',
// //                     'material':[{
// //                         'material_list': [1, 2, 3]
// //                     }]
// //                     }]
// //                 }]
// //             },
// //             { 
// //                 'course_no': 3,
// //                 'session': [{
// //                     'session_no': [1, 2, 3],
// //                     'lesson': [{
// //                         'lesson_no': [1, 2, 3],
// //                         'quiz': 'Quiz 3',
// //                         'material':[{
// //                             'material_list': [1, 2, 3]
// //                         }]
// //                         }]
// //                     }]
// //                 }]
// //     }
// // })
        
// // >>>>>>> a25e2d26abd8522f5feb4e5ac5185dc59d5bbc63
// =======

// >>>>>>> Stashed changes
