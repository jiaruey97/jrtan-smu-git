course_details = [{
  'course_id': '1',
  'course_name': 'Circuit Theory',
  'course_details': 'In this course, students are required to understand the underlying infrastructure of a circuit board and how each nodes are connected to each other.',
  'duration': '',
  'prerequisite': '',
  'start_time': '2021-12-01 00:00:00',
  'end_time': '2021-12-29 00:00:00',
}]

lesson_materials = [
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

// -> Section -> Lesson -> Materials

const vueApp = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        selectedFile: null,
        course_details: course_details,
        lesson_materials: lesson_materials
    },
    methods: {
      onFileSelected(event){
        console.log(event)
        this.selectedFile = event.target.files[0]
      },
      onUpload(){
        const fd = new FormData();
        fd.append('material', this.selectedFile, this.selectedFile.name)
        axios.post('Schema_Generation.sql', fd)
        .then(res => {
          console.log(res)
        })

      }

      },
  })

//We create a course prototype
function Course(course_id, course_name, course_details, duration, prerequisite, start_time, end_time){
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