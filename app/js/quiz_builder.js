//Please extract them as a variable!!
const addressQuiz = "3.131.65.207:5544"
const addressClass = "3.131.65.207:5044"

const vueApp = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: {
    mcq: true,
    binary: false,
    q_type_top: 'MCQ',
    Course_ID: "",
    Section: "",
    questions_store: [],
    question_title:'',
    question_name: '',
    options: ['', '', '', ''],
    correct_option: '',
    correct_option_binary: 'true',
    num_options: 4,
    question_latest: 1,
    question_edit: 1, //Keeps track if mode is edit, the question number. It MUST correspond with the index position in the question store
    mode: true, //true == new or false == edit
    show_quiz: false, //true means show quiz buildinng interface
    Quiz_ID: "", //For storing purpose
    items: [1, 2, 3, 5, 6, 7],
    selected_section: "",
    Class_ID:"",

    headers: [
      {
        text: 'Quiz ID',
        align: 'start',
        value: 'Quiz_ID',
      },
      { text: 'Course_ID', value: 'Course_ID' },
      { text: 'Section', value: 'Section' },
      { text: 'Actions', value: 'actions' },
    ],

    headers2: [
      {
        text: 'Class_ID',
        align: 'start',
        value: 'Class_ID',
      },
      { text: 'Class_Name', value: 'Class_Name' },
      { text: 'Class_Details', value: 'Class_Details' },
      { text: 'Course_ID', value: 'Course_ID' },
      { text: 'Section', value: 'Section' },
      { text: 'Selected_Section', value: 'act' },
    ],

    quiz_list: [],
    course_list: [],

  },

  created: function() {
    this.initialize()
  },
  
  methods: {
    
    newQuiz: function(item){
      console.log(item)
      if (this.selected_section > item.Section){
        alert("Please Select a Section Lower than the Section")
      } else{
        this.Course_ID = item.Course_ID
        this.Section = item.selected_section
        this.Class_ID = item.Class_ID
        this.show_quiz = true
      }
    },


    editQuiz: function(item) {
      console.log(item)
      question = JSON.parse(item.Question_Object)
      this.questions_store = question
      this.Course_ID = item.Course_ID
      this.Section = item.Section
      this.Quiz_ID = item.Quiz_ID
      this.show_quiz = true
      console.log(this.Quiz_ID)
    },
    
    deleteExistingQuiz: function (item) {
      axios.post(`http://${addressQuiz}/quiz/delete/` + item.Quiz_ID)
      .then(function (response) {
        console.log(response)
        alert("Your Quiz has been deleted")
        window.location.reload()
      })
      .catch(function (error) {
        alert("Something have went wrong")
      });
    },

    initialize: function() {
      typo = Array()
      axios.get(`http://${addressQuiz}/spm/quiz/12`)
      // axios.get("http://3.131.65.207:5244/spm/quiz/12")
      .then(function (response) {
        quiz = response.data.data.course
        console.log(quiz)
        for (let i = 0; i < quiz.length; i++) {
          placehold = {
            Quiz_ID:quiz[i].Quiz_ID,
            Course_ID:quiz[i].Course_ID,
            Section:quiz[i].Section,
            Question_Object: quiz[i].Question_Object
          }
          typo.push(placehold)
        }
      })
      
      .catch(function (error) {
        console.log(error);
      });

      this.quiz_list = typo

      typo2 = Array()

      axios.get(`http://${addressClass}/spm/class/12`)
      //axios.get("http://3.131.65.207:5244/spm/class/12")
      .then(function (response) {
        class_list = response.data.data.course
        for (let i = 0; i < class_list.length; i++) {
          placehold = {
            Class_ID:class_list[i].Class_ID,
            Class_Name:class_list[i].Class_Name,
            Class_Details:class_list[i].Class_Details,
            Course_ID:class_list[i].Course_ID,
            Section:class_list[i].Sections,
          }
          typo2.push(placehold)
        }
      })
      
      .catch(function (error) {
        console.log(error);
      });

      this.course_list = typo2
    },


    submit_database: function() {

      // To Purge the Database of the current one
      if(this.questions_store.length != 0){
        if(this.Quiz_ID != ""){

          post_object = {
            'Question_Object': JSON.stringify(this.questions_store),
          }
          console.log(post_object)
          axios.post(`http://${addressQuiz}/quiz/`+ this.Quiz_ID + `/update`, post_object)
          .then(function (response) {
            console.log(response);
            alert("UpdaTED  ")
            window.location.reload()
            })
          
          .catch(function (error) {
            console.log(error);
            alert("It seems that something have went wrong")
          });

        }
        else{

          post_object = {
            'Course_ID': this.Course_ID,
            'Instructor_ID': 12,
            'Section': this.selected_section, //originally, this.section 
            'Question_Object': JSON.stringify(this.questions_store),
            'Class_ID': this.Class_ID 
          } 
          
          console.log(post_object)
  
          //axios.post("http://3.131.65.207:5244/create_quiz", post_object) 
          axios.post(`http://${addressQuiz}/create_quiz`, post_object) 
  
          .then(function (response) {
            console.log(response);
            alert("Your Message have been save in teh database")
            window.location.reload()
            })
          
          .catch(function (error) {
            console.log(error);
            alert("It seems that something have went wrong")
          });


        }

      } else {
       alert("There is No Question Stored. Please submit a Question")
      }

    },


    switch_mcq: function () {
      this.mcq = true
      this.binary = false
      this.mode = 'new'
      this.q_type_top = 'MCQ'
      //wipe everything
      this.question_name = ''
      this.options = ['', '', '', '']
      correct_option = ''
      correct_option_binary = 'true'

    },
    switch_binary: function () {
      this.binary = true
      this.mcq = false
      this.q_type_top = 'Binary'
      //wipe everything
      this.question_name = ''
      this.options = ['', '', '', '']
      correct_option = ''
      correct_option_binary = 'true'
    },

    
    // Delete the Question in the Store
    delete_question: function(question_number){
      this.questions_store.splice(question_number-1,1)
      this.question_title = ""
      this.question_name = ""
      this.options = ['', '', '', '']
      this.correct_option = ''
      this.mode = true
    },

    //Edit the Question in the Store
    edit_question: function (question_number) {

      question_obj = this.questions_store.find(({ question_no }) => question_no === question_number)

      if (question_obj.type == 'mcq') {
        this.mcq = true
        this.binary = false
        this.q_type_top = 'MCQ'

        this.question_title = question_obj.question_title
        this.question_name = question_obj.question
        this.options = question_obj.options
        this.correct_option = question_obj.answer


        this.mode = false
        this.question_edit = question_obj.question_no
      }
      if (question_obj.type == 'binary'){
        this.mcq = false
        this.binary = true
        this.q_type_top = 'Binary'
        
        this.question_title = question_obj.question_title
        this.question_name = question_obj.question
        this.correct_option_binary = question_obj.answer

        this.mode = false
        this.question_edit = question_obj.question_no

      }
    }
  }
})



