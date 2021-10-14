const quiz_app = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
      questions: [{
          'question_no': 1,
          'question_title': 'Question 1',
          'question': 'Which planet is the smallest in our Solar System?',
          'options': ['Jupiter', 'Mars', 'Mercury', 'Pluto'],
          'answer': 3,
          'type': 'mcq'
      },
      {
          'question_no': 2,
          'question_title': 'Question 2',
          'question': 'Elon Musk was the co-founder of Paypal before he sold it',
          'answer': 'true',
          'type': 'binary',
      },
      {
          'question_no': 3,
          'question_title': 'Question 3',
          'question': 'Are frogs reptilians?',
          'answer': 'false',
          'type': 'binary'
      },
      {
        'question_no': 4,
        'question_title': 'Question 4',
        'question': "Which of the following disorders has Savant Syndrome been observed the most?",
        'options': ['Narcolepsy', 'Autism', 'Kleptomania', 'Dyslexia'],
        'answer': 2,
        'type': 'mcq'
    },],
    answer_options: [],
    quiz_section: true, //This tick implies that you are in the quiz portion,
    score: 0,
    percentage: 0,
    banner_flag: false,
    banner_flag_msg: "",
    submit_msg: ""
    }
})

function quiz_submit() {
    //There will be submission portion, but there will be grading!
    //Manual grading will happen first, then submission of grades together with answer
    quiz_app.banner_flag = false
    //TO-DO: Check if user completed all the questions!
    if (quiz_app.answer_options.length != quiz_app.questions.length){
        //user did not complete question
        quiz_app.banner_flag = true
        quiz_app.banner_flag_msg = "Please complete all questions before submitting!"
        return
    }

    if (quiz_app.answer_options.includes(null)){
        //user did not complete question
        quiz_app.banner_flag = true
        quiz_app.banner_flag_msg = "Please complete all questions before submitting!"
        return 
    }

    number_of_questions = quiz_app.questions.length

    for (i = 0; i < quiz_app.questions.length; i++){
        correct_answer = quiz_app.questions[i].answer
        user_answer = quiz_app.answer_options[i]

        if (correct_answer == user_answer) {
            quiz_app.score += 1
        }

    }

    //Percentage:
    percentage_score = Math.round(quiz_app.score / number_of_questions * 100)
    quiz_app.submit_msg = "You've successfully submitted your quiz! You've attained " + percentage_score.toString() + "%!"

    //Flip user back!
    quiz_app.quiz_section = false

}