const addressQuiz = "3.131.65.207:5544"

const quiz_app = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        isLoaded: true,
        results: [],
        questions: [],
        answer_options: [],
        quiz_section: true, //'init, quiz, end' -> They denote the 3 phases, initilization phase, quiz, and submission page
        score: 0,
        percentage: 0,
        banner_flag: false,
        banner_flag_msg: "",
        submit_msg: ""
    },
    created(){
        
        axios.get(`http://${addressQuiz}/spm/quiz_retrieve/4`)
        .then(function (response) {
            loaded_question = JSON.parse(response.data.data.Question_Object)
            quiz_app.questions = loaded_question
      
        })
        .catch( function (error) {
            console.log(error)
        })
    }, 
    computed: {
        returnQuiz: function() {
            return this.questions
        }
    },
    methods: {
        mountQuiz: function() {
            this.questions = this.results
            console.log(this.questions)
            return None
        }
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