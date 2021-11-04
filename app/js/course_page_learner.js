
const courseAddress = '3.131.65.207:5144'
const materialAddress = '3.131.65.207:5344'
const classAddress='3.131.65.207:5044'
const userAddress='3.131.65.207:5744'
const trackerAddress = '3.131.65.207:5644'
// -> Section -> Lesson -> Materials

//Get parameter query
const urlSearchParams = new URLSearchParams(window.location.search)
const params = Object.fromEntries(urlSearchParams.entries())

course_tracking = { "sections_cleared": 0, "quiz_cleared": 0 }

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
    tracking_section: [],
    section_cleared: 0,
    quiz_cleared: 0
  },
  created() {

    //Get courses
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

        for (i = 0; i < vueApp.current_sections; i++) {
          vueApp.tracking_section.push(true)
        }

        // Get tracking data
        axios.get(`http://${trackerAddress}/spm/get_tracker/${vueApp.student}/${vueApp.course_id}/${vueApp.class_id}`)
          .then(function (response) {
            return_response = response.data.data
            vueApp.section_cleared = return_response.Sections_cleared
            vueApp.quiz_cleared = return_response.Quiz_cleared

            update_section_unlock()


          })
          .catch(function (error) {
            console.log(error)
          })

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

    },
    update_section: function () {
      //Update the section clear
      vueApp.section_cleared += 1

      //Update the mincount, this scenario is if user has completed quiz before the section
      //min_clear = Math.min(vueApp.section_cleared, vueApp.quiz_cleared) + 1
      //Vue.set(vueApp.tracking_section, min_clear, false)

      //Send the info to server AND return the results
      axios.get(`http://${trackerAddress}/spm/update_tracker/${vueApp.student}/${vueApp.course_id}/${vueApp.class_id}/${vueApp.section_cleared}`)
        .then(function (response) {
          result = response.data.data
          console.log(result)
          vueApp.quiz_cleared = result.Quiz_cleared
          vueApp.sections_cleared = result.Sections_cleared

          update_section_unlock()

        })
        .catch(function(error){
          console.log(error)
        })
    },
    go_to_quiz: function(section_id){
      url = "quiz.html?course_id=" + this.course_id + "&section_id=" + section_id + "&course_name=" + vueApp.chosen_course_name + "&user=" + vueApp.student
      window.open(url, "_blank")
    }
  },
})

function update_section_unlock() {

  min_clear = Math.min(vueApp.section_cleared, vueApp.quiz_cleared) + 1

  for (i = 0; i < this.min_clear; i++) {
    //vueApp.tracking_section.set()
    Vue.set(vueApp.tracking_section, i, false)
  }
}

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

