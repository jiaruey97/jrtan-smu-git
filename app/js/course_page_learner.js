
const courseAddress = '3.131.65.207:5144'
const materialAddress = '3.131.65.207:5344'
const classAddress='3.131.65.207:5044'
const userAddress='3.131.65.207:5744'
const quizAddress="3.131.65.207:5544"
// -> Section -> Lesson -> Materials

const vueApp = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: {
    student:'',
    class_id:8,
    course_id:4,
    all_classes:[],
    all_courses:[],
    all_quiz:[],
    chosen_class:{},
    course_name:''
  },
  created() {
    // this.current_sections = this.lesson_materials.length

    axios.get(`http://${classAddress}/spm/search_class/8`)
        .then(function (response) {
            // loaded_question = JSON.parse(response.data.data.Question_Object)
            // quiz_app.questions = loaded_question
            class_data = response.data.data
            vueApp.all_classes = class_data.course

            // vueApp.course_id=vueApp.all_classes.Course_ID
            console.log(vueApp.all_classes)
            console.log(vueApp.course_id)
      
        })
        .catch( function (error) {
            console.log(error)
        })
    axios.get(`http://${courseAddress}/spm/course`)
        .then(function (response) {
          course_data = response.data.data
          vueApp.all_courses = course_data.course
          console.log(vueApp.all_courses)
        })
        .catch(function (error) {
          console.log(error)
        })
    axios.get(`http://${quizAddress}/spm/quiz`)
        .then(function (response) {
          quiz_data = response.data.data
          vueApp.all_quiz= quiz_data.course
          console.log(vueApp.all_quiz)
        })
        .catch(function (error) {
          console.log(error)
        })
  },
  methods: {
    load_course_content: function () {

      //Display the course name:
      display_course_content()
      // this.chosen_course_id = this.chosen_course
      axios.get(`http://${courseAddress}/spm/course_retrieve/${this.course_id}`)
        .then(function (response) {
          return_response = response.data.data
          vueApp.course_name = return_response.Course_Name
        })
        .catch(function (error) {
          console.log(error)
        })

      }
    }
})

// Find course name to display
function display_course_content(course_id){
    course_obj = vueApp.all_courses.find(course => course.Course_ID == vueApp.course_id)
    // vueApp.chosen_course_name = course_obj.Course_Name
    vueApp.course_name = course_obj.Course_Name
    console.log(vueApp.course_name)
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

function Lesson(section, lesson, materials) {
  this.section = section
  this.lesson = lesson
  this.materials = materials
}