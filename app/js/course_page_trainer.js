course_details = [{
  'course_id': '1',
  'course_name': 'Circuit Theory',
  'course_details': 'In this course, students are required to understand the underlying infrastructure of a circuit board and how each nodes are connected to each other.',
  'duration': '',
  'prerequisite': '',
  'start_time': '2021-12-01 00:00:00',
  'end_time': '2021-12-29 00:00:00',
}]

top_materials = {
  'Lesson_Materials_ID': 1,
  'Course_ID': 1,
  'Section': 1,
  Lesson_Materials:
  [
    {
      'section_no': '1',
      'materials': [
        {
          'material_title': 'Introudction to Circuit Theory',
          'material_path': 'filepath'
        },
        {
          'material_title': 'Intro Tutorial',
          'material_path': 'filepath'
        }
      ]
    },
    {
      'section_no': '2',
      'materials': [
        {
          'material_title': 'DC Circuits Lecture',
          'material_path': 'filepath'
        },
        {
          'material_title': 'DC Circuit Tutorial',
          'material_path': 'filepath'
        }
      ]
    }
  ]
}

// -> Section -> Lesson -> Materials

const vueApp = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: {
    selectedFile: null,
    course_details: course_details,
    lesson_materials: top_materials,
    current_sections: 0, //Current number of sections
    new_old_section_choice: 'new',
    chosen_section: 1, //Which section user choose if they want to update old sessions
    new_material: "",
    material_path: [],
  },
  created() {
    this.current_sections = this.lesson_materials.length
  },
  methods: {
    append_material: function () {
      if (vueApp.new_old_section_choice == 'old') {
        const select_section = vueApp.lesson_materials.Lesson_Materials.find(section => section.section_no == this.chosen_section)
        console.log(select_section)
        const materials_arr = select_section.materials
        console.log(materials_arr)
        materials_arr.push({
          'material_title': this.new_material,
          'material_path': 'upload/' + this.material_path.name
        })
      } else {
        //Create a new section
        new_section = {
          'section_no': (this.current_sections + 1).toString(),
          'materials': [{
            'material_title': this.new_material,
            'material_path': 'upload/' + this.material_path.name
          }]
        }
        this.lesson_materials.push(new_section)
        this.current_sections += 1
      }
    }
  },
})

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