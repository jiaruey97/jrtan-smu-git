const addressQuiz = "3.131.65.207:5544"
const addressQuizResult = "3.131.65.207:5444"

const urlSearchParams = new URLSearchParams(window.location.search)
const params = Object.fromEntries(urlSearchParams.entries())

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
        time: 0,
        timer_text: '',
        quiz_id: 0,
        course_id: params.course_id,
        section_id: params.section_id,
        class_id: params.class_id,
        student: params.user,
        course_name: params.course_name,
        banner_flag: false,
        banner_flag_msg: "",
        submit_msg: ""
    },
    created() {

        axios.get(`http://${addressQuiz}/spm/quiz_retrieve/${this.course_id}/${this.class_id}/${this.section_id}`)
            .then(function (response) {
                loaded_question = JSON.parse(response.data.data.Question_Object)
                quiz_app.questions = loaded_question
                quiz_app.time = response.data.data.Time
                quiz_app.quiz_id = response.data.data.Quiz_ID
                //Time is on hourly basis, convert to seconds
                time_seconds = quiz_app.time * 60 * 60
                startTimer(time_seconds)

            })
            .catch(function (error) {
                console.log(error)
            })
    },
    computed: {
        returnQuiz: function () {
            return this.questions
        }
    },
    methods: {
        mountQuiz: function () {
            this.questions = this.results
            console.log(this.questions)
            return None
        },
        return_to_course_page: function () {
            url = "course_page_learner.html&class=" 
        }
        //?class=6&course_id=2&course_name=Studies%20on%20the%20Xerox%20Printer&user=Tommy
    }
})

function quiz_submit() {
    //There will be submission portion, but there will be grading!
    //Manual grading will happen first, then submission of grades together with answer
    quiz_app.banner_flag = false

    //TO-DO: Check if user completed all the questions!
    // if (quiz_app.answer_options.length != quiz_app.questions.length) {
    //     //user did not complete question
    //     quiz_app.banner_flag = true
    //     quiz_app.banner_flag_msg = "Please complete all questions before submitting!"
    //     return
    // }

    // if (quiz_app.answer_options.includes(null)) {
    //     //user did not complete question
    //     quiz_app.banner_flag = true
    //     quiz_app.banner_flag_msg = "Please complete all questions before submitting!"
    //     return
    // }

    number_of_questions = quiz_app.questions.length

    for (i = 0; i < quiz_app.questions.length; i++) {
        correct_answer = quiz_app.questions[i].answer
        user_answer = quiz_app.answer_options[i]

        if (correct_answer == user_answer) {
            quiz_app.score += 1
        }

    }

    //Percentage:
    percentage_score = Math.round(quiz_app.score / number_of_questions * 100)

    pass_or_fail = 0

    if (percentage_score >= 50) {
        pass_or_fail = 1
    }

    post_result = {
        'Username': quiz_app.student,
        'Quiz_ID': quiz_app.quiz_id,
        "Course_ID": quiz_app.course_id,
        "Section": quiz_app.section_id,
        "Marks": quiz_app.score,
        "Pass": pass_or_fail
    }

    //Submit user score into the database
    axios.post(`http://${addressQuizResult}/create_results`, post_result)
    .then(function(response){
        alert("Your results have been successfully submitted!")
    })
    .catch(function(error){
        alert("Something went wrong with the submission!")
    })


    quiz_app.submit_msg = "You've successfully submitted your quiz! You've attained " + percentage_score.toString() + "%!"

    //Flip user to the end of quiz!
    quiz_app.quiz_section = false

}

function startTimer(duration) {
    var timer = duration, minutes, seconds;
    var interval = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        if (minutes == "00" && seconds == "00") {
            quiz_app.timer_text = "Time's up~!"
            quiz_submit()
            clearInterval(interval)
        } else {
            quiz_app.timer_text = minutes + ":" + seconds;
        }

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}