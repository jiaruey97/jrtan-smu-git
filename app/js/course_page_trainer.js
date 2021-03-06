const courseAddress = '3.131.65.207:5144'
const materialAddress = '3.131.65.207:5344'
const classAddress = '3.131.65.207:5044'

//Get parameter query
const urlSearchParams = new URLSearchParams(window.location.search)
const params = Object.fromEntries(urlSearchParams.entries())

const vueApp = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: {
    selectedFile: null,
    all_courses: [],
    lesson_materials: [],
    current_sections: 0, //Current number of sections
    new_old_section_choice: 'new',
    chosen_course: {}, //This one holds the course id chosen initially
    chosen_course_name: 'Course',
    chosen_course_id: 0, //This one locks the course id loaded
    chosen_section: 1, //Which section user choose if they want to update old sessions
    new_material: '',
    material_path: [],
    instructor: params.instructor,
    lock_upload_materials_interface: true, //Loock the Upload Material Interface, only unlock once user choose course!
    lock_course_update_button: true, //Unlock only after user has selected and loaded a course
  },
  created() {
    this.current_sections = this.lesson_materials.length
    axios.get(`http://${courseAddress}/spm/course`)
      .then(function (response) {
        course_data = response.data.data
        vueApp.all_courses = course_data.course
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  methods: {
    selectFile: function (file) {
      this.material_path = file
    },
    load_course_content: function () {
      //Display the course name:
      display_course_name()

      this.chosen_course_id = this.chosen_course
      axios.get(`http://${materialAddress}/spm/materials/${this.chosen_course_id}`)
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
    append_material: function () {
      if (this.new_old_section_choice == 'old') {
        const select_section = vueApp.lesson_materials.Lesson_Materials.find(section => section.section_no == this.chosen_section)
        const materials_arr = select_section.materials
        materials_arr.push({
          'material_title': this.new_material,
          'material_path': '/upload/' + replace_whitespace(this.material_path.name)
        })

      } else {
        //Create a new section
        new_section = {
          'section_no': (this.current_sections + 1).toString(),
          'materials': [{
            'material_title': this.new_material,
            'material_path': 'upload/' + replace_whitespace(this.material_path.name)
          }]
        }
        //Check if it's a new course
        if (this.lesson_materials.Lesson_Materials == '') {
          //If it's a new course
          this.lesson_materials.Lesson_Materials = [new_section]
        } else {
          //If it's an old course
          this.lesson_materials.Lesson_Materials.push(new_section)
        }
        this.current_sections += 1
      }
    },
    update_course_material: function () {
      lesson_material_id = this.lesson_materials.Lesson_Materials_ID
      console.log(this.lesson_materials)
      axios.post(`http://${materialAddress}/update_materials/${lesson_material_id}`, this.lesson_materials)
        .then(function (response) {
          server_reply = response.data.message
          alert(server_reply + " updating sections")

          number_of_sections = vueApp.current_sections

          //This function updates the section for the classes with the corresponding course id
          axios.get(`http://${classAddress}/spm/class/update_section/${vueApp.chosen_course_id}/${number_of_sections}`)
          .then(function(response){
            server_reply = response.data.message
            alert(server_reply)

          }).catch(function (response){

            alert(error)
          })

        })
        .catch(function (error) {
          alert(error)
        })

    },
    download_materials: function (file) {
      //window.location.href = file
      window.open(file, '_blank');

    },
    go_to_quiz_builder: function(){
      url = "quiz_builder.html?instructor=" + this.instructor
      window.open(url, "_blank")
    }
  },
})

function file_upload() {
  var formData = new FormData();
  formData.append('file', vueApp.material_path)
  axios.post(`http://${materialAddress}/spm/upload_materials/`, formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(function (response) {
      data = response.data.message
      alert(data)
    }).catch(function (error) {
      alert(error)
    })
}

function replace_whitespace(item) {
  return item.replace(/ /g, "_")
}

//Find course name to display
function display_course_name(course_id) {
  course_obj = vueApp.all_courses.find(course => course.Course_ID == vueApp.chosen_course)
  vueApp.chosen_course_name = course_obj.Course_Name
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

function Lesson(section, lesson, materials) {
  this.section = section
  this.lesson = lesson
  this.materials = materials
}