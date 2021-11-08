const addressQuiz = "3.131.65.207:5544"
const addressQuizResult = "3.131.65.207:5444"
const trackerAddress = '3.131.65.207:5644'
const userAddress = '3.131.65.207:5744'

const urlSearchParams = new URLSearchParams(window.location.search)
const params = Object.fromEntries(urlSearchParams.entries())

var intervalTimer;

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
        submit_msg: "",
        is_repeat: false,
    },
    created() {

        axios.get(`http://${addressQuiz}/spm/quiz_retrieve/${this.course_id}/${this.class_id}/${this.section_id}`)
            .then(function (response) {
                loaded_question = JSON.parse(response.data.data.Question_Object)
                quiz_app.questions = loaded_question
                quiz_app.time = response.data.data.Time
                quiz_app.quiz_id = response.data.data.Quiz_ID
                check_if_user_has_attempted_quiz()
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
            url = "course_page_learner.html?class=" + quiz_app.class_id + "&course_id=" + quiz_app.course_id + "&course_name=" + quiz_app.course_name + "&user=" + quiz_app.student
            window.open(url)
        }
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

    clearInterval(intervalTimer)

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
        .then(function (response) {
            alert("Your results have been successfully submitted!")

            if (quiz_app.section_id != 'final') {

                update_quiz_tracker()

            } else {

                //If it's the final quiz, need to update more things
                update_final_quiz_tracker(pass_or_fail)

                //If user pass, can considered course complete!
                if (pass_or_fail == 1) {
                    axios.get(`http://${userAddress}/user_database/mark_user_course_complete/${quiz_app.student}/${quiz_app.course_id}/${quiz_app.class_id}`)
                        .then(function (response) {
                            alert("Congratulations! You've successfully finished the course!")
                        })
                        .catch(function (response) {
                            alert("Something went wrong with updating the course!!")
                        })
                }


            }
        })
        .catch(function (error) {
            alert("Something went wrong with the submission!")
        })

    quiz_app.submit_msg = "You've successfully submitted your quiz! You've attained " + percentage_score.toString() + "%!"

    //Flip user to the end of quiz!
    quiz_app.quiz_section = false

}

function check_if_user_has_attempted_quiz() {
    axios.get(`http://${addressQuizResult}/spm/check_if_quiz_completed/${quiz_app.quiz_id}/${quiz_app.course_id}/${quiz_app.section_id}/${quiz_app.student}`)
        .then(function (response) {
            check_repeat = response.data.result
            
            if (quiz_app.section_id == 'final') {
<<<<<<< HEAD
                //Finals treated differently, user can try until they pass, but if they passed, lock them out!
                console.log(response.data.pass)
                if (response.data.pass == true) {
=======
                // //Finals treated differently, lock them out if user completed
                // clearInterval(intervalTimer)
                // quiz_app.timer_text = "You've completed!"
                // quiz_app.quiz_section = false
                // quiz_app.score = response.data.marks
                // quiz_app.submit_msg = "You've already attempted the quiz!"

                if (check_repeat == true) {
>>>>>>> 7c579483398a335ebf3b517b2d3cb1cd662dd9cd
                    clearInterval(intervalTimer)
                    quiz_app.timer_text = "You've completed!"
                    quiz_app.quiz_section = false
                    quiz_app.score = response.data.marks
                    quiz_app.submit_msg = "You've already completed and passed your quiz!"
                }

<<<<<<< HEAD

=======
>>>>>>> 7c579483398a335ebf3b517b2d3cb1cd662dd9cd
            } else {
                quiz_app.is_repeat = check_repeat
                if (check_repeat == true) {
                    quiz_app.banner_flag = true
                    quiz_app.banner_flag_msg = "You've done this quiz before!"
                }
            }
        })
        .catch(function (error) {
            alert("Something went wrong when checking if user has quiz completed!")
        })
}

function update_quiz_tracker() {
    if (quiz_app.is_repeat == false) {
        axios.get(`http://${trackerAddress}/spm/update_quiz_tracker/${quiz_app.student}/${quiz_app.course_id}/${quiz_app.class_id}`)
            .then(function (response) {
                alert("Your quiz results are successfully recorded!")
            })
            .catch(function (response) {
                alert("The tracker did not successfully update!")
            })
    }
}

function update_final_quiz_tracker(pass_or_fail) {
    axios.get(`http://${trackerAddress}/spm/update_final_quiz_tracker/${quiz_app.student}/${quiz_app.course_id}/${quiz_app.class_id}/${pass_or_fail}`)
        .then(function (response) {
            alert("Your final quiz results are successfully recorded!")
        })
        .catch(function (response) {
            alert("The tracker did not successfully update!")
        })
}

function startTimer(duration) {

    var timer = duration, minutes, seconds;
    intervalTimer = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        if (minutes == "00" && seconds == "00") {
            quiz_app.timer_text = "Time's up~!"
            quiz_submit()
        } else {
            quiz_app.timer_text = minutes + ":" + seconds;
        }

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}