function mcq_question_submit() {

  if (vueApp.mode) {

    question_number = vueApp.question_latest
    question_title = vueApp.question_title
    question_name = vueApp.question_name
    question_option = vueApp.options
    question_answer = vueApp.correct_option

    if (question_title != "" & question_name != "" & question_option.length != 0 & question_answer != ""){
      mcq_question = {
        'question_no': question_number,
        'question_title': question_title,
        'question': question_name,
        'options': question_option,
        'answer': question_answer,
        'type': 'mcq'
      }
  
      vueApp.questions_store.push(mcq_question)
      vueApp.question_latest += 1
      vueApp.mode = true //Ensure that it is NEW!!
  
      vueApp.question_title = ""
      vueApp.question_name = ""
      vueApp.options = ['', '', '', '']
      vueApp.correct_option = ''   
    } else {
      alert("Sad Noises")
    }

  } else {
    //Assume edit mode, we use the question number to track
    question_index = vueApp.question_edit - 1
    question_title = vueApp.question_title
    question_name = vueApp.question_name
    question_option = vueApp.options
    question_answer = vueApp.correct_option
    if (question_title != "" & question_name != "" & question_option.length != 0 & question_answer != ""){
      mcq_question = {
        'question_no': vueApp.question_edit,
        'question_title': vueApp.question_title,
        'question': vueApp.question_name,
        'options': vueApp.options,
        'answer': vueApp.correct_option,
        'type': 'mcq'
      }
  
      //Modify the edited question
      vueApp.questions_store[question_index] = mcq_question
  
      vueApp.question_title = ""
      vueApp.question_name = ""
      vueApp.options = ['', '', '', '']
      vueApp.correct_option = ''
  
      vueApp.mode = true
    } else {
      alert("Birds Chirping????")
    }


  }

}

function binary_question_submit() {

  if (vueApp.mode) {
    question_number = vueApp.question_latest
    question_title = vueApp.question_title
    question_name = vueApp.question_name
    question_answer = vueApp.correct_option_binary

    if (question_answer != "" & question_title != "" & question_name != ""){
      binary_question = {
        'question_no': question_number,
        'question_title': question_title,
        'question': question_name,
        'answer': question_answer,
        'type': 'binary'
      }
  
      vueApp.questions_store.push(binary_question)
      vueApp.question_latest += 1
      vueApp.mode = true //Ensure that it is NEW!!
  
      vueApp.question_title = ""
      vueApp.question_name = ""
      vueApp.options = ['', '', '', '']
      vueApp.correct_option = ''

    } else {

      alert("Life is SaD!")

    }




  } else {
    //Assume edit mode, we use the question number to track
    question_index = vueApp.question_edit - 1

    if (question_answer != "" & question_title != "" & question_name != ""){
      binary_question = {
      
        'question_no': vueApp.question_edit,
        'question_title': vueApp.question_title,
        'question': vueApp.question_name,
        'answer': vueApp.correct_option_binary,
        'type': 'binary'
      }
  
      //Modify the edited question
      vueApp.questions_store[question_index] = binary_question
  
      vueApp.question_title = ""
      vueApp.question_name = ""
      vueApp.options = ['', '', '', '']
      vueApp.correct_option = ''
  
      vueApp.mode = true

    } else {
      alert("I is SaD!")
    }



  }

}

