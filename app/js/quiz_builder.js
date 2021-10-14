const vueApp = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: {
    mcq: true,
    binary: false,
    q_type_top: 'MCQ',
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
  },
  methods: {
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
    //Assume edit mode, we use the question number to track
    question_index = vueApp.question_edit - 1

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

  }

}

function binary_question_submit() {

  if (vueApp.mode) {
    question_number = vueApp.question_latest
    question_title = vueApp.question_title
    question_name = vueApp.question_name
    question_answer = vueApp.correct_option_binary

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
    //Assume edit mode, we use the question number to track
    question_index = vueApp.question_edit - 1

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

  }

}