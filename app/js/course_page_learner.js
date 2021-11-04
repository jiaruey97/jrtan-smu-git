
const courseAddress = '3.131.65.207:5144'
const materialAddress = '3.131.65.207:5344'
const classAddress='3.131.65.207:5044'
const userAddress='3.131.65.207:5744'
// -> Section -> Lesson -> Materials

//Get parameter query
const urlSearchParams = new URLSearchParams(window.location.search)
const params = Object.fromEntries(urlSearchParams.entries())

const vueApp = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: {
    student:params.user,
    class_id:params.class,
    course_id:params.course_id,
    current_sections: 0,
    lesson_materials: [],
    chosen_course_name: params.course_name,
    finished_material: [], //store all the materials the person has completed
  },
  created() {
    // this.current_sections = this.lesson_materials.length
    axios.get(`http://${materialAddress}/spm/materials/${this.course_id}`)
        .then(function (response) {
          return_response = response.data.data

          //Need to parse the lesson materials, cos it's in JSON form.
          if (return_response.Lesson_Materials != '') {
            return_response.Lesson_Materials = JSON.parse(return_response.Lesson_Materials)
          }

          vueApp.lesson_materials = return_response
          console.log(vueApp.class_id)

          //Unlock!
          vueApp.current_sections = vueApp.lesson_materials.Lesson_Materials.length
          vueApp.load_course_content()
        })
        .catch(function (error) {
          console.log(error)
        })

  },
  methods: {
    load_course_content: function () {
      
      this.chosen_course_id = this.chosen_course
      axios.get(`http://${materialAddress}/spm/materials/${this.course_id}`)
        .then(function (response) {
          return_response = response.data.data

          //Need to parse the lesson materials, cos it's in JSON form.
          if (return_response.Lesson_Materials != '') {
            return_response.Lesson_Materials = JSON.parse(return_response.Lesson_Materials)
          }

          vueApp.lesson_materials = return_response

          //Unlock!
          vueApp.current_sections = vueApp.lesson_materials.Lesson_Materials.length
          vueApp.lock_upload_materials_interface = false
          vueApp.lock_course_update_button = false
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    download_materials: function (file) {
      //window.location.href = file
      window.open(file, '_blank');

      }
    }
})

//Find course name to display
function display_class_content(class_id){
    class_obj = vueApp.all_classes.find(course => course.Class_ID == vueApp.chosen_class)
    // vueApp.chosen_course_name = course_obj.Course_Name
    vueApp.class_id=class_obj.Class_ID
    vueApp.student=class_obj.Students
}

// //We create a course prototype
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